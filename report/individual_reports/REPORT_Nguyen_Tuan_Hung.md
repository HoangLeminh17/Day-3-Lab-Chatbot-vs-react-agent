# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyễn Tuấn Hưng
- **Student ID**: 2A202600230
- **Date**: 06/04/2026

## I. Technical Contribution (15 Points)

- **Modules Implementated**: `src/tools/voice_interaction.py` và `run_agent.py`
- **Code Highlights**: 
  Xây dựng lớp `VoiceInteractionTool` sử dụng thư viện `SpeechRecognition` để thu thập âm thanh qua microphone mặc định của hệ thống (`sr.Microphone()`). Module tích hợp tính năng tự động điều chỉnh độ nhạy theo tiếng ồn môi trường (`ambient_duration`, `adjust_for_ambient_noise`) và gọi public API Google Speech Recognition (`recognize_google`) để xử lý Speech-to-Text. Chức năng hỗ trợ tùy chỉnh ngôn ngữ (mặc định: `vi-VN`) cùng cấu hình ngắt nhịp (`pause_threshold`) qua biến môi trường.
- **Documentation**: 
  Công cụ cung cấp luồng tương tác linh hoạt xử lý và chuyển đổi giọng nói thành văn bản. Khi được tích hợp trên `run_agent.py`, người dùng có thể kích hoạt chế độ lắng nghe bằng câu lệnh "voice". Âm thanh thu được sẽ được chuyển thành dạng text làm input cho Agent xử lý, nhờ đó người dùng có thể vừa nấu ăn vừa tương tác với Agent.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Khi người dùng kích hoạt "voice" nhưng không nói gì hoặc xuất hiện tạp âm lớn, phương thức thu âm trả về dữ liệu rác, gây ra lỗi crash chương trình do không thể dịch ra văn bản thông qua API.
- **Log Source**: In ra exception `sr.UnknownValueError` từ module nhận dạng của SpeechRecognition.
- **Diagnosis**: Hàm `recognize_google` không thể biên dịch một đoạn audio rỗng hoặc quá nhiễu dẫn đến văng exception. Nếu không xử lý kịp thời ở lớp giao tiếp, ReAct Agent sẽ bị dừng đột ngột (crash vòng lặp while).
- **Solution**: Bổ sung khối `try-except` bên trong hàm bắt các lỗi chuyên biệt như `sr.UnknownValueError` và `sr.RequestError`. Các lỗi này in ra thông báo "Could not understand audio" và trả về `None`, qua đó vòng lặp main ở `run_agent.py` bắt được và yêu cầu thu âm lại.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1.  **Reasoning**: Khối `Thought` giúp Agent hiểu rõ ngữ cảnh của mệnh lệnh giọng nói, chuyển âm thanh thành văn bản, phân tích từ khóa, sau đó suy luận ý nghĩa thay vì xử lý máy móc từ khóa ra text như Chatbot thông thường.
2.  **Reliability**: Việc tích hợp Voice API đi kèm với độ trễ và trong môi trường ồn ào, kết quả nhận giọng nói bị sai sẽ điều hướng quá trình suy luận của hành động đi chệch khỏi định hướng ban đầu.
3.  **Observation**: Phản hồi từ các tool giúp tác tử ReAct điều hướng linh hoạt hơn. Nếu văn bản dịch ra từ giọng nói không rõ ý, hoặc Observation trả về lỗi do tham số trích xuất sai, Agent có thể quan sát, suy luận tiếp và tự động gọi lại.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Áp dụng cơ chế xử lý hàng đợi (queue) hoặc nhận dạng giọng nói real-time để giảm thiểu độ trễ thay vì phải đợi nói xong cả câu mới convert thành text.
- **Safety**: Xây dựng module kiểm tra an toàn sau quá trình Speech-to-Text để filter ngay các input cố tình vượt quyền hệ thống (Prompt Injection) bằng giọng nói.
- **Performance**: Tích hợp module ngoại tuyến, cấu hình nhẹ để giảm chi phí gọi API và độ trễ.

---