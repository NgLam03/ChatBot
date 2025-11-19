# src/search/query_parser.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, Set, List, Dict, Any, Tuple


@dataclass
class QueryConstraints:
    """
    Các ràng buộc trích từ câu hỏi người dùng.
    """
    min_price: Optional[int] = None        # VND
    max_price: Optional[int] = None        # VND
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None

    buildings: Set[str] = field(default_factory=set)   # ví dụ: {"S1", "S2", "P2"}
    views: Set[str] = field(default_factory=set)       # ví dụ: {"VinUni", "hồ"}

    # các “tính chất mềm”
    furniture_keywords: Set[str] = field(default_factory=set)   # full, cơ bản, trống
    move_in_keywords: Set[str] = field(default_factory=set)     # ngay, đầu tháng,...

    raw_entities: Dict[str, Any] = field(default_factory=dict)  # debug / log


VN_NUMBER_WORDS = {
    "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5,
    "sáu": 6, "bảy": 7, "tám": 8, "chín": 9,
}


def _normalize_text(text: str) -> str:
    return text.lower().strip()


def _extract_price(text: str) -> Tuple[(Optional[int], Optional[int])]:
    """
    Trích giá từ câu hỏi (đơn vị triệu, tr, m).
    Trả về (min_price, max_price) theo VND.
    Ví dụ hỗ trợ:
        - "dưới 8tr"
        - "8-9tr"
        - "tầm 9 đến 10 triệu"
        - "khoảng 8tr"
    """
    t = _normalize_text(text)

    # pattern bắt số + đơn vị
    price_pattern = r"(\d+)\s*(triệu|tr|m)"
    matches = list(re.finditer(price_pattern, t))

    if not matches:
        return None, None

    # chuyển về triệu
    prices_million = [int(m.group(1)) for m in matches]

    # case có range: "8-9tr", "8 đến 9tr", "từ 8 đến 10tr"
    range_pattern = r"(\d+)\s*(?:-|đến|->|tới)\s*(\d+)\s*(triệu|tr|m)"
    range_match = re.search(range_pattern, t)
    if range_match:
        p1 = int(range_match.group(1))
        p2 = int(range_match.group(2))
        min_p = min(p1, p2) * 1_000_000
        max_p = max(p1, p2) * 1_000_000
        return min_p, max_p

    # từ khoá hướng
    if "dưới" in t or "≤" in t or "<=" in t or "<" in t:
        max_p = min(prices_million) * 1_000_000
        return None, max_p

    if "trên" in t or ">" in t or "≥" in t or ">=" in t:
        min_p = max(prices_million) * 1_000_000
        return min_p, None

    if "tầm" in t or "khoảng" in t or "khoảng tầm" in t:
        # coi như khoảng +-1tr xung quanh số bắt được đầu tiên
        p = prices_million[0]
        return max((p - 1) * 1_000_000, 0), (p + 1) * 1_000_000

    # mặc định: 1 số → max_price
    p = prices_million[0]
    return None, p * 1_000_000


def _word_to_int(word: str) -> Optional[int]:
    word = word.strip().lower()
    if word.isdigit():
        return int(word)
    return VN_NUMBER_WORDS.get(word)


def _extract_bedrooms(text: str) -> Tuple[(Optional[int], Optional[int])]:
    """
    Trích số phòng ngủ: '2 ngủ', '2pn', '2 phòng ngủ', 'hai ngủ',...
    """
    t = _normalize_text(text)

    # số dạng digit
    digit_pattern = r"(\d+)\s*(?:pn|phòng ngủ|ngủ)"
    m = re.search(digit_pattern, t)
    if m:
        n = int(m.group(1))
        return n, n

    # số dạng chữ
    word_pattern = r"(một|hai|ba|bốn|năm|sáu|bảy|tám|chín)\s*(?:pn|phòng ngủ|ngủ)"
    m2 = re.search(word_pattern, t)
    if m2:
        n = _word_to_int(m2.group(1))
        return n, n

    return None, None


def _extract_buildings(text: str) -> Set[str]:
    """
    Bắt toà: S1, S2, S1.01, P2, P3,...
    """
    t = text.upper()
    pattern = r"\b(S|P)\s*[\d]{1,2}(?:\.\d+)?\b"
    matches = re.findall(pattern, t)
    # pattern trên chỉ lấy chữ cái; cần pattern đầy đủ hơn:
    full_pattern = r"\b(S|P)\s*([\d]{1,2}(?:\.\d+)?)\b"
    full_matches = re.findall(full_pattern, t)
    buildings = {f"{m[0]}{m[1]}".replace(" ", "") for m in full_matches}
    return buildings


