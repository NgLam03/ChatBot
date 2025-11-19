from ..llm.extract_request_rule_regex import extract_request
from .semantic_search import SemanticSearch
from .rule_filter import rule_filter


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

    def run(self, query: str):
        """
        Chạy full pipeline để trả về danh sách căn hộ phù hợp
        """

        # ===== 1. Parse yêu cầu người dùng → JSON rules =====
        rules = extract_request(query)
        # print("Rules:", rules)

        # ===== 2. Semantic Search bằng FAISS =====
        sem_results = self.searcher.search(query, top_k=self.top_k_semantic)

        # ===== 3. Lọc bằng rule =====
        filtered = rule_filter(sem_results, rules)

        # ===== 4. Sắp xếp lại theo score tăng dần (score của FAISS) =====
        # vì FAISS: số nhỏ hơn = giống hơn
        final_results = sorted(filtered, key=lambda x: x["score"])

        # ===== 5. Trả về top N =====
        return final_results[: self.top_k_final]


# test
if __name__ == "__main__":
    pipeline = SearchPipeline()

    q = "tìm căn 2 ngủ full đồ dưới 10tr view VinUni"

    results = pipeline.run(q)

    for item in results:
        print(item["ms"], item["price"], item["bedrooms"], item["furniture"], "score:", item["score"])
