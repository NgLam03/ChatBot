import streamlit as st
from OceanParkBot.src.search.search_pipeline import SearchPipeline
from PIL import Image
import os

# ===== KHỞI TẠO PIPELINE =====
@st.cache_resource
def load_pipeline():
    return SearchPipeline()

pipeline = load_pipeline()

st.set_page_config(page_title="OceanParkBot", layout="wide")

st.title("🏠 OceanParkBot – Chatbot tìm căn hộ Ocean Park")
st.write("Gõ câu hỏi vào bên dưới để tìm căn hộ phù hợp.")

query = st.text_input("Nhập câu hỏi:")

if st.button("Tìm kiếm"):
    if not query:
        st.warning("Bạn chưa nhập câu hỏi!")
    else:
        results = pipeline.run(query)

        if not results:
            st.error("Không tìm thấy căn phù hợp.")
        else:
            st.success(f"Tìm thấy {len(results)} căn phù hợp:")
            st.write("---")

            # HIỂN THỊ MỖI CĂN DẠNG CARD
            for item in results:
                col1, col2 = st.columns([1, 2])

                # === ẢNH ===
                with col1:
                    if "images" in item and item["images"]:
                        for img_path in item["images"][:2]:  # hiển thị max 2 ảnh
                            full_path = os.path.join("OceanParkBot", img_path)
                            if os.path.exists(full_path):
                                st.image(full_path, use_column_width=True)
                            else:
                                st.write("⚠ Không tìm thấy ảnh:", full_path)
                    else:
                        st.write("(Không có ảnh)")

                # === THÔNG TIN CĂN HỘ ===
                with col2:
                    st.subheader(f"🏷 Mã căn: {item.get('code')}")
                    st.write(f"**Tòa:** {item.get('building')}")
                    st.write(f"**View:** {item.get('view')}")
                    st.write(f"**Phòng:** {item.get('bedrooms')} ngủ – {item.get('bathrooms')} vệ sinh")
                    st.write(f"**Nội thất:** {item.get('furniture')}")
                    st.write(f"**Giá:** {item.get('price_display')}")
                    st.write(f"**Mô tả:** {item.get('description','(Không mô tả)')}")


            st.write("---")
