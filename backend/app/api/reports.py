from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from app.services.report_generator import ReportGenerator
import os

router = APIRouter()

@router.get("/{analysis_id}/pdf")
def generate_pdf_report(
    analysis_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate investor-ready PDF report"""
    
    # Get analysis
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id,
        models.Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Generate report
    generator = ReportGenerator(analysis, current_user)
    report_path = generator.generate_pdf()
    
    # Save report record
    report = models.Report(
        analysis_id=analysis_id,
        report_path=report_path,
        language=analysis.ai_insights.get('language', 'en')
    )
    db.add(report)
    db.commit()
    
    # Return file
    if os.path.exists(report_path):
        return FileResponse(
            report_path,
            media_type='application/pdf',
            filename=f"financial_report_{analysis_id}.pdf"
        )
    else:
        raise HTTPException(status_code=500, detail="Report generation failed")
