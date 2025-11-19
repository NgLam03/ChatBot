from .src.search.search_pipeline import SearchPipeline
from .src.response.response_text import format_result_text


def main():
    print("=== OceanParkBot Chatbot ===")
    pipeline = SearchPipeline()

    while True:
        query = input("\nBạn: ")

        if query.lower() in ["exit", "quit"]:
            print("Tạm biệt!")
            break

        results = pipeline.run(query)

        if not results:
            print("Bot: Không tìm thấy căn nào phù hợp.")
            continue

        print("\nBot:")
        print(format_result_text(results))


if __name__ == "__main__":
    main()
