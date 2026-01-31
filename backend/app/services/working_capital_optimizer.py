from scipy.optimize import minimize
import numpy as np
from typing import Dict, List, Tuple

class WorkingCapitalOptimizer:
    """Optimize working capital using mathematical optimization"""
    
    def __init__(self, financial_data: Dict):
        self.data = financial_data
        self.revenue = financial_data.get('revenue', 0)
        self.current_assets = financial_data.get('current_assets', 0)
        self.current_liabilities = financial_data.get('current_liabilities', 1)
        self.inventory = financial_data.get('inventory', 0)
        self.receivables_days = financial_data.get('receivables_days', 45)
        self.payables_days = financial_data.get('payables_days', 30)
        self.inventory_days = financial_data.get('inventory_days', 30)
    
    def optimize_working_capital(self) -> Dict:
        """Optimize working capital levels"""
        # Current working capital
        current_wc = self.current_assets - self.current_liabilities
        current_ccc = self.receivables_days + self.inventory_days - self.payables_days
        
        # Optimal targets
        optimal_results = self.calculate_optimal_levels()
        
        # Calculate improvements
        improvements = {
            "current_working_capital": current_wc,
            "optimal_working_capital": optimal_results["optimal_wc"],
            "potential_savings": current_wc - optimal_results["optimal_wc"],
            "current_ccc": current_ccc,
            "optimal_ccc": optimal_results["optimal_ccc"],
            "ccc_improvement": current_ccc - optimal_results["optimal_ccc"],
            "recommendations": optimal_results["recommendations"]
        }
        
        return improvements
    
    def calculate_optimal_levels(self) -> Dict:
        """Calculate optimal inventory, receivables, and payables levels"""
        daily_revenue = self.revenue / 365 if self.revenue > 0 else 0
        
        # Industry benchmarks for optimal levels
        optimal_receivables_days = 30  # Target: 30 days
        optimal_inventory_days = 20    # Target: 20 days
        optimal_payables_days = 45     # Target: 45 days (maximize)
        
        optimal_ccc = optimal_receivables_days + optimal_inventory_days - optimal_payables_days
        
        # Calculate optimal amounts
        optimal_receivables = daily_revenue * optimal_receivables_days
        optimal_inventory = daily_revenue * optimal_inventory_days * 0.7  # Assuming 70% COGS
        optimal_payables = daily_revenue * optimal_payables_days * 0.7
        
        optimal_current_assets = optimal_receivables + optimal_inventory + (self.current_assets - self.inventory - (daily_revenue * self.receivables_days))
        optimal_current_liabilities = optimal_payables + (self.current_liabilities - (daily_revenue * self.payables_days * 0.7))
        
        optimal_wc = optimal_current_assets - optimal_current_liabilities
        
        # Generate recommendations
        recommendations = []
        
        if self.receivables_days > optimal_receivables_days:
            days_to_reduce = self.receivables_days - optimal_receivables_days
            cash_to_free = daily_revenue * days_to_reduce
            recommendations.append({
                "area": "Receivables",
                "current": f"{self.receivables_days} days",
                "target": f"{optimal_receivables_days} days",
                "action": f"Reduce receivables collection period by {days_to_reduce} days",
                "impact": f"Free up ₹{cash_to_free:,.0f} in cash"
            })
        
        if self.inventory_days > optimal_inventory_days:
            days_to_reduce = self.inventory_days - optimal_inventory_days
            cash_to_free = daily_revenue * days_to_reduce * 0.7
            recommendations.append({
                "area": "Inventory",
                "current": f"{self.inventory_days} days",
                "target": f"{optimal_inventory_days} days",
                "action": f"Reduce inventory holding period by {days_to_reduce} days",
                "impact": f"Free up ₹{cash_to_free:,.0f} in cash"
            })
        
        if self.payables_days < optimal_payables_days:
            days_to_extend = optimal_payables_days - self.payables_days
            cash_to_retain = daily_revenue * days_to_extend * 0.7
            recommendations.append({
                "area": "Payables",
                "current": f"{self.payables_days} days",
                "target": f"{optimal_payables_days} days",
                "action": f"Negotiate to extend payment terms by {days_to_extend} days",
                "impact": f"Retain ₹{cash_to_retain:,.0f} in cash longer"
            })
        
        return {
            "optimal_wc": optimal_wc,
            "optimal_ccc": optimal_ccc,
            "optimal_receivables_days": optimal_receivables_days,
            "optimal_inventory_days": optimal_inventory_days,
            "optimal_payables_days": optimal_payables_days,
            "recommendations": recommendations
        }
    
    def sensitivity_analysis(self, variable: str, range_percent: float = 0.20) -> Dict:
        """Analyze sensitivity of working capital to changes in a variable"""
        base_value = getattr(self, variable, 0)
        
        # Create range of values (±20% by default)
        min_value = base_value * (1 - range_percent)
        max_value = base_value * (1 + range_percent)
        values = np.linspace(min_value, max_value, 11)
        
        results = []
        for value in values:
            # Temporarily set the variable
            original_value = getattr(self, variable)
            setattr(self, variable, value)
            
            # Calculate working capital
            wc = self.current_assets - self.current_liabilities
            ccc = self.receivables_days + self.inventory_days - self.payables_days
            
            results.append({
                "value": round(value, 2),
                "working_capital": round(wc, 2),
                "cash_conversion_cycle": round(ccc, 2),
                "change_percent": round((value - base_value) / base_value * 100, 2) if base_value > 0 else 0
            })
            
            # Restore original value
            setattr(self, variable, original_value)
        
        # Calculate sensitivity coefficient
        wc_changes = [r["working_capital"] for r in results]
        sensitivity = (max(wc_changes) - min(wc_changes)) / (max_value - min_value) if (max_value - min_value) > 0 else 0
        
        return {
            "variable": variable,
            "base_value": base_value,
            "sensitivity_coefficient": round(sensitivity, 4),
            "interpretation": self._interpret_sensitivity(sensitivity),
            "results": results
        }
    
    def _interpret_sensitivity(self, coefficient: float) -> str:
        """Interpret sensitivity coefficient"""
        if abs(coefficient) > 1.0:
            return "High sensitivity - Small changes have large impact"
        elif abs(coefficient) > 0.5:
            return "Moderate sensitivity - Changes have noticeable impact"
        else:
            return "Low sensitivity - Changes have minimal impact"
    
    def monte_carlo_simulation(self, iterations: int = 1000) -> Dict:
        """Run Monte Carlo simulation for working capital"""
        np.random.seed(42)  # For reproducibility
        
        # Define uncertainty ranges (±20% for each variable)
        receivables_range = (self.receivables_days * 0.8, self.receivables_days * 1.2)
        inventory_range = (self.inventory_days * 0.8, self.inventory_days * 1.2)
        payables_range = (self.payables_days * 0.8, self.payables_days * 1.2)
        
        wc_results = []
        ccc_results = []
        
        for _ in range(iterations):
            # Random values within ranges
            rec_days = np.random.uniform(*receivables_range)
            inv_days = np.random.uniform(*inventory_range)
            pay_days = np.random.uniform(*payables_range)
            
            # Calculate CCC
            ccc = rec_days + inv_days - pay_days
            ccc_results.append(ccc)
            
            # Estimate WC impact (simplified)
            daily_revenue = self.revenue / 365 if self.revenue > 0 else 0
            wc = (rec_days + inv_days - pay_days) * daily_revenue * 0.7
            wc_results.append(wc)
        
        # Calculate statistics
        wc_array = np.array(wc_results)
        ccc_array = np.array(ccc_results)
        
        return {
            "iterations": iterations,
            "working_capital": {
                "mean": round(np.mean(wc_array), 2),
                "std_dev": round(np.std(wc_array), 2),
                "min": round(np.min(wc_array), 2),
                "max": round(np.max(wc_array), 2),
                "percentile_5": round(np.percentile(wc_array, 5), 2),
                "percentile_95": round(np.percentile(wc_array, 95), 2)
            },
            "cash_conversion_cycle": {
                "mean": round(np.mean(ccc_array), 2),
                "std_dev": round(np.std(ccc_array), 2),
                "min": round(np.min(ccc_array), 2),
                "max": round(np.max(ccc_array), 2),
                "percentile_5": round(np.percentile(ccc_array, 5), 2),
                "percentile_95": round(np.percentile(ccc_array, 95), 2)
            },
            "risk_assessment": self._assess_risk(wc_array, ccc_array)
        }
    
    def _assess_risk(self, wc_array: np.ndarray, ccc_array: np.ndarray) -> Dict:
        """Assess risk based on simulation results"""
        wc_volatility = np.std(wc_array) / np.mean(wc_array) if np.mean(wc_array) > 0 else 0
        ccc_volatility = np.std(ccc_array) / np.mean(ccc_array) if np.mean(ccc_array) > 0 else 0
        
        if wc_volatility > 0.3 or ccc_volatility > 0.3:
            risk_level = "High"
            recommendation = "High variability detected. Focus on stabilizing working capital components."
        elif wc_volatility > 0.15 or ccc_volatility > 0.15:
            risk_level = "Medium"
            recommendation = "Moderate variability. Monitor working capital closely."
        else:
            risk_level = "Low"
            recommendation = "Working capital is relatively stable."
        
        return {
            "risk_level": risk_level,
            "wc_volatility": round(wc_volatility, 4),
            "ccc_volatility": round(ccc_volatility, 4),
            "recommendation": recommendation
        }


