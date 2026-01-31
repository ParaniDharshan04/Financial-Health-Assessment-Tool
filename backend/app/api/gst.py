from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.gst_integration import GSTIntegration

router = APIRouter()

class GSTCalculationRequest(BaseModel):
    revenue: float
    gst_rate: Optional[float] = 0.18

@router.post("/upload-return")
async def upload_gst_return(
    file: UploadFile = File(...),
    return_type: str = Form(...),  # GSTR-1 or GSTR-3B
    file_type: str = Form("json"),  # json or xml
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and parse GST return"""
    try:
        contents = await file.read()
        
        gst_service = GSTIntegration()
        
        if return_type == "GSTR-1":
            parsed_data = gst_service.parse_gstr1(contents, file_type)
        elif return_type == "GSTR-3B":
            parsed_data = gst_service.parse_gstr3b(contents, file_type)
        else:
            raise HTTPException(status_code=400, detail="Invalid return type. Use 'GSTR-1' or 'GSTR-3B'")
        
        # Store in database (create GSTData model if needed)
        # For now, return parsed data
        
        return {
            "message": "GST return uploaded and parsed successfully",
            "data": parsed_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing GST return: {str(e)}")

@router.post("/calculate-liability")
async def calculate_gst_liability(
    request: GSTCalculationRequest,
    current_user: models.User = Depends(get_current_user)
):
    """Calculate GST liability"""
    try:
        gst_service = GSTIntegration()
        
        liability = gst_service.calculate_gst_liability(
            {"revenue": request.revenue},
            request.gst_rate
        )
        
        return liability
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating GST: {str(e)}")

@router.post("/check-compliance")
async def check_gst_compliance(
    financial_data_id: int,
    gstin: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check GST compliance"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        gst_service = GSTIntegration()
        
        # Get mock GST data for demo
        gst_data = gst_service.get_mock_gst_data(gstin or "29ABCDE1234F1Z5")
        
        # Validate compliance
        compliance_result = gst_service.validate_compliance(
            gst_data,
            financial_data.normalized_data
        )
        
        return {
            "gst_data": gst_data,
            "compliance": compliance_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error checking compliance: {str(e)}")

@router.get("/summary-report")
async def get_gst_summary_report(
    gstin: Optional[str] = None,
    current_user: models.User = Depends(get_current_user)
):
    """Get GST summary report"""
    try:
        gst_service = GSTIntegration()
        
        # Get mock GST data for demo
        gst_data = gst_service.get_mock_gst_data(gstin or "29ABCDE1234F1Z5")
        
        # Generate summary report
        report = gst_service.generate_gst_summary_report(gst_data)
        
        return report
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating report: {str(e)}")

@router.get("/demo-data")
async def get_demo_gst_data(
    gstin: Optional[str] = None,
    current_user: models.User = Depends(get_current_user)
):
    """Get demo GST data"""
    try:
        gst_service = GSTIntegration()
        demo_data = gst_service.get_mock_gst_data(gstin or "29ABCDE1234F1Z5")
        
        return {
            "message": "Demo GST data. Upload actual GST returns for real data.",
            "data": demo_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching demo data: {str(e)}")

@router.get("/rates")
async def get_gst_rates():
    """Get GST rates"""
    return {
        "rates": [0, 5, 12, 18, 28],
        "description": {
            "0%": "Essential goods (food grains, fresh vegetables, etc.)",
            "5%": "Household necessities (edible oil, sugar, tea, coffee, etc.)",
            "12%": "Processed food, computers, etc.",
            "18%": "Most goods and services (standard rate)",
            "28%": "Luxury items (cars, tobacco, aerated drinks, etc.)"
        }
    }

@router.get("/filing-calendar")
async def get_gst_filing_calendar():
    """Get GST filing calendar"""
    return {
        "monthly_returns": [
            {
                "return": "GSTR-1",
                "description": "Details of outward supplies",
                "due_date": "11th of next month",
                "frequency": "Monthly"
            },
            {
                "return": "GSTR-3B",
                "description": "Summary return",
                "due_date": "20th of next month",
                "frequency": "Monthly"
            }
        ],
        "annual_returns": [
            {
                "return": "GSTR-9",
                "description": "Annual return",
                "due_date": "December 31",
                "frequency": "Yearly"
            },
            {
                "return": "GSTR-9C",
                "description": "Reconciliation statement (if turnover > 2 Cr)",
                "due_date": "December 31",
                "frequency": "Yearly"
            }
        ],
        "penalties": {
            "late_filing_gstr3b": "₹50 per day (₹20 if nil return)",
            "late_filing_gstr1": "₹200 per day",
            "max_penalty": "₹5,000 per return"
        }
    }

@router.get("/status")
async def get_gst_integration_status(
    current_user: models.User = Depends(get_current_user)
):
    """Get GST integration status"""
    return {
        "is_integrated": False,
        "is_demo_mode": True,
        "message": "GST integration available in demo mode. Upload GST returns or connect to GST portal for real data.",
        "features_available": [
            "Upload GSTR-1 and GSTR-3B returns",
            "Calculate GST liability",
            "Check GST compliance",
            "Generate GST summary reports",
            "View GST filing calendar"
        ],
        "setup_instructions": {
            "step1": "Register for GST (if turnover > ₹40 lakhs)",
            "step2": "File monthly GST returns (GSTR-1 and GSTR-3B)",
            "step3": "Upload returns to platform for analysis",
            "step4": "Get compliance insights and recommendations"
        }
    }
