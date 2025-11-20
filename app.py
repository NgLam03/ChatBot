import streamlit as st
import os
from PIL import Image

# ==== IMPORT BACKEND ====
from OceanParkBot.src.search.search_pipeline import SearchPipeline
from OceanParkBot.src.response.response_text import format_result_text
from OceanParkBot.src.llm.extract_request_rule_regex_nltk import extract_request


# ==== CACHE PIPELINE ====
@st.cache_resource
def load_pipeline():
    return SearchPipeline()

pipeline = load_pipeline()

# ==== NGỮ CẢNH ====
if "last_filter" not in st.session_state:
    st.session_state.last_filter = None


# ==== STREAMLIT UI ====
st.set_page_config(page_title="OceanParkBot", layout="wide")
st.title("OceanParkBot – Chatbot tìm căn hộ Ocean Park")


query = st.text_input("Nhập câu hỏi của bạn:")

if st.button("Tìm kiếm"):

    if not query.strip():
        st.warning("⚠ Bạn chưa nhập gì!")
        st.stop()

    rules = extract_request(query)
    intent = rules.get("intent")

    # ====================================
    # GREETING
    # ====================================
    if intent == "greeting":
        st.success("Chào bạn! Bạn muốn tìm căn hộ như thế nào ạ?")
        st.stop()

    # ====================================
    # COUNT ALL
    # ====================================
    if intent == "count_all":
        total = len(pipeline.metadata)
        st.info(f"Hiện tại có tổng cộng **{total} căn** trong dữ liệu.")
        st.stop()

    # ====================================
    # COUNT BY BEDROOM
    # ====================================
    if intent == "count_by_bedroom":
        beds = rules["bedrooms"]
        st.session_state.last_filter = {"bedrooms": beds}

        items = [x for x in pipeline.metadata if x.get("bedrooms") == beds]
        st.info(f"Có tổng cộng **{len(items)} căn {beds} ngủ**.")
        st.stop()

    # ====================================
    # COUNT BY BATHROOM
    # ====================================
    if intent == "count_by_bathroom":
        baths = rules["bathrooms"]
        st.session_state.last_filter = {"bathrooms": baths}

        items = [x for x in pipeline.metadata if x.get("bathrooms") == baths]
        st.info(f"Có tổng cộng **{len(items)} căn {baths} vệ sinh**.")
        st.stop()

    # ====================================
    # COUNT BY BED + BATH
    # ====================================
    if intent == "count_by_bedbath":
        beds = rules["bedrooms"]
        baths = rules["bathrooms"]
        st.session_state.last_filter = {"bedrooms": beds, "bathrooms": baths}

        items = [x for x in pipeline.metadata
                 if x.get("bedrooms") == beds and x.get("bathrooms") == baths]

        st.info(f"Có tổng cộng **{len(items)} căn {beds} ngủ {baths} vệ sinh**.")
        st.stop()

    # ====================================
    # COUNT BY VIEW
    # ====================================
    if intent == "count_by_view":
        view = rules["view"]
        st.session_state.last_filter = {"view": view}

        items = [x for x in pipeline.metadata if x.get("view") == view]

        st.info(f"Có tổng cộng **{len(items)} căn view {view}**.")
        st.stop()

    # ====================================
    # SHOW EXAMPLES
    # ====================================
    if intent == "show_examples":

        # Không có ngữ cảnh → fallback search
        if st.session_state.last_filter is None:
            results = pipeline.searcher.search("căn hộ", top_k=5)
        else:
            filtered = pipeline.metadata

            if "bedrooms" in st.session_state.last_filter:
                filtered = [x for x in filtered if x.get("bedrooms") ==
                            st.session_state.last_filter["bedrooms"]]

            if "bathrooms" in st.session_state.last_filter:
                filtered = [x for x in filtered if x.get("bathrooms") ==
                            st.session_state.last_filter["bathrooms"]]

            if "view" in st.session_state.last_filter:
                filtered = [x for x in filtered if x.get("view") ==
                            st.session_state.last_filter["view"]]

            results = filtered[:5]

        # ==== HIỂN THỊ DANH SÁCH ====
        st.subheader("Danh sách căn phù hợp:")
        st.write("---")

        for item in results:
            col1, col2 = st.columns([1, 2])

            with col1:
                imgs = item.get("images", [])
                if imgs:
                    for img_path in imgs[:2]:
                        full = os.path.join("OceanParkBot", img_path)
                        if os.path.exists(full):
                            st.image(full, use_column_width=True)
                else:
                    st.write("(Không có ảnh)")

            with col2:
                st.markdown(f"### 🏷 {item.get('code')}")
                st.write(f"• **Tòa:** {item.get('building')}")
                st.write(f"• **View:** {item.get('view')}")
                st.write(f"• **Phòng:** {item.get('bedrooms')} ngủ – {item.get('bathrooms')} vệ sinh")
                st.write(f"• **Nội thất:** {item.get('furniture')}")
                st.write(f"• **Giá:** {item.get('price_display')}")
                st.write(f"• **Mô tả:** {item.get('description', '(Không mô tả)')}")

        st.write("---")
        st.stop()

    # ====================================
    # FALLBACK → SEMANTIC SEARCH
    # ====================================
    results = pipeline.searcher.search(query, top_k=5)

    st.subheader("Kết quả tìm kiếm:")
    st.write("---")

    for item in results:
        col1, col2 = st.columns([1, 2])

        with col1:
            imgs = item.get("images", [])
            if imgs:
                for img_path in imgs[:2]:
                    full = os.path.join("OceanParkBot", img_path)
                    if os.path.exists(full):
                        st.image(full, use_column_width=True)

        with col2:
            st.markdown(f"### 🏷 {item.get('code')}")
            st.write(f"• **Tòa:** {item.get('building')}")
            st.write(f"• **View:** {item.get('view')}")
            st.write(f"• **Phòng:** {item.get('bedrooms')} ngủ – {item.get('bathrooms')} vệ sinh")
            st.write(f"• **Nội thất:** {item.get('furniture')}")
            st.write(f"• **Giá:** {item.get('price_display')}")
            st.write(f"• **Mô tả:** {item.get('description', '(Không mô tả)')}")

    st.write("---")
