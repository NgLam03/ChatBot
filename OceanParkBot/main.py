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

        # ========== XỬ LÝ INTENT Ở ĐÂY ==========
        rules = extract_request(query)

        if rules.get("intent") == "greeting":
            print("\nBot: Chào bạn! Bạn muốn tìm căn hộ như thế nào ạ?\n")
            continue

        if rules.get("intent") == "unknown":
            print("\nBot: Bạn mô tả rõ hơn giúp mình nhé (ví dụ: 2 ngủ dưới 8tr, full đồ...)\n")
            continue

        # ========== CHỈ CHẠY SEARCH NẾU intent = search ==========
        results = pipeline.run(query)

        response = format_result_text(results)

        print("\nBot:")
        print(response)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()
