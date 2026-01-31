# Start Backend Server
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Set-Location backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
