# Restart Backend and Frontend Servers
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Restarting Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "IMPORTANT: This script will help you restart the servers." -ForegroundColor Yellow
Write-Host "You need to manually stop the current servers first!" -ForegroundColor Yellow
Write-Host ""

Write-Host "Steps to restart:" -ForegroundColor White
Write-Host ""
Write-Host "1. BACKEND SERVER:" -ForegroundColor Cyan
Write-Host "   - Go to the terminal running the backend" -ForegroundColor White
Write-Host "   - Press Ctrl+C to stop it" -ForegroundColor White
Write-Host "   - Run: cd backend" -ForegroundColor Green
Write-Host "   - Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Green
Write-Host ""

Write-Host "2. FRONTEND SERVER:" -ForegroundColor Cyan
Write-Host "   - Go to the terminal running the frontend" -ForegroundColor White
Write-Host "   - Press Ctrl+C to stop it" -ForegroundColor White
Write-Host "   - Run: cd frontend" -ForegroundColor Green
Write-Host "   - Run: npm run dev" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "After restarting, the Plaid integration" -ForegroundColor Yellow
Write-Host "will work correctly!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
