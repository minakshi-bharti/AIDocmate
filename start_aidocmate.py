#!/usr/bin/env python3
"""
AIDocMate Unified Startup Script
Runs the FastAPI backend and serves the React frontend from one location.
"""

import sys
import os
from pathlib import Path
import uvicorn

# Add the current directory to Python path so app modules can be imported
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_frontend_build():
    """Check if the React frontend has been built"""
    build_path = current_dir / "frontend" / "build"
    index_path = build_path / "index.html"
    
    if not build_path.exists():
        print("❌ Frontend build directory not found!")
        print("   Please run: cd frontend && npm run build")
        return False
    
    if not index_path.exists():
        print("❌ Frontend index.html not found!")
        print("   Please run: cd frontend && npm run build")
        return False
    
    print("✅ Frontend build found and ready!")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting AIDocMate...")
    print("=" * 50)
    
    # Check if frontend is built
    if not check_frontend_build():
        print("\n💡 To build the frontend:")
        print("   1. cd frontend")
        print("   2. npm install")
        print("   3. npm run build")
        print("   4. Run this script again")
        return
    
    # Check environment variables
    print("\n🔑 Environment Check:")
    if os.getenv("OPENAI_API_KEY"):
        print("   ✅ OPENAI_API_KEY is set")
    else:
        print("   ⚠️  OPENAI_API_KEY not set (LLM features will use fallbacks)")
    
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("   ✅ GOOGLE_APPLICATION_CREDENTIALS is set")
    else:
        print("   ⚠️  GOOGLE_APPLICATION_CREDENTIALS not set (Vision/Translate will use fallbacks)")
    
    print("\n🌐 Starting AIDocMate API Server...")
    print("   Frontend will be served at: http://127.0.0.1:8000")
    print("   API docs will be at: http://127.0.0.1:8000/docs")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n🛑 AIDocMate server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("   Make sure you're in the correct directory and all dependencies are installed")

if __name__ == "__main__":
    main()
