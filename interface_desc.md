# HỆ THỐNG API CHO AGENT DU LỊCH

## TỔNG QUAN CÁC API

### 📚 Database APIs
- `/api/db/index_doc`: Đẩy và cập nhật dữ liệu văn bản vào vector database QDrant

### 🤖 Agent APIs  
- `/api/agent/chat`: Gửi tin nhắn và nhận phản hồi từ AI agent
- `/api/agent/get_history`: Lấy lịch sử tin nhắn của một thread
- `/api/agent/update_sys_instruction`: Cập nhật hướng dẫn hệ thống cho AI agent
- `/api/agent/generate_thread_description`: Tạo mô tả ngắn gọn cho thread dựa trên tin nhắn đầu tiên

## CHI TIẾT CÁC API
---  
### `/api/db/index_doc`: sync (POST)

**Mô tả:** Đẩy dữ liệu văn bản vào vector database QDrant để hệ thống có thể tìm kiếm và truy xuất thông tin liên quan khi trả lời câu hỏi của người dùng.

**PAYLOAD**  
```json
{
  "content": "string - Nội dung văn bản cần được lưu trữ"
}
```

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

**Mô tả:** Gửi tin nhắn từ người dùng và nhận phản hồi từ AI agent. AI sẽ sử dụng thông tin trong vector database để trả lời các câu hỏi về du lịch.

**PAYLOAD**
```json
{
  "thread_id": "string - ID của thread cuộc hội thoại",
  "message": "string - Tin nhắn từ người dùng"
}
```

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

---

### `/api/agent/get_history`: sync (POST)

**Mô tả:** Lấy toàn bộ lịch sử tin nhắn của một thread cụ thể, bao gồm tin nhắn từ người dùng, AI và hệ thống.

**PAYLOAD**   
```json
{
  "thread_id": "string - ID của thread cần lấy lịch sử"
}
```

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

### `/api/agent/update_sys_instruction`: sync (POST)

**Mô tả:** Cập nhật hướng dẫn hệ thống (system prompt) cho AI agent để thay đổi cách thức hoạt động, phong cách trả lời hoặc kiến thức chuyên môn.

**PAYLOAD**
```json
{
  "instruction": "string - Hướng dẫn hệ thống mới cho AI agent"
}
```

**RESPONSE**
```json
{
  "status": "SUCCEEDED" | "FAILED"
}
```

**VÍ DỤ:**
```bash
curl -X POST http://localhost:8000/api/agent/update_sys_instruction \
-H "Content-Type: application/json" \
-d '{
  "instruction": "Bạn là một chuyên gia du lịch Việt Nam với 10 năm kinh nghiệm. Hãy đưa ra lời khuyên chi tiết về các địa điểm, ẩm thực, văn hóa và lịch trình du lịch. Luôn đề xuất các hoạt động phù hợp với ngân sách và thời gian của khách hàng."
}'

# Response:
{
  "status": "SUCCEEDED"
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

## ⚠️ RÀNG BUỘC HỆ THỐNG

**QUAN TRỌNG:** 
- **Tất cả các API đều là ĐỒNG BỘ (synchronous)** 
- **Hệ thống sử dụng thread lock để đảm bảo chỉ có DUY NHẤT MỘT endpoint hoạt động cùng một lúc**
- **Điều này đảm bảo tính nhất quán của dữ liệu và tránh xung đột khi xử lý đồng thời**

## 📋 GHI CHÚ THÊM

### Mã lỗi HTTP phổ biến:
- **200 OK**: Yêu cầu thành công
- **400 Bad Request**: Dữ liệu đầu vào không hợp lệ  
- **500 Internal Server Error**: Lỗi hệ thống

### Định dạng ID:
- **Thread ID**: UUID4 format (ví dụ: `f47ac10b-58cc-4372-a567-0e02b2c3d479`)
- **Message ID**: UUID4 format (ví dụ: `a3bb189e-8bf9-3888-9912-ace4e6543002`)
