import re

def extract_request(query: str):
    q = query.lower().strip()

    # ===============================
    # GREETING
    # ===============================
    if q in ["hi", "hello", "xin chào", "chào", "alo", "hey"] or q.startswith("chào"):
        return {"intent": "greeting"}

    # ===============================
    # SHOW EXAMPLES (phải ưu tiên)
    # ===============================
    show_patterns = [
        "xem", "xem đi", "cho xem", "cho mình xem",
        "xem vài căn", "xem qua vài căn", "cho xem vài căn",
        "xem căn", "xem những căn", "cho mình xem vài căn"
    ]
    if any(p in q for p in show_patterns):
        # kiểm tra có số phòng ngủ kèm theo
        bed = re.search(r"(\d+)\s*(ngủ|pn|phòng ngủ)", q)
        bath = re.search(r"(\d+)\s*(vệ sinh|vs|wc)", q)

        rules = {"intent": "show_examples"}

        if bed:
            rules["bedrooms"] = int(bed.group(1))
        if bath:
            rules["bathrooms"] = int(bath.group(1))

        return rules

    # ===============================
    # COUNT BED + BATH (ưu tiên)
    # ===============================
    combo = re.search(r"(\d+)\s*ngủ.*(\d+)\s*(vệ sinh|vs|wc)", q)
    if combo:
        return {
            "intent": "count_by_bedbath",
            "bedrooms": int(combo.group(1)),
            "bathrooms": int(combo.group(2))
        }

    # ===============================
    # COUNT BEDROOM
    # ===============================
    bed = re.search(r"(\d+)\s*(ngủ|pn|phòng ngủ)", q)
    if bed:
        return {
            "intent": "count_by_bedroom",
            "bedrooms": int(bed.group(1))
        }

    # ===============================
    # COUNT BATHROOM
    # ===============================
    bath = re.search(r"(\d+)\s*(vệ sinh|vs|wc)", q)
    if bath:
        return {
            "intent": "count_by_bathroom",
            "bathrooms": int(bath.group(1))
        }

    # ===============================
    # COUNT VIEW
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
    if "bao nhiêu căn" in q or "tổng số căn" in q or "tất cả căn" in q:
        return {"intent": "count_all"}

    # ===============================
    # FALLBACK → SEARCH
    # ===============================
    return {"intent": "search", "query": q}
