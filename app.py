import streamlit as st
from OceanParkBot.src.search.search_pipeline import SearchPipeline
from OceanParkBot.src.llm.extract_request_rule_regex_nltk import extract_request
from PIL import Image
import os

@st.cache_resource
def load_pipeline():
    return SearchPipeline()

pipeline = load_pipeline()

st.set_page_config(page_title="OceanParkBot", layout="wide")

st.title("OceanParkBot – Chatbot tìm căn hộ Ocean Park")

query = st.text_input("Nhập câu hỏi:", key="user_input")

# Nút tìm kiếm (chạy lại mỗi lần bấm)
if st.button("Tìm kiếm", key="search_btn"):

    if not query.strip():
        st.warning("Bạn chưa nhập câu hỏi!")
        st.stop()

    # chạy phân tích + tìm kiếm
    rules = extract_request(query)
    results = pipeline.run(query)

    if not results:
        st.error("Không tìm thấy căn phù hợp.")
        st.stop()

    st.success(f"🔎 Tìm thấy {len(results)} căn phù hợp:")
    st.write("---")

    # HIỂN THỊ KẾT QUẢ
    for item in results:
        col1, col2 = st.columns([1, 2])

        with col1:
            images = item.get("images", [])
            if images:
                for img_path in images[:2]:
                    full = os.path.join("OceanParkBot", img_path)
                    if os.path.exists(full):
                        st.image(full, use_column_width=True)
                    else:
                        st.write("⚠ Không tìm thấy ảnh:", full)
            else:
                st.write("(Không có ảnh)")

        with col2:
            st.subheader(f"🏷 Mã căn: {item.get('code')}")
            st.write(f"• **Tòa:** {item.get('building')}")
            st.write(f"• **View:** {item.get('view')}")
            st.write(f"• **Phòng:** {item.get('bedrooms')} ngủ – {item.get('bathrooms')} vệ sinh")
            st.write(f"• **Nội thất:** {item.get('furniture')}")
            st.write(f"• **Giá:** {item.get('price_display')}")
            st.write(f"• **Mô tả:** {item.get('description','(Không mô tả)')}")

    st.write("---")
