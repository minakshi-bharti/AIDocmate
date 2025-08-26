# AIDocMate Unified Startup Script for Windows
# This script starts the FastAPI backend and serves the React frontend

Write-Host "🚀 Starting AIDocMate..." -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "app")) {
    Write-Host "❌ Please run this script from the hackathon directory!" -ForegroundColor Red
    Write-Host "   Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "   Expected: hackathon directory with 'app' folder" -ForegroundColor Yellow
    exit 1
}

# Check if frontend is built
$buildPath = "frontend\build"
$indexPath = "frontend\build\index.html"

if (-not (Test-Path $buildPath)) {
    Write-Host "❌ Frontend build directory not found!" -ForegroundColor Red
    Write-Host "   Please run: cd frontend && npm run build" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $indexPath)) {
    Write-Host "❌ Frontend index.html not found!" -ForegroundColor Red
    Write-Host "   Please run: cd frontend && npm run build" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Frontend build found and ready!" -ForegroundColor Green

# Check environment variables
Write-Host "`n🔑 Environment Check:" -ForegroundColor Cyan
if ($env:OPENAI_API_KEY) {
    Write-Host "   ✅ OPENAI_API_KEY is set" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  OPENAI_API_KEY not set (LLM features will use fallbacks)" -ForegroundColor Yellow
}

if ($env:GOOGLE_APPLICATION_CREDENTIALS) {
    Write-Host "   ✅ GOOGLE_APPLICATION_CREDENTIALS is set" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  GOOGLE_APPLICATION_CREDENTIALS not set (Vision/Translate will use fallbacks)" -ForegroundColor Yellow
}

Write-Host "`n🌐 Starting AIDocMate API Server..." -ForegroundColor Green
Write-Host "   Frontend will be served at: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   API docs will be at: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor White
Write-Host "=" * 50 -ForegroundColor Cyan

try {
    # Start the FastAPI server using the unified Python script
    python start_aidocmate.py
} catch {
    Write-Host "`n❌ Error starting server: $_" -ForegroundColor Red
    Write-Host "   Make sure you're in the correct directory and all dependencies are installed" -ForegroundColor Yellow
    Write-Host "   Try running: python start_aidocmate.py" -ForegroundColor Yellow
}
