from typing import Dict, List

class CreditAssessment:
    """Assess credit readiness and recommend financing options"""
    
    # Mock financing products
    FINANCING_OPTIONS = [
        {
            'id': 1,
            'provider': 'ABC Bank',
            'product': 'Working Capital Loan',
            'type': 'working_capital',
            'min_score': 60,
            'interest_rate': '10-12%',
            'max_amount': 5000000,
            'tenure': '12-36 months',
            'features': ['Quick disbursement', 'Flexible repayment', 'No collateral up to 2L']
        },
        {
            'id': 2,
            'provider': 'XYZ NBFC',
            'product': 'Business Term Loan',
            'type': 'term_loan',
            'min_score': 50,
            'interest_rate': '12-15%',
            'max_amount': 10000000,
            'tenure': '24-60 months',
            'features': ['Longer tenure', 'Fixed interest rate', 'Business expansion']
        },
        {
            'id': 3,
            'provider': 'QuickFin',
            'product': 'Invoice Financing',
            'type': 'invoice_financing',
            'min_score': 55,
            'interest_rate': '1-2% per month',
            'max_amount': 2000000,
            'tenure': '30-90 days',
            'features': ['Instant liquidity', 'Based on receivables', 'No fixed EMI']
        },
        {
            'id': 4,
            'provider': 'Growth Capital',
            'product': 'Equipment Financing',
            'type': 'equipment_loan',
            'min_score': 65,
            'interest_rate': '11-13%',
            'max_amount': 7500000,
            'tenure': '36-60 months',
            'features': ['Asset-backed', 'Tax benefits', 'Up to 90% funding']
        },
        {
            'id': 5,
            'provider': 'SME Finance Co',
            'product': 'Emergency Credit Line',
            'type': 'credit_line',
            'min_score': 40,
            'interest_rate': '14-18%',
            'max_amount': 1000000,
            'tenure': '6-12 months',
            'features': ['Quick approval', 'Emergency funding', 'Minimal documentation']
        }
    ]
    
    def __init__(self, health_score: float, metrics: Dict, cash_flow_data: Dict):
        self.health_score = health_score
        self.metrics = metrics
        self.cash_flow_data = cash_flow_data
    
    def assess_credit_readiness(self) -> Dict:
        """Assess overall credit readiness"""
        
        # Calculate credit score components
        score_component = min(40, (self.health_score / 100) * 40)
        
        # Debt servicing capacity
        interest_coverage = self.metrics.get('interest_coverage', 0)
        debt_capacity = min(25, (interest_coverage / 5) * 25) if interest_coverage > 0 else 0
        
        # Cash flow stability
        cf_margin = self.metrics.get('cash_flow_margin', 0)
        cash_flow_component = min(20, max(0, (cf_margin + 5) * 2))
        
        # Profitability
        net_margin = self.metrics.get('net_profit_margin', 0)
        profitability_component = min(15, max(0, (net_margin + 5) * 1.5))
        
        # Calculate overall credit readiness score
        credit_score = score_component + debt_capacity + cash_flow_component + profitability_component
        
        # Determine readiness level
        if credit_score >= 75:
            readiness = 'Excellent'
            description = 'Strong credit profile. Eligible for premium financing options with favorable terms.'
        elif credit_score >= 60:
            readiness = 'Good'
            description = 'Solid credit profile. Eligible for most financing options with competitive rates.'
        elif credit_score >= 45:
            readiness = 'Fair'
            description = 'Moderate credit profile. Some financing options available, may need to improve metrics.'
        else:
            readiness = 'Poor'
            description = 'Weak credit profile. Limited options available. Focus on improving financial health first.'
        
        return {
            'credit_readiness_score': round(credit_score, 2),
            'readiness_level': readiness,
            'description': description,
            'components': {
                'financial_health': round(score_component, 2),
                'debt_capacity': round(debt_capacity, 2),
                'cash_flow_stability': round(cash_flow_component, 2),
                'profitability': round(profitability_component, 2)
            }
        }
    
    def recommend_financing(self) -> List[Dict]:
        """Recommend suitable financing options"""
        
        credit_assessment = self.assess_credit_readiness()
        credit_score = credit_assessment['credit_readiness_score']
        
        # Filter suitable options
        suitable_options = []
        for option in self.FINANCING_OPTIONS:
            if credit_score >= option['min_score']:
                # Calculate suitability score
                suitability = self._calculate_suitability(option)
                suitable_options.append({
                    **option,
                    'suitability_score': suitability,
                    'recommended': suitability >= 70
                })
        
        # Sort by suitability
        suitable_options.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return suitable_options[:4]  # Return top 4
    
    def _calculate_suitability(self, option: Dict) -> float:
        """Calculate how suitable a financing option is"""
        
        base_score = 50
        
        # Score based on credit readiness
        if self.health_score >= option['min_score'] + 20:
            base_score += 30
        elif self.health_score >= option['min_score'] + 10:
            base_score += 20
        elif self.health_score >= option['min_score']:
            base_score += 10
        
        # Adjust based on business needs
        current_ratio = self.metrics.get('current_ratio', 0)
        if option['type'] == 'working_capital' and current_ratio < 1.5:
            base_score += 20
        elif option['type'] == 'invoice_financing' and self.metrics.get('receivables_days', 0) > 45:
            base_score += 15
        elif option['type'] == 'credit_line' and self.health_score < 50:
            base_score += 10
        
        return min(100, base_score)
    
    def get_full_assessment(self) -> Dict:
        """Get complete credit assessment with recommendations"""
        
        readiness = self.assess_credit_readiness()
        financing_options = self.recommend_financing()
        
        return {
            'credit_readiness': readiness,
            'recommended_financing': financing_options,
            'next_steps': self._get_next_steps(readiness['readiness_level'])
        }
    
    def _get_next_steps(self, readiness_level: str) -> List[str]:
        """Get recommended next steps based on readiness"""
        
        if readiness_level == 'Excellent':
            return [
                'Compare financing options and negotiate terms',
                'Prepare required documentation',
                'Consider multiple lenders for best rates'
            ]
        elif readiness_level == 'Good':
            return [
                'Review financing options carefully',
                'Prepare financial statements and business plan',
                'Consider improving metrics for better terms'
            ]
        elif readiness_level == 'Fair':
            return [
                'Focus on improving cash flow and profitability',
                'Reduce debt levels if possible',
                'Consider alternative financing options',
                'Build relationship with potential lenders'
            ]
        else:
            return [
                'Prioritize improving financial health',
                'Implement cost reduction strategies',
                'Improve cash flow management',
                'Delay financing until metrics improve'
            ]
