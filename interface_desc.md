# HỆ THỐNG API CHO AGENT DU LỊCH

## TỔNG QUAN CÁC API

### 📚 Database APIs
- `/api/db/index_doc`: Đẩy và cập nhật dữ liệu văn bản vào cơ sở dữ liệu tri thức của agent, agent sẽ dùng thông tin trong này để trả lời. Dữ liệu cũ sẽ bị xóa

### 🤖 Agent APIs  
- `/api/agent/chat`: Gửi tin nhắn và nhận phản hồi từ AI agent
- `/api/agent/get_history`: Lấy lịch sử tin nhắn của một thread
- `/api/agent/generate_thread_description`: Tạo mô tả ngắn gọn cho thread dựa trên tin nhắn đầu tiên

## CHI TIẾT CÁC API
---  
### `/api/db/index_doc`: sync (POST)

**Mô tả:** Đẩy dữ liệu văn bản vào cơ sở tri thức để agent có thể tìm kiếm và truy xuất thông tin liên quan khi trả lời câu hỏi của người dùng. Dữ liệu này sẽ thay thế dữ liệu cũ (dữ liệu cũ bị xóa)

**PAYLOAD**  
```json
{
  "content": "string - Nội dung văn bản cần được lưu trữ"
}
```

**VALIDATION:**
- `content`: BẮT BUỘC (nên xử lý thành văn bản thuần)

**RESPONSE**
```json
{
  "status": "SUCCEEDED" | "FAILED"
}
```

**VÍ DỤ:**
```bash
curl -X POST http://localhost:8000/api/db/index_doc \
-H "Content-Type: application/json" \
-d '{
  "content": "Hà Nội là thủ đô của Việt Nam, nổi tiếng với Hồ Hoàn Kiếm, Văn Miếu và nhiều di tích lịch sử. Thành phố có khí hậu nhiệt đới gió mùa với 4 mùa rõ rệt."
}'

# Response:
{
  "status": "SUCCEEDED"
}
```

---  

### `/api/agent/chat`: sync (POST)

**Mô tả:** Gửi tin nhắn từ người dùng và nhận phản hồi từ agent. Agent sẽ sử dụng thông tin trong cơ sở tri thức để trả lời các câu hỏi. Có thể tùy chọn cung cấp hướng dẫn hệ thống để tùy chỉnh cách agent phản hồi.

**PAYLOAD**
```json
{
  "thread_id": "string - ID của thread cuộc hội thoại",
  "message": "string - Tin nhắn từ người dùng",
  "system_instruction": "string - (Tùy chọn) Hướng dẫn hệ thống để tùy chỉnh cách AI phản hồi"
}
```

**VALIDATION:**
- `thread_id`: BẮT BUỘC (khuyến khích dùng UUID4)
- `message`: BẮT BUỘC
- `system_instruction`: TÙY CHỌN, tối đa 5000 ký tự. Dùng để thay đổi hành vi trả lời của AI

**RESPONSE**
```json
{   
  "message_id": "string - ID duy nhất của tin nhắn",
  "ai_message": "string - Phản hồi từ AI agent"
}
```

**VÍ DỤ:**
```bash
curl -X POST http://localhost:8000/api/agent/chat \
-H "Content-Type: application/json" \
-d '{
  "thread_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": "Cho tôi biết những địa điểm du lịch nổi tiếng ở Hà Nội?"
}'

# Response:
{
  "message_id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "ai_message": "Hà Nội có nhiều địa điểm du lịch nổi tiếng như: 1) Hồ Hoàn Kiếm - trung tâm thành phố với Đền Ngọc Sơn, 2) Văn Miếu - Quốc Tử Giám - nơi thờ Khổng Tử và các bậc hiền tài, 3) Phố cổ Hà Nội với 36 phố phường truyền thống..."
}
```

