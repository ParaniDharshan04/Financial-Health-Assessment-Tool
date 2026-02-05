from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import pandas as pd
import json
import numpy as np
from io import BytesIO
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.pdf_parser import PDFParser

router = APIRouter()

def convert_to_native_types(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization"""
    if isinstance(obj, dict):
        return {key: convert_to_native_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    return obj

@router.post("/upload")
async def upload_financial_data(
    file: UploadFile = File(...),
    data_type: str = Form(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process financial data from CSV/XLSX/PDF"""
    
    try:
        # Read file
        contents = await file.read()
        
        # Handle different file types
        if file.filename.endswith('.pdf'):
            # Parse PDF
            pdf_parser = PDFParser()
            normalized_data = pdf_parser.extract_financial_data(contents, data_type)
            
            # Validate extracted data
            if not pdf_parser.validate_extracted_data(normalized_data, data_type):
                raise HTTPException(
                    status_code=400, 
                    detail="Could not extract sufficient financial data from PDF. Please ensure the PDF contains a financial statement with clear labels and values."
                )
            
            # Convert to native types
            raw_data = [normalized_data]  # Store extracted data as raw
            normalized_data = convert_to_native_types(normalized_data)
            
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
            normalized_data = normalize_financial_data(df, data_type)
            raw_data = convert_to_native_types(df.to_dict('records'))
            normalized_data = convert_to_native_types(normalized_data)
            
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(contents))
            normalized_data = normalize_financial_data(df, data_type)
            raw_data = convert_to_native_types(df.to_dict('records'))
            normalized_data = convert_to_native_types(normalized_data)
            
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV, XLSX, or PDF")
        
        # Store in database
        financial_data = models.FinancialData(
            user_id=current_user.id,
            data_type=data_type,
            raw_data=raw_data,
            normalized_data=normalized_data
        )
        
        db.add(financial_data)
        db.commit()
        db.refresh(financial_data)
        
        return {
            "message": "Financial data uploaded successfully",
            "data_id": financial_data.id,
            "records_processed": len(raw_data) if isinstance(raw_data, list) else 1,
            "file_type": "PDF" if file.filename.endswith('.pdf') else "CSV/XLSX"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

def normalize_financial_data(df: pd.DataFrame, data_type: str) -> dict:
    """Normalize financial data based on type"""
    
    # Convert to lowercase column names
    df.columns = df.columns.str.lower().str.strip()
    
    normalized = {}
    
    # Get the latest row (most recent data)
    latest = df.iloc[-1] if len(df) > 0 else pd.Series()
    
    # Try to extract all possible fields regardless of data_type
    # This allows for combined financial statements
    all_fields = {
        # P&L fields
        'revenue': float(latest.get('revenue', 0)),
        'cost_of_goods_sold': float(latest.get('cost_of_goods_sold', 0)),
        'gross_profit': float(latest.get('gross_profit', 0)),
        'operating_expenses': float(latest.get('operating_expenses', 0)),
        'operating_profit': float(latest.get('operating_profit', 0)),
        'net_profit': float(latest.get('net_profit', 0)),
        'ebit': float(latest.get('ebit', 0)),
        'ebitda': float(latest.get('ebitda', 0)),
        'interest_expense': float(latest.get('interest_expense', 0)),
        'depreciation': float(latest.get('depreciation', 0)),
        # Balance Sheet fields
        'current_assets': float(latest.get('current_assets', 0)),
        'cash': float(latest.get('cash', 0)),
        'inventory': float(latest.get('inventory', 0)),
        'accounts_receivable': float(latest.get('accounts_receivable', 0)),
        'current_liabilities': float(latest.get('current_liabilities', 0)),
        'accounts_payable': float(latest.get('accounts_payable', 0)),
        'total_assets': float(latest.get('total_assets', 0)),
        'fixed_assets': float(latest.get('fixed_assets', 0)),
        'total_debt': float(latest.get('long_term_debt', 0)),
        'total_liabilities': float(latest.get('total_liabilities', 0)),
        'equity': float(latest.get('equity', 0)),
        # Cash Flow fields
        'operating_cash_flow': float(latest.get('operating_cash_flow', 0)),
        'investing_cash_flow': float(latest.get('investing_cash_flow', 0)),
        'financing_cash_flow': float(latest.get('financing_cash_flow', 0)),
        'receivables_days': float(latest.get('receivables_days', 45)),
        'payables_days': float(latest.get('payables_days', 30)),
        'inventory_days': float(latest.get('inventory_days', 30)),
    }
    
    # Only include non-zero values (except for days which can be zero)
    normalized = {k: v for k, v in all_fields.items() if v != 0 or k in ['receivables_days', 'payables_days', 'inventory_days']}
    
    # Calculate derived fields if not provided
    if 'gross_profit' not in normalized and normalized.get('revenue', 0) > 0:
        normalized['gross_profit'] = normalized.get('revenue', 0) - normalized.get('cost_of_goods_sold', 0)
    
    if 'ebit' not in normalized and normalized.get('operating_profit', 0) > 0:
        normalized['ebit'] = normalized['operating_profit']
    
    return normalized

@router.get("/my-data")
def get_my_financial_data(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all financial data for current user"""
    
    data = db.query(models.FinancialData).filter(
        models.FinancialData.user_id == current_user.id
    ).all()
    
    return {"data": data}
