import re
from openai import OpenAI

client = OpenAI()

PROMPT_TEMPLATE = """
Bạn là AI chuyên phân tích yêu cầu tìm căn hộ tại Ocean Park.
Hãy trích xuất yêu cầu của người dùng thành JSON.

Các trường cần có (nếu không có, để null):
- bedrooms (int)
- bathrooms (int)
- furniture ("full", "co_ban", "none")
- price_min (int)
- price_max (int)
- building (string hoặc null)
- view (string hoặc null)
- move_in (string hoặc null)

Dữ liệu đầu vào: "{query}"

Trả về đúng JSON, không thêm giải thích.
"""

def extract_request(query: str):
    prompt = PROMPT_TEMPLATE.format(query=query)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    # LLM trả về JSON dạng text → convert
    import json
    try:
        data = json.loads(answer)
    except:
        data = {}

    return data


if __name__ == "__main__":
    q = "tìm căn 2 ngủ full đồ 8-10tr view VinUni"
    print(extract_request(q))
