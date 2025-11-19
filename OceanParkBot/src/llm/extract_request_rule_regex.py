import re

import re

def extract_request(query: str):
    q = query.lower().strip()

    # ===============================
    # GREETING
    # ===============================
    if q in ["hi", "hello", "xin chào", "chào", "alo", "hey"] or q.startswith("chào"):
        return {"intent": "greeting"}

    # ===============================
    # COUNT BY BEDROOM + BATHROOM
    # ===============================
    # Ví dụ: "bao nhiêu căn 1 ngủ 1 vệ sinh"
    combo = re.search(r"(\d+)\s*(ngủ|pn).*(\d+)\s*(vệ sinh|vs|wc)", q)
    if combo:
        return {
            "intent": "count_by_bedbath",
            "bedrooms": int(combo.group(1)),
            "bathrooms": int(combo.group(3))
        }

    # Ví dụ: "có bao nhiêu căn 2 ngủ", "bao nhiêu căn 1 phòng ngủ"
    bed = re.search(r"(\d+)\s*(ngủ|phòng ngủ|pn)", q)
    if bed:
        return {
            "intent": "count_by_bedroom",
            "bedrooms": int(bed.group(1))
        }

    # Ví dụ: "bao nhiêu căn 1 wc"
    bath = re.search(r"(\d+)\s*(vệ sinh|vs|wc)", q)
    if bath:
        return {
            "intent": "count_by_bathroom",
            "bathrooms": int(bath.group(1))
        }

    # ===============================
    # COUNT BY VIEW
    # ===============================
    if "nội khu" in q:
        return {"intent": "count_by_view", "view": "Nội khu"}
    if "vinuni" in q:
        return {"intent": "count_by_view", "view": "VinUni"}
    if "hồ" in q:
        return {"intent": "count_by_view", "view": "Hồ"}

    # ===============================
    # COUNT ALL
    # ===============================
    # Đặt SAU tất cả count_by_* để không override
    if "bao nhiêu căn" in q or "tổng số căn" in q or "tất cả căn" in q:
        return {"intent": "count_all"}

    # ===============================
    # CHEAPEST / EXPENSIVE
    # ===============================
    if "rẻ nhất" in q:
        return {"intent": "cheapest"}
    if "đắt nhất" in q:
        return {"intent": "expensive"}

    # ===============================
    # FALLBACK → SEARCH
    # ===============================
    return {"intent": "search", "query": q}

