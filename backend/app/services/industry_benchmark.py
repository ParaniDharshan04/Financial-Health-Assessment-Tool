from typing import Dict

class IndustryBenchmark:
    """Industry benchmarking service with static data"""
    
    # Static industry benchmarks (can be expanded)
    BENCHMARKS = {
        'retail': {
            'name': 'Retail',
            'gross_margin': 30.0,
            'net_margin': 5.0,
            'current_ratio': 1.5,
            'debt_to_equity': 1.2,
            'cash_conversion_cycle': 45,
            'inventory_turnover': 8.0
        },
        'manufacturing': {
            'name': 'Manufacturing',
            'gross_margin': 35.0,
            'net_margin': 8.0,
            'current_ratio': 1.8,
            'debt_to_equity': 1.5,
            'cash_conversion_cycle': 60,
            'inventory_turnover': 6.0
        },
        'services': {
            'name': 'Services',
            'gross_margin': 50.0,
            'net_margin': 12.0,
            'current_ratio': 1.3,
            'debt_to_equity': 0.8,
            'cash_conversion_cycle': 30,
            'inventory_turnover': 0
        },
        'technology': {
            'name': 'Technology',
            'gross_margin': 60.0,
            'net_margin': 15.0,
            'current_ratio': 2.0,
            'debt_to_equity': 0.5,
            'cash_conversion_cycle': 40,
            'inventory_turnover': 12.0
        },
        'hospitality': {
            'name': 'Hospitality',
            'gross_margin': 40.0,
            'net_margin': 6.0,
            'current_ratio': 1.2,
            'debt_to_equity': 1.8,
            'cash_conversion_cycle': 20,
            'inventory_turnover': 15.0
        },
        'agriculture': {
            'name': 'Agriculture',
            'gross_margin': 25.0,
            'net_margin': 10.0,
            'current_ratio': 1.4,
            'debt_to_equity': 1.3,
            'cash_conversion_cycle': 90,
            'inventory_turnover': 4.0
        },
        'logistics': {
            'name': 'Logistics',
            'gross_margin': 20.0,
            'net_margin': 5.0,
            'current_ratio': 1.3,
            'debt_to_equity': 1.6,
            'cash_conversion_cycle': 35,
            'inventory_turnover': 10.0
        },
        'ecommerce': {
            'name': 'E-commerce',
            'gross_margin': 45.0,
            'net_margin': 8.0,
            'current_ratio': 1.6,
            'debt_to_equity': 1.0,
            'cash_conversion_cycle': 25,
            'inventory_turnover': 12.0
        }
    }
    
    def __init__(self, industry: str):
        self.industry = industry.lower() if industry else 'services'
        self.benchmark = self.BENCHMARKS.get(self.industry, self.BENCHMARKS['services'])
    
    def compare(self, metrics: Dict) -> Dict:
        """Compare company metrics against industry benchmarks"""
        
        comparisons = {}
        
        # Gross margin comparison
        company_gm = metrics.get('gross_profit_margin', 0)
        benchmark_gm = self.benchmark['gross_margin']
        comparisons['gross_margin'] = {
            'company': company_gm,
            'industry': benchmark_gm,
            'difference': round(company_gm - benchmark_gm, 2),
            'performance': 'Above' if company_gm > benchmark_gm else 'Below' if company_gm < benchmark_gm else 'At',
            'status': 'good' if company_gm >= benchmark_gm * 0.9 else 'poor'
        }
        
        # Net margin comparison
        company_nm = metrics.get('net_profit_margin', 0)
        benchmark_nm = self.benchmark['net_margin']
        comparisons['net_margin'] = {
            'company': company_nm,
            'industry': benchmark_nm,
            'difference': round(company_nm - benchmark_nm, 2),
            'performance': 'Above' if company_nm > benchmark_nm else 'Below' if company_nm < benchmark_nm else 'At',
            'status': 'good' if company_nm >= benchmark_nm * 0.8 else 'poor'
        }
        
        # Current ratio comparison
        company_cr = metrics.get('current_ratio', 0)
        benchmark_cr = self.benchmark['current_ratio']
        comparisons['current_ratio'] = {
            'company': company_cr,
            'industry': benchmark_cr,
            'difference': round(company_cr - benchmark_cr, 2),
            'performance': 'Above' if company_cr > benchmark_cr else 'Below' if company_cr < benchmark_cr else 'At',
            'status': 'good' if company_cr >= benchmark_cr * 0.8 else 'poor'
        }
        
        # Debt to equity comparison
        company_dte = metrics.get('debt_to_equity', 0)
        benchmark_dte = self.benchmark['debt_to_equity']
        comparisons['debt_to_equity'] = {
            'company': company_dte,
            'industry': benchmark_dte,
            'difference': round(company_dte - benchmark_dte, 2),
            'performance': 'Below' if company_dte < benchmark_dte else 'Above' if company_dte > benchmark_dte else 'At',
            'status': 'good' if company_dte <= benchmark_dte * 1.2 else 'poor'
        }
        
        # Cash conversion cycle
        company_ccc = metrics.get('cash_conversion_cycle', 0)
        benchmark_ccc = self.benchmark['cash_conversion_cycle']
        comparisons['cash_conversion_cycle'] = {
            'company': company_ccc,
            'industry': benchmark_ccc,
            'difference': round(company_ccc - benchmark_ccc, 2),
            'performance': 'Below' if company_ccc < benchmark_ccc else 'Above' if company_ccc > benchmark_ccc else 'At',
            'status': 'good' if company_ccc <= benchmark_ccc * 1.2 else 'poor'
        }
        
        # Overall performance summary
        good_count = sum(1 for c in comparisons.values() if c['status'] == 'good')
        total_count = len(comparisons)
        overall_performance = 'Strong' if good_count >= total_count * 0.7 else 'Average' if good_count >= total_count * 0.4 else 'Weak'
        
        return {
            'industry': self.benchmark['name'],
            'comparisons': comparisons,
            'overall_performance': overall_performance,
            'metrics_above_industry': good_count,
            'total_metrics': total_count
        }
