#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add the current directory to Python path so app modules can be imported
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
