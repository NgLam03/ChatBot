import re

def normalize_price(price_text: str):
    """
    Chuyển các dạng:
    - "8tr bao phí"
    - "6.5tr"
    - "7tr/tháng"
    - "8000k"
    → về dạng số: 8000000
    """
    if not price_text:
        return None

    text = price_text.lower().replace(" ", "")

    # dạng: 8tr, 6.5tr
    match_tr = re.findall(r"(\d+\.?\d*)tr", text)
    if match_tr:
        value = float(match_tr[0])
        return int(value * 1_000_000)

    # dạng: 8000k
    match_k = re.findall(r"(\d+)k", text)
    if match_k:
        value = int(match_k[0])
        return value * 1000

    # fallback: lấy số đầu tiên
    match_digits = re.findall(r"\d+", text)
    if match_digits:
        return int(match_digits[0])

    return None
