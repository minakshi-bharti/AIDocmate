import os
import uuid
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.services.ocr import extract_text_from_file
from app.services.llm import simplify_text_with_llm, generate_checklist_with_llm, explain_notice_with_llm, translate_text_with_llm
from app.services.translate import translate_text_with_provider
from app.utils.cleaning import clean_extracted_text
from app.models.schemas import SimplifyRequest, SimplifyResponse, TranslateRequest, TranslateResponse, ChecklistRequest, ChecklistResponse, UploadResponse, ExplainNoticeRequest, ExplainNoticeResponse, ChecklistItem


app = FastAPI(
    title="AIDocMate API",
    description="AI-powered document simplification and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files from the React build
# Try inner project path first, then fallback to parent (for different repo layouts)
_inner_build_path = Path(__file__).parent.parent / "frontend" / "build"
_outer_build_path = Path(__file__).parent.parent.parent / "frontend" / "build"
build_path = _inner_build_path if _inner_build_path.exists() else _outer_build_path
if build_path.exists():
    app.mount("/static", StaticFiles(directory=str(build_path / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the React frontend"""
    index_path = build_path / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>AIDocMate Backend Running</h1><p>Frontend not found. Please build the React app first.</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AIDocMate API"}

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    use_vision: bool = Query(False, description="Use Google Vision API instead of Tesseract"),
    language_hint: Optional[str] = Query(default=None, description="ISO language hint for OCR, e.g., 'en', 'hi'"),
):
    """
    Upload and extract text from a document (PDF/Image)
    """
    try:
        # Validate file type
        if not file.content_type.startswith(('image/', 'application/pdf')):
            raise HTTPException(status_code=400, detail="Only PDF and image files are supported")
        
        # Read file bytes
        file_bytes = await file.read()
        if not file_bytes:
            return {
                "extracted_text": "Could not extract text.",
                "file_name": file.filename,
                "file_size": 0,
                "file_type": file.content_type,
            }

        # Extract text
        text = extract_text_from_file(
            file_bytes=file_bytes,
            filename=file.filename or "uploaded",
            use_vision=use_vision,
            language_hint=language_hint,
        )
        extracted_text = clean_extracted_text(text)
        print(f"[upload] extracted length = {len(extracted_text or '')}")
        if extracted_text:
            print(f"[upload] first 100 chars: {extracted_text[:100]}...")
        
        if not extracted_text:
            extracted_text = "Could not extract text."
        
        return {
            "extracted_text": extracted_text,
            "file_name": file.filename,
            "file_size": file.size,
            "file_type": file.content_type,
        }
        
    except Exception:
        return {
            "extracted_text": "Could not extract text.",
            "file_name": file.filename or "unknown",
            "file_size": 0,
            "file_type": file.content_type or "unknown",
        }

@app.post("/simplify")
async def simplify_document(request: SimplifyRequest):
    """
    Simplify complex document text using AI
    """
    try:
        result = simplify_text_with_llm(
            text=request.text,
            language=request.language,
            reading_level=request.reading_level,
            use_bullets=request.use_bullets,
        )
        
        if not result.text:
            return {
                "simplified_text": "Sorry, we couldn't simplify the text right now.",
                "original_length": len(request.text),
                "simplified_length": 0,
                "language": request.language,
            }
        
        return {
            "simplified_text": result.text,
            "original_length": len(request.text),
            "simplified_length": len(result.text),
            "language": result.language,
        }
        
    except Exception:
        return {
            "simplified_text": "Sorry, we couldn't simplify the text right now.",
            "original_length": len(request.text),
            "simplified_length": 0,
            "language": request.language,
        }

@app.post("/translate")
async def translate_document(request: TranslateRequest):
    """
    Translate document text to target language
    """
    try:
        # Prefer LLM-based translation when OpenAI is configured; fallback to provider
        translated_text = translate_text_with_llm(text=request.text, target_language=request.target_language)
        provider = "openai"
        
        if not translated_text:
            return {
                "translated_text": "Sorry, we couldn't translate the text right now.",
                "original_text": request.text,
                "source_language": "auto",
                "target_language": request.target_language,
            }
        
        return {
            "translated_text": translated_text,
            "original_text": request.text,
            "source_language": "auto",
            "target_language": request.target_language,
            "provider": provider,
        }
        
    except Exception:
        return {
            "translated_text": "Sorry, we couldn't translate the text right now.",
            "original_text": request.text,
            "source_language": "auto",
            "target_language": request.target_language,
        }

@app.post("/checklist")
async def generate_checklist(request: ChecklistRequest):
    """
    Generate checklist of required documents
    """
    try:
        checklist = generate_checklist_with_llm(
            text=request.text,
            document_type=request.document_type,
            context=request.context,
        )
        
        if not checklist or not checklist.items:
            return {
                "document_type": request.document_type,
                "items": [],
                "total_items": 0,
                "message": "Sorry, we couldn't generate a checklist right now.",
            }
        
        return {
            "document_type": request.document_type,
            "items": [item.model_dump() for item in checklist.items],
            "total_items": len(checklist.items),
            "message": "Checklist generated successfully",
        }
        
    except Exception:
        return {
            "document_type": request.document_type,
            "items": [],
            "total_items": 0,
            "message": "Sorry, we couldn't generate a checklist right now.",
        }

@app.post("/explain")
async def explain_notice(request: ExplainNoticeRequest):
    """
    Explain legal notices and suggest next steps
    """
    try:
        explanation = explain_notice_with_llm(text=request.text, language=request.language)
        
        if not explanation or not explanation.steps:
            return {
                "summary": "Sorry, we couldn't explain the notice right now.",
                "steps": [],
                "next_actions": [],
                "urgency_level": "unknown",
            }
        
        return {
            "summary": "\n".join(explanation.steps[:3]),
            "steps": explanation.steps,
            "next_actions": explanation.next_actions,
            "urgency_level": "normal",
        }
        
    except Exception:
        return {
            "summary": "Sorry, we couldn't explain the notice right now.",
            "steps": [],
            "next_actions": [],
            "urgency_level": "unknown",
        }

@app.get("/debug/openai")
async def debug_openai():
    """Debug endpoint to check OpenAI configuration"""
    api_key = os.getenv("OPENAI_API_KEY")
    api_key_length = len(api_key) if api_key else 0
    api_key_preview = f"{api_key[:10]}..." if api_key and len(api_key) > 10 else "None"
    
    # Test LLM service initialization
    try:
        from app.services.llm import _get_openai_client
        client = _get_openai_client()
        client_status = "Available" if client else "Not Available"
    except Exception as e:
        client_status = f"Error: {e}"
    
    return {
        "openai_api_key_set": bool(api_key),
        "api_key_length": api_key_length,
        "api_key_preview": api_key_preview,
        "llm_client_status": client_status,
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get("/debug/test-llm")
async def test_llm():
    """Test endpoint to verify LLM service works"""
    try:
        from app.services.llm import simplify_text_with_llm
        result = simplify_text_with_llm("This is a test message to verify OpenAI integration.")
        return {
            "status": "success",
            "result": result.text,
            "result_length": len(result.text)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 AIDocMate API running at http://127.0.0.1:8000\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Entrypoint for local dev: uvicorn app.main:app --reload 