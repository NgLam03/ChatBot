import os

# Thư mục chứa file path.py  → OceanParkBot/src/config
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục src → OceanParkBot/src
SRC_DIR = os.path.abspath(os.path.join(CONFIG_DIR, ".."))

# Thư mục gốc dự án → OceanParkBot/
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, ".."))

# ============================
# PATH CHO CÁC FOLDER CHÍNH
# ============================

# DATA nằm cạnh src
DATA_DIR = os.path.join(ROOT_DIR, "data")
ASSET_DIR = os.path.join(ROOT_DIR, "assets")

# Subdirs
DATA_RAW = os.path.join(DATA_DIR, "raw")
DATA_CLEANED = os.path.join(DATA_DIR, "cleaned")
DATA_VECTOR = os.path.join(DATA_DIR, "vector_store")

ASSET_IMAGES = os.path.join(ASSET_DIR, "images")

def path_from_root(*parts):
    """Tạo path tuyệt đối từ ROOT_DIR."""
    return os.path.join(ROOT_DIR, *parts)

def path_from_data(*parts):
    """Tạo path tuyệt đối từ DATA_DIR."""
    return os.path.join(DATA_DIR, *parts)

def path_from_assets(*parts):
    """Tạo path tuyệt đối từ ASSET_DIR."""
    return os.path.join(ASSET_DIR, *parts)