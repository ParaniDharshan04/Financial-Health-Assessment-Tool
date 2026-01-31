# Real-Time Data Sources for Testing 📊

## Overview
This guide explains where to get real financial data to test your application with actual business scenarios.

---

## 🏢 Option 1: Use Your Own Business Data (Recommended)

### Financial Statements:
If you have a business, export data from your accounting software:

#### **Tally ERP**
1. Open Tally
2. Go to **Gateway of Tally** → **Display** → **Statements of Accounts**
3. Select **Profit & Loss Account** or **Balance Sheet**
4. Press **Alt + E** to export
5. Choose **Excel** or **CSV** format
6. Save and upload to platform

#### **QuickBooks**
1. Go to **Reports** → **Company & Financial**
2. Select **Profit & Loss** or **Balance Sheet**
3. Click **Export** → **Export to Excel**
4. Save as CSV
5. Upload to platform

#### **Zoho Books**
1. Go to **Reports** → **Financial Statements**
2. Select report type
3. Click **Export** → **CSV**
4. Upload to platform

#### **Excel/Manual Books**
If you maintain books in Excel:
1. Ensure columns: Category, Item, Amount, Date
2. Save as CSV
3. Upload to platform

---

## 🏦 Option 2: Bank Statements (Real Transaction Data)

### Download from Your Bank:

#### **HDFC Bank**
1. Login to NetBanking
2. Go to **Accounts** → **Account Statement**
3. Select date range (last 3-6 months)
4. Download as **Excel** or **CSV**
5. Upload to platform

#### **ICICI Bank**
1. Login to Internet Banking
2. **My Accounts** → **Account Statement**
3. Select period
4. Download **Excel format**
5. Upload to platform

#### **SBI**
1. Login to OnlineSBI
2. **e-Services** → **Account Statement**
3. Choose format: **Excel**
4. Download and upload

#### **Axis Bank**
1. Login to Axis Bank Internet Banking
2. **Accounts** → **Statement**
3. Export to Excel
4. Upload to platform

### What the Platform Will Do:
- Categorize transactions automatically
- Calculate revenue vs expenses
- Generate cash flow analysis
- Identify spending patterns

---

## 📄 Option 3: GST Returns (From GST Portal)

### Download Your GST Returns:

1. **Login to GST Portal**: https://www.gst.gov.in/
2. Go to **Services** → **Returns** → **Track Return Status**
3. Select **Financial Year** and **Return Period**
4. Click on filed return (GSTR-1 or GSTR-3B)
5. Click **Download** → Choose **JSON** format
6. Save the JSON file
7. Upload to your platform's GST Management page

### Available Returns:
- **GSTR-1**: Outward supplies (your sales)
- **GSTR-3B**: Summary return (tax liability)
- **GSTR-2A**: Auto-populated purchases (for ITC)
- **GSTR-9**: Annual return

### What You'll Get:
- Complete GST analysis
- Compliance score
- Tax liability breakdown
- ITC optimization suggestions

---

## 💼 Option 4: Sample Real Business Data (Public Sources)

### 1. **Government Open Data**
**India Data Portal**: https://data.gov.in/
- Search for "financial statements"
- Download CSV files
- Use for testing

### 2. **Company Annual Reports**
**BSE/NSE Listed Companies**:
1. Go to company website
2. Find **Investor Relations** section
3. Download **Annual Report** (PDF)
4. Extract financial statements
5. Convert to CSV using Excel
6. Upload to platform

**Example Companies**:
- Infosys: https://www.infosys.com/investors.html
- TCS: https://www.tcs.com/investor-relations
- Wipro: https://www.wipro.com/investors/

### 3. **Kaggle Datasets**
**Kaggle**: https://www.kaggle.com/datasets
- Search: "financial statements" or "company financials"
- Download CSV datasets
- Use for testing

**Recommended Datasets**:
- Indian Company Financial Data
- SME Financial Statements
- Startup Financial Data

### 4. **World Bank Open Data**
**World Bank**: https://data.worldbank.org/
- Financial indicators
- Economic data
- Business statistics

---

## 🧪 Option 5: Generate Realistic Test Data

### Use the Data Generator Script:

