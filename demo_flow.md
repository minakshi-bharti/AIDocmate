# AIDocMate Demo Flow

This walkthrough shows the end-to-end experience used in the hackathon demo.

## 0) Start the API
```powershell
# From project root
uvicorn app.main:app --reload --port 8000
```
Open `http://127.0.0.1:8000/docs` to explore.

## 1) Upload a document (OCR)
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "file=@samples/form_sample.png" \
  -F "use_vision=false"
```
Response (shape):
```json
{
  "request_id": "...",
  "filename": "form_sample.png",
  "text": "<extracted raw text>"
}
```

## 2) Simplify text
```bash
curl -X POST "http://127.0.0.1:8000/simplify" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "<paste raw text from step 1>",
    "language": "en",
    "reading_level": "basic",
    "use_bullets": true
  }'
```
Response (shape):
```json
{
  "language": "en",
  "reading_level": "basic",
  "text": "- key points..."
}
```

## 3) Generate a checklist
```bash
curl -X POST "http://127.0.0.1:8000/checklist" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "<paste same text>",
    "document_type": "Scholarship Application",
    "context": "student"
  }'
```
Response (shape):
```json
{
  "items": [
    { "name": "Aadhaar", "description": "Copy of Aadhaar", "mandatory": true, "copies": 1, "source": "user" }
  ],
  "raw": "..."
}
```

## 4) Translate to Hindi (or other language)
```bash
curl -X POST "http://127.0.0.1:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "<paste simplified text>",
    "target_language": "hi"
  }'
```
Response (shape):
```json
{
  "text": "<अनुवादित पाठ>",
  "target_language": "hi",
  "provider": "google-cloud-translate | googletrans"
}
```

Notes:
- For offline demo without Google Cloud, set `USE_TRANSLATE_FALLBACK=true`.
- You can skip `/simplify` and translate the raw OCR text directly. 