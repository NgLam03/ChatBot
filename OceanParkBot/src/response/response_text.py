def format_price(price: int):
    """
    Convert số nguyên → dạng 8.000.000đ hoặc 8tr
    """
    if price is None:
        return "N/A"
    if price >= 1_000_000:
        tr = price / 1_000_000
        if tr.is_integer():
            return f"{int(tr)}tr"
        return f"{tr:.1f}tr"
    return f"{price:,}đ"


def format_result_item(item: dict, index: int):
    """
    Format 1 căn hộ thành text đẹp.
    """
    ms = item.get("ms", "N/A")
    building = item.get("building", "N/A")
    view = item.get("view", "N/A")

    bedrooms = item.get("bedrooms", "N/A")
    bathrooms = item.get("bathrooms", "N/A")
    furniture = item.get("furniture", "N/A")

    price = format_price(item.get("price"))

    return f"""
[{index}]  MÃ CĂN: {ms}
    • Toà: {building}
    • View: {view}
    • Phòng: {bedrooms} ngủ – {bathrooms} vệ sinh
    • Nội thất: {furniture}
    • Giá: {price}
"""


def format_result_text(results: list):
    """
    Format nhiều kết quả thành text để in ra terminal hoặc gửi về API.
    """
    if not results:
        return "Không tìm thấy căn nào phù hợp yêu cầu của bạn."

    text_list = []
    for i, item in enumerate(results, start=1):
        text_list.append(format_result_item(item, i))

    return "\n".join(text_list)
