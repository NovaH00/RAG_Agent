#!/usr/bin/env python3
"""
Quick start script for Agent Du Lịch API

Usage:
    python start_server.py
"""

import subprocess
import sys
import os


def main():
    """Start the FastAPI server"""
    print("🚀 Starting Agent Du Lịch API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation will be available at: http://localhost:8000/redoc")
    print("🌐 API Base URL: http://localhost:8000")
    print()
    
    try:
        # Run uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except FileNotFoundError:
        print("❌ Error: uvicorn not found. Please install dependencies first:")
        print("   uv sync")
        print("   # or")
        print("   pip install -e .")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    main()