class ScenarioModeler:
    """Model different working capital scenarios"""
    
    def __init__(self, base_data: Dict):
        self.base_data = base_data
    
    def create_scenario(self, changes: Dict) -> Dict:
        """Create a scenario with specified changes"""
        scenario_data = self.base_data.copy()
        scenario_data.update(changes)
        
        # Calculate metrics for this scenario
        optimizer = WorkingCapitalOptimizer(scenario_data)
        results = optimizer.optimize_working_capital()
        
        return {
            "scenario_name": changes.get('name', 'Custom Scenario'),
            "changes": changes,
            "results": results
        }
    
    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """Compare multiple scenarios"""
        comparison = {
            "scenarios": [],
            "best_scenario": None,
            "worst_scenario": None
        }
        
        best_wc = float('inf')
        worst_wc = 0
        
        for scenario in scenarios:
            scenario_result = self.create_scenario(scenario)
            comparison["scenarios"].append(scenario_result)
            
            wc = scenario_result["results"]["optimal_working_capital"]
            if wc < best_wc:
                best_wc = wc
                comparison["best_scenario"] = scenario_result["scenario_name"]
            if wc > worst_wc:
                worst_wc = wc
                comparison["worst_scenario"] = scenario_result["scenario_name"]
        
        return comparison
    
    def what_if_analysis(self, variable: str, values: List[float]) -> Dict:
        """Perform what-if analysis for a variable"""
        results = []
        
        for value in values:
            changes = {variable: value, 'name': f'{variable}={value}'}
            scenario = self.create_scenario(changes)
            results.append({
                "value": value,
                "working_capital": scenario["results"]["optimal_working_capital"],
                "ccc": scenario["results"]["optimal_ccc"]
            })
        
        return {
            "variable": variable,
            "analysis": results,
            "recommendation": self._generate_what_if_recommendation(results)
        }
    
    def _generate_what_if_recommendation(self, results: List[Dict]) -> str:
        """Generate recommendation from what-if analysis"""
        wc_values = [r["working_capital"] for r in results]
        best_idx = wc_values.index(min(wc_values))
        
        return f"Optimal value: {results[best_idx]['value']} (Working Capital: ₹{results[best_idx]['working_capital']:,.0f})"
