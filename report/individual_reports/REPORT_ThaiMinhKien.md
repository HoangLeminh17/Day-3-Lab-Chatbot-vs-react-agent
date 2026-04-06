# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: [Thái Minh Kiên]
- **Student ID**: [2A202600288]
- **Date**: [06/04/2026]

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: [e.g., `src/tools/similar_recipe_recommend.py`]
- **Code Highlights**: 
```python 
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
```
- **Documentation**: Khi người dùng yêu cầu đưa ra các món ăn tương tự với món nào, thì agent sẽ sử dụng tavily search để tìm các món ăn tương tự

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Đã define tool(cụ thể là tìm món ăn tương tự) nhưng agent khi được yêu cầu tìm món ăn vẫn ko sử dụng tool.
- **Diagnosis**: Mặc dù đã có file define tool nhưng chưa đưa tool vào list các tool sử dụng cho agent.
- **Solution**: phải update thêm tool vào list các tool agent sử dụng trong file run_agent.py --> lúc yêu cầu tìm các món ăn tương tự agent đã sử dụng tool để tìm.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: Điểm khác biệt lớn nhất em nhận thấy là ReAct Agent không chỉ tạo câu trả lời trực tiếp mà còn tạo ra một bước suy luận trung gian thông qua Thought. Bước này giúp mô hình xác định khi nào cần gọi công cụ thay vì đoán bằng kiến thức sẵn có. Với các bài toán cần tra cứu hoặc cần dữ liệu bên ngoài, Thought làm cho quá trình giải quyết bài toán có cấu trúc hơn so với chatbot thông thường.
2.  **Reliability**: Tuy nhiên, Agent không phải lúc nào cũng tốt hơn Chatbot. Trong các câu hỏi đơn giản, chatbot thường nhanh hơn và ổn định hơn vì không cần qua thêm bước chọn tool, parse action và xử lý observation. Agent có thể hoạt động tệ hơn khi prompt chưa đủ chặt, mô tả tool chưa rõ, hoặc output của model không đúng format mà parser mong đợi. Khi đó hệ thống dễ lỗi hơn chatbot thường.
3.  **Observation**: Observation là điểm quan trọng nhất của ReAct. Sau mỗi action, agent nhận lại kết quả thực tế từ, ví dụ dữ liệu từ tool hoặc thông báo lỗi. Observation giúp mô hình điều chỉnh bước tiếp theo thay vì tiếp tục suy luận mù. Em thấy đây là khác biệt bản chất giữa chatbot trả lời một lượt và agent có khả năng tương tác qua nhiều bước.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Nếu mở rộng hệ thống lên production, em sẽ tách tool execution thành service riêng hoặc hàng đợi bất đồng bộ để xử lý các tool call chậm như web search hoặc database query.
- **Safety**:Em sẽ thêm một lớp kiểm tra action trước khi thực thi, ví dụ xác thực tên tool, kiểm tra schema của arguments, và giới hạn số bước lặp để tránh agent chạy sai hoặc lặp vô hạn.
- **Performance**: Khi số lượng tools tăng lên, em sẽ dùng cơ chế tool selection thông minh hơn, chẳng hạn semantic retrieval hoặc vector search trên mô tả tool, để agent chỉ nhìn thấy những tool liên quan thay vì toàn bộ danh sách.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
