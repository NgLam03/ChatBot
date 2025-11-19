from .src.search.search_pipeline import SearchPipeline
from .src.response.response_text import format_result_text
from .src.llm.extract_request_rule_regex import extract_request


def main():
    print("=== OceanParkBot Chatbot ===")
    print("Gõ 'exit' để thoát.\n")

    pipeline = SearchPipeline()

    while True:
        query = input("Bạn: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Bot: Tạm biệt!")
            break

        rules = extract_request(query)
        intent = rules.get("intent")

        # =========================
        # INTENT HANDLING
        # =========================

        if intent == "greeting":
            print("\nBot: Chào bạn! Bạn muốn tìm căn hộ như thế nào ạ?\n")
            continue

        if intent == "unknown":
            print("\nBot: Bạn mô tả rõ hơn giúp mình nhé (vd: 2 ngủ dưới 8tr, full đồ...)\n")
            continue

        if intent == "count_all":
            total = len(pipeline.metadata)
            print(f"\nBot: Hiện tại có tổng cộng {total} căn trong dữ liệu.\n")
            continue

        if intent == "count_by_bedroom":
            b = rules["bedrooms"]
            total = sum(1 for x in pipeline.metadata if x.get("bedrooms") == b)
            print(f"\nBot: Có tổng cộng {total} căn {b} ngủ.\n")
            continue
        
        if intent == "count_by_view":
            v = rules["view"]
            total = sum(1 for x in pipeline.metadata if x.get("view") == v)
            print(f"\nBot: Có tổng cộng {total} căn view {v}.\n")
            continue

        if intent == "cheapest":
            cheapest = min(pipeline.metadata, key=lambda x: x.get("price", 999999999))
            print("\nBot: Đây là căn rẻ nhất:\n")
            print(format_result_text([cheapest]))
            continue

        if intent == "expensive":
            expensive = max(pipeline.metadata, key=lambda x: x.get("price", 0))
            print("\nBot: Đây là căn đắt nhất:\n")
            print(format_result_text([expensive]))
            continue

        # =========================
        # DEFAULT: SEARCH
        # =========================

        results = pipeline.run(query)
        response = format_result_text(results)

        print("\nBot:")
        print(response)
        print("\n------------------------------------\n")


if __name__ == "__main__":
    main()
