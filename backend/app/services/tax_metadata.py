from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import models

class TaxMetadataManager:
    """Manage tax deductions and compliance metadata"""
    
    # Tax deduction limits (India - FY 2024-25)
    DEDUCTION_LIMITS = {
        "80C": {
            "name": "Section 80C",
            "limit": 150000,
            "description": "Life insurance, PPF, ELSS, EPF, etc.",
            "eligible_items": ["LIC Premium", "PPF", "ELSS", "EPF", "NSC", "Home Loan Principal"]
        },
        "80D": {
            "name": "Section 80D",
            "limit": 25000,
            "senior_limit": 50000,
            "description": "Health insurance premiums",
            "eligible_items": ["Health Insurance", "Preventive Health Checkup"]
        },
        "80E": {
            "name": "Section 80E",
            "limit": None,  # No limit
            "description": "Education loan interest",
            "eligible_items": ["Education Loan Interest"]
        },
        "80G": {
            "name": "Section 80G",
            "limit": None,  # Varies by donation
            "description": "Donations to charitable institutions",
            "eligible_items": ["Charitable Donations"]
        },
        "24B": {
            "name": "Section 24(b)",
            "limit": 200000,
            "description": "Home loan interest",
            "eligible_items": ["Home Loan Interest"]
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def track_deduction(self, user_id: int, deduction_data: Dict) -> Dict:
        """Track a tax deduction"""
        section = deduction_data.get('section', '')
        amount = deduction_data.get('amount', 0)
        
        # Validate deduction
        is_eligible, message = self.validate_deduction_eligibility(section, amount)
        
        # Convert boolean to integer for database (0 or 1)
        is_eligible_int = 1 if is_eligible else 0
        
        deduction = models.TaxDeduction(
            user_id=user_id,
            financial_year=deduction_data.get('financial_year', self._get_current_fy()),
            section=section,
            description=deduction_data.get('description', ''),
            amount=amount,
            is_eligible=is_eligible_int,  # Use integer instead of boolean
            document_path=deduction_data.get('document_path')
        )
        
        self.db.add(deduction)
        self.db.commit()
        self.db.refresh(deduction)
        
        return {
            "id": deduction.id,
            "is_eligible": bool(is_eligible_int),  # Convert back to boolean for response
            "message": message,
            "amount": amount,
            "section": section
        }
    
    def validate_deduction_eligibility(self, section: str, amount: float, 
                                      is_senior: bool = False) -> tuple[bool, str]:
        """Validate if a deduction is eligible"""
        if section not in self.DEDUCTION_LIMITS:
            return False, f"Unknown deduction section: {section}"
        
        limit_info = self.DEDUCTION_LIMITS[section]
        limit = limit_info.get('senior_limit' if is_senior else 'limit')
        
        if limit is None:
            return True, f"Deduction eligible under {limit_info['name']}"
        
        if amount > limit:
            return False, f"Amount exceeds limit of ₹{limit:,.0f} for {limit_info['name']}"
        
        return True, f"Deduction eligible under {limit_info['name']}"
    
    def get_deduction_summary(self, user_id: int, financial_year: str = None) -> Dict:
        """Get summary of all deductions for a financial year"""
        if not financial_year:
            financial_year = self._get_current_fy()
        
        deductions = self.db.query(models.TaxDeduction).filter(
            models.TaxDeduction.user_id == user_id,
            models.TaxDeduction.financial_year == financial_year
        ).all()
        
        summary = {
            "financial_year": financial_year,
            "total_deductions": 0,
            "eligible_deductions": 0,
            "by_section": {},
            "deductions": []
        }
        
        for deduction in deductions:
            summary["total_deductions"] += deduction.amount
            if deduction.is_eligible:
                summary["eligible_deductions"] += deduction.amount
            
            section = deduction.section
            if section not in summary["by_section"]:
                summary["by_section"][section] = {
                    "total": 0,
                    "limit": self.DEDUCTION_LIMITS.get(section, {}).get('limit'),
                    "count": 0
                }
            
            summary["by_section"][section]["total"] += deduction.amount
            summary["by_section"][section]["count"] += 1
            
            summary["deductions"].append({
                "id": deduction.id,
                "section": deduction.section,
                "description": deduction.description,
                "amount": deduction.amount,
                "is_eligible": bool(deduction.is_eligible)  # Convert integer to boolean
            })
        
        return summary
    
    def track_compliance(self, user_id: int, compliance_data: Dict) -> Dict:
        """Track tax compliance status"""
        compliance = models.TaxCompliance(
            user_id=user_id,
            financial_year=compliance_data.get('financial_year', self._get_current_fy()),
            compliance_type=compliance_data.get('compliance_type'),
            status=compliance_data.get('status', 'Pending'),
            due_date=compliance_data.get('due_date'),
            filed_date=compliance_data.get('filed_date'),
            compliance_metadata=compliance_data.get('metadata', {})  # Updated field name
        )
        
        self.db.add(compliance)
        self.db.commit()
        self.db.refresh(compliance)
        
        return {
            "id": compliance.id,
            "compliance_type": compliance.compliance_type,
            "status": compliance.status,
            "due_date": compliance.due_date
        }
    
    def get_compliance_status(self, user_id: int, financial_year: str = None) -> Dict:
        """Get compliance status for a financial year"""
        if not financial_year:
            financial_year = self._get_current_fy()
        
        compliances = self.db.query(models.TaxCompliance).filter(
            models.TaxCompliance.user_id == user_id,
            models.TaxCompliance.financial_year == financial_year
        ).all()
        
        status = {
            "financial_year": financial_year,
            "total_items": len(compliances),
            "compliant": 0,
            "non_compliant": 0,
            "pending": 0,
            "items": []
        }
        
        for compliance in compliances:
            if compliance.status == "Compliant":
                status["compliant"] += 1
            elif compliance.status == "Non-compliant":
                status["non_compliant"] += 1
            else:
                status["pending"] += 1
            
            status["items"].append({
                "id": compliance.id,
                "type": compliance.compliance_type,
                "status": compliance.status,
                "due_date": compliance.due_date.isoformat() if compliance.due_date else None,
                "filed_date": compliance.filed_date.isoformat() if compliance.filed_date else None
            })
        
        return status
    
    def get_tax_optimization_suggestions(self, user_id: int, 
                                        financial_data: Dict) -> List[Dict]:
        """Get tax optimization suggestions based on financial data"""
        suggestions = []
        
        # Get current deductions
        current_fy = self._get_current_fy()
        deduction_summary = self.get_deduction_summary(user_id, current_fy)
        
        # Check 80C utilization
        section_80c = deduction_summary["by_section"].get("80C", {"total": 0})
        if section_80c["total"] < 150000:
            remaining = 150000 - section_80c["total"]
            suggestions.append({
                "section": "80C",
                "title": "Maximize Section 80C Deductions",
                "description": f"You can save up to ₹{remaining:,.0f} more under Section 80C",
                "potential_saving": remaining * 0.3,  # Assuming 30% tax bracket
                "options": self.DEDUCTION_LIMITS["80C"]["eligible_items"]
            })
        
        # Check 80D (Health Insurance)
        section_80d = deduction_summary["by_section"].get("80D", {"total": 0})
        if section_80d["total"] < 25000:
            remaining = 25000 - section_80d["total"]
            suggestions.append({
                "section": "80D",
                "title": "Health Insurance Deduction",
                "description": f"Invest in health insurance to save up to ₹{remaining:,.0f}",
                "potential_saving": remaining * 0.3,
                "options": self.DEDUCTION_LIMITS["80D"]["eligible_items"]
            })
        
        # Check home loan interest
        interest_expense = financial_data.get('interest_expense', 0)
        if interest_expense > 0:
            section_24b = deduction_summary["by_section"].get("24B", {"total": 0})
            if section_24b["total"] < interest_expense:
                suggestions.append({
                    "section": "24B",
                    "title": "Home Loan Interest Deduction",
                    "description": "Claim home loan interest deduction up to ₹2,00,000",
                    "potential_saving": min(interest_expense, 200000) * 0.3,
                    "options": ["Home Loan Interest"]
                })
        
        return suggestions
    
    def _get_current_fy(self) -> str:
        """Get current financial year (Apr-Mar)"""
        now = datetime.now()
        if now.month >= 4:
            return f"FY{now.year}-{now.year + 1}"
        else:
            return f"FY{now.year - 1}-{now.year}"
