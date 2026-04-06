import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def suggest_similar_by_tavily(dish_name: str):
    """
    Gợi ý các món ăn tương tự sử dụng AI Search (Tavily).
    
    Cơ chế: 
    - Thực hiện tìm kiếm chuyên sâu (advanced search) dựa trên hương vị và cách chế biến.
    - Trích xuất câu trả lời tổng hợp từ AI và top 3 nguồn tham khảo uy tín.
    
    Args:
        dish_name (str): Tên món ăn cần tìm kiếm sự tương đồng.
        
    Returns:
        dict: Chứa 'summary' (tóm tắt lý do) và 'details' (danh sách món & URL).
        str: Thông báo lỗi nếu thiếu API Key hoặc lỗi kết nối.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Lỗi: Thiếu TAVILY_API_KEY trong .env"

    tavily = TavilyClient(api_key=api_key)
    
    # Câu lệnh search tập trung vào sự tương đồng
    query = f"Các món ăn có hương vị và cách chế biến tương tự như {dish_name}"

    try:
        # search_depth="advanced" lấy kết quả chất lượng hơn
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_answer=True # Tavily tự tổng hợp câu trả lời ngắn gọn
        )

        # 1. Lấy câu trả lời tổng hợp từ AI của Tavily (nếu có)
        ai_answer = response.get("answer")
        
        # 2. Lấy danh sách các nguồn tham khảo
        results = response.get("results", [])
        
        suggestions = []
        for res in results:
            suggestions.append({
                "title": res.get("title"),
                "content": res.get("content")[:200] + "...", # Cắt bớt cho gọn
                "url": res.get("url")
            })

        return {
            "summary": ai_answer,
            "details": suggestions
        }

    except Exception as e:
        return f"Lỗi khi gọi Tavily: {e}"

