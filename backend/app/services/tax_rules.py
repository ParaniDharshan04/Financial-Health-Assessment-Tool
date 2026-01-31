"""Tax rules database for different countries"""

TAX_RULES = {
    "IN": {  # India
        "country_name": "India",
        "currency": "INR",
        
        "income_tax": {
            "financial_year": "April-March",
            "filing_deadline": "July 31",
            
            # Corporate tax rates
            "corporate_tax": {
                "domestic_company": 0.30,  # 30%
                "foreign_company": 0.40,   # 40%
                "small_business": 0.25,    # 25% (turnover < 400 Cr)
            },
            
            # Individual tax slabs (New Regime FY 2024-25)
            "individual_slabs": [
                {"min": 0, "max": 300000, "rate": 0.00},
                {"min": 300000, "max": 700000, "rate": 0.05},
                {"min": 700000, "max": 1000000, "rate": 0.10},
                {"min": 1000000, "max": 1200000, "rate": 0.15},
                {"min": 1200000, "max": 1500000, "rate": 0.20},
                {"min": 1500000, "max": float('inf'), "rate": 0.30},
            ],
            
            # Deductions
            "deductions": {
                "80C": {
                    "name": "Section 80C",
                    "limit": 150000,
                    "description": "Life insurance, PPF, ELSS, EPF, NSC, Home Loan Principal",
                    "eligible_items": [
                        "Life Insurance Premium",
                        "Public Provident Fund (PPF)",
                        "Equity Linked Savings Scheme (ELSS)",
                        "Employee Provident Fund (EPF)",
                        "National Savings Certificate (NSC)",
                        "Home Loan Principal Repayment",
                        "Tuition Fees",
                        "Sukanya Samriddhi Account"
                    ]
                },
                "80D": {
                    "name": "Section 80D",
                    "limit": 25000,
                    "senior_limit": 50000,
                    "description": "Health insurance premiums",
                    "eligible_items": [
                        "Health Insurance Premium (Self, Spouse, Children)",
                        "Health Insurance Premium (Parents)",
                        "Preventive Health Checkup (₹5,000)"
                    ]
                },
                "80E": {
                    "name": "Section 80E",
                    "limit": None,
                    "description": "Education loan interest",
                    "eligible_items": [
                        "Interest on Education Loan"
                    ]
                },
                "80G": {
                    "name": "Section 80G",
                    "limit": None,
                    "description": "Donations to charitable institutions",
                    "deduction_percentage": {
                        "100_with_limit": 0.10,  # 10% of adjusted gross income
                        "50_with_limit": 0.10,
                        "100_without_limit": 1.0,
                        "50_without_limit": 0.50
                    }
                },
                "24B": {
                    "name": "Section 24(b)",
                    "limit": 200000,
                    "description": "Home loan interest",
                    "eligible_items": [
                        "Interest on Home Loan (Self-Occupied Property)"
                    ]
                },
                "80CCD": {
                    "name": "Section 80CCD(1B)",
                    "limit": 50000,
                    "description": "Additional NPS contribution",
                    "eligible_items": [
                        "National Pension System (NPS) Contribution"
                    ]
                },
                "80TTA": {
                    "name": "Section 80TTA",
                    "limit": 10000,
                    "description": "Interest on savings account",
                    "eligible_items": [
                        "Interest on Savings Bank Account"
                    ]
                }
            },
            
            # Advance tax payment schedule
            "advance_tax": {
                "threshold": 10000,
                "installments": [
                    {"due_date": "June 15", "percentage": 0.15},
                    {"due_date": "September 15", "percentage": 0.45},
                    {"due_date": "December 15", "percentage": 0.75},
                    {"due_date": "March 15", "percentage": 1.00}
                ]
            }
        },
        
        "gst": {
            "full_name": "Goods and Services Tax",
            "registration_threshold": 4000000,  # ₹40 lakhs (₹20L for special states)
            "composition_threshold": 15000000,  # ₹1.5 crores
            
            "rates": [0, 5, 12, 18, 28],
            
            "filing_frequency": {
                "regular": "Monthly",
                "composition": "Quarterly",
                "annual_return": "Yearly"
            },
            
            "returns": {
                "GSTR-1": {
                    "name": "Outward Supplies",
                    "frequency": "Monthly",
                    "due_date": "11th of next month"
                },
                "GSTR-3B": {
                    "name": "Summary Return",
                    "frequency": "Monthly",
                    "due_date": "20th of next month"
                },
                "GSTR-9": {
                    "name": "Annual Return",
                    "frequency": "Yearly",
                    "due_date": "December 31"
                }
            },
            
            "exemptions": [
                "Healthcare services",
                "Educational services",
                "Fresh fruits and vegetables",
                "Unbranded food grains"
            ],
            
            "penalties": {
                "late_filing": {
                    "GSTR-3B": 50,  # ₹50 per day (₹20 if nil return)
                    "GSTR-1": 200,  # ₹200 per day
                    "max_penalty": 5000
                },
                "non_registration": "10% of tax amount",
                "tax_evasion": "100% of tax amount"
            }
        },
        
        "tds": {
            "full_name": "Tax Deducted at Source",
            
            "rates": {
                "salary": "As per slab",
                "professional_fees": 0.10,  # 10%
                "contractor_payment": 0.02,  # 2% (individual) / 1% (company)
                "rent": 0.10,  # 10%
                "commission": 0.05,  # 5%
                "interest": 0.10,  # 10%
            },
            
            "thresholds": {
                "professional_fees": 30000,
                "rent": 240000,  # Annual
                "commission": 15000,
                "interest": 40000  # For senior citizens: 50000
            },
            
            "filing": {
                "frequency": "Quarterly",
                "forms": ["24Q", "26Q", "27Q"],
                "due_dates": {
                    "Q1": "July 31",
                    "Q2": "October 31",
                    "Q3": "January 31",
                    "Q4": "May 31"
                }
            },
            
            "penalties": {
                "late_deduction": "Interest @ 1% per month",
                "late_payment": "Interest @ 1.5% per month",
                "non_deduction": "Disallowance of expense + interest"
            }
        },
        
        "compliance_calendar": {
            "monthly": [
                {"task": "GST Return (GSTR-3B)", "deadline": "20th"},
                {"task": "TDS Payment", "deadline": "7th"}
            ],
            "quarterly": [
                {"task": "TDS Return Filing", "deadline": "Last day of next month"},
                {"task": "Advance Tax Payment", "deadline": "15th of last month"}
            ],
            "annual": [
                {"task": "Income Tax Return", "deadline": "July 31"},
                {"task": "GST Annual Return", "deadline": "December 31"},
                {"task": "Audit Report (if applicable)", "deadline": "September 30"}
            ]
        },
        
        "audit_requirements": {
            "tax_audit": {
                "threshold_business": 10000000,  # ₹1 crore
                "threshold_profession": 5000000,  # ₹50 lakhs
                "form": "3CA/3CB",
                "deadline": "September 30"
            },
            "gst_audit": {
                "threshold": 200000000,  # ₹2 crores
                "form": "GSTR-9C",
                "deadline": "December 31"
            }
        }
    },
    
    "US": {  # United States (Basic structure for future expansion)
        "country_name": "United States",
        "currency": "USD",
        
        "income_tax": {
            "financial_year": "January-December",
            "filing_deadline": "April 15",
            
            "corporate_tax": {
                "federal_rate": 0.21,  # 21%
                "state_rate": "Varies by state"
            },
            
            "individual_slabs": [
                {"min": 0, "max": 11000, "rate": 0.10},
                {"min": 11000, "max": 44725, "rate": 0.12},
                {"min": 44725, "max": 95375, "rate": 0.22},
                {"min": 95375, "max": 182100, "rate": 0.24},
                {"min": 182100, "max": 231250, "rate": 0.32},
                {"min": 231250, "max": 578125, "rate": 0.35},
                {"min": 578125, "max": float('inf'), "rate": 0.37},
            ]
        }
    }
}

