# Set your Google API Key here
# Usage: .\set_api_key.ps1
# Then run: python generate_memories_v2.py

$apiKey = Read-Host ""
$env:GOOGLE_API_KEY = $apiKey

Write-Host "API Key set for this session!" -ForegroundColor Green
Write-Host "Now you can run: python generate_memories_v2.py" -ForegroundColor Cyan
