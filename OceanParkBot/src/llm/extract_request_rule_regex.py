import re


def extract_request(query: str):
    """
    Phân tích câu hỏi user bằng rule + regex.
    Đã thêm Intent Detection để ngăn bot trả nhà bừa.
    """

    q = query.lower().strip()

    # ==========================
    # 1) INTENT DETECTION
    # ==========================

    # ---- intent: greeting ----
    greetings = ["hi", "hello", "chào", "alo", "hey", "xin chào"]
    if q in greetings:
        return {"intent": "greeting"}

    # ---- intent: câu không có từ khóa BĐS ----
    # bộ từ khóa gợi ý user đang muốn tìm nhà
    bds_keywords = [
        "ngủ", "n ngủ", "phòng", "vs", "wc",
        "full", "cơ bản", "cb", "giá", "tr", "triệu",
        "toà", "s1", "s2", "s3", "s4",
        "view", "vinuni", "nội khu", "hồ",
        "studio", "st", "căn", "chung cư"
    ]

    if not any(k in q for k in bds_keywords):
        return {"intent": "unknown"}   # không phải câu tìm nhà

    # Nếu không rơi vào 2 intent trên → tiếp tục parse rule như bình thường

    # ==========================
    # 2) RULE-BASED PARSING
    # ==========================

    result = {
        "intent": "search",         # thêm intent
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

    # ===== BATHROOMS =====
    if "2vs" in q:
        result["bathrooms"] = 2
    if "1vs" in q or "1 wc" in q or "1 vệ sinh" in q:
        result["bathrooms"] = 1

    # ===== FURNITURE =====
    if "full đồ" in q or "full nt" in q or "đầy đủ nội thất" in q or "full nội thất" in q:
        result["furniture"] = "full"
    if "cơ bản" in q or "cb" in q:
        result["furniture"] = "co_ban"
    if "trống" in q or "không nội thất" in q:
        result["furniture"] = "none"

    if "tổng" in q and "có bao" in q:
        return {"intent": "count_all"}

    if "bao nhiêu căn 2 ngủ" in q:
        return {"intent": "count_bedrooms", "bedrooms": 2}

    if "rẻ nhất" in q:
        return {"intent": "cheapest"}

    if "đắt nhất" in q:
        return {"intent": "expensive"}

    if "view vinuni" in q:
        return {"intent": "search_by_view", "view": "VinUni"}

    if "bạn tên gì" in q:
        return {"intent": "chitchat_name"}


    # ===== PRICE RANGE =====

    # dạng: 7-9tr, 7~9tr
    match_range = re.findall(r"(\d+)\s*[-~]\s*(\d+)\s*tr", q)
    if match_range:
        pmin = int(match_range[0][0]) * 1_000_000
        pmax = int(match_range[0][1]) * 1_000_000
        result["price_min"] = pmin
        result["price_max"] = pmax

    # dạng: dưới 8tr
    match_under = re.findall(r"dưới\s*(\d+)\s*tr", q)
    if match_under:
        result["price_max"] = int(match_under[0]) * 1_000_000

    # dạng: tầm 8tr, khoảng 8tr
    match_approx = re.findall(r"(tầm|khoảng)\s*(\d+)\s*tr", q)
    if match_approx:
        price = int(match_approx[0][1]) * 1_000_000
        result["price_min"] = price - 1_000_000
        result["price_max"] = price + 1_000_000

    # ===== VIEW =====
    if "vinuni" in q:
        result["view"] = "VinUni"
    if "hồ" in q or "view ho" in q:
        result["view"] = "Hồ"
    if "nội khu" in q:
        result["view"] = "Nội khu"

    # ===== BUILDING =====
    match_build = re.findall(r"s\d+\.?\d*", q)
    if match_build:
        result["building"] = match_build[0].upper()

    # ===== MOVE IN =====
    if "vào ở ngay" in q or "ở luôn" in q:
        result["move_in"] = "ngay"
    if "cuối tháng" in q:
        result["move_in"] = "cuối tháng"

    return result


if __name__ == "__main__":
    print(extract_request("hi"))
    print(extract_request("alo alo"))
    print(extract_request("tìm căn 2 ngủ full đồ dưới 9tr view VinUni"))