# Helper functions
def get_tax_rules(country: str = "IN") -> dict:
    """Get tax rules for a specific country"""
    return TAX_RULES.get(country, TAX_RULES["IN"])

def get_gst_rate_for_category(category: str) -> float:
    """Get GST rate for a product/service category"""
    # Simplified mapping - in reality, this would be much more detailed
    gst_rates = {
        "essential_goods": 0.05,
        "standard_goods": 0.18,
        "luxury_goods": 0.28,
        "services": 0.18,
        "healthcare": 0.00,
        "education": 0.00
    }
    return gst_rates.get(category, 0.18)

def calculate_income_tax(income: float, country: str = "IN") -> dict:
    """Calculate income tax based on slabs"""
    rules = get_tax_rules(country)
    slabs = rules["income_tax"]["individual_slabs"]
    
    tax = 0
    tax_breakdown = []
    
    for slab in slabs:
        if income > slab["min"]:
            taxable_in_slab = min(income, slab["max"]) - slab["min"]
            tax_in_slab = taxable_in_slab * slab["rate"]
            tax += tax_in_slab
            
            tax_breakdown.append({
                "slab": f"₹{slab['min']:,.0f} - ₹{slab['max']:,.0f}",
                "rate": f"{slab['rate']*100}%",
                "taxable_amount": taxable_in_slab,
                "tax": tax_in_slab
            })
    
    return {
        "total_tax": tax,
        "effective_rate": (tax / income * 100) if income > 0 else 0,
        "breakdown": tax_breakdown
    }
