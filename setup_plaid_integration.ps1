# Setup Plaid Banking Integration
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Plaid Banking Integration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Add database table
Write-Host "Step 1: Adding bank_connections table to database..." -ForegroundColor Yellow
Set-Location backend
python add_bank_connections_table.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error adding database table!" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "✓ Database table added" -ForegroundColor Green
Write-Host ""

# Step 2: Install frontend dependencies
Write-Host "Step 2: Installing react-plaid-link package..." -ForegroundColor Yellow
Set-Location frontend
npm install react-plaid-link@3.5.2
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing npm packages!" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 3: Verify Plaid credentials
Write-Host "Step 3: Verifying Plaid credentials..." -ForegroundColor Yellow
$envFile = Get-Content backend/.env
$hasClientId = $envFile | Select-String "PLAID_CLIENT_ID="
$hasSecret = $envFile | Select-String "PLAID_SECRET="
$hasEnv = $envFile | Select-String "PLAID_ENV="

if ($hasClientId -and $hasSecret -and $hasEnv) {
    Write-Host "✓ Plaid credentials found in .env" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: Plaid credentials not fully configured in backend/.env" -ForegroundColor Yellow
    Write-Host "  Make sure you have:" -ForegroundColor Yellow
    Write-Host "  - PLAID_CLIENT_ID=your_client_id" -ForegroundColor Yellow
    Write-Host "  - PLAID_SECRET=your_secret" -ForegroundColor Yellow
    Write-Host "  - PLAID_ENV=https://sandbox.plaid.com" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart the backend server (if running)" -ForegroundColor White
Write-Host "2. Restart the frontend server (if running)" -ForegroundColor White
Write-Host "3. Navigate to /banking page" -ForegroundColor White
Write-Host "4. Click 'Connect Bank Account'" -ForegroundColor White
Write-Host "5. Use Plaid sandbox credentials:" -ForegroundColor White
Write-Host "   Username: user_good" -ForegroundColor Cyan
Write-Host "   Password: pass_good" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features now available:" -ForegroundColor Yellow
Write-Host "✓ Real Plaid Link integration" -ForegroundColor Green
Write-Host "✓ Secure token storage in database" -ForegroundColor Green
Write-Host "✓ Real-time account balances" -ForegroundColor Green
Write-Host "✓ Transaction history sync" -ForegroundColor Green
Write-Host "✓ Automatic categorization" -ForegroundColor Green
Write-Host "✓ Bank disconnect feature" -ForegroundColor Green
Write-Host ""
