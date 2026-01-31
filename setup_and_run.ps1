# SME Financial Health Platform - Setup and Run Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SME Financial Health Platform Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create PostgreSQL Database
Write-Host "Step 1: Setting up PostgreSQL Database..." -ForegroundColor Yellow
Write-Host "Please enter your PostgreSQL password when prompted" -ForegroundColor Gray
Write-Host ""

# Try to create database
$dbExists = psql -U postgres -lqt | Select-String -Pattern "sme_financial_db"
if (-not $dbExists) {
    Write-Host "Creating database 'sme_financial_db'..." -ForegroundColor Gray
    psql -U postgres -c "CREATE DATABASE sme_financial_db;"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database created successfully!" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create database. Please create it manually:" -ForegroundColor Red
        Write-Host "  Run: psql -U postgres" -ForegroundColor Yellow
        Write-Host "  Then: CREATE DATABASE sme_financial_db;" -ForegroundColor Yellow
        Write-Host ""
        $continue = Read-Host "Press Enter after creating the database manually, or type 'exit' to quit"
        if ($continue -eq 'exit') { exit }
    }
} else {
    Write-Host "✓ Database 'sme_financial_db' already exists!" -ForegroundColor Green
}

Write-Host ""

# Step 2: Setup Backend
Write-Host "Step 2: Setting up Backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "✓ Virtual environment created!" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists!" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Gray
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit
}

# Initialize database
Write-Host "Initializing database tables..." -ForegroundColor Gray
python init_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to initialize database" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Backend Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 3: Setup Frontend
Write-Host "Step 3: Setting up Frontend..." -ForegroundColor Yellow
Set-Location ../frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Frontend dependencies installed!" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install frontend dependencies" -ForegroundColor Red
        exit
    }
} else {
    Write-Host "✓ Frontend dependencies already installed!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Frontend Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 4: Start the application
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Application..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend will run on: http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor Green
Write-Host "API Docs available at: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in background
Set-Location ../backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend
Set-Location ../frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Application Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open your browser and go to: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "To stop the application, close both PowerShell windows" -ForegroundColor Yellow
