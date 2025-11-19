from OceanParkBot.src.search.search_pipeline import SearchPipeline
from OceanParkBot.src.response.response_text import format_result_text
from OceanParkBot.src.llm.extract_request_rule_regex import extract_request

# ----- BIẾN LƯU NGỮ CẢNH -----
last_filter = None


def main():
    global last_filter

    print("=== OceanParkBot Chatbot ===")
    print("Gõ 'exit' để thoát.\n")

    pipeline = SearchPipeline()

    while True:
        query = input("Bạn: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Bot: Tạm biệt!")
            break

        # ---- PHÂN TÍCH CÂU HỎI ----
        rules = extract_request(query)
        intent = rules.get("intent")

        # ---------------------------
        # GREETING
        # ---------------------------
        if intent == "greeting":
            print("Bot: Chào bạn! Bạn muốn tìm căn hộ như thế nào ạ?")
            continue

        # ---------------------------
        # COUNT ALL
        # ---------------------------
        if intent == "count_all":
            total = len(pipeline.metadata)
            print(f"Bot: Hiện tại có tổng cộng {total} căn trong dữ liệu.")
            continue

        # ---------------------------
        # COUNT BY BEDROOM
        # ---------------------------
        if intent == "count_by_bedroom":
            beds = rules["bedrooms"]
            last_filter = {"bedrooms": beds}  # Lưu context
            items = [x for x in pipeline.metadata if x.get("bedrooms") == beds]

            print(f"Bot: Có tổng cộng {len(items)} căn {beds} ngủ.")
            continue

        # ---------------------------
        # COUNT BY BATHROOM
        # ---------------------------
        if intent == "count_by_bathroom":
            baths = rules["bathrooms"]
            last_filter = {"bathrooms": baths}  # Lưu context
            items = [x for x in pipeline.metadata if x.get("bathrooms") == baths]

            print(f"Bot: Có tổng cộng {len(items)} căn {baths} vệ sinh.")
            continue

        # ---------------------------
        # COUNT BY BED + BATH
        # ---------------------------
        if intent == "count_by_bedbath":
            beds = rules["bedrooms"]
            baths = rules["bathrooms"]
            last_filter = {"bedrooms": beds, "bathrooms": baths}

            items = [
                x for x in pipeline.metadata
                if x.get("bedrooms") == beds and x.get("bathrooms") == baths
            ]

            print(f"Bot: Có tổng cộng {len(items)} căn {beds} ngủ {baths} vệ sinh.")
            continue

        # ---------------------------
        # COUNT BY VIEW
        # ---------------------------
        if intent == "count_by_view":
            view = rules["view"]
            last_filter = {"view": view}

            items = [x for x in pipeline.metadata if x.get("view") == view]

            print(f"Bot: Có tổng cộng {len(items)} căn view {view}.")
            continue

        # ---------------------------
        # SHOW EXAMPLES (dùng ngữ cảnh)
        # ---------------------------
        if intent == "show_examples":
            if last_filter is None:
                # Không có ngữ cảnh → fallback semantic search
                results = pipeline.searcher.search("căn hộ", top_k=5)
                print("\nBot:")
                print(format_result_text(results))
                print("\n" + "-"*50 + "\n")
                continue

            # Có ngữ cảnh → lọc đúng loại căn
            filtered = pipeline.metadata

            if "bedrooms" in last_filter:
                filtered = [x for x in filtered if x.get("bedrooms") == last_filter["bedrooms"]]

            if "bathrooms" in last_filter:
                filtered = [x for x in filtered if x.get("bathrooms") == last_filter["bathrooms"]]

            if "view" in last_filter:
                filtered = [x for x in filtered if x.get("view") == last_filter["view"]]

            results = filtered[:5]  # lấy 5 căn

            print("\nBot:")
            print(format_result_text(results))
            print("\n" + "-"*50 + "\n")
            continue

        # ---------------------------
        # FALLBACK → SEMANTIC SEARCH
        # ---------------------------
        results = pipeline.searcher.search(query, top_k=5)

        print("\nBot:")
        print(format_result_text(results))
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()
