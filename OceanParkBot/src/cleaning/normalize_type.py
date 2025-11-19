import re

def normalize_type(loai_can: str):
    """
    Chuyển:
    - "2n1vs" → (2 ngủ, 1 vệ sinh)
    - "1n1vs"
    - "studio"
    """
    if not loai_can:
        return 0, 0

    text = loai_can.lower()

    # trường hợp studio
    if "studio" in text or text.strip() == "st":
        # mặc định: studio = 0 ngủ, 1 wc
        return 0, 1

    bedrooms = 0
    bathrooms = 0

    # tìm số ngủ: 2n, 3n...
    match_n = re.findall(r"(\d+)n", text)
    if match_n:
        bedrooms = int(match_n[0])

    # tìm số wc: 1vs, 2vs...
    match_vs = re.findall(r"(\d+)vs", text)
    if match_vs:
        bathrooms = int(match_vs[0])

    return bedrooms, bathrooms