def _extract_views(text: str) -> Set[str]:
    """
    Bắt các view phổ biến: VinUni, hồ, biển, công viên...
    Có thể mở rộng từ điển.
    """
    t = _normalize_text(text)
    views = set()

    if "vinuni" in t or "vin uni" in t:
        views.add("VinUni")
    if "hồ" in t or "ho lake" in t:
        views.add("Hồ")
    if "biển" in t:
        views.add("Biển")
    if "công viên" in t or "cv" in t:
        views.add("Công viên")

    return views


def _extract_furniture(text: str) -> Set[str]:
    t = _normalize_text(text)
    kws = set()

    if "full đồ" in t or "full nội thất" in t or "full nt" in t or "full đồ đạc" in t:
        kws.add("full")
    if "cơ bản" in t or "cb nt" in t:
        kws.add("cơ bản")
    if "trống" in t or "không nội thất" in t or "ko nội thất" in t:
        kws.add("trống")

    return kws


def _extract_move_in(text: str) -> Set[str]:
    t = _normalize_text(text)
    kws = set()

    if "ở ngay" in t or "vào ở ngay" in t or "nhận nhà ngay" in t:
        kws.add("ngay")
    if "đầu tháng" in t:
        kws.add("đầu tháng")
    if "cuối tháng" in t:
        kws.add("cuối tháng")
    if "sau tết" in t:
        kws.add("sau tết")

    return kws


def parse_user_query(text: str) -> QueryConstraints:
    """
    Hàm chính: nhận câu hỏi → trả ra các ràng buộc.
    """
    min_price, max_price = _extract_price(text)
    min_bedrooms, max_bedrooms = _extract_bedrooms(text)
    buildings = _extract_buildings(text)
    views = _extract_views(text)
    furniture_kws = _extract_furniture(text)
    move_in_kws = _extract_move_in(text)

    constraints = QueryConstraints(
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        max_bedrooms=max_bedrooms,
        buildings=buildings,
        views=views,
        furniture_keywords=furniture_kws,
        move_in_keywords=move_in_kws,
        raw_entities={
            "text": text,
            "price_raw": (min_price, max_price),
            "bedrooms_raw": (min_bedrooms, max_bedrooms),
            "buildings_raw": list(buildings),
            "views_raw": list(views),
        },
    )
    return constraints


def apply_constraints(
    listings: List[Dict[str, Any]],
    constraints: QueryConstraints,
    top_k: int = 10,
) -> List[Dict[str, Any]]:
    """
    Lọc + chấm điểm danh sách căn theo ràng buộc.
    listings: list dict theo format listings_clean.json
    """
    results = []

    for item in listings:
        # ----- HARD FILTER -----
        price = item.get("price")
        if constraints.min_price is not None and price is not None:
            if price < constraints.min_price:
                continue
        if constraints.max_price is not None and price is not None:
            if price > constraints.max_price:
                continue

        bedrooms = item.get("bedrooms")
        if constraints.min_bedrooms is not None and bedrooms is not None:
            if bedrooms < constraints.min_bedrooms:
                continue
        if constraints.max_bedrooms is not None and bedrooms is not None:
            if bedrooms > constraints.max_bedrooms:
                continue

        building = str(item.get("building", "")).upper()
        if constraints.buildings:
            # nếu user chỉ định toà, bắt buộc phải match
            if building not in constraints.buildings:
                continue

        view = str(item.get("view", "")).lower()
        if constraints.views:
            # view là ràng buộc “mềm”: nếu không match, vẫn cho nhưng trừ điểm
            view_match = any(v.lower() in view for v in constraints.views)
        else:
            view_match = True

        # ----- SOFT SCORE -----
        score = 0.0

        # view phù hợp
        if view_match:
            score += 1.0

        # furniture
        furniture_text = str(item.get("furniture", "")).lower()
        if constraints.furniture_keywords:
            if any(k in furniture_text for k in constraints.furniture_keywords):
                score += 0.5

        # move in
        move_in_text = str(item.get("move_in", "")).lower()
        if constraints.move_in_keywords:
            if any(k in move_in_text for k in constraints.move_in_keywords):
                score += 0.3

        results.append((score, item))

    # sort theo score (desc) rồi cắt top_k
    results.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in results[:top_k]]
