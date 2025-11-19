import os

def build_tree(startpath, indent=""):
    """Đệ quy duyệt cây thư mục và trả về chuỗi kết quả"""
    tree_str = ""
    items = sorted(os.listdir(startpath))
    for index, name in enumerate(items):
        path = os.path.join(startpath, name)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        tree_str += indent + connector + name + "\n"
        if os.path.isdir(path):
            new_indent = indent + ("    " if is_last else "│   ")
            tree_str += build_tree(path, new_indent)
    return tree_str


if __name__ == "__main__":
    # 🔧 CHỈNH SỬA ĐƯỜNG DẪN Ở ĐÂY
    folder_path = r"C:\Users\Admin\Documents\NLP\ChatBot\OceanParkBot"

    if not os.path.isdir(folder_path):
        print("❌ Thư mục không tồn tại!")
    else:
        print(f"🔍 Đang quét thư mục: {folder_path}")

        result = f"Cấu trúc thư mục của: {folder_path}\n\n"
        result += build_tree(folder_path)

        # Xuất ra file cùng thư mục chứa script
        output_file = "tree_structure.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✅ Hoàn tất! Cấu trúc đã được lưu vào file: {output_file}")
