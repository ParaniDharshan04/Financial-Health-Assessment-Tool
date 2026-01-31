from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.bookkeeping_automation import BookkeepingAutomation, TransactionCategorizer

router = APIRouter()

class Transaction(BaseModel):
    id: Optional[int] = None
    date: str
    description: str
    amount: float
    merchant: Optional[str] = None

class CorrectionRequest(BaseModel):
    transaction: Transaction
    correct_category: str

@router.post("/categorize")
async def categorize_transactions(
    transactions: List[Transaction],
    current_user: models.User = Depends(get_current_user)
):
    """Categorize transactions automatically"""
    try:
        automation = BookkeepingAutomation()
        
        # Convert to dict format
        txn_dicts = [t.dict() for t in transactions]
        
        # Categorize
        categorized = automation.categorizer.categorize_bulk(txn_dicts)
        
        return {
            "message": "Transactions categorized successfully",
            "total_transactions": len(categorized),
            "categorized_transactions": categorized
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error categorizing transactions: {str(e)}")

@router.post("/journal-entries")
async def generate_journal_entries(
    transactions: List[Transaction],
    current_user: models.User = Depends(get_current_user)
):
    """Generate journal entries from transactions"""
    try:
        automation = BookkeepingAutomation()
        
        # Convert to dict and categorize first
        txn_dicts = [t.dict() for t in transactions]
        categorized = automation.categorizer.categorize_bulk(txn_dicts)
        
        # Generate journal entries
        journal_entries = automation.generate_journal_entries(categorized)
        
        return {
            "message": "Journal entries generated successfully",
            "total_entries": len(journal_entries),
            "journal_entries": journal_entries
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating journal entries: {str(e)}")

@router.post("/reconcile")
async def reconcile_accounts(
    bank_statement: List[Transaction],
    book_entries: List[Transaction],
    current_user: models.User = Depends(get_current_user)
):
    """Reconcile bank statement with book entries"""
    try:
        automation = BookkeepingAutomation()
        
        # Convert to dict format
        bank_dicts = [t.dict() for t in bank_statement]
        book_dicts = [t.dict() for t in book_entries]
        
        # Reconcile
        reconciliation = automation.reconcile_accounts(bank_dicts, book_dicts)
        
        return reconciliation
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reconciling accounts: {str(e)}")

@router.post("/detect-duplicates")
async def detect_duplicates(
    transactions: List[Transaction],
    current_user: models.User = Depends(get_current_user)
):
    """Detect duplicate transactions"""
    try:
        automation = BookkeepingAutomation()
        
        # Convert to dict format
        txn_dicts = [t.dict() for t in transactions]
        
        # Detect duplicates
        duplicates = automation.detect_duplicates(txn_dicts)
        
        return {
            "message": "Duplicate detection complete",
            "total_duplicates": len(duplicates),
            "duplicates": duplicates
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error detecting duplicates: {str(e)}")

@router.post("/expense-report")
async def generate_expense_report(
    transactions: List[Transaction],
    current_user: models.User = Depends(get_current_user)
):
    """Generate expense tracking report"""
    try:
        automation = BookkeepingAutomation()
        
        # Convert to dict format
        txn_dicts = [t.dict() for t in transactions]
        
        # Track expenses
        expense_report = automation.track_expenses(txn_dicts)
        
        return expense_report
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating expense report: {str(e)}")

@router.post("/learn")
async def learn_from_correction(
    correction: CorrectionRequest,
    current_user: models.User = Depends(get_current_user)
):
    """Learn from user corrections"""
    try:
        categorizer = TransactionCategorizer()
        
        result = categorizer.learn_from_corrections(
            correction.transaction.dict(),
            correction.correct_category
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error learning from correction: {str(e)}")

@router.get("/demo-transactions")
async def get_demo_transactions(
    current_user: models.User = Depends(get_current_user)
):
    """Get demo transactions for testing"""
    try:
        automation = BookkeepingAutomation()
        demo_transactions = automation.get_demo_transactions()
        
        return {
            "message": "Demo transactions for testing bookkeeping features",
            "transactions": demo_transactions
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching demo transactions: {str(e)}")

@router.get("/categories")
async def get_available_categories(
    current_user: models.User = Depends(get_current_user)
):
    """Get list of available transaction categories"""
    categorizer = TransactionCategorizer()
    
    return {
        "categories": categorizer.categories,
        "total_categories": len(categorizer.categories)
    }

@router.get("/status")
async def get_bookkeeping_status(
    current_user: models.User = Depends(get_current_user)
):
    """Get bookkeeping automation status"""
    return {
        "is_active": True,
        "features_available": [
            "Automatic transaction categorization",
            "Journal entry generation",
            "Bank reconciliation",
            "Duplicate detection",
            "Expense tracking and reporting",
            "Machine learning-based categorization"
        ],
        "ml_model_status": "Trained and ready",
        "supported_categories": 17,
        "message": "Bookkeeping automation is active and ready to use"
    }
