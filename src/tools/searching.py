import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def search(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query, max_results=5)

    res = ""
    # Lấy danh sách kết quả, nếu không có thì trả về list rỗng []
    results = response.get('results', [])

    # Lặp qua các kết quả thực tế lấy được (có bao nhiêu lặp bấy nhiêu)
    for i, item in enumerate(results):
        res += f"Result {i + 1}:\n"
        res += item['content'] + "\n\n"

    # Nếu không có kết quả nào, báo lại cho AI biết để nó tự xử lý
    if not res:
        return "No results found for this query."

    return res