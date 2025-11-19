from .src.search.search_pipeline import SearchPipeline
from .src.response.response_text import format_result_text


def main():
    print("=== OceanParkBot Chatbot ===")
    print("Gõ 'exit' để thoát.\n")

    pipeline = SearchPipeline()

    while True:
        query = input("Bạn: ")

        if query.lower().strip() in ["exit", "quit"]:
            print("Bot: Tạm biệt!")
            break

        # chạy pipeline tìm kiếm
        results = pipeline.run(query)

        # format kết quả
        response = format_result_text(results)

        print("\nBot:")
        print(response)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    main()
