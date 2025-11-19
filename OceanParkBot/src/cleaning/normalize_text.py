def build_text_for_embedding(item):
    """
    Tạo text mô tả đầy đủ để đưa vào embedding.
    """
    ms = item.get("ms", "")
    building = item.get("building", "")
    view = item.get("view", "")
    bedrooms = item.get("bedrooms", "")
    bathrooms = item.get("bathrooms", "")
    noi_that = item.get("noi_that", "")
    gia = item.get("gia", "")
    payment = item.get("hinh_thuc_dong", "")
    xem = item.get("thoi_gian_xem", "")
    vao = item.get("thoi_gian_vao_o", "")

    text = (
        f"Mã căn {ms}, toà {building}, view {view}. "
        f"Loại {bedrooms} ngủ {bathrooms} vệ sinh. "
        f"Nội thất: {noi_that}. "
        f"Giá: {gia}. "
        f"Thanh toán: {payment}. "
        f"Xem nhà: {xem}. "
        f"Vào ở: {vao}."
    )

    return text