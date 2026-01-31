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
    
    if data_type == "profit_loss":
        normalized = {
            'revenue': float(df.get('revenue', df.get('sales', pd.Series([0]))).sum()),
            'cost_of_goods_sold': float(df.get('cogs', df.get('cost_of_goods_sold', pd.Series([0]))).sum()),
            'gross_profit': float(df.get('gross_profit', pd.Series([0])).sum()),
            'operating_expenses': float(df.get('operating_expenses', df.get('opex', pd.Series([0]))).sum()),
            'operating_profit': float(df.get('operating_profit', df.get('ebit', pd.Series([0]))).sum()),
            'net_profit': float(df.get('net_profit', df.get('net_income', pd.Series([0]))).sum()),
            'ebit': float(df.get('ebit', df.get('operating_profit', pd.Series([0]))).sum()),
            'interest_expense': float(df.get('interest_expense', pd.Series([0])).sum()),
        }
        
        # Calculate if not provided
        if normalized['gross_profit'] == 0:
            normalized['gross_profit'] = normalized['revenue'] - normalized['cost_of_goods_sold']
        
    elif data_type == "balance_sheet":
        normalized = {
            'current_assets': float(df.get('current_assets', pd.Series([0])).sum()),
            'cash': float(df.get('cash', df.get('cash_and_equivalents', pd.Series([0]))).sum()),
            'inventory': float(df.get('inventory', pd.Series([0])).sum()),
            'current_liabilities': float(df.get('current_liabilities', pd.Series([0])).sum()),
            'total_assets': float(df.get('total_assets', pd.Series([0])).sum()),
            'total_debt': float(df.get('total_debt', df.get('total_liabilities', pd.Series([0]))).sum()),
            'equity': float(df.get('equity', df.get('shareholders_equity', pd.Series([0]))).sum()),
        }
        
    elif data_type == "cash_flow":
        normalized = {
            'operating_cash_flow': float(df.get('operating_cash_flow', df.get('ocf', pd.Series([0]))).sum()),
            'investing_cash_flow': float(df.get('investing_cash_flow', pd.Series([0])).sum()),
            'financing_cash_flow': float(df.get('financing_cash_flow', pd.Series([0])).sum()),
            'net_cash_flow': float(df.get('net_cash_flow', pd.Series([0])).sum()),
            'receivables_days': float(df.get('receivables_days', pd.Series([45])).mean()),
            'payables_days': float(df.get('payables_days', pd.Series([30])).mean()),
            'inventory_days': float(df.get('inventory_days', pd.Series([30])).mean()),
        }
    
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
