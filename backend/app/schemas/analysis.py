from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    financial_data_id: int
    created_at: datetime
    health_score: float
    risk_band: str
    liquidity_score: float
    profitability_score: float
    cash_flow_score: float
    debt_health_score: float
    metrics: Dict
    ai_insights: Dict
    recommendations: List[Dict]
    industry_comparison: Optional[Dict]
    credit_readiness: Optional[Dict]
    cash_flow_forecast: Optional[Dict]
    
    class Config:
        from_attributes = True

class FinancialMetrics(BaseModel):
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    gross_profit_margin: Optional[float]
    net_profit_margin: Optional[float]
    operating_cash_flow: Optional[float]
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]
