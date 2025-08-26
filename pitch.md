# AIDocMate – Your AI Guide for Government & Legal Documents

## Problem
Government and legal documents in India are complex, full of jargon, and often not available in the reader’s preferred language. Citizens (students, job seekers, farmers, elderly) struggle to understand requirements, fill forms correctly, and act on notices in time.

## Solution
AIDocMate is an AI assistant that turns bureaucratic paperwork into clear, actionable steps.
- Upload a PDF/image → OCR extracts text
- Simplify complex language → easy, bullet-point summary
- Generate a checklist → exactly what to collect and submit
- Translate → Hindi and other Indian languages
- Explain notices → step-by-step guidance with next actions

## Key Features
- OCR: Tesseract (local) + optional Google Vision for accuracy
- Simplify: OpenAI LLM with tailored prompts for Indian context
- Checklist: LLM outputs structured JSON of required documents
- Translate: Google Cloud Translate (fallback available for demos)
- qRaptor: Agents for Document, Prompt, and Chatbot orchestration

## Tech Stack
- Backend: FastAPI (Python)
- OCR: PyMuPDF + Tesseract / Google Vision
- LLM: OpenAI API
- Translation: Google Cloud Translation API
- UI: qRaptor agents (chatbot + upload), Data Vault for ephemeral state

## Demo Flow (2 minutes)
1. Upload an example form → get raw text
2. Simplify the text → bullet-point summary
3. Generate a checklist → structured items
4. Translate summary → Hindi

## Impact
- Reduces confusion and errors in applications
- Saves time for citizens and administrators
- Increases accessibility across languages

## Future Scope
- Mobile app with camera OCR and voice guidance
- Deeper “Explain Notice” with timelines and legal references
- Support for more Indian languages and dialects
- Offline mode using on-device small models

## Team & Ask
We’re seeking feedback and partnerships with government agencies and NGOs to pilot AIDocMate in citizen service centers. 