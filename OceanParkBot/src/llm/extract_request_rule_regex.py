import re

def extract_request(query: str):
    """
    Rule-based Intent Parser cho chatbot tìm nhà Ocean Park.
    Phát hiện:
    - greeting
    - unknown
    - count_all
    - count_by_bedroom
    - cheapest
    - expensive
    - search (default)
    """

    q = query.lower().strip()

    # ============================================
    # 1. GREETING
    # ============================================
    greetings = ["hi", "hello", "chào", "alo", "hey", "xin chào"]
    if q in greetings or q.startswith("chào"):
        return {"intent": "greeting"}

    # ============================================
    # 2. INTENT: COUNT ALL
    # ============================================
    # 2a. COUNT BY VIEW (phải đặt TRƯỚC count_all)
    if "nội khu" in q or "noi khu" in q:
        return {"intent": "count_by_view", "view": "Nội khu"}

    if "view vinuni" in q or "vinuni" in q:
        return {"intent": "count_by_view", "view": "VinUni"}

    if "view hồ" in q or "view ho" in q or "hồ" in q:
        return {"intent": "count_by_view", "view": "Hồ"}

    # 2b. COUNT ALL (đặt SAU cùng)
    if ("tổng" in q and "căn" in q) or ("bao nhiêu căn" in q) or ("bao nhieu can" in q):
        return {"intent": "count_all"}

    # ============================================
    # 3. INTENT: COUNT BY BEDROOM
    # ============================================
    match_bed = re.findall(r"bao nhiêu căn\s*(\d+)\s*ngủ", q)
    if match_bed:
        return {
            "intent": "count_by_bedroom",
            "bedrooms": int(match_bed[0])
        }

    match_bed2 = re.findall(r"có bao nhiêu căn\s*(\d+)\s*ngủ", q)
    if match_bed2:
        return {
            "intent": "count_by_bedroom",
            "bedrooms": int(match_bed2[0])
        }

    # ============================================
    # 4. INTENT: CHEAPEST (căn rẻ nhất)
    # ============================================
    if "rẻ nhất" in q or "re nhat" in q:
        return {"intent": "cheapest"}

    # ============================================
    # 5. INTENT: EXPENSIVE (căn đắt nhất)
    # ============================================
    if "đắt nhất" in q or "dat nhat" in q:
        return {"intent": "expensive"}

    # ============================================
    # 6. Remove noise — nếu không có từ BĐS → unknown
    # ============================================
    bds_keywords = [
        "ngủ", "phòng", "vs", "wc", "full", "cb", "giá", "tr", "triệu",
        "toà", "s1", "s2", "s3", "s4", "view", "vinuni", "nội khu",
        "studio", "căn", "chung cư", "hồ"
    ]

    if not any(k in q for k in bds_keywords):
        return {"intent": "unknown"}

    # ============================================
    # 7. DEFAULT: INTENT SEARCH → parse rule
    # ============================================

    result = {
        "intent": "search",
        "bedrooms": None,
        "bathrooms": None,
        "furniture": None,
        "price_min": None,
        "price_max": None,
        "view": None,
        "building": None,
        "move_in": None
    }

    # ===== BEDROOMS =====
    if "2 ngủ" in q or "2n" in q:
        result["bedrooms"] = 2
    if "1 ngủ" in q or "1n" in q:
        result["bedrooms"] = 1
    if "studio" in q or "st" in q:
        result["bedrooms"] = 0

    # ===== FURNITURE =====
    if "full đồ" in q or "full nt" in q or "đầy đủ nội thất" in q or "full nội thất" in q:
        result["furniture"] = "full"
    if "cơ bản" in q or "cb" in q:
        result["furniture"] = "co_ban"
    if "trống" in q or "không nội thất" in q:
        result["furniture"] = "none"

    # ===== PRICE RANGE =====
    match_range = re.findall(r"(\d+)\s*[-~]\s*(\d+)\s*tr", q)
    if match_range:
        pmin = int(match_range[0][0]) * 1_000_000
        pmax = int(match_range[0][1]) * 1_000_000
        result["price_min"] = pmin
        result["price_max"] = pmax

    match_under = re.findall(r"dưới\s*(\d+)\s*tr", q)
    if match_under:
        result["price_max"] = int(match_under[0]) * 1_000_000

    match_approx = re.findall(r"(tầm|khoảng)\s*(\d+)\s*tr", q)
    if match_approx:
        price = int(match_approx[0][1]) * 1_000_000
        result["price_min"] = price - 1_000_000
        result["price_max"] = price + 1_000_000

    # ===== VIEW =====
    if "vinuni" in q:
        result["view"] = "VinUni"
    if "hồ" in q:
        result["view"] = "Hồ"
    if "nội khu" in q:
        result["view"] = "Nội khu"

    # ===== BUILDING =====
    match_build = re.findall(r"s\d+\.?\d*", q)
    if match_build:
        result["building"] = match_build[0].upper()

    # ===== MOVE IN =====
    if "ở luôn" in q or "vào ở ngay" in q:
        result["move_in"] = "ngay"

    return result
