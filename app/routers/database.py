from fastapi import APIRouter, HTTPException, Depends
import threading
from qdrant.client import Client

from ..dependencies import (
  get_qdrant_service,
  require_global_lock
)
from ..schemas import (
  IndexDocRequest,
  IndexDocResponse
)


router = APIRouter()


@router.post("/index_doc", response_model=IndexDocResponse)
async def index_document(
  request: IndexDocRequest, 
  qdrant_service: Client = Depends(get_qdrant_service),
  _lock: None  = Depends(require_global_lock)
  
) -> IndexDocResponse:
  pass