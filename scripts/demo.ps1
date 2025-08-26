$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-MultipartFormUpload {
	param(
		[string]$Uri,
		[string]$FilePath,
		[string]$FieldName = "file"
	)
	Add-Type -AssemblyName System.Net.Http | Out-Null
	$client = New-Object System.Net.Http.HttpClient
	$content = New-Object System.Net.Http.MultipartFormDataContent
	$fileStream = [System.IO.File]::OpenRead($FilePath)
	$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
	$fileName = [System.IO.Path]::GetFileName($FilePath)
	# Try to set a basic content type for common images
	$fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("image/png")
	$content.Add($fileContent, $FieldName, $fileName)
	$response = $client.PostAsync($Uri, $content).GetAwaiter().GetResult()
	$respBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
	$fileStream.Dispose()
	$client.Dispose()
	if (-not $response.IsSuccessStatusCode) {
		throw "Upload failed: $($response.StatusCode) $respBody"
	}
	return $respBody
}

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$demoOut = Join-Path $root "demo_output"
if (-not (Test-Path $demoOut)) { New-Item -ItemType Directory -Path $demoOut | Out-Null }

# Generate sample image if not present
$samplesDir = Join-Path $root "samples"
if (-not (Test-Path $samplesDir)) { New-Item -ItemType Directory -Path $samplesDir | Out-Null }
if (-not (Test-Path (Join-Path $samplesDir "form_sample.png"))) {
	Write-Host "[AIDocMate Demo] Generating sample image..." -ForegroundColor Cyan
	python (Join-Path $samplesDir "make_sample.py") | Out-Null
}

$api = "http://127.0.0.1:8000"

# Wait for API health
Write-Host "[AIDocMate Demo] Checking API health..." -ForegroundColor Cyan
$healthy = $false
for ($i = 0; $i -lt 10; $i++) {
	try {
		$health = Invoke-RestMethod -Method Get -Uri "$api/health" -TimeoutSec 2
		if ($health.status -eq "ok") { $healthy = $true; break }
	} catch {}
	Start-Sleep -Seconds 1
}
if (-not $healthy) { Write-Warning "API not responding at $api. Ensure server is running." }

Write-Host "[AIDocMate Demo] Step 1: Upload (OCR)" -ForegroundColor Cyan
$samplePath = Join-Path $samplesDir "form_sample.png"
$uploadUri = "$api/upload?use_vision=false"
$uploadRespRaw = Invoke-MultipartFormUpload -Uri $uploadUri -FilePath $samplePath
$uploadRespPath = Join-Path $demoOut "upload.json"
$uploadRespRaw | Out-File $uploadRespPath -Encoding UTF8

# Extract and save raw text
$uploadJson = $uploadRespRaw | ConvertFrom-Json
$rawText = $uploadJson.text
$rawOut = Join-Path $demoOut "upload_raw.txt"
$rawText | Out-File $rawOut -Encoding UTF8
Write-Host "Saved: $rawOut" -ForegroundColor Green

Write-Host "[AIDocMate Demo] Step 2: Simplify" -ForegroundColor Cyan
$simplifyBody = @{ text = $rawText; language = "en"; reading_level = "basic"; use_bullets = $true } | ConvertTo-Json
$simplifyRespPath = Join-Path $demoOut "simplify.json"
Invoke-RestMethod -Method Post -Uri "$api/simplify" -ContentType "application/json" -Body $simplifyBody | ConvertTo-Json -Depth 5 | Out-File $simplifyRespPath -Encoding UTF8
$simplified = (Get-Content $simplifyRespPath | ConvertFrom-Json).text
$simplifiedOut = Join-Path $demoOut "simplified.txt"
$simplified | Out-File $simplifiedOut -Encoding UTF8
Write-Host "Saved: $simplifiedOut" -ForegroundColor Green

Write-Host "[AIDocMate Demo] Step 3: Checklist" -ForegroundColor Cyan
$checkBody = @{ text = $rawText; document_type = "Scholarship Application"; context = "student" } | ConvertTo-Json
$checklistOutJson = Join-Path $demoOut "checklist.json"
Invoke-RestMethod -Method Post -Uri "$api/checklist" -ContentType "application/json" -Body $checkBody | ConvertTo-Json -Depth 5 | Out-File $checklistOutJson -Encoding UTF8
Write-Host "Saved: $checklistOutJson" -ForegroundColor Green

Write-Host "[AIDocMate Demo] Step 4: Translate (to hi)" -ForegroundColor Cyan
$transBody = @{ text = $simplified; target_language = "hi" } | ConvertTo-Json
$transRespPath = Join-Path $demoOut "translate.json"
Invoke-RestMethod -Method Post -Uri "$api/translate" -ContentType "application/json" -Body $transBody | ConvertTo-Json -Depth 5 | Out-File $transRespPath -Encoding UTF8
$translated = (Get-Content $transRespPath | ConvertFrom-Json).text
$translatedOut = Join-Path $demoOut "translated.txt"
$translated | Out-File $translatedOut -Encoding UTF8
Write-Host "Saved: $translatedOut" -ForegroundColor Green

Write-Host "[AIDocMate Demo] Completed. See demo_output/ (upload_raw.txt, simplified.txt, checklist.json, translated.txt)" -ForegroundColor Yellow 