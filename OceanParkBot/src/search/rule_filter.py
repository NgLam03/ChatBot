def match_numeric(value, target):
    """Nếu target là None → không filter."""
    if target is None:
        return True
    return value == target


def match_max(value, max_value):
    """Giá <= max_value."""
    if max_value is None:
        return True
    return value <= max_value


def match_min(value, min_value):
    """Giá >= min_value."""
    if min_value is None:
        return True
    return value >= min_value


def match_text(value, target):
    """So khớp text (chính xác)."""
    if target is None:
        return True
    if value is None:
        return False
    return value.lower() == target.lower()


def rule_filter(results, query_rules):
    """
    results: list kết quả từ semantic_search (metadata)
    query_rules: JSON parse từ extract_request
    
    Trả về danh sách căn hộ thỏa tất cả rule.
    """

    filtered = []

    for item in results:
        ok = True

        # ===== BEDROOMS =====
        if query_rules.get("bedrooms") is not None:
            if item.get("bedrooms") != query_rules["bedrooms"]:
                ok = False

        # ===== BATHROOMS =====
        if query_rules.get("bathrooms") is not None:
            if item.get("bathrooms") != query_rules["bathrooms"]:
                ok = False

        # ===== FURNITURE =====
        if query_rules.get("furniture") is not None:
            if item.get("furniture") != query_rules["furniture"]:
                ok = False

        # ===== PRICE MIN/MAX =====
        if query_rules.get("price_min") is not None:
            if item.get("price") < query_rules["price_min"]:
                ok = False

        if query_rules.get("price_max") is not None:
            if item.get("price") > query_rules["price_max"]:
                ok = False

        # ===== VIEW =====
        if query_rules.get("view") is not None:
            if item.get("view") is None or item.get("view").lower() != query_rules["view"].lower():
                ok = False

        # ===== BUILDING =====
        if query_rules.get("building") is not None:
            if item.get("building") is None or item.get("building").lower() != query_rules["building"].lower():
                ok = False

        # ===== MOVE IN =====
        if query_rules.get("move_in") is not None:
            # move_in = "ngay", "cuối tháng"
            if item.get("move_in") is None or item.get("move_in") != query_rules["move_in"]:
                ok = False

        if ok:
            filtered.append(item)

    return filtered


# test
if __name__ == "__main__":
    fake_results = [
        {
            "ms": "A3068",
            "bedrooms": 2,
            "bathrooms": 1,
            "furniture": "full",
            "price": 8000000,
            "view": "VinUni",
            "building": "S2"
        },
        {
            "ms": "B2001",
            "bedrooms": 1,
            "bathrooms": 1,
            "furniture": "co_ban",
            "price": 7000000,
            "view": "Hồ",
            "building": "S3"
        }
    ]

    rules = {
        "bedrooms": 2,
        "furniture": "full",
        "price_max": 9000000,
        "view": "VinUni",
        "building": None
    }

    print(rule_filter(fake_results, rules))
