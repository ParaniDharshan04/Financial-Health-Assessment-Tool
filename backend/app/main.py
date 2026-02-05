from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, financial_data, analysis, reports, banking, tax, gst, optimization, bookkeeping
from app.core.config import settings

app = FastAPI(
    title="SME Financial Health Assessment API",
    description="AI-powered financial intelligence platform for SMEs",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://financial-health-assessment-tool-tan.vercel.app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(financial_data.router, prefix="/api/financial-data", tags=["Financial Data"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(banking.router, prefix="/api/banking", tags=["Banking Integration"])
app.include_router(tax.router, prefix="/api/tax", tags=["Tax Compliance"])
app.include_router(gst.router, prefix="/api/gst", tags=["GST Integration"])
app.include_router(optimization.router, prefix="/api/optimization", tags=["Working Capital Optimization"])
app.include_router(bookkeeping.router, prefix="/api/bookkeeping", tags=["Automated Bookkeeping"])

@app.get("/")
async def root():
    return {
        "message": "SME Financial Health Assessment API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
