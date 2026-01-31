# Installation script for new features
Write-Host "Installing new Python dependencies..." -ForegroundColor Green

cd backend

# Install PDF parsing libraries
pip install PyPDF2==3.0.1
pip install pdfplumber==0.10.3
pip install tabula-py==2.9.0

Write-Host "`nNew dependencies installed successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Run database migration: python init_db.py" -ForegroundColor Yellow
Write-Host "2. Restart backend server" -ForegroundColor Yellow
Write-Host "3. Test PDF upload feature" -ForegroundColor Yellow

cd ..
