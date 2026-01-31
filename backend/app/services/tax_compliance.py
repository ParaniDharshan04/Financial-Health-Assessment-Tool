from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.services.tax_rules import TAX_RULES

class TaxComplianceChecker:
    """Comprehensive tax compliance checking system"""
    
    def __init__(self, country: str = "IN"):
        self.country = country
        self.rules = TAX_RULES.get(country, TAX_RULES["IN"])
    
    def check_compliance(self, financial_data: Dict, user_data: Dict = None) -> Dict:
        """Check overall tax compliance"""
        compliance_results = {
            "overall_status": "Compliant",
            "compliance_score": 100,
            "issues": [],
            "warnings": [],
            "recommendations": [],
            "checks_performed": []
        }
        
        # Check TDS compliance
        tds_result = self._check_tds_compliance(financial_data)
        compliance_results["checks_performed"].append(tds_result)
        if tds_result["status"] != "Compliant":
            compliance_results["issues"].extend(tds_result.get("issues", []))
            compliance_results["compliance_score"] -= 20
        
        # Check GST compliance
        gst_result = self._check_gst_compliance(financial_data)
        compliance_results["checks_performed"].append(gst_result)
        if gst_result["status"] != "Compliant":
            compliance_results["issues"].extend(gst_result.get("issues", []))
            compliance_results["compliance_score"] -= 20
        
        # Check income tax compliance
        income_tax_result = self._check_income_tax_compliance(financial_data)
        compliance_results["checks_performed"].append(income_tax_result)
        if income_tax_result["status"] != "Compliant":
            compliance_results["issues"].extend(income_tax_result.get("issues", []))
            compliance_results["compliance_score"] -= 20
        
        # Check filing deadlines
        deadline_result = self._check_filing_deadlines(financial_data)
        compliance_results["checks_performed"].append(deadline_result)
        if deadline_result.get("warnings"):
            compliance_results["warnings"].extend(deadline_result["warnings"])
            compliance_results["compliance_score"] -= 10
        
        # Determine overall status
        if compliance_results["compliance_score"] >= 80:
            compliance_results["overall_status"] = "Compliant"
        elif compliance_results["compliance_score"] >= 60:
            compliance_results["overall_status"] = "Partially Compliant"
        else:
            compliance_results["overall_status"] = "Non-Compliant"
        
        # Generate recommendations
        compliance_results["recommendations"] = self._generate_compliance_recommendations(
            compliance_results["issues"],
            compliance_results["warnings"]
        )
        
        return compliance_results
    
    def _check_tds_compliance(self, financial_data: Dict) -> Dict:
        """Check TDS (Tax Deducted at Source) compliance"""
        result = {
            "check_name": "TDS Compliance",
            "status": "Compliant",
            "issues": [],
            "details": {}
        }
        
        # Check if TDS is being deducted on applicable payments
        operating_expenses = financial_data.get('operating_expenses', 0)
        
        # TDS should be deducted on professional fees, rent, etc.
        if operating_expenses > 500000:  # Threshold
            result["details"]["tds_applicable"] = True
            result["details"]["estimated_tds"] = operating_expenses * 0.10  # 10% TDS
            result["status"] = "Review Required"
            result["issues"].append({
                "severity": "Medium",
                "description": "Operating expenses exceed ₹5L. Ensure TDS is deducted on applicable payments.",
                "action": "Review TDS deductions on rent, professional fees, and contractor payments"
            })
        else:
            result["details"]["tds_applicable"] = False
        
        return result
    
    def _check_gst_compliance(self, financial_data: Dict) -> Dict:
        """Check GST compliance"""
        result = {
            "check_name": "GST Compliance",
            "status": "Compliant",
            "issues": [],
            "details": {}
        }
        
        revenue = financial_data.get('revenue', 0)
        
        # GST registration threshold
        gst_threshold = self.rules["gst"]["registration_threshold"]
        
        if revenue > gst_threshold:
            result["details"]["gst_registration_required"] = True
            result["details"]["estimated_gst_liability"] = revenue * 0.18  # Assuming 18% GST
            
            # Check if GST is being collected
            if not financial_data.get('gst_collected'):
                result["status"] = "Non-Compliant"
                result["issues"].append({
                    "severity": "High",
                    "description": f"Revenue exceeds GST threshold of ₹{gst_threshold:,.0f}. GST registration is mandatory.",
                    "action": "Register for GST immediately and start collecting GST on sales"
                })
        else:
            result["details"]["gst_registration_required"] = False
            result["details"]["threshold_remaining"] = gst_threshold - revenue
        
        return result
    
    def _check_income_tax_compliance(self, financial_data: Dict) -> Dict:
        """Check income tax compliance"""
        result = {
            "check_name": "Income Tax Compliance",
            "status": "Compliant",
            "issues": [],
            "details": {}
        }
        
        net_profit = financial_data.get('net_profit', 0)
        
        if net_profit > 0:
            # Calculate estimated tax liability
            tax_liability = self._calculate_tax_liability(net_profit)
            result["details"]["estimated_tax_liability"] = tax_liability
            result["details"]["effective_tax_rate"] = (tax_liability / net_profit * 100) if net_profit > 0 else 0
            
            # Check if advance tax should be paid
            if tax_liability > 10000:
                result["status"] = "Review Required"
                result["issues"].append({
                    "severity": "Medium",
                    "description": f"Estimated tax liability is ₹{tax_liability:,.0f}. Advance tax payment required.",
                    "action": "Pay advance tax in quarterly installments to avoid interest"
                })
        else:
            result["details"]["tax_liability"] = 0
            result["details"]["loss_carried_forward"] = abs(net_profit)
        
        return result
    
    def _check_filing_deadlines(self, financial_data: Dict) -> Dict:
        """Check upcoming filing deadlines"""
        result = {
            "check_name": "Filing Deadlines",
            "warnings": [],
            "upcoming_deadlines": []
        }
        
        current_date = datetime.now()
        
        # GST filing deadlines (monthly)
        gst_deadline = self._get_next_gst_deadline(current_date)
        days_to_gst = (gst_deadline - current_date).days
        
        if days_to_gst <= 7:
            result["warnings"].append({
                "severity": "High",
                "description": f"GST return filing due in {days_to_gst} days",
                "deadline": gst_deadline.strftime("%Y-%m-%d"),
                "action": "Prepare and file GSTR-3B immediately"
            })
        
        result["upcoming_deadlines"].append({
            "type": "GST Return (GSTR-3B)",
            "deadline": gst_deadline.strftime("%Y-%m-%d"),
            "days_remaining": days_to_gst
        })
        
        # Income tax return deadline (July 31)
        itr_deadline = datetime(current_date.year, 7, 31)
        if current_date.month > 7:
            itr_deadline = datetime(current_date.year + 1, 7, 31)
        
        days_to_itr = (itr_deadline - current_date).days
        
        if days_to_itr <= 30 and days_to_itr > 0:
            result["warnings"].append({
                "severity": "Medium",
                "description": f"Income Tax Return filing due in {days_to_itr} days",
                "deadline": itr_deadline.strftime("%Y-%m-%d"),
                "action": "Prepare financial statements and file ITR"
            })
        
        result["upcoming_deadlines"].append({
            "type": "Income Tax Return",
            "deadline": itr_deadline.strftime("%Y-%m-%d"),
            "days_remaining": days_to_itr
        })
        
        return result
    
    def _get_next_gst_deadline(self, current_date: datetime) -> datetime:
        """Get next GST filing deadline (20th of next month)"""
        if current_date.day <= 20:
            return datetime(current_date.year, current_date.month, 20)
        else:
            next_month = current_date.month + 1
            year = current_date.year
            if next_month > 12:
                next_month = 1
                year += 1
            return datetime(year, next_month, 20)
    
    def _calculate_tax_liability(self, net_profit: float) -> float:
        """Calculate estimated tax liability"""
        # Simplified calculation for companies (30% flat rate)
        # In reality, this would be more complex with slabs for individuals
        tax_rate = 0.30  # 30% for companies
        return net_profit * tax_rate
    
    def _generate_compliance_recommendations(self, issues: List[Dict], 
                                            warnings: List[Dict]) -> List[Dict]:
        """Generate actionable compliance recommendations"""
        recommendations = []
        
        # High priority issues
        high_priority = [i for i in issues if i.get("severity") == "High"]
        if high_priority:
            recommendations.append({
                "priority": "High",
                "title": "Address Critical Compliance Issues",
                "description": f"You have {len(high_priority)} critical compliance issue(s) that need immediate attention.",
                "actions": [issue["action"] for issue in high_priority]
            })
        
        # Medium priority issues
        medium_priority = [i for i in issues if i.get("severity") == "Medium"]
        if medium_priority:
            recommendations.append({
                "priority": "Medium",
                "title": "Review Tax Obligations",
                "description": f"You have {len(medium_priority)} tax obligation(s) to review.",
                "actions": [issue["action"] for issue in medium_priority]
            })
        
        # Upcoming deadlines
        if warnings:
            recommendations.append({
                "priority": "High",
                "title": "Upcoming Filing Deadlines",
                "description": f"You have {len(warnings)} upcoming deadline(s).",
                "actions": [warning["action"] for warning in warnings]
            })
        
        # General recommendations
        recommendations.append({
            "priority": "Low",
            "title": "Maintain Compliance Records",
            "description": "Keep all tax-related documents organized and accessible.",
            "actions": [
                "Maintain digital copies of all invoices",
                "Keep bank statements for at least 7 years",
                "Document all business expenses with receipts",
                "Maintain a tax calendar for deadlines"
            ]
        })
        
        return recommendations
    
    def validate_deductions(self, deductions: List[Dict]) -> Dict:
        """Validate tax deductions"""
        validation_results = {
            "total_deductions": 0,
            "valid_deductions": 0,
            "invalid_deductions": 0,
            "deduction_details": []
        }
        
        for deduction in deductions:
            section = deduction.get('section', '')
            amount = deduction.get('amount', 0)
            
            validation_results["total_deductions"] += amount
            
            # Validate against rules
            is_valid, message = self._validate_single_deduction(section, amount)
            
            validation_results["deduction_details"].append({
                "section": section,
                "amount": amount,
                "is_valid": is_valid,
                "message": message
            })
            
            if is_valid:
                validation_results["valid_deductions"] += amount
            else:
                validation_results["invalid_deductions"] += amount
        
        return validation_results
    
    def _validate_single_deduction(self, section: str, amount: float) -> tuple:
        """Validate a single deduction"""
        deduction_rules = self.rules["income_tax"]["deductions"]
        
        if section not in deduction_rules:
            return False, f"Unknown deduction section: {section}"
        
        rule = deduction_rules[section]
        limit = rule.get("limit")
        
        if limit and amount > limit:
            return False, f"Amount exceeds limit of ₹{limit:,.0f}"
        
        return True, f"Valid deduction under {section}"
    
    def assess_filing_readiness(self, financial_data: Dict, 
                               user_documents: List[str] = None) -> Dict:
        """Assess readiness for tax filing"""
        readiness = {
            "is_ready": True,
            "readiness_score": 100,
            "missing_items": [],
            "warnings": [],
            "checklist": []
        }
        
        # Required documents checklist
        required_docs = [
            "Financial Statements (P&L, Balance Sheet)",
            "Bank Statements",
            "GST Returns (if applicable)",
            "TDS Certificates",
            "Investment Proofs (for deductions)",
            "Previous Year Tax Return"
        ]
        
        for doc in required_docs:
            is_available = user_documents and doc in user_documents if user_documents else False
            readiness["checklist"].append({
                "item": doc,
                "status": "Available" if is_available else "Missing",
                "required": True
            })
            
            if not is_available:
                readiness["missing_items"].append(doc)
                readiness["readiness_score"] -= 15
        
        # Check data completeness
        required_fields = ['revenue', 'operating_expenses', 'net_profit']
        for field in required_fields:
            if field not in financial_data or financial_data[field] == 0:
                readiness["warnings"].append(f"Missing or zero value for {field}")
                readiness["readiness_score"] -= 10
        
        # Determine overall readiness
        if readiness["readiness_score"] >= 80:
            readiness["is_ready"] = True
            readiness["status"] = "Ready to File"
        elif readiness["readiness_score"] >= 60:
            readiness["is_ready"] = False
            readiness["status"] = "Almost Ready"
        else:
            readiness["is_ready"] = False
            readiness["status"] = "Not Ready"
        
        return readiness
    
    def identify_penalty_risks(self, financial_data: Dict, 
                              compliance_history: Dict = None) -> List[Dict]:
        """Identify potential penalty risks"""
        risks = []
        
        # Late filing risk
        if compliance_history and compliance_history.get('late_filings', 0) > 0:
            risks.append({
                "risk_type": "Late Filing Penalty",
                "severity": "High",
                "description": "History of late filings detected",
                "potential_penalty": "₹5,000 - ₹10,000 per return",
                "mitigation": "Set up filing reminders and automate where possible"
            })
        
        # Incorrect filing risk
        net_profit = financial_data.get('net_profit', 0)
        if net_profit < 0:
            risks.append({
                "risk_type": "Loss Reporting",
                "severity": "Medium",
                "description": "Business showing losses - ensure proper documentation",
                "potential_penalty": "Scrutiny and potential disallowance of losses",
                "mitigation": "Maintain detailed records of all expenses and business activities"
            })
        
        # GST non-compliance risk
        revenue = financial_data.get('revenue', 0)
        if revenue > 4000000 and not financial_data.get('gst_registered'):
            risks.append({
                "risk_type": "GST Non-Registration",
                "severity": "High",
                "description": "Revenue exceeds GST threshold but not registered",
                "potential_penalty": "10% of tax amount + interest",
                "mitigation": "Register for GST immediately"
            })
        
        # TDS non-deduction risk
        operating_expenses = financial_data.get('operating_expenses', 0)
        if operating_expenses > 500000:
            risks.append({
                "risk_type": "TDS Non-Deduction",
                "severity": "Medium",
                "description": "High operating expenses - ensure TDS compliance",
                "potential_penalty": "Interest @ 1% per month + disallowance of expense",
                "mitigation": "Review all payments and deduct TDS where applicable"
            })
        
        return risks
    
    def suggest_tax_optimizations(self, financial_data: Dict, 
                                  current_deductions: Dict = None) -> List[Dict]:
        """Suggest tax optimization strategies"""
        optimizations = []
        
        net_profit = financial_data.get('net_profit', 0)
        
        if net_profit > 0:
            # Suggest deductions
            optimizations.append({
                "strategy": "Maximize Section 80C Deductions",
                "potential_saving": min(net_profit * 0.30, 45000),  # 30% of ₹1.5L
                "description": "Invest in ELSS, PPF, or life insurance to save up to ₹45,000",
                "action": "Invest ₹1,50,000 in eligible instruments before March 31"
            })
            
            # Suggest business expenses
            optimizations.append({
                "strategy": "Claim All Business Expenses",
                "potential_saving": "Variable",
                "description": "Ensure all legitimate business expenses are claimed",
                "action": "Review and document: travel, meals, office supplies, software subscriptions"
            })
            
            # Suggest depreciation
            optimizations.append({
                "strategy": "Claim Depreciation on Assets",
                "potential_saving": "Variable",
                "description": "Claim depreciation on business assets like computers, furniture, vehicles",
                "action": "Maintain asset register and claim depreciation as per IT rules"
            })
        
        return optimizations
