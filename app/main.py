from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from contextlib import asynccontextmanager

from .routers import database, agent
from .dependencies import get_agent_service, get_qdrant_service

from agent.agent import Agent
from qdrant.client import Client, qdrant_service
from pydantic import BaseModel

class AppState(BaseModel):
    agent: Agent
    qdrant_service: Client

app_state = AppState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting Agent Du Lịch API...")

    print("App states mounted")    

    # TODO: Implement checkpointer
    app_state.agent = Agent(
        qdrant_service=qdrant_service
    )
    
    app_state.qdrant_service = qdrant_service
    
    
    
    yield
    
    # Shutdown
    print("🔄 Shutting down Agent Du Lịch API...")
    # Cleanup if needed
    print("✅ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Agent Du Lịch API",
    description="RAG AI Agent with LangGraph and Qdrant Vector Database",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    database.router,
    prefix="/api/db",
    tags=["Database"]
)

app.include_router(
    agent.router,
    prefix="/api/agent",
    tags=["Agent"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Agent Du Lịch API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
