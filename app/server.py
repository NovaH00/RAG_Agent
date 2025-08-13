"""
Server startup script for Agent Du Lịch API

Run with: python -m uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
"""

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("🚀 Starting Agent Du Lịch API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation: http://localhost:8000/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
