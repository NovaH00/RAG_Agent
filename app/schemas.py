"""
Response models and schemas for the API
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


# Common response models
class StatusResponse(BaseModel):
	status: Literal["SUCCEEDED", "FAILED"]


# Database API models
class IndexDocRequest(BaseModel):
	content: str = Field(
  	description="Nội dung văn bản cần được lưu trữ"
  )

class IndexDocResponse(StatusResponse):
  pass

# Agent API models
class ChatRequest(BaseModel):
  thread_id: str = Field(
    description="ID của thread cuộc hội thoại"
  )
  message: str = Field(
    description="Tin nhắn từ người dùng"
  )
  system_instruction: Optional[str] = Field(
    default=None,
    description="Hướng dẫn hệ thống tùy chọn để tùy chỉnh cách AI phản hồi"
  )


class ChatResponse(BaseModel):
  message_id: str = Field(
    description="ID của tin nhắn"
  )
  ai_message: str = Field(
    description="Phản hồi từ AI agent"
  )


class GetHistoryRequest(BaseModel):
  thread_id: str = Field(
    description="ID của thread cần lấy lịch sử"
  )

class HistoryMessage(BaseModel):
  message_id: str = Field(
    description="ID của tin nhắn"
  )
  role: Literal["user", "ai", "system"] = Field(
    description="Vai trò của tin nhắn"
  )
  message: str = Field(
    description="Nội dung tin nhắn"
  )

class GetHistoryResponse(BaseModel):
  messages: List[HistoryMessage] = Field(
    description="Danh sách tin nhắn"
  )

class GenerateThreadDescriptionRequest(BaseModel):
  initial_message: str = Field(
    description="Tin nhắn đầu tiên của người dùng trong thread"
  )

class GenerateThreadDescriptionResponse(BaseModel):
  description: str = Field(
    description="Mô tả ngắn gọn cho thread"
  )

