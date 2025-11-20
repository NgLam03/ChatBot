import re
import nltk
from nltk.corpus import stopwords

# tải tài nguyên NLTK lần đầu
try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except:
    nltk.download("stopwords")

# stopwords tiếng Việt + tiếng Anh
VI_STOP = set(stopwords.words("english"))  # nltk không có stopwords VN, mình dùng custom
VI_STOP.update([
    "mình", "tôi", "bạn", "cho", "xin", "muốn", "tìm", "xem",
    "căn", "hộ", "đi", "với", "một", "có", "không", "thì",
    "những", "nào", "nhiêu", "bao", "nhiêu", "gì", "ấ", "ạ"
])

def normalize_query(q: str):
    q = q.lower().strip()

    # thay word_tokenize = tokenize bằng split đơn giản
    raw_tokens = re.split(r"[ ,.;:!?()\-\n\t]+", q)

    # remove stopwords
    tokens = [t for t in raw_tokens if t and t not in VI_STOP]

    return tokens, " ".join(tokens)


def extract_request(query: str):
    tokens, qnorm = normalize_query(query)

    q = query.lower().strip()

    # ===============================
    # GREETING
    # ===============================
    if any(w in tokens for w in ["hi", "hello", "chào", "hey"]):
        return {"intent": "greeting"}

    # ===============================
    # INTENT: SHOW LIST
    # ===============================
    show_keywords = ["xem", "xem vài", "xem qua", "cho xem", "xem thử"]
    if any(k in q for k in show_keywords) or any(w in tokens for w in ["xem"]):
        rules = {"intent": "show_examples"}

        # detect bedrooms
        bed = re.search(r"(\d+)\s*(pn|n|ngủ|phòng)", qnorm)
        if bed:
            rules["bedrooms"] = int(bed.group(1))

        # detect bathroom
        bath = re.search(r"(\d+)\s*(vs|wc|vệ sinh)", qnorm)
        if bath:
            rules["bathrooms"] = int(bath.group(1))

        return rules

    # ===============================
    # INTENT: COUNT BED + BATH
    # ===============================
    combo = re.search(r"(\d+)\s*(pn|n|ngủ).*(\d+)\s*(vs|wc|vệ sinh)", qnorm)
    if combo:
        return {
            "intent": "count_by_bedbath",
            "bedrooms": int(combo.group(1)),
            "bathrooms": int(combo.group(3))
        }

    # ===============================
    # INTENT: COUNT BEDROOM
    # ===============================
    bed = re.search(r"(\d+)\s*(pn|n|ngủ|phòng)", qnorm)
    if bed:
        return {
            "intent": "count_by_bedroom",
            "bedrooms": int(bed.group(1))
        }

    # kiểu chữ: "hai ngủ"
    word_to_num = {
        "một": 1, "mot": 1, "1": 1,
        "hai": 2, "2": 2,
        "ba": 3, "3": 3
    }
    for w, num in word_to_num.items():
        if w in tokens and "ngủ" in tokens:
            return {"intent": "count_by_bedroom", "bedrooms": num}

    # ===============================
    # COUNT BATHROOM
    # ===============================
    bath = re.search(r"(\d+)\s*(vs|wc|vệ sinh)", qnorm)
    if bath:
        return {
            "intent": "count_by_bathroom",
            "bathrooms": int(bath.group(1))
        }

    # ===============================
    # COUNT VIEW
    # ===============================
    if "nội khu" in q or "noi khu" in qnorm:
        return {"intent": "count_by_view", "view": "Nội khu"}

    if "vinuni" in q or "vin" in tokens:
        return {"intent": "count_by_view", "view": "VinUni"}

    if "hồ" in q or "lake" in tokens:
        return {"intent": "count_by_view", "view": "Hồ"}

    # "thoáng", "sáng" → ưu tiên nội khu / hồ
    if any(w in tokens for w in ["thoáng", "sáng", "ánh"]):
        return {"intent": "count_by_view", "view": "Nội khu"}

    # ===============================
    # COUNT ALL
    # ===============================
    if any(k in q for k in ["bao nhiêu căn", "tổng số căn", "tất cả căn"]):
        return {"intent": "count_all"}

    # ===============================
    # FALLBACK → SEMANTIC SEARCH
    # ===============================
    return {"intent": "search", "query": qnorm}