I'll create a Python script to generate realistic financial data:

```python
# Save as: generate_test_data.py
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_financial_data(company_name, months=12):
    """Generate realistic financial data for testing"""
    
    data = []
    base_revenue = random.randint(500000, 5000000)
    
    for month in range(months):
        date = datetime.now() - timedelta(days=30*month)
        
        # Revenue (with seasonal variation)
        revenue = base_revenue * random.uniform(0.8, 1.2)
        
        # Expenses (60-80% of revenue)
        cogs = revenue * random.uniform(0.35, 0.45)
        salaries = base_revenue * 0.15 * random.uniform(0.95, 1.05)
        rent = base_revenue * 0.05
        utilities = base_revenue * 0.02 * random.uniform(0.8, 1.2)
        marketing = revenue * random.uniform(0.05, 0.10)
        
        # Add rows
        data.append(['Revenue', 'Sales Revenue', revenue, date, 'Product Sales', 'No', 18])
        data.append(['Expenses', 'Cost of Goods Sold', cogs, date, 'Materials', 'Yes', 18])
        data.append(['Expenses', 'Employee Salaries', salaries, date, 'Payroll', 'Yes', 0])
        data.append(['Expenses', 'Office Rent', rent, date, 'Rent', 'Yes', 18])
        data.append(['Expenses', 'Utilities', utilities, date, 'Electricity & Water', 'Yes', 18])
        data.append(['Expenses', 'Marketing', marketing, date, 'Advertising', 'Yes', 18])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        'Category', 'Item', 'Amount', 'Date', 'Description', 'Tax_Deductible', 'GST_Rate'
    ])
    
    # Save to CSV
    filename = f'{company_name.replace(" ", "_")}_financial_data.csv'
    df.to_csv(filename, index=False)
    print(f"Generated: {filename}")
    return filename

# Generate data
generate_financial_data("My Test Company", months=12)
```

**Run the script:**
```bash
python generate_test_data.py
```

This creates a CSV file with realistic financial data you can upload!

---

## 📊 Data Format Requirements

### For Financial Data Upload:

**Required Columns:**
```csv
Category,Item,Amount,Date,Description,Tax_Deductible,GST_Rate
Revenue,Sales Revenue,1000000,2024-01-31,Product Sales,No,18
Expenses,Raw Materials,400000,2024-01-31,Manufacturing,Yes,18
Expenses,Salaries,200000,2024-01-31,Employee Payroll,Yes,0
```

**Column Descriptions:**
- **Category**: Revenue, Expenses, Assets, Liabilities
- **Item**: Specific item name
- **Amount**: Numerical value (no currency symbols)
- **Date**: YYYY-MM-DD format
- **Description**: Brief description
- **Tax_Deductible**: Yes/No
- **GST_Rate**: 0, 5, 12, 18, or 28

### For GST Returns:

**JSON Format** (from GST Portal):
```json
{
  "gstin": "29ABCDE1234F1Z5",
  "return_period": "012025",
  "return_type": "GSTR-3B",
  "legal_name": "Your Company Name",
  "outward_supplies": { ... },
  "inward_supplies": { ... }
}
```

---

## 🎯 Recommended Testing Approach

### Phase 1: Start with Sample Data (Already Provided)
Use the files in `data/` folder:
- ✅ `1_complete_financial_data.csv`
- ✅ `2_tax_deductions.csv`
- ✅ `3_gst_return_GSTR1.json`
- ✅ `4_gst_return_GSTR3B.json`
- ✅ `5_tax_compliance_check.csv`

### Phase 2: Use Your Bank Statements
1. Download last 3 months of bank statements
2. Upload to platform
3. Let AI categorize transactions
4. Review and adjust categories

### Phase 3: Use Your Accounting Software Data
1. Export from Tally/QuickBooks/Zoho
2. Upload to platform
3. Get comprehensive analysis
4. Compare with your existing reports

### Phase 4: Use Your GST Returns
1. Download from GST Portal
2. Upload JSON files
3. Check compliance score
4. Review recommendations

---

## 🔒 Data Privacy & Security

