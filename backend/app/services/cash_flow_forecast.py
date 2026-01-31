import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

class CashFlowForecaster:
    """Forecast cash flow for next 6 months"""
    
    def __init__(self, historical_data: Dict):
        self.historical_data = historical_data
    
    def forecast(self) -> Dict:
        """Generate 6-month cash flow forecast"""
        
        # Extract historical cash flow data
        historical_cf = self.historical_data.get('monthly_cash_flow', [])
        
        if not historical_cf or len(historical_cf) < 3:
            # Use simple projection if insufficient data
            return self._simple_forecast()
        
        # Calculate trend and seasonality
        forecast_months = []
        current_date = datetime.now()
        
        # Calculate average and trend
        values = [month['net_cash_flow'] for month in historical_cf[-6:]]
        avg_cf = np.mean(values)
        trend = np.polyfit(range(len(values)), values, 1)[0] if len(values) > 1 else 0
        
        # Generate forecast
        for i in range(6):
            forecast_date = current_date + timedelta(days=30 * (i + 1))
            
            # Simple linear projection with some randomness
            projected_cf = avg_cf + (trend * (len(values) + i))
            
            # Add confidence intervals
            std_dev = np.std(values) if len(values) > 1 else abs(avg_cf * 0.2)
            
            forecast_months.append({
                'month': forecast_date.strftime('%B %Y'),
                'projected_cash_flow': round(projected_cf, 2),
                'lower_bound': round(projected_cf - std_dev, 2),
                'upper_bound': round(projected_cf + std_dev, 2),
                'confidence': 'Medium' if i < 3 else 'Low'
            })
        
        # Identify risks
        risks = self._identify_risks(forecast_months)
        
        return {
            'forecast_period': '6 months',
            'forecast': forecast_months,
            'trend': 'Improving' if trend > 0 else 'Declining' if trend < 0 else 'Stable',
            'average_projected_cf': round(np.mean([m['projected_cash_flow'] for m in forecast_months]), 2),
            'risks': risks,
            'recommendations': self._get_forecast_recommendations(forecast_months, risks)
        }
    
    def _simple_forecast(self) -> Dict:
        """Simple forecast when historical data is limited"""
        
        current_cf = self.historical_data.get('operating_cash_flow', 0)
        revenue = self.historical_data.get('revenue', 0)
        monthly_cf = current_cf / 12 if current_cf else revenue * 0.1 / 12
        
        forecast_months = []
        current_date = datetime.now()
        
        for i in range(6):
            forecast_date = current_date + timedelta(days=30 * (i + 1))
            
            # Add slight variation
            variation = np.random.uniform(-0.1, 0.1)
            projected = monthly_cf * (1 + variation)
            
            forecast_months.append({
                'month': forecast_date.strftime('%B %Y'),
                'projected_cash_flow': round(projected, 2),
                'lower_bound': round(projected * 0.8, 2),
                'upper_bound': round(projected * 1.2, 2),
                'confidence': 'Low'
            })
        
        return {
            'forecast_period': '6 months',
            'forecast': forecast_months,
            'trend': 'Stable',
            'average_projected_cf': round(monthly_cf, 2),
            'risks': [],
            'recommendations': ['Collect more historical data for accurate forecasting'],
            'note': 'Limited historical data - forecast based on current metrics'
        }
    
    def _identify_risks(self, forecast_months: List[Dict]) -> List[Dict]:
        """Identify potential cash flow risks"""
        
        risks = []
        
        # Check for negative cash flow
        negative_months = [m for m in forecast_months if m['projected_cash_flow'] < 0]
        if negative_months:
            risks.append({
                'type': 'Negative Cash Flow',
                'severity': 'High',
                'description': f'Projected negative cash flow in {len(negative_months)} month(s)',
                'months_affected': [m['month'] for m in negative_months]
            })
        
        # Check for declining trend
        values = [m['projected_cash_flow'] for m in forecast_months]
        if len(values) >= 3:
            recent_trend = values[-1] - values[0]
            if recent_trend < -values[0] * 0.2:  # 20% decline
                risks.append({
                    'type': 'Declining Trend',
                    'severity': 'Medium',
                    'description': 'Cash flow showing declining trend over forecast period'
                })
        
        # Check for high volatility
        if len(values) >= 3:
            std_dev = np.std(values)
            mean_val = np.mean(values)
            if mean_val != 0 and (std_dev / abs(mean_val)) > 0.3:  # CV > 30%
                risks.append({
                    'type': 'High Volatility',
                    'severity': 'Medium',
                    'description': 'High variability in projected cash flows indicates uncertainty'
                })
        
        # Check for low cash flow
        avg_cf = np.mean(values)
        if avg_cf < 50000 and avg_cf > 0:  # Arbitrary threshold
            risks.append({
                'type': 'Low Cash Flow',
                'severity': 'Medium',
                'description': 'Projected cash flow levels are low, limiting financial flexibility'
            })
        
        return risks
    
    def _get_forecast_recommendations(self, forecast_months: List[Dict], risks: List[Dict]) -> List[str]:
        """Get recommendations based on forecast"""
        
        recommendations = []
        
        if any(r['type'] == 'Negative Cash Flow' for r in risks):
            recommendations.append('Urgent: Arrange additional financing or credit line')
            recommendations.append('Accelerate receivables collection')
            recommendations.append('Defer non-essential expenses')
        
        if any(r['type'] == 'Declining Trend' for r in risks):
            recommendations.append('Review and optimize operating expenses')
            recommendations.append('Focus on revenue generation activities')
            recommendations.append('Improve working capital management')
        
        if any(r['type'] == 'High Volatility' for r in risks):
            recommendations.append('Build cash reserves for uncertain periods')
            recommendations.append('Implement more frequent cash flow monitoring')
            recommendations.append('Diversify revenue streams')
        
        if not recommendations:
            recommendations.append('Maintain current cash flow management practices')
            recommendations.append('Continue monitoring monthly performance')
            recommendations.append('Build emergency cash reserves')
        
        return recommendations[:5]
