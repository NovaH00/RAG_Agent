from agent.agent import Agent
from agent.config import Configuration
from qdrant.client import qdrant_service
import threading
from typing import Annotated
from fastapi import Depends
from qdrant.client import Client
import asyncio
from fastapi import HTTPException

from .main import app_state

def get_qdrant_service() -> Client:
  """Dependency to get Qdrant service instance."""
  return app_state.qdrant_service


def get_agent_service() -> Agent:
  """Dependency to get Agent service instance."""
  return app_state.agent

_global_lock = asyncio.Lock()

async def require_global_lock():
  if _global_lock.locked():
    raise HTTPException(
      status_code=503,
      detail="Resource busy"
    )
  
  async with _global_lock:
    yield