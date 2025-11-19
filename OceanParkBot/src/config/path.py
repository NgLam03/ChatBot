import os

# Thư mục chứa file path.py (tức: OceanParkBot/src)
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục gốc của project: OceanParkBot/
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, ".."))

# Thư mục data
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Thư mục assets
ASSET_DIR = os.path.join(ROOT_DIR, "assets")

# Sub-folder bên trong data
DATA_CLEANED = os.path.join(DATA_DIR, "cleaned")
DATA_RAW = os.path.join(DATA_DIR, "raw")
DATA_VECTOR = os.path.join(DATA_DIR, "vector_store")

# Sub-folder bên trong assets
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