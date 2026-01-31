from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.financial_analyzer import FinancialAnalyzer
from app.services.ai_insights import AIInsightsGenerator
from app.services.industry_benchmark import IndustryBenchmark
from app.services.credit_assessment import CreditAssessment
from app.services.cash_flow_forecast import CashFlowForecaster
from app.schemas.analysis import AnalysisResponse

router = APIRouter()

@router.post("/create/{financial_data_id}")
def create_analysis(
    financial_data_id: int,
    language: str = Query("en", regex="^(en|hi)$"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create comprehensive financial analysis"""
    
    # Get financial data
    financial_data = db.query(models.FinancialData).filter(
        models.FinancialData.id == financial_data_id,
        models.FinancialData.user_id == current_user.id
    ).first()
    
    if not financial_data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    
    # Combine normalized data
    combined_data = financial_data.normalized_data
    
    # Run financial analysis
    analyzer = FinancialAnalyzer(combined_data)
    health_score, risk_band, metrics, scores = analyzer.calculate_health_score()
    
    # Generate AI insights
    ai_generator = AIInsightsGenerator(language=language)
    ai_insights = ai_generator.generate_insights(health_score, risk_band, metrics, scores)
    recommendations = ai_generator.generate_recommendations(health_score, metrics, scores)
    
    # Industry benchmarking
    industry = current_user.industry or 'services'
    benchmark = IndustryBenchmark(industry)
    industry_comparison = benchmark.compare(metrics)
    
    # Credit assessment
    credit_assessor = CreditAssessment(health_score, metrics, combined_data)
    credit_readiness = credit_assessor.get_full_assessment()
    
    # Cash flow forecast
    forecaster = CashFlowForecaster(combined_data)
    cash_flow_forecast = forecaster.forecast()
    
    # Create analysis record
    analysis = models.Analysis(
        user_id=current_user.id,
        financial_data_id=financial_data_id,
        health_score=health_score,
        risk_band=risk_band,
        liquidity_score=scores['liquidity_score'],
        profitability_score=scores['profitability_score'],
        cash_flow_score=scores['cash_flow_score'],
        debt_health_score=scores['debt_health_score'],
        metrics=metrics,
        ai_insights=ai_insights,
        recommendations=recommendations,
        industry_comparison=industry_comparison,
        credit_readiness=credit_readiness,
        cash_flow_forecast=cash_flow_forecast
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return {
        "message": "Analysis completed successfully",
        "analysis_id": analysis.id,
        "health_score": health_score,
        "risk_band": risk_band
    }

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analysis results"""
    
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id,
        models.Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis

@router.get("/list/all")
def list_analyses(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all analyses for current user"""
    
    analyses = db.query(models.Analysis).filter(
        models.Analysis.user_id == current_user.id
    ).order_by(models.Analysis.created_at.desc()).all()
    
    return {
        "analyses": [
            {
                "id": a.id,
                "created_at": a.created_at,
                "health_score": a.health_score,
                "risk_band": a.risk_band
            }
            for a in analyses
        ]
    }
