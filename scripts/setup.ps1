param(
	[string]$Port = "8000"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot  # .../hackathon
Set-Location $projectRoot

Write-Host "[AIDocMate] Using project root: $projectRoot" -ForegroundColor Cyan

# 1) Create venv if missing
$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
	Write-Host "[AIDocMate] Creating virtual environment..." -ForegroundColor Cyan
	python -m venv $venvPath
}

# 2) Activate venv
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
. $activateScript
Write-Host "[AIDocMate] Virtual environment activated." -ForegroundColor Green

# 3) Install dependencies
Write-Host "[AIDocMate] Installing dependencies..." -ForegroundColor Cyan
pip install -r (Join-Path $projectRoot "requirements.txt")

# 4) Check Tesseract availability
try {
	$tess = & tesseract -v 2>$null
	Write-Host "[AIDocMate] Tesseract detected." -ForegroundColor Green
} catch {
	Write-Warning "Tesseract not found. Install it from https://github.com/UB-Mannheim/tesseract/wiki and add it to PATH."
}

# 5) Warn about missing environment variables
if (-not $env:OPENAI_API_KEY) {
	Write-Warning "OPENAI_API_KEY is not set. /simplify, /checklist, /explain will not work."
}
if (-not $env:GOOGLE_APPLICATION_CREDENTIALS -or -not $env:GOOGLE_PROJECT_ID) {
	Write-Host "[AIDocMate] Google Cloud not configured. Vision/Translate will be disabled unless USE_TRANSLATE_FALLBACK=true." -ForegroundColor Yellow
}

# 6) Run server
Write-Host "[AIDocMate] Starting API at http://127.0.0.1:$Port ..." -ForegroundColor Cyan
uvicorn app.main:app --reload --port $Port 