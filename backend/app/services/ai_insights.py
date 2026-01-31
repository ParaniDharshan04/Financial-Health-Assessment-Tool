import google.generativeai as genai
from typing import Dict, List
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIInsightsGenerator:
    """Generate AI-powered insights using Google Gemini"""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_insights(self, health_score: float, risk_band: str, metrics: Dict, scores: Dict) -> Dict:
        """Generate comprehensive AI insights"""
        
        prompt = self._build_insights_prompt(health_score, risk_band, metrics, scores)
        
        try:
            response = self.model.generate_content(prompt)
            insights_text = response.text
            return self._parse_insights(insights_text)
            
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return self._get_fallback_insights(health_score, risk_band, metrics)
    
    def generate_recommendations(self, health_score: float, metrics: Dict, scores: Dict) -> List[Dict]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Liquidity recommendations
        if scores.get('liquidity_score', 0) < 60:
            current_ratio = metrics.get('current_ratio', 0)
            if current_ratio < 1.0:
                recommendations.append({
                    'category': 'Liquidity',
                    'priority': 'High',
                    'title': 'Improve Current Ratio',
                    'description': f'Your current ratio is {current_ratio}, indicating potential liquidity issues. Consider reducing short-term liabilities or increasing liquid assets.',
                    'impact': 'High',
                    'actions': [
                        'Accelerate receivables collection',
                        'Negotiate extended payment terms with suppliers',
                        'Consider short-term financing options'
                    ]
                })
        
        # Profitability recommendations
        if scores.get('profitability_score', 0) < 60:
            net_margin = metrics.get('net_profit_margin', 0)
            if net_margin < 5:
                recommendations.append({
                    'category': 'Profitability',
                    'priority': 'High',
                    'title': 'Increase Profit Margins',
                    'description': f'Net profit margin of {net_margin}% is below healthy levels. Focus on cost optimization and revenue enhancement.',
                    'impact': 'High',
                    'actions': [
                        'Review and reduce operating expenses',
                        'Optimize pricing strategy',
                        'Improve operational efficiency',
                        'Focus on high-margin products/services'
                    ]
                })
        
        # Cash flow recommendations
        if scores.get('cash_flow_score', 0) < 60:
            ccc = metrics.get('cash_conversion_cycle', 0)
            if ccc > 60:
                recommendations.append({
                    'category': 'Cash Flow',
                    'priority': 'Medium',
                    'title': 'Optimize Cash Conversion Cycle',
                    'description': f'Cash conversion cycle of {ccc} days is high. Faster conversion improves working capital.',
                    'impact': 'Medium',
                    'actions': [
                        'Implement stricter credit policies',
                        'Offer early payment discounts',
                        'Optimize inventory management',
                        'Negotiate better payment terms'
                    ]
                })
        
        # Debt recommendations
        if scores.get('debt_health_score', 0) < 60:
            dte = metrics.get('debt_to_equity', 0)
            if dte > 2.0:
                recommendations.append({
                    'category': 'Debt Management',
                    'priority': 'High',
                    'title': 'Reduce Debt Burden',
                    'description': f'Debt-to-equity ratio of {dte} indicates high leverage. Consider debt reduction strategies.',
                    'impact': 'High',
                    'actions': [
                        'Prioritize debt repayment',
                        'Consider debt restructuring',
                        'Avoid taking on new debt',
                        'Explore equity financing options'
                    ]
                })
        
        # Working capital recommendation
        if health_score < 70:
            recommendations.append({
                'category': 'Working Capital',
                'priority': 'Medium',
                'title': 'Strengthen Working Capital Position',
                'description': 'Improve overall working capital management to enhance financial stability.',
                'impact': 'Medium',
                'actions': [
                    'Monitor cash flow daily',
                    'Maintain adequate cash reserves',
                    'Implement cash flow forecasting',
                    'Review all recurring expenses'
                ]
            })
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations[:5]  # Return top 5
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for AI"""
        if self.language == "hi":
            return """आप एक विशेषज्ञ वित्तीय सलाहकार हैं जो छोटे और मध्यम व्यवसायों (SME) की मदद करते हैं। 
            आपका काम जटिल वित्तीय डेटा को सरल, स्पष्ट भाषा में समझाना है जो व्यवसाय के मालिक समझ सकें।"""
        else:
            return """You are an expert financial advisor specializing in small and medium enterprises (SMEs). 
            Your role is to translate complex financial data into simple, clear language that business owners can understand. 
            Focus on practical insights, identify strengths and weaknesses, and provide actionable guidance."""
    
    def _build_insights_prompt(self, health_score: float, risk_band: str, metrics: Dict, scores: Dict) -> str:
        """Build prompt for insights generation"""
        
        system_prompt = self._get_system_prompt()
        
        user_prompt = f"""
Analyze this SME's financial health and provide clear insights:

Financial Health Score: {health_score}/100 ({risk_band})

Component Scores:
- Liquidity: {scores.get('liquidity_score', 0)}/100
- Profitability: {scores.get('profitability_score', 0)}/100
- Cash Flow: {scores.get('cash_flow_score', 0)}/100
- Debt Health: {scores.get('debt_health_score', 0)}/100

Key Metrics:
- Current Ratio: {metrics.get('current_ratio', 0)}
- Net Profit Margin: {metrics.get('net_profit_margin', 0)}%
- Cash Flow Margin: {metrics.get('cash_flow_margin', 0)}%
- Debt-to-Equity: {metrics.get('debt_to_equity', 0)}

Provide:
1. Overall Assessment (2-3 sentences)
2. Key Strengths (2-3 points)
3. Key Weaknesses (2-3 points)
4. Critical Risks (if any)
5. Immediate Actions (2-3 priorities)

Keep language simple and non-technical. Focus on what matters to business owners.
"""
        
        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        return full_prompt
    
    def _parse_insights(self, insights_text: str) -> Dict:
        """Parse AI response into structured format"""
        return {
            'summary': insights_text,
            'generated_by': 'AI',
            'language': self.language
        }
    
    def _get_fallback_insights(self, health_score: float, risk_band: str, metrics: Dict) -> Dict:
        """Fallback insights if AI fails"""
        if risk_band == "Safe":
            summary = f"Your business shows strong financial health with a score of {health_score}/100. Key strengths include solid liquidity and manageable debt levels. Continue monitoring cash flow and maintain current financial discipline."
        elif risk_band == "Watch":
            summary = f"Your business has moderate financial health with a score of {health_score}/100. Some areas need attention, particularly around profitability or cash flow management. Implement recommended actions to improve stability."
        else:
            summary = f"Your business faces financial challenges with a score of {health_score}/100. Immediate action is needed to address liquidity, profitability, or debt concerns. Prioritize the high-impact recommendations provided."
        
        return {
            'summary': summary,
            'generated_by': 'System',
            'language': self.language
        }
