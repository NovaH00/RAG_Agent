from fastapi import APIRouter, HTTPException
import threading
import uuid
from langchain_core.messages import HumanMessage
from fastapi import Depends

from agent.agent import Agent

from ..dependencies import (
  get_qdrant_service,
  get_agent_service,
  require_global_lock
)

from ..schemas import (
  ChatRequest,
  ChatResponse,
  GetHistoryRequest,
  GetHistoryResponse
)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
  request: ChatRequest, 
  agent: Agent = Depends(get_agent_service), 
  _lock: None = Depends(require_global_lock)
):
  pass

@router.post("/get-history", response_model=GetHistoryResponse)
async def get_history(
  request: GetHistoryRequest,
  agent: Agent = Depends(get_agent_service)
) -> GetHistoryResponse:
  pass