from ..llm.extract_request_rule_regex import extract_request
from .semantic_search import SemanticSearch
from .rule_filter import rule_filter
import re


class SearchPipeline:
    def __init__(self, top_k_semantic=20, top_k_final=5):
        """
        top_k_semantic: lấy bao nhiêu căn từ FAISS
        top_k_final: trả về bao nhiêu căn cuối sau lọc rule
        """
        self.top_k_semantic = top_k_semantic
        self.top_k_final = top_k_final

        # Init FAISS searcher
        self.searcher = SemanticSearch()
        self.metadata = self.searcher.metadata

    # ================== CÁC HÀM NER & RÀNG BUỘC BỔ SUNG ==================

    def _normalize_text(self, text: str) -> str:
        return text.lower().strip()

    def _extract_price_range(self, query: str):
        """
        NER giá: trả về (min_price, max_price) theo VND nếu bắt được.
        Hỗ trợ các kiểu:
            - "dưới 8tr", "dưới 8 triệu"
            - "8-9tr", "8 đến 9tr", "8 tới 9 triệu"
            - "tầm 9tr", "khoảng 9 triệu"
            - "10tr" (coi là max_price = 10tr)
        """
        text = self._normalize_text(query)

        # bắt số + đơn vị
        price_pattern = r"(\d+)\s*(triệu|tr|m)"
        matches = list(re.finditer(price_pattern, text))
        if not matches:
            return None, None

        prices_million = [int(m.group(1)) for m in matches]

        # range "8-9tr" / "8 đến 9tr"
        range_pattern = r"(\d+)\s*(?:-|đến|->|tới)\s*(\d+)\s*(triệu|tr|m)"
        m_range = re.search(range_pattern, text)
        if m_range:
            p1 = int(m_range.group(1))
            p2 = int(m_range.group(2))
            mn = min(p1, p2) * 1_000_000
            mx = max(p1, p2) * 1_000_000
            return mn, mx

        # dưới / không quá
        if "dưới" in text or "không quá" in text or "<" in text or "≤" in text:
            mx = min(prices_million) * 1_000_000
            return None, mx

        # trên / ít nhất
        if "trên" in text or "tối thiểu" in text or "ít nhất" in text or ">" in text or "≥" in text:
            mn = max(prices_million) * 1_000_000
            return mn, None

        # tầm / khoảng
        if "tầm" in text or "khoảng" in text or "khoảng tầm" in text:
            p = prices_million[0]
            mn = max((p - 1) * 1_000_000, 0)
            mx = (p + 1) * 1_000_000
            return mn, mx

        # mặc định: 1 con số → coi như max_price
        p = prices_million[0]
        return None, p * 1_000_000

    def _extract_bedrooms_range(self, query: str):
        """
        NER số phòng ngủ: trả về (min_bedrooms, max_bedrooms) nếu bắt được.
        Hỗ trợ:
            - "2 ngủ", "2pn", "2 phòng ngủ"
            - "2n1vs" (lấy 2)
        """
        text = self._normalize_text(query)

        # dạng 2pn / 2 phòng ngủ / 2 ngủ
        pattern_digit = r"(\d+)\s*(?:pn|phòng ngủ|ngủ)"
        m = re.search(pattern_digit, text)
        if m:
            n = int(m.group(1))
            return n, n

        # dạng 2n1vs
        pattern_type = r"(\d+)\s*n\s*\d*\s*vs"
        m2 = re.search(pattern_type, text)
        if m2:
            n = int(m2.group(1))
            return n, n

        return None, None

    def _extract_buildings(self, query: str):
        """
        NER toà: S1, S2, S2.01, P2,...
        """
        text = query.upper()
        # ví dụ: S2, S2.01, P3
        pattern = r"\b(S|P)\s*([\d]{1,2}(?:\.\d+)?)\b"
        matches = re.findall(pattern, text)
        buildings = {f"{m[0]}{m[1]}".replace(" ", "") for m in matches}
        return buildings

    def _parse_constraints(self, query: str):
        """
        Gom các thực thể & ràng buộc phát hiện được vào 1 dict.
        Chỉ dùng để FILTER thêm trên kết quả semantic.
        """
        min_price, max_price = self._extract_price_range(query)
        min_bed, max_bed = self._extract_bedrooms_range(query)
        buildings = self._extract_buildings(query)

        return {
            "min_price": min_price,
            "max_price": max_price,
            "min_bedrooms": min_bed,
            "max_bedrooms": max_bed,
            "buildings": buildings,  # set
        }

    def _filter_by_constraints(self, results, constraints):
        """
        Lọc danh sách căn theo ràng buộc cứng:
            - min_price, max_price
            - min_bedrooms, max_bedrooms
            - buildings
        Nếu lọc xong rỗng → trả lại list ban đầu (tránh quá chặt).
        """
        if not results:
            return results

        min_price = constraints.get("min_price")
        max_price = constraints.get("max_price")
        min_bed = constraints.get("min_bedrooms")
        max_bed = constraints.get("max_bedrooms")
        buildings = constraints.get("buildings") or set()

        filtered = []
        for item in results:
            price = item.get("price")
            bedrooms = item.get("bedrooms")
            building = str(item.get("building", "")).upper()

            # --------- PRICE FILTER ---------
            if min_price is not None and price is not None and price < min_price:
                continue
            if max_price is not None and price is not None and price > max_price:
                continue

            # --------- BEDROOMS FILTER ---------
            if min_bed is not None and bedrooms is not None and bedrooms < min_bed:
                continue
            if max_bed is not None and bedrooms is not None and bedrooms > max_bed:
                continue

            # --------- BUILDING FILTER ---------
            if buildings and building not in buildings:
                continue

            filtered.append(item)

        # nếu lọc xong rỗng thì dùng lại kết quả cũ
        return filtered if filtered else results

    # ================== HẾT PHẦN NER & RÀNG BUỘC ==================

    def run(self, query: str):
        """
        Chạy full pipeline để trả về danh sách căn hộ phù hợp
        """

        # ===== 1. Parse yêu cầu người dùng → JSON rules (LLM / regex cũ) =====
        rules = extract_request(query)
        # print("Rules:", rules)

        # ===== 2. NER bằng regex để lấy ràng buộc cứng (giá, ngủ, toà) =====
        constraints = self._parse_constraints(query)
        # print("Constraints:", constraints)

        # ===== 3. Semantic Search bằng FAISS =====
        sem_results = self.searcher.search(query, top_k=self.top_k_semantic)

        # sem_results dự kiến là list[dict] chứa:
        #   - ms, price, bedrooms, building, furniture, score, ...
        # Nếu khác, chỉ cần chỉnh SemanticSearch cho phù hợp.

        # ===== 4. Lọc thêm bằng ràng buộc NER (giá / ngủ / toà) =====
        sem_results = self._filter_by_constraints(sem_results, constraints)

        # ===== 5. Lọc bằng rule (từ extract_request) =====
        filtered = rule_filter(sem_results, rules)

        # ===== 6. Sắp xếp lại theo score tăng dần (score của FAISS) =====
        # vì FAISS: số nhỏ hơn = giống hơn
        final_results = sorted(filtered, key=lambda x: x["score"])

        # ===== 7. Trả về top N =====
        return final_results[: self.top_k_final]


# test
if __name__ == "__main__":
    pipeline = SearchPipeline()

    q = "tìm căn S2 2 ngủ full đồ dưới 10tr view VinUni"

    results = pipeline.run(q)

    for item in results:
        print(
            item["ms"],
            item["price"],
            item["bedrooms"],
            item.get("building"),
            item.get("furniture"),
            "score:",
            item["score"],
        )
