from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.tax_compliance import TaxComplianceChecker
from app.services.tax_metadata import TaxMetadataManager
from app.services.tax_rules import get_tax_rules, calculate_income_tax

router = APIRouter()

class DeductionRequest(BaseModel):
    section: str
    description: str
    amount: float
    is_eligible: Optional[bool] = True
    financial_year: Optional[str] = None
    document_path: Optional[str] = None

class ComplianceRequest(BaseModel):
    compliance_type: str
    status: str
    due_date: Optional[str] = None
    filed_date: Optional[str] = None
    metadata: Optional[dict] = None

@router.post("/check-compliance")
async def check_tax_compliance(
    financial_data_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check overall tax compliance"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        # Run compliance check
        checker = TaxComplianceChecker(country="IN")
        compliance_result = checker.check_compliance(
            financial_data.normalized_data,
            {"company_name": current_user.company_name}
        )
        
        return compliance_result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error checking compliance: {str(e)}")

@router.post("/deductions/add")
async def add_tax_deduction(
    deduction: DeductionRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a tax deduction"""
    try:
        tax_manager = TaxMetadataManager(db)
        
        # Convert is_eligible to integer if it's a boolean
        deduction_dict = deduction.dict()
        if 'is_eligible' in deduction_dict and isinstance(deduction_dict['is_eligible'], bool):
            deduction_dict['is_eligible'] = 1 if deduction_dict['is_eligible'] else 0
        
        result = tax_manager.track_deduction(
            user_id=current_user.id,
            deduction_data=deduction_dict
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding deduction: {str(e)}")

@router.get("/deductions/summary")
async def get_deduction_summary(
    financial_year: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary of tax deductions"""
    try:
        tax_manager = TaxMetadataManager(db)
        summary = tax_manager.get_deduction_summary(current_user.id, financial_year)
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching summary: {str(e)}")

@router.post("/deductions/validate")
async def validate_deductions(
    deductions: List[DeductionRequest],
    current_user: models.User = Depends(get_current_user)
):
    """Validate multiple tax deductions"""
    try:
        checker = TaxComplianceChecker(country="IN")
        
        deduction_list = [d.dict() for d in deductions]
        validation_result = checker.validate_deductions(deduction_list)
        
        return validation_result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validating deductions: {str(e)}")

@router.get("/filing-readiness")
async def assess_filing_readiness(
    financial_data_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assess tax filing readiness"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        checker = TaxComplianceChecker(country="IN")
        readiness = checker.assess_filing_readiness(
            financial_data.normalized_data,
            user_documents=[]  # In production, fetch from database
        )
        
        return readiness
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error assessing readiness: {str(e)}")

@router.get("/penalty-risks")
async def identify_penalty_risks(
    financial_data_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Identify potential penalty risks"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        checker = TaxComplianceChecker(country="IN")
        risks = checker.identify_penalty_risks(
            financial_data.normalized_data,
            compliance_history={}  # In production, fetch from database
        )
        
        return {"risks": risks, "total_risks": len(risks)}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error identifying risks: {str(e)}")

@router.get("/optimizations")
async def suggest_tax_optimizations(
    financial_data_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tax optimization suggestions"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        # Get tax manager for deduction-based optimizations
        tax_manager = TaxMetadataManager(db)
        deduction_suggestions = tax_manager.get_tax_optimization_suggestions(
            current_user.id,
            financial_data.normalized_data
        )
        
        # Get compliance checker for general optimizations
        checker = TaxComplianceChecker(country="IN")
        general_optimizations = checker.suggest_tax_optimizations(
            financial_data.normalized_data
        )
        
        return {
            "deduction_optimizations": deduction_suggestions,
            "general_optimizations": general_optimizations,
            "total_suggestions": len(deduction_suggestions) + len(general_optimizations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating optimizations: {str(e)}")

@router.post("/compliance/track")
async def track_compliance(
    compliance: ComplianceRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track tax compliance status"""
    try:
        tax_manager = TaxMetadataManager(db)
        
        result = tax_manager.track_compliance(
            user_id=current_user.id,
            compliance_data=compliance.dict()
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error tracking compliance: {str(e)}")

@router.get("/compliance/status")
async def get_compliance_status(
    financial_year: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance status"""
    try:
        tax_manager = TaxMetadataManager(db)
        status = tax_manager.get_compliance_status(current_user.id, financial_year)
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching status: {str(e)}")

@router.get("/rules")
async def get_tax_rules_info(
    country: str = Query("IN", regex="^(IN|US)$")
):
    """Get tax rules for a country"""
    try:
        rules = get_tax_rules(country)
        
        return {
            "country": rules["country_name"],
            "currency": rules["currency"],
            "income_tax": {
                "financial_year": rules["income_tax"]["financial_year"],
                "filing_deadline": rules["income_tax"]["filing_deadline"],
                "corporate_tax_rate": rules["income_tax"]["corporate_tax"]["domestic_company"]
            },
            "gst": {
                "registration_threshold": rules["gst"]["registration_threshold"],
                "rates": rules["gst"]["rates"]
            },
            "deductions_available": list(rules["income_tax"]["deductions"].keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching rules: {str(e)}")

@router.post("/calculate-tax")
async def calculate_tax(
    income: float,
    country: str = Query("IN", regex="^(IN|US)$")
):
    """Calculate income tax"""
    try:
        result = calculate_income_tax(income, country)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating tax: {str(e)}")

@router.get("/calendar")
async def get_compliance_calendar(
    country: str = Query("IN", regex="^(IN|US)$")
):
    """Get tax compliance calendar"""
    try:
        rules = get_tax_rules(country)
        calendar = rules.get("compliance_calendar", {})
        
        return {
            "country": rules["country_name"],
            "monthly_tasks": calendar.get("monthly", []),
            "quarterly_tasks": calendar.get("quarterly", []),
            "annual_tasks": calendar.get("annual", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching calendar: {str(e)}")
