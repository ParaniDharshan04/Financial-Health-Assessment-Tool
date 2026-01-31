from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.plaid_integration import PlaidIntegration

router = APIRouter()

class LinkBankRequest(BaseModel):
    public_token: str
    institution_id: Optional[str] = None
    institution_name: Optional[str] = None
    accounts: Optional[list] = None

class SyncRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@router.post("/create-link-token")
async def create_link_token(
    current_user: models.User = Depends(get_current_user)
):
    """Create a Plaid Link token for connecting bank account"""
    try:
        plaid = PlaidIntegration()
        result = plaid.create_link_token(current_user.id, current_user.email)
        
        if result.get("error"):
            # Return error but allow demo mode
            return {
                "link_token": None,
                "is_demo": True,
                "error": result.get("error"),
                "message": "Plaid configuration issue. Using demo mode.",
                "demo_data_available": True
            }
        
        return {
            "link_token": result["link_token"],
            "expiration": result.get("expiration"),
            "is_demo": False
        }
        
    except Exception as e:
        return {
            "link_token": None,
            "is_demo": True,
            "error": str(e),
            "message": f"Banking integration error: {str(e)}",
            "demo_data_available": True
        }

@router.post("/link-bank")
async def link_bank_account(
    request: LinkBankRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exchange public token and link bank account"""
    try:
        plaid = PlaidIntegration()
        result = plaid.exchange_public_token(request.public_token)
        
        if not result or not result.get("access_token"):
            raise HTTPException(status_code=400, detail="Failed to link bank account")
        
        access_token = result["access_token"]
        item_id = result["item_id"]
        
        # Check if connection already exists
        existing = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.item_id == item_id
        ).first()
        
        if existing:
            # Update existing connection
            existing.access_token = access_token
            existing.is_active = 1
            existing.connected_at = datetime.utcnow()
            existing.sync_status = "active"
            existing.error_message = None
            if request.institution_name:
                existing.institution_name = request.institution_name
            if request.institution_id:
                existing.institution_id = request.institution_id
            if request.accounts:
                existing.account_ids = [acc.get("id") for acc in request.accounts]
        else:
            # Create new connection
            bank_connection = models.BankConnection(
                user_id=current_user.id,
                access_token=access_token,
                item_id=item_id,
                institution_id=request.institution_id,
                institution_name=request.institution_name or "Connected Bank",
                account_ids=[acc.get("id") for acc in request.accounts] if request.accounts else [],
                is_active=1,
                sync_status="active"
            )
            db.add(bank_connection)
        
        db.commit()
        
        # Fetch initial account data
        accounts = plaid.get_accounts(access_token)
        
        return {
            "message": "Bank account linked successfully",
            "status": "connected",
            "institution_name": request.institution_name or "Connected Bank",
            "accounts_count": len(accounts),
            "accounts": accounts
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error linking bank: {str(e)}")

@router.get("/accounts")
async def get_bank_accounts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get linked bank accounts"""
    try:
        # Check for active bank connection
        bank_connection = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.is_active == 1
        ).first()
        
        if not bank_connection:
            # Return demo data if no connection
            plaid = PlaidIntegration()
            mock_data = plaid.get_mock_data_for_demo()
            return {
                "accounts": mock_data["accounts"],
                "is_demo": True,
                "message": "No bank connected. Showing demo data. Click 'Connect Bank Account' to link your bank."
            }
        
        # Fetch real account data
        plaid = PlaidIntegration()
        accounts = plaid.get_accounts(bank_connection.access_token)
        
        # Update last sync
        bank_connection.last_sync = datetime.utcnow()
        db.commit()
        
        return {
            "accounts": accounts,
            "is_demo": False,
            "institution_name": bank_connection.institution_name,
            "last_sync": bank_connection.last_sync.isoformat(),
            "message": f"Connected to {bank_connection.institution_name}"
        }
        
    except Exception as e:
        # Return demo data on error
        plaid = PlaidIntegration()
        mock_data = plaid.get_mock_data_for_demo()
        return {
            "accounts": mock_data["accounts"],
            "is_demo": True,
            "error": str(e),
            "message": f"Error fetching accounts: {str(e)}. Showing demo data."
        }

