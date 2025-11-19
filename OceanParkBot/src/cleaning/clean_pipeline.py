import json
import os

from .normalize_price import normalize_price
from .normalize_type import normalize_type
from .normalize_text import build_text_for_embedding

from OceanParkBot.src.config.path import DATA_RAW, DATA_CLEANED

def clean_item(raw):
    """
    Chuyển từ raw object → clean object
    """
    # --- Chuẩn hoá loại căn ---
    bedrooms, bathrooms = normalize_type(raw.get("loai_can", ""))

    # --- Chuẩn hoá giá ---
    price_value = normalize_price(raw.get("gia", ""))

    # --- Chuẩn hoá text embedding ---
    text_for_embed = build_text_for_embedding(raw)

    # --- Chuẩn hoá view + building ---
    # ví dụ: "S2 VIEW VINUNI"
    ma_can = raw.get("ma_can", "").upper()

    building = None
    view = "Nội khu"

    # tách building (S1, S2.03…)
    import re
    match_build = re.findall(r"S\d+\.?\d*", ma_can)
    if match_build:
        building = match_build[0]

    # tách view
    if "VINUNI" in ma_can:
        view = "VinUni"
    elif "HỒ" in ma_can:
        view = "Hồ"

    # OBJECT sạch
    cleaned = {
        "ms": raw.get("ms"),

        "title": f"Căn {building}, view {view}, {bedrooms} ngủ, {raw.get('gia', '')}",

        "building": building,
        "view": view,

        "type": raw.get("loai_can"),
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,

        "furniture": raw.get("noi_that", "").lower(),

        "price": price_value,
        "price_text": raw.get("gia"),

        "payment": raw.get("hinh_thuc_dong"),
        "visit": raw.get("thoi_gian_xem"),
        "move_in": raw.get("thoi_gian_vao_o"),

        "raw_fields": {
            "noi_that": raw.get("noi_that"),
            "loai_can": raw.get("loai_can"),
            "ma_can": raw.get("ma_can")
        },

        "text_for_embedding": text_for_embed,

        "images": raw.get("images", [])
    }

    return cleaned



def run_clean_pipeline(raw_path=None,out_path=None):
    """
    Chạy pipeline:
    - đọc raw json
    - clean từng item
    - ghi ra listings_clean.json
    """
    if raw_path is None:
        raw_path = os.path.join(DATA_RAW, "listings_raw.json")

    if out_path is None:
        out_path = os.path.join(DATA_CLEANED, "listings_clean.json")
    print(">>> Loading raw data...")
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print(f">>> Cleaning {len(raw_data)} listings...")
    cleaned_list = [clean_item(item) for item in raw_data]

    # tạo folder output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(">>> Saving cleaned data...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_list, f, ensure_ascii=False, indent=4)

    print(">>> DONE! Clean data saved to:", out_path)



if __name__ == "__main__":
    run_clean_pipeline()
