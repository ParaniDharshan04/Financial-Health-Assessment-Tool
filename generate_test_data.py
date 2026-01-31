#!/usr/bin/env python3
"""
Financial Data Generator for Testing
Generates realistic financial data for your business
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import json

def generate_financial_data(company_name="Test Company", months=12, base_revenue=1000000):
    """
    Generate realistic financial data for testing
    
    Args:
        company_name: Name of the company
        months: Number of months of data to generate
        base_revenue: Base monthly revenue
    
    Returns:
        filename: Path to generated CSV file
    """
    
    print(f"\n🏢 Generating financial data for: {company_name}")
    print(f"📅 Period: {months} months")
    print(f"💰 Base Revenue: ₹{base_revenue:,}\n")
    
    data = []
    
    for month in range(months):
        date = (datetime.now() - timedelta(days=30*month)).strftime('%Y-%m-%d')
        
        # Revenue (with seasonal variation ±20%)
        monthly_revenue = base_revenue * random.uniform(0.8, 1.2)
        service_revenue = monthly_revenue * 0.3
        product_revenue = monthly_revenue * 0.7
        
        # Expenses (typically 60-75% of revenue)
        cogs = product_revenue * random.uniform(0.40, 0.50)
        salaries = base_revenue * 0.18 * random.uniform(0.95, 1.05)
        rent = base_revenue * 0.06
        utilities = base_revenue * 0.02 * random.uniform(0.8, 1.2)
        marketing = monthly_revenue * random.uniform(0.05, 0.08)
        professional_fees = base_revenue * 0.02
        insurance = base_revenue * 0.01
        depreciation = base_revenue * 0.03
        interest = base_revenue * 0.02
        
        # Tax payments
        gst_payment = monthly_revenue * 0.05
        tds_payment = salaries * 0.10
        advance_tax = (monthly_revenue - cogs - salaries) * 0.03
        
        # Assets
        fixed_assets = base_revenue * 2.5
        current_assets = base_revenue * 1.8
        cash_bank = base_revenue * 0.75
        
        # Liabilities
        business_loan = base_revenue * 1.2
        creditors = cogs * 0.3
        
        # Add revenue rows
        data.append(['Revenue', 'Product Sales', product_revenue, date, 'Product Sales Revenue', 'No', 18])
        data.append(['Revenue', 'Service Income', service_revenue, date, 'Consulting Services', 'No', 18])
        
        # Add expense rows
        data.append(['Expenses', 'Raw Materials', cogs, date, 'Cost of Goods Sold', 'Yes', 18])
        data.append(['Expenses', 'Employee Salaries', salaries, date, 'Staff Salaries', 'Yes', 0])
        data.append(['Expenses', 'Office Rent', rent, date, 'Office Space Rent', 'Yes', 18])
        data.append(['Expenses', 'Utilities', utilities, date, 'Electricity & Water', 'Yes', 18])
        data.append(['Expenses', 'Marketing', marketing, date, 'Digital Marketing', 'Yes', 18])
        data.append(['Expenses', 'Professional Fees', professional_fees, date, 'CA & Legal Fees', 'Yes', 18])
        data.append(['Expenses', 'Insurance', insurance, date, 'Business Insurance', 'Yes', 18])
        data.append(['Expenses', 'Depreciation', depreciation, date, 'Asset Depreciation', 'Yes', 0])
        data.append(['Expenses', 'Interest on Loan', interest, date, 'Business Loan Interest', 'Yes', 0])
        
        # Add tax payment rows (only for recent months)
        if month < 3:
            data.append(['Tax_Payments', 'GST Paid', gst_payment, date, 'GST Payment', 'No', 0])
            data.append(['Tax_Payments', 'TDS on Salaries', tds_payment, date, 'TDS Payment', 'No', 0])
            data.append(['Tax_Payments', 'Advance Income Tax', advance_tax, date, 'Advance Tax Q' + str(month+1), 'No', 0])
        
        # Add asset rows (only for first month)
        if month == 0:
            data.append(['Assets', 'Fixed Assets', fixed_assets, date, 'Machinery & Equipment', 'No', 0])
            data.append(['Assets', 'Current Assets', current_assets, date, 'Inventory & Receivables', 'No', 0])
            data.append(['Assets', 'Cash & Bank', cash_bank, date, 'Liquid Assets', 'No', 0])
            
            # Add liability rows
            data.append(['Liabilities', 'Business Loan', business_loan, date, 'Term Loan', 'No', 0])
            data.append(['Liabilities', 'Creditors', creditors, date, 'Trade Payables', 'No', 0])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        'Category', 'Item', 'Amount', 'Date', 'Description', 'Tax_Deductible', 'GST_Rate'
    ])
    
    # Round amounts to 2 decimal places
    df['Amount'] = df['Amount'].round(2)
    
    # Save to CSV
    filename = f'{company_name.replace(" ", "_")}_financial_data.csv'
    df.to_csv(filename, index=False)
    
    # Print summary
    total_revenue = df[df['Category'] == 'Revenue']['Amount'].sum()
    total_expenses = df[df['Category'] == 'Expenses']['Amount'].sum()
    net_profit = total_revenue - total_expenses
    
    print(f"✅ Generated: {filename}")
    print(f"\n📊 Summary:")
    print(f"   Total Revenue:  ₹{total_revenue:,.2f}")
    print(f"   Total Expenses: ₹{total_expenses:,.2f}")
    print(f"   Net Profit:     ₹{net_profit:,.2f}")
    print(f"   Profit Margin:  {(net_profit/total_revenue*100):.2f}%")
    print(f"   Total Rows:     {len(df)}")
    
    return filename


def generate_tax_deductions(company_name="Test Company"):
    """Generate realistic tax deductions data"""
    
    print(f"\n📋 Generating tax deductions for: {company_name}")
    
    deductions = [
        ['80C', 'Employee Provident Fund', 150000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80C', 'Life Insurance Premium', 50000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80C', 'Public Provident Fund', 100000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80D', 'Health Insurance Premium', 25000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80D', 'Preventive Health Checkup', 5000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80E', 'Education Loan Interest', 45000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['80G', 'Charitable Donations', 30000, 'Yes', 'Yes', 'No', '2024-25'],
        ['80TTA', 'Savings Account Interest', 8000, 'Yes', 'Yes', 'Yes', '2024-25'],
        ['24B', 'Home Loan Interest', 200000, 'Yes', 'Yes', 'Yes', '2024-25'],
    ]
    
    df = pd.DataFrame(deductions, columns=[
        'Section', 'Description', 'Amount', 'Eligible', 'Document_Available', 'Claimed', 'Financial_Year'
    ])
    
    filename = f'{company_name.replace(" ", "_")}_tax_deductions.csv'
    df.to_csv(filename, index=False)
    
    total = df['Amount'].sum()
    claimed = df[df['Claimed'] == 'Yes']['Amount'].sum()
    
    print(f"✅ Generated: {filename}")
    print(f"   Total Deductions: ₹{total:,}")
    print(f"   Claimed: ₹{claimed:,}")
    print(f"   Tax Savings: ₹{claimed * 0.3:,.0f} (at 30% rate)")
    
    return filename


def generate_gst_return(company_name="Test Company", gstin="29ABCDE1234F1Z5"):
    """Generate realistic GST return JSON"""
    
    print(f"\n📄 Generating GST return for: {company_name}")
    
    gstr3b = {
        "gstin": gstin,
        "return_period": "012025",
        "return_type": "GSTR-3B",
        "filing_date": "2025-01-20",
        "legal_name": company_name,
        "outward_supplies": {
            "taxable_supplies": {
                "taxable_value": 2500000,
                "igst": 150000,
                "cgst": 75000,
                "sgst": 75000,
                "cess": 0
            },
            "zero_rated_supplies": {
                "taxable_value": 500000,
                "igst": 0,
                "cgst": 0,
                "sgst": 0
            }
        },
        "inward_supplies": {
            "imports": {
                "taxable_value": 200000,
                "igst": 36000,
                "cess": 0
            }
        },
        "itc_claimed": {
            "igst": 120000,
            "cgst": 45000,
            "sgst": 45000,
            "cess": 0,
            "total": 210000
        },
        "itc_reversed": {
            "igst": 5000,
            "cgst": 2000,
            "sgst": 2000,
            "total": 9000,
            "reason": "Rule 42 - Personal use"
        },
        "net_itc": {
            "igst": 115000,
            "cgst": 43000,
            "sgst": 43000,
            "total": 201000
        },
        "tax_payable": {
            "igst": 35000,
            "cgst": 32000,
            "sgst": 32000,
            "total": 99000
        },
        "tax_paid": {
            "igst": 35000,
            "cgst": 32000,
            "sgst": 32000,
            "total": 99000,
            "payment_mode": "Electronic Cash Ledger",
            "payment_date": "2025-01-20",
            "challan_number": "CH-2025-1234"
        }
    }
    
    filename = f'{company_name.replace(" ", "_")}_gst_return_GSTR3B.json'
    with open(filename, 'w') as f:
        json.dump(gstr3b, f, indent=2)
    
    print(f"✅ Generated: {filename}")
    print(f"   Taxable Value: ₹{gstr3b['outward_supplies']['taxable_supplies']['taxable_value']:,}")
    print(f"   ITC Claimed: ₹{gstr3b['itc_claimed']['total']:,}")
    print(f"   Tax Payable: ₹{gstr3b['tax_payable']['total']:,}")
    
    return filename


def main():
    """Main function to generate all test data"""
    
    print("=" * 60)
    print("  📊 Financial Data Generator for Testing")
    print("=" * 60)
    
    # Get user input
    company_name = input("\n🏢 Enter company name (or press Enter for 'Test Company'): ").strip()
    if not company_name:
        company_name = "Test Company"
    
    months_input = input("📅 Enter number of months (default 12): ").strip()
    months = int(months_input) if months_input else 12
    
    revenue_input = input("💰 Enter base monthly revenue (default 1000000): ").strip()
    base_revenue = int(revenue_input) if revenue_input else 1000000
    
    gstin_input = input("🔢 Enter GSTIN (or press Enter for default): ").strip()
    gstin = gstin_input if gstin_input else "29ABCDE1234F1Z5"
    
    print("\n" + "=" * 60)
    print("  🚀 Generating Data...")
    print("=" * 60)
    
    # Generate all files
    financial_file = generate_financial_data(company_name, months, base_revenue)
    deduction_file = generate_tax_deductions(company_name)
    gst_file = generate_gst_return(company_name, gstin)
    
    print("\n" + "=" * 60)
    print("  ✅ All Files Generated Successfully!")
    print("=" * 60)
    print(f"\n📁 Files created:")
    print(f"   1. {financial_file}")
    print(f"   2. {deduction_file}")
    print(f"   3. {gst_file}")
    
    print(f"\n📤 Next Steps:")
    print(f"   1. Login to your application")
    print(f"   2. Upload {financial_file} to Financial Data Upload")
    print(f"   3. Add deductions from {deduction_file} to Tax Compliance")
    print(f"   4. Upload {gst_file} to GST Management")
    print(f"   5. Review analysis and insights!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Generation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please ensure pandas is installed: pip install pandas")
