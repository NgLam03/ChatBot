def format_result_with_images(results: list, limit_images=3):
    """
    Format trả về kết quả có kèm ảnh.
    - results: list kết quả từ search_pipeline
    - limit_images: số ảnh tối đa muốn gửi cho mỗi căn (mặc định 3)
    """

    if not results:
        return {
            "message": "Không tìm thấy căn nào phù hợp.",
            "items": []
        }

    formatted_items = []

    for item in results:
        ms = item.get("ms", "N/A")
        building = item.get("building", "N/A")
        view = item.get("view", "N/A")
        bedrooms = item.get("bedrooms", "N/A")
        bathrooms = item.get("bathrooms", "N/A")
        furniture = item.get("furniture", "N/A")

        price = item.get("price", None)
        if price is None:
            price_text = "N/A"
        else:
            tr = price / 1_000_000
            if tr.is_integer():
                price_text = f"{int(tr)}tr"
            else:
                price_text = f"{tr:.1f}tr"

        # Lấy ảnh (nếu có)
        imgs = item.get("images", [])
        imgs = imgs[:limit_images]  # giới hạn số lượng ảnh

        formatted_items.append({
            "ms": ms,
            "building": building,
            "view": view,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "furniture": furniture,
            "price": price_text,
            "images": imgs
        })

    return {
        "message": "Tìm thấy các căn phù hợp:",
        "items": formatted_items
    }


# TEST
if __name__ == "__main__":
    fake = [
        {
            "ms": "A3068",
            "building": "S2.05",
            "view": "VinUni",
            "bedrooms": 2,
            "bathrooms": 1,
            "furniture": "full",
            "price": 8000000,
            "images": [
                "images/A3068/img1.jpg",
                "images/A3068/img2.jpg",
                "images/A3068/img3.jpg",
                "images/A3068/img4.jpg"
            ]
        }
    ]

    out = format_result_with_images(fake)
    print(out)
