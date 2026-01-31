from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.working_capital_optimizer import WorkingCapitalOptimizer, ScenarioModeler

router = APIRouter()

class ScenarioRequest(BaseModel):
    name: str
    receivables_days: Optional[float] = None
    inventory_days: Optional[float] = None
    payables_days: Optional[float] = None

class WhatIfRequest(BaseModel):
    variable: str
    values: List[float]

@router.post("/working-capital")
async def optimize_working_capital(
    financial_data_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Optimize working capital"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        optimizer = WorkingCapitalOptimizer(financial_data.normalized_data)
        results = optimizer.optimize_working_capital()
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error optimizing working capital: {str(e)}")

@router.post("/scenario")
async def create_scenario(
    financial_data_id: int,
    scenario: ScenarioRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and analyze a scenario"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        modeler = ScenarioModeler(financial_data.normalized_data)
        
        # Create scenario with changes
        changes = {"name": scenario.name}
        if scenario.receivables_days is not None:
            changes["receivables_days"] = scenario.receivables_days
        if scenario.inventory_days is not None:
            changes["inventory_days"] = scenario.inventory_days
        if scenario.payables_days is not None:
            changes["payables_days"] = scenario.payables_days
        
        result = modeler.create_scenario(changes)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating scenario: {str(e)}")

@router.post("/compare-scenarios")
async def compare_scenarios(
    financial_data_id: int,
    scenarios: List[ScenarioRequest],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare multiple scenarios"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        modeler = ScenarioModeler(financial_data.normalized_data)
        
        # Convert scenarios to dict format
        scenario_dicts = []
        for s in scenarios:
            changes = {"name": s.name}
            if s.receivables_days is not None:
                changes["receivables_days"] = s.receivables_days
            if s.inventory_days is not None:
                changes["inventory_days"] = s.inventory_days
            if s.payables_days is not None:
                changes["payables_days"] = s.payables_days
            scenario_dicts.append(changes)
        
        comparison = modeler.compare_scenarios(scenario_dicts)
        
        return comparison
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error comparing scenarios: {str(e)}")

@router.post("/what-if")
async def what_if_analysis(
    financial_data_id: int,
    request: WhatIfRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform what-if analysis"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        modeler = ScenarioModeler(financial_data.normalized_data)
        result = modeler.what_if_analysis(request.variable, request.values)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in what-if analysis: {str(e)}")

@router.post("/sensitivity")
async def sensitivity_analysis(
    financial_data_id: int,
    variable: str = Query(..., description="Variable to analyze (receivables_days, inventory_days, payables_days)"),
    range_percent: float = Query(0.20, description="Range as percentage (default 20%)"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform sensitivity analysis"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        optimizer = WorkingCapitalOptimizer(financial_data.normalized_data)
        result = optimizer.sensitivity_analysis(variable, range_percent)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in sensitivity analysis: {str(e)}")

@router.post("/monte-carlo")
async def monte_carlo_simulation(
    financial_data_id: int,
    iterations: int = Query(1000, description="Number of simulation iterations"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run Monte Carlo simulation"""
    try:
        # Get financial data
        financial_data = db.query(models.FinancialData).filter(
            models.FinancialData.id == financial_data_id,
            models.FinancialData.user_id == current_user.id
        ).first()
        
        if not financial_data:
            raise HTTPException(status_code=404, detail="Financial data not found")
        
        optimizer = WorkingCapitalOptimizer(financial_data.normalized_data)
        result = optimizer.monte_carlo_simulation(iterations)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in Monte Carlo simulation: {str(e)}")

@router.get("/demo")
async def get_optimization_demo(
    current_user: models.User = Depends(get_current_user)
):
    """Get demo optimization data"""
    demo_data = {
        "revenue": 10000000,
        "current_assets": 2500000,
        "current_liabilities": 1500000,
        "inventory": 500000,
        "receivables_days": 45,
        "payables_days": 30,
        "inventory_days": 30
    }
    
    optimizer = WorkingCapitalOptimizer(demo_data)
    results = optimizer.optimize_working_capital()
    
    return {
        "message": "Demo optimization results",
        "demo_data": demo_data,
        "optimization_results": results
    }
