# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Lê Minh Hoàng
- **Student ID**: 2A202600101
- **Date**: 06/04/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implemented**: `Day-3-Lab-Chatbot-vs-react-agent\src\agent\agent.py`
- **Code Highlights**:
  - Hoàn thiện vòng lặp ReAct trong `ReActAgent.run()` để gọi LLM, phân tích `Action:` và thực thi công cụ.
  - Thêm `get_system_prompt()` để định nghĩa prompt chứa danh sách tool và hướng dẫn định dạng `Thought` / `Action` / `Observation` / `Final Answer`.
  - Xây dựng `_execute_tool()` và `_parse_args()` để parse tham số tool, hỗ trợ chuỗi có ngoặc kép/nháy đơn và gọi đúng hàm công cụ.
- **Documentation**:
  - `ReActAgent.run()` tạo prompt ban đầu từ truy vấn người dùng, sau đó lặp lại: hỏi LLM, parse hành động, gọi tool, thêm observation và tiếp tục.
  - Khi LLM trả về `Final Answer:`, agent kết thúc vòng lặp và trả câu trả lời cuối cùng.
  - Cơ chế này giúp agent không chỉ trả lời trực tiếp mà còn thực hiện thao tác ngoài mô hình khi cần thông tin mới.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Baseline chatbot bị cutoff dữ liệu 2024 khi hỏi giá xăng. Khi test câu hỏi "giá xăng ngày hôm nay là gì", mô hình chỉ trả về giá từ dữ liệu huấn luyện cũ, không có thông tin thời gian thực.
- **Log Source**: `logs/2026-04-06.log`
  - Ví dụ: `AGENT_START` lúc `08:08:06`, truy vấn `giá xăng ngày hôm nay là gì`
  - LLM đã sinh: `Action: search_web(query="giá xăng hôm nay Việt Nam")`
  - Observation cho thấy giá xăng vẫn được trích từ thông tin chỉnh sửa ngày `23/05/2024`.
- **Diagnosis**: Lỗi chính là do baseline chatbot chỉ dựa vào kiến thức tĩnh của mô hình. Mô hình có kiến thức cutoff nên không thể biết giá xăng hiện tại nếu không sử dụng tool truy vấn web thực tế.
- **Solution**: Thiết kế agent ReAct để ưu tiên gọi tool khi cần thông tin thời gian thực. Trong `agent.py`, vòng lặp `Thought-Action-Observation` cho phép agent xác định rõ khi nào cần tool, sau đó dùng kết quả `Observation` để tạo `Final Answer` chính xác hơn.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: `Thought` buộc agent giải thích suy nghĩ trước khi hành động. Điều này giúp agent nhận ra yêu cầu cần truy vấn thông tin bên ngoài, thay vì trả lời ngay bằng kiến thức cũ như chatbot.
2.  **Reliability**: Agent có thể hoạt động kém hơn khi bài toán quá đơn giản hoặc khi parser tool sai. Với câu hỏi chào hỏi, chatbot trả lời nhanh, còn agent nếu không cần tool sẽ mất thêm bước xác nhận, nên độ trễ cao hơn.
3.  **Observation**: Feedback từ tool (`Observation`) định hướng bước kế tiếp. Ví dụ, sau khi `search_web` trả về giá xăng năm 2024, agent biết rõ nguồn dữ liệu và có thể kết luận rằng cần cập nhật hoặc cảnh báo người dùng nếu muốn thông tin hiện tại.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Triển khai hàng đợi bất đồng bộ cho tool calls, cho phép agent gọi nhiều công cụ cùng lúc và xử lý song song.
- **Safety**: Thêm lớp kiểm tra hành động trước khi thực thi tool, hoặc dùng một LLM giám sát (Supervisor) để audit `Action` và chặn truy vấn nhạy cảm.
- **Performance**: Lưu cache kết quả tool cho các yêu cầu gần giống nhau, dùng vector DB để truy vấn lại nhanh các thông tin đã thu thập và giảm tải cho LLM.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
