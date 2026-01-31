# Backend - Financial Health Assessment API

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn app.main:app --reload`

## API Documentation
Access at http://localhost:8000/docs

## Key Endpoints
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/financial-data/upload - Upload financial data
- GET /api/analysis/{analysis_id} - Get analysis results
- GET /api/report/{analysis_id}/pdf - Generate PDF report
