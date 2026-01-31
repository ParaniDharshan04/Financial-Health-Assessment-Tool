import pandas as pd
import numpy as np
from typing import Dict, Tuple

class FinancialAnalyzer:
    """Core financial intelligence engine for SME analysis"""
    
    # Weights for health score calculation
    WEIGHTS = {
        'liquidity': 0.30,
        'profitability': 0.25,
        'cash_flow': 0.25,
        'debt_health': 0.20
    }
    
    def __init__(self, financial_data: Dict):
        self.data = financial_data
        self.metrics = {}
    
    def calculate_liquidity_metrics(self) -> Dict:
        """Calculate liquidity ratios"""
        current_assets = self.data.get('current_assets', 0)
        current_liabilities = self.data.get('current_liabilities', 1)
        inventory = self.data.get('inventory', 0)
        cash = self.data.get('cash', 0)
        
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0
        cash_ratio = cash / current_liabilities if current_liabilities > 0 else 0
        
        return {
            'current_ratio': round(current_ratio, 2),
            'quick_ratio': round(quick_ratio, 2),
            'cash_ratio': round(cash_ratio, 2)
        }
    
    def calculate_profitability_metrics(self) -> Dict:
        """Calculate profitability ratios"""
        revenue = self.data.get('revenue', 1)
        gross_profit = self.data.get('gross_profit', 0)
        net_profit = self.data.get('net_profit', 0)
        operating_profit = self.data.get('operating_profit', 0)
        total_assets = self.data.get('total_assets', 1)
        equity = self.data.get('equity', 1)
        
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        net_margin = (net_profit / revenue * 100) if revenue > 0 else 0
        operating_margin = (operating_profit / revenue * 100) if revenue > 0 else 0
        roa = (net_profit / total_assets * 100) if total_assets > 0 else 0
        roe = (net_profit / equity * 100) if equity > 0 else 0
        
        return {
            'gross_profit_margin': round(gross_margin, 2),
            'net_profit_margin': round(net_margin, 2),
            'operating_margin': round(operating_margin, 2),
            'return_on_assets': round(roa, 2),
            'return_on_equity': round(roe, 2)
        }
    
    def calculate_cash_flow_metrics(self) -> Dict:
        """Calculate cash flow metrics"""
        operating_cash_flow = self.data.get('operating_cash_flow', 0)
        revenue = self.data.get('revenue', 1)
        current_liabilities = self.data.get('current_liabilities', 1)
        
        cash_flow_margin = (operating_cash_flow / revenue * 100) if revenue > 0 else 0
        cash_flow_coverage = operating_cash_flow / current_liabilities if current_liabilities > 0 else 0
        
        # Calculate cash conversion cycle
        receivables_days = self.data.get('receivables_days', 45)
        payables_days = self.data.get('payables_days', 30)
        inventory_days = self.data.get('inventory_days', 30)
        cash_conversion_cycle = receivables_days + inventory_days - payables_days
        
        return {
            'operating_cash_flow': round(operating_cash_flow, 2),
            'cash_flow_margin': round(cash_flow_margin, 2),
            'cash_flow_coverage': round(cash_flow_coverage, 2),
            'cash_conversion_cycle': round(cash_conversion_cycle, 2)
        }
    
    def calculate_debt_metrics(self) -> Dict:
        """Calculate debt and solvency ratios"""
        total_debt = self.data.get('total_debt', 0)
        equity = self.data.get('equity', 1)
        total_assets = self.data.get('total_assets', 1)
        ebit = self.data.get('ebit', 0)
        interest_expense = self.data.get('interest_expense', 1)
        
        debt_to_equity = total_debt / equity if equity > 0 else 0
        debt_to_assets = (total_debt / total_assets * 100) if total_assets > 0 else 0
        interest_coverage = ebit / interest_expense if interest_expense > 0 else 0
        
        return {
            'debt_to_equity': round(debt_to_equity, 2),
            'debt_to_assets': round(debt_to_assets, 2),
            'interest_coverage': round(interest_coverage, 2),
            'total_debt': round(total_debt, 2)
        }
    
    def score_liquidity(self, metrics: Dict) -> float:
        """Score liquidity health (0-100)"""
        current_ratio = metrics.get('current_ratio', 0)
        quick_ratio = metrics.get('quick_ratio', 0)
        
        # Ideal current ratio: 1.5-2.0, quick ratio: 1.0-1.5
        cr_score = min(100, (current_ratio / 2.0) * 100) if current_ratio <= 2.0 else max(0, 100 - (current_ratio - 2.0) * 20)
        qr_score = min(100, (quick_ratio / 1.5) * 100) if quick_ratio <= 1.5 else max(0, 100 - (quick_ratio - 1.5) * 20)
        
        return round((cr_score * 0.6 + qr_score * 0.4), 2)
    
    def score_profitability(self, metrics: Dict) -> float:
        """Score profitability health (0-100)"""
        net_margin = metrics.get('net_profit_margin', 0)
        gross_margin = metrics.get('gross_profit_margin', 0)
        
        # Scoring based on typical SME benchmarks
        nm_score = min(100, max(0, (net_margin + 5) * 10))  # -5% to 10% range
        gm_score = min(100, max(0, gross_margin * 2))  # 0% to 50% range
        
        return round((nm_score * 0.6 + gm_score * 0.4), 2)
    
    def score_cash_flow(self, metrics: Dict) -> float:
        """Score cash flow health (0-100)"""
        cf_margin = metrics.get('cash_flow_margin', 0)
        cf_coverage = metrics.get('cash_flow_coverage', 0)
        ccc = metrics.get('cash_conversion_cycle', 90)
        
        cfm_score = min(100, max(0, (cf_margin + 5) * 10))
        cfc_score = min(100, cf_coverage * 50)
        ccc_score = max(0, 100 - (ccc / 90) * 100)  # Lower is better
        
        return round((cfm_score * 0.4 + cfc_score * 0.3 + ccc_score * 0.3), 2)
    
    def score_debt_health(self, metrics: Dict) -> float:
        """Score debt health (0-100)"""
        dte = metrics.get('debt_to_equity', 0)
        dta = metrics.get('debt_to_assets', 0)
        ic = metrics.get('interest_coverage', 0)
        
        # Lower debt ratios are better
        dte_score = max(0, 100 - (dte * 50))  # Ideal < 2.0
        dta_score = max(0, 100 - dta)  # Ideal < 50%
        ic_score = min(100, ic * 20)  # Ideal > 5
        
        return round((dte_score * 0.3 + dta_score * 0.3 + ic_score * 0.4), 2)
    
    def calculate_health_score(self) -> Tuple[float, str, Dict]:
        """Calculate overall financial health score and risk band"""
        # Calculate all metrics
        liquidity_metrics = self.calculate_liquidity_metrics()
        profitability_metrics = self.calculate_profitability_metrics()
        cash_flow_metrics = self.calculate_cash_flow_metrics()
        debt_metrics = self.calculate_debt_metrics()
        
        # Combine all metrics
        all_metrics = {
            **liquidity_metrics,
            **profitability_metrics,
            **cash_flow_metrics,
            **debt_metrics
        }
        
        # Calculate component scores
        liquidity_score = self.score_liquidity(liquidity_metrics)
        profitability_score = self.score_profitability(profitability_metrics)
        cash_flow_score = self.score_cash_flow(cash_flow_metrics)
        debt_health_score = self.score_debt_health(debt_metrics)
        
        # Calculate weighted health score
        health_score = (
            liquidity_score * self.WEIGHTS['liquidity'] +
            profitability_score * self.WEIGHTS['profitability'] +
            cash_flow_score * self.WEIGHTS['cash_flow'] +
            debt_health_score * self.WEIGHTS['debt_health']
        )
        
        # Determine risk band
        if health_score >= 70:
            risk_band = "Safe"
        elif health_score >= 40:
            risk_band = "Watch"
        else:
            risk_band = "Critical"
        
        scores = {
            'liquidity_score': liquidity_score,
            'profitability_score': profitability_score,
            'cash_flow_score': cash_flow_score,
            'debt_health_score': debt_health_score
        }
        
        return round(health_score, 2), risk_band, all_metrics, scores