### Important Notes:
1. **Sensitive Data**: Your financial data is stored securely in your local database
2. **No Cloud Upload**: Data stays on your machine (unless you deploy to cloud)
3. **Anonymize if Needed**: Replace company names and sensitive info before testing
4. **Test Environment**: Use a separate test database for real data testing

### How to Anonymize Data:
```python
# Replace sensitive info in CSV
import pandas as pd

df = pd.read_csv('your_real_data.csv')
df['Company_Name'] = 'Test Company'
df['Customer_Name'] = df['Customer_Name'].apply(lambda x: f'Customer_{hash(x) % 1000}')
df.to_csv('anonymized_data.csv', index=False)
```

---

## 📥 Quick Start: Get Data Right Now

### Option A: Use Your Bank (5 minutes)
1. Login to your bank's internet banking
2. Download last month's statement as Excel
3. Save as CSV
4. Upload to platform ✅

### Option B: Use GST Portal (5 minutes)
1. Login to https://www.gst.gov.in/
2. Go to Returns → Filed Returns
3. Download GSTR-3B as JSON
4. Upload to GST Management page ✅

### Option C: Use Tally (2 minutes)
1. Open Tally
2. Display → Profit & Loss
3. Alt + E → Export to Excel
4. Save as CSV
5. Upload to platform ✅

### Option D: Create in Excel (10 minutes)
1. Open Excel
2. Create columns: Category, Item, Amount, Date
3. Add your business data (even rough estimates)
4. Save as CSV
5. Upload to platform ✅

---

## 🎓 Example: Real Business Scenario

### Scenario: Small Retail Business

**Monthly Data:**
```csv
Category,Item,Amount,Date,Description,Tax_Deductible,GST_Rate
Revenue,Product Sales,500000,2024-01-31,Retail Sales,No,18
Revenue,Online Sales,200000,2024-01-31,E-commerce,No,18
Expenses,Inventory Purchase,300000,2024-01-31,Stock,Yes,18
Expenses,Rent,50000,2024-01-31,Shop Rent,Yes,18
Expenses,Salaries,80000,2024-01-31,Staff Salaries,Yes,0
Expenses,Electricity,8000,2024-01-31,Utilities,Yes,18
Expenses,Marketing,15000,2024-01-31,Facebook Ads,Yes,18
Tax_Payments,GST Paid,45000,2024-01-20,GST Payment,No,0
Tax_Payments,TDS,8000,2024-01-15,TDS on Salaries,No,0
```

**Upload this and get:**
- Financial Health Score
- Profit Margin Analysis
- Cash Flow Forecast
- Tax Optimization Tips
- GST Compliance Check

---

## 📞 Need Help?

### If you can't find data:
1. **Use the sample data provided** in `data/` folder
2. **Create dummy data** based on your business estimates
3. **Use the Python generator script** above
4. **Download public datasets** from Kaggle

### Data Quality Tips:
- ✅ Use consistent date formats
- ✅ Remove currency symbols (₹, $)
- ✅ Use numerical values only in Amount column
- ✅ Include at least 3 months of data for better analysis
- ✅ Separate revenue and expenses clearly

---

## 🎉 Ready to Test!

**Quick Checklist:**
- [ ] Choose data source (bank, accounting software, or sample)
- [ ] Download/export data
- [ ] Format as CSV (if needed)
- [ ] Login to application
- [ ] Upload to platform
- [ ] Review analysis
- [ ] Test all features

**Start with the easiest option and gradually move to more complex real data!**

---

## 📊 Data Sources Summary Table

| Source | Time to Get | Accuracy | Best For |
|--------|-------------|----------|----------|
| Sample Data (Provided) | 0 min | Demo | Learning the platform |
| Bank Statements | 5 min | 100% Real | Transaction analysis |
| Accounting Software | 2-5 min | 100% Real | Complete financial analysis |
| GST Portal | 5 min | 100% Real | GST compliance |
| Excel/Manual | 10 min | Depends | Custom scenarios |
| Public Datasets | 10 min | Real but not yours | Testing at scale |
| Generated Data | 2 min | Realistic | Stress testing |

**Recommendation: Start with Bank Statements or Accounting Software for the most realistic testing experience!**