**VÍ DỤ VỚI SYSTEM INSTRUCTION:**
```bash
curl -X POST http://localhost:8000/api/agent/chat \
-H "Content-Type: application/json" \
-d '{
  "thread_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": "Cho tôi biết những địa điểm du lịch nổi tiếng ở Hà Nội?",
  "system_instruction": "Bạn là một chuyên gia du lịch với 10 năm kinh nghiệm. Hãy đưa ra lời khuyên chi tiết về giá cả, thời gian tốt nhất để đi và những lưu ý quan trọng."
}'

# Response:
{
  "message_id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "ai_message": "Dựa trên kinh nghiệm 10 năm của tôi, Hà Nội có những địa điểm không thể bỏ qua: 1) Hồ Hoàn Kiếm (miễn phí, đẹp nhất vào buổi sáng sớm 5-7h), 2) Văn Miếu (30,000đ/vé, nên đi sáng thứ 7 để tránh đông), 3) Phố cổ (miễn phí dạo bộ, cuối tuần có phố đi bộ). Lưu ý: tránh giờ cao điểm 7-9h và 17-19h..."
}
```

---

### `/api/agent/get_history`: sync (POST)

**Mô tả:** Lấy toàn bộ lịch sử tin nhắn của một thread cụ thể, bao gồm tin nhắn từ người dùng, AI và hệ thống.

**PAYLOAD**   
```json
{
  "thread_id": "string - ID của thread cần lấy lịch sử"
}
```

**VALIDATION:**
- `thread_id`: BẮT BUỘC (khuyến khích UUID4)
- Thread phải tồn tại trong hệ thống (tạo bởi API chat trước đó, client phải quản lý điều này để tránh xung đột)

**RESPONSE**  
```json
{
  "messages": [
    {
      "message_id": "string - ID duy nhất của tin nhắn",
      "role": "user" | "ai" | "system",
      "message": "string - Nội dung tin nhắn"
    }
  ]
}
```

**VÍ DỤ:**
```bash
curl -X POST http://localhost:8000/api/agent/get_history \
-H "Content-Type: application/json" \
-d '{
  "thread_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}'

# Response:
{
  "messages": [
    {
      "message_id": "12345678-1234-4567-8901-123456789012",
      "role": "system",
      "message": "Bạn là một AI hướng dẫn du lịch."
    },
    {
      "message_id": "87654321-4321-4567-8901-987654321098",
      "role": "user",
      "message": "Xin chào! Tôi muốn du lịch Hà Nội."
    },
    {
      "message_id": "11111111-2222-4567-8901-333333333333", 
      "role": "ai",
      "message": "Chào bạn! Tôi rất vui được hỗ trợ bạn lên kế hoạch du lịch Hà Nội. Bạn có thể cho tôi biết thời gian dự kiến và sở thích của bạn không?"
    },
    {
      "message_id": "44444444-5555-4567-8901-666666666666",
      "role": "user", 
      "message": "Tôi có 3 ngày và thích tham quan các di tích lịch sử."
    }
  ]
}
```
---  

### `/api/agent/generate_thread_description`: sync (POST)

**Mô tả:** Tạo mô tả ngắn gọn và dễ hiểu cho một thread dựa trên tin nhắn đầu tiên của người dùng. Mô tả này được sử dụng để hiển thị trên giao diện người dùng.

**PAYLOAD**
```json
{
  "initial_message": "string - Tin nhắn đầu tiên của người dùng trong thread"
}
```

**VALIDATION:**
- `initial_message`: BẮT BUỘC, độ dài 1-2,000 ký tự, văn bản thuần

**RESPONSE**
```json
{
  "description": "string - Mô tả ngắn gọn cho thread"
}
```

**VÍ DỤ:**
```bash
curl -X POST http://localhost:8000/api/agent/generate_thread_description \
-H "Content-Type: application/json" \
-d '{
  "initial_message": "Tôi muốn lên kế hoạch du lịch Đà Nẵng 4 ngày 3 đêm với ngân sách 5 triệu đồng"
}'

# Response:
{
  "description": "Kế hoạch du lịch Đà Nẵng 4 ngày - ngân sách 5 triệu"
}
```

---



## RÀNG BUỘC KHÁC
- **Hệ thống sử dụng khóa toàn cục để đảm bảo chỉ có DUY NHẤT MỘT ENDPOINT được xử lý cùng một lúc**
- **Tất cả API `/api/agent/*` và `/api/db/*` đều ĐỒNG BỘ và sử dụng chung một khóa. Nếu có request đang xử lý, các request khác sẽ nhận HTTP 503 (Service Unavailable)**
- **Các tin nhắn của AI sẽ luôn trả về dạng Markdown và có Latex, nếu muốn thay đổi hành vi này thì hãy nói rõ trong `system_instruction` là *"...Đừng sử dụng Markdown hoặc Latex...***