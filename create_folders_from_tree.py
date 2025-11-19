import os
import re

def create_folders_from_tree(tree_file, base_path):
    with open(tree_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    stack = [base_path]
    prev_level = 0

    for line in lines:
        raw = line.rstrip("\n")

        # Bỏ dòng trống
        if not raw.strip():
            continue

        # Bỏ dòng root kiểu: OceanParkBot/
        if raw.strip().endswith("/") and raw.strip().count(" ") == 0:
            root_name = raw.strip().rstrip("/")
            root_path = os.path.join(base_path, root_name)
            os.makedirs(root_path, exist_ok=True)
            stack = [root_path]
            continue

        # Tính level dựa vào số lần xuất hiện của "│   "
        level = raw.count("│   ")

        # Lấy tên thật
        name = re.split(r"[├└]── ", raw)[-1].strip().rstrip("/")

        # Đúng cấp indent: điều chỉnh stack
        while len(stack) > level + 1:
            stack.pop()

        # Tạo path đầy đủ
        full_path = os.path.join(stack[-1], name)

        # Nếu là file
        if "." in name:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            open(full_path, "a", encoding="utf-8").close()
        else:
            os.makedirs(full_path, exist_ok=True)
            stack.append(full_path)

    print("Done! Đã tạo đúng toàn bộ cây thư mục.")

if __name__ == "__main__":
    # 🔧 Đường dẫn file tree và thư mục gốc cần tạo
    tree_file = r"D:\Xu_Ly_Ngon_Ngu_Tu_Nhien\ChatBoT\ChatBot\tree.txt"
    base_output = r"D:\Xu_Ly_Ngon_Ngu_Tu_Nhien\ChatBoT\ChatBot"

    os.makedirs(base_output, exist_ok=True)
    created = create_folders_from_tree(tree_file, base_output)

    print(f"✅ Đã tạo {len(created)} mục (folder + file) trong: {base_output}")