@router.get("/transactions")
async def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get bank transactions"""
    try:
        # Check for active bank connection
        bank_connection = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.is_active == 1
        ).first()
        
        if not bank_connection:
            # Return demo data if no connection
            plaid = PlaidIntegration()
            mock_data = plaid.get_mock_data_for_demo()
            return {
                "transactions": mock_data["transactions"],
                "total_count": len(mock_data["transactions"]),
                "is_demo": True,
                "message": "No bank connected. Showing demo data."
            }
        
        # Parse dates
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        # Fetch real transactions
        plaid = PlaidIntegration()
        transactions = plaid.get_transactions(bank_connection.access_token, start, end)
        
        # Update last sync
        bank_connection.last_sync = datetime.utcnow()
        db.commit()
        
        return {
            "transactions": transactions,
            "total_count": len(transactions),
            "is_demo": False,
            "institution_name": bank_connection.institution_name,
            "last_sync": bank_connection.last_sync.isoformat()
        }
        
    except Exception as e:
        # Return demo data on error
        plaid = PlaidIntegration()
        mock_data = plaid.get_mock_data_for_demo()
        return {
            "transactions": mock_data["transactions"],
            "total_count": len(mock_data["transactions"]),
            "is_demo": True,
            "error": str(e),
            "message": f"Error fetching transactions: {str(e)}"
        }

@router.post("/sync")
async def sync_banking_data(
    request: SyncRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync banking data to financial data"""
    try:
        # Check for active bank connection
        bank_connection = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.is_active == 1
        ).first()
        
        plaid = PlaidIntegration()
        
        if not bank_connection:
            # Use demo data
            mock_data = plaid.get_mock_data_for_demo()
            financial_data = plaid.sync_to_financial_data(
                mock_data["transactions"],
                mock_data["accounts"]
            )
            is_demo = True
        else:
            # Fetch real data
            accounts = plaid.get_accounts(bank_connection.access_token)
            
            start = datetime.fromisoformat(request.start_date) if request.start_date else None
            end = datetime.fromisoformat(request.end_date) if request.end_date else None
            transactions = plaid.get_transactions(bank_connection.access_token, start, end)
            
            financial_data = plaid.sync_to_financial_data(transactions, accounts)
            is_demo = False
            
            # Update last sync
            bank_connection.last_sync = datetime.utcnow()
        
        # Store in database
        db_financial_data = models.FinancialData(
            user_id=current_user.id,
            data_type="bank_sync",
            raw_data={"accounts": accounts if not is_demo else mock_data["accounts"], 
                     "transactions": transactions if not is_demo else mock_data["transactions"]},
            normalized_data=financial_data
        )
        
        db.add(db_financial_data)
        db.commit()
        db.refresh(db_financial_data)
        
        return {
            "message": "Banking data synced successfully",
            "data_id": db_financial_data.id,
            "financial_data": financial_data,
            "is_demo": is_demo
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error syncing data: {str(e)}")

@router.get("/balance")
async def get_account_balance(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get total account balance"""
    try:
        # Check for active bank connection
        bank_connection = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.is_active == 1
        ).first()
        
        plaid = PlaidIntegration()
        
        if not bank_connection:
            # Return demo data
            mock_data = plaid.get_mock_data_for_demo()
            accounts = mock_data["accounts"]
            is_demo = True
        else:
            # Fetch real data
            accounts = plaid.get_accounts(bank_connection.access_token)
            is_demo = False
        
        total_balance = sum(acc['balance']['current'] for acc in accounts)
        
        return {
            "total_balance": total_balance,
            "currency": accounts[0]['balance']['currency'] if accounts else "INR",
            "accounts": accounts,
            "is_demo": is_demo,
            "message": "Demo data" if is_demo else f"Connected to {bank_connection.institution_name}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching balance: {str(e)}")

@router.get("/status")
async def get_banking_status(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get banking integration status"""
    bank_connection = db.query(models.BankConnection).filter(
        models.BankConnection.user_id == current_user.id,
        models.BankConnection.is_active == 1
    ).first()
    
    if bank_connection:
        return {
            "is_connected": True,
            "is_demo_mode": False,
            "provider": "Plaid",
            "institution_name": bank_connection.institution_name,
            "connected_at": bank_connection.connected_at.isoformat(),
            "last_sync": bank_connection.last_sync.isoformat() if bank_connection.last_sync else None,
            "sync_status": bank_connection.sync_status,
            "message": f"Connected to {bank_connection.institution_name}"
        }
    
    return {
        "is_connected": False,
        "is_demo_mode": True,
        "provider": "Plaid",
        "message": "No bank connected. Click 'Connect Bank Account' to link your bank.",
        "setup_instructions": {
            "step1": "Click 'Connect Bank Account' button",
            "step2": "Select your bank from the list",
            "step3": "Login with your online banking credentials",
            "step4": "Select accounts to connect"
        }
    }

@router.post("/disconnect")
async def disconnect_bank(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect bank account"""
    try:
        bank_connection = db.query(models.BankConnection).filter(
            models.BankConnection.user_id == current_user.id,
            models.BankConnection.is_active == 1
        ).first()
        
        if not bank_connection:
            raise HTTPException(status_code=404, detail="No active bank connection found")
        
        # Mark as inactive instead of deleting
        bank_connection.is_active = 0
        bank_connection.sync_status = "disconnected"
        db.commit()
        
        return {
            "message": "Bank account disconnected successfully",
            "status": "disconnected"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error disconnecting bank: {str(e)}")
