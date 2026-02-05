# SME Financial Health Assessment Tool - Features Guide

## Table of Contents
1. [Upload Financial Data](#1-upload-financial-data)
2. [Tax Compliance](#2-tax-compliance)
3. [GST Returns Management](#3-gst-returns-management)
4. [Banking Integration](#4-banking-integration)
5. [Financial Analysis](#5-financial-analysis)

---

## 1. Upload Financial Data

### Overview
The Upload Data feature allows SMEs to import their financial statements in multiple formats (CSV, Excel, PDF) for automated analysis and insights generation.

### Supported File Types
- **CSV Files** (.csv)
- **Excel Files** (.xlsx, .xls)
- **PDF Documents** (.pdf) - Automatically extracts financial data using AI-powered parsing

### Data Types Accepted

#### A. Profit & Loss Statement
Contains income and expense information:
- **Revenue**: Sales revenue, service income, other income
- **Cost of Goods Sold (COGS)**: Direct costs of production
- **Operating Expenses**: Rent, salaries, utilities, marketing, etc.
- **Profitability Metrics**: Gross profit, operating profit, net profit, EBIT, EBITDA
- **Other**: Interest expense, tax expense, depreciation

**Required Columns:**
```csv
Date, Revenue, Cost_of_Goods_Sold, Gross_Profit, Operating_Expenses, 
Operating_Profit, Interest_Expense, Net_Profit, EBIT, EBITDA
```

#### B. Balance Sheet
Contains assets, liabilities, and equity information:
- **Assets**: Current assets, fixed assets, cash, inventory, accounts receivable
- **Liabilities**: Current liabilities, long-term debt, accounts payable
- **Equity**: Shareholder equity, retained earnings
- **Cash Flow**: Operating, investing, and financing cash flows

**Required Columns:**
```csv
Date, Current_Assets, Fixed_Assets, Total_Assets, Current_Liabilities, 
Long_Term_Debt, Total_Liabilities, Equity, Cash, Accounts_Receivable, 
Inventory, Accounts_Payable, Operating_Cash_Flow
```

#### C. Cash Flow Statement
Contains cash movement information:
- **Operating Activities**: Cash from business operations
- **Investing Activities**: Capital expenditures, asset purchases
- **Financing Activities**: Loans, dividends, equity transactions
- **Working Capital Metrics**: Receivables days, payables days, inventory days

**Required Columns:**
```csv
Date, Operating_Cash_Flow, Investing_Cash_Flow, Financing_Cash_Flow, 
Receivables_Days, Payables_Days, Inventory_Days
```

### How to Upload

1. **Navigate to Upload Page**
   - Click "Upload Data" from the dashboard
   - Or use the quick action card

2. **Select File**
   - Click "Choose File" or drag & drop your file
   - Supported formats: CSV, XLSX, PDF

3. **Choose Data Type**
   - Select from dropdown: Profit & Loss, Balance Sheet, or Cash Flow
   - The system will automatically extract relevant fields

4. **Upload & Process**
   - Click "Upload" button
   - System processes and normalizes the data
   - Confirmation message shows records processed

5. **Create Analysis**
   - After upload, click "Analyze" to generate insights
   - System combines all uploaded data for comprehensive analysis

### Best Practices

✅ **Upload Multiple Files**: Upload both P&L and Balance Sheet for complete analysis
✅ **Use Latest Data**: Upload most recent financial statements
✅ **Consistent Format**: Keep column names consistent across uploads
✅ **Complete Data**: Include all required fields for accurate metrics
✅ **Regular Updates**: Upload quarterly or monthly for trend analysis

### Sample Data Files

The application includes sample files in the `data/` folder:
- `complete_financial_statement.csv` - All-in-one comprehensive file
- `profit_loss_statement_100.csv` - Sample P&L statement
- `balance_sheet_100.csv` - Sample balance sheet

---

## 2. Tax Compliance

### Overview
The Tax Compliance feature helps SMEs track, manage, and ensure compliance with Indian tax regulations including Income Tax, TDS, and Professional Tax.

### Key Features

#### A. Compliance Dashboard
- **Real-time Status**: View compliance status for all tax types
- **Due Date Tracking**: Upcoming deadlines and overdue items
- **Filing History**: Track all past tax filings
- **Compliance Score**: Overall tax compliance health indicator

#### B. Tax Types Monitored

##### 1. Income Tax
- **Advance Tax Payments**: Quarterly advance tax tracking
- **Annual Return Filing**: ITR filing status and deadlines
- **Tax Computation**: Automated tax calculation based on financial data
- **Deduction Tracking**: Section 80C, 80D, and other deductions

##### 2. TDS (Tax Deducted at Source)
- **TDS on Salaries**: Employee TDS tracking
- **TDS on Professional Fees**: Contractor and consultant payments
- **TDS on Rent**: Property rent TDS compliance
- **Quarterly Returns**: TDS return filing (24Q, 26Q, 27Q)
- **TDS Certificates**: Form 16, 16A generation

##### 3. Professional Tax
- **Monthly Tracking**: State-wise professional tax monitoring
- **Employee-wise Calculation**: Individual PT deductions
- **Compliance Status**: Monthly payment status

#### C. Tax Deduction Management

**Supported Deductions:**
- Section 80C: Life insurance, PPF, ELSS, home loan principal
- Section 80D: Health insurance premiums
- Section 80G: Charitable donations
- Section 24: Home loan interest
- Business Expenses: Eligible business deductions

**Features:**
- Upload deduction documents
- Automatic eligibility checking
- Deduction optimization suggestions
- Document storage and retrieval

#### D. Compliance Alerts

The system provides proactive alerts for:
- Upcoming tax payment deadlines
- Pending return filings
- Missing documentation
- Non-compliance risks
- Penalty warnings

### How to Use Tax Compliance

1. **Access Tax Compliance Page**
   - Click "Tax Compliance" from dashboard
   - View overall compliance status

2. **Add Tax Deductions**
   - Click "Add Deduction"
   - Select financial year and section
   - Enter amount and upload supporting documents
   - System validates eligibility

3. **Track Compliance Status**
   - View color-coded status indicators:
     - 🟢 Green: Compliant
     - 🟡 Yellow: Pending action
     - 🔴 Red: Non-compliant/Overdue

4. **File Returns**
   - System generates pre-filled return data
   - Review and confirm details
   - Download return forms
   - Mark as filed with acknowledgment number

5. **Generate Reports**
   - Tax computation statements
   - Deduction summaries
   - Compliance certificates
   - Audit trail reports

### Tax Compliance Checks

The system automatically checks:
- ✅ Timely advance tax payments
- ✅ TDS deduction and deposit compliance
- ✅ Return filing within deadlines
- ✅ Proper documentation maintenance
- ✅ Deduction claim validity
- ✅ Interest and penalty calculations

---

## 3. GST Returns Management

### Overview
The GST Returns feature provides comprehensive Goods and Services Tax compliance management for Indian SMEs, covering registration, invoicing, return filing, and reconciliation.

### Key Features

#### A. GST Dashboard
- **GST Liability Summary**: Current month's GST payable/receivable
- **Return Filing Status**: GSTR-1, GSTR-3B, GSTR-9 status
- **Input Tax Credit (ITC)**: Available ITC balance
- **Compliance Calendar**: Due dates for all GST returns

#### B. GST Return Types Supported

##### 1. GSTR-1 (Outward Supplies)
**Purpose**: Report all sales and outward supplies

**Includes:**
- B2B invoices (Business to Business)
- B2C invoices (Business to Consumer)
- Credit/debit notes
- Export invoices
- Nil-rated, exempted supplies

**Filing Frequency**: Monthly (for turnover > ₹5 crore) or Quarterly (QRMP scheme)

**Features:**
- Auto-populate from uploaded financial data
- Invoice-wise details extraction
- HSN/SAC code mapping
- Tax rate validation (0%, 5%, 12%, 18%, 28%)

##### 2. GSTR-3B (Summary Return)
**Purpose**: Monthly summary of outward and inward supplies

**Includes:**
- Total outward supplies (taxable, exempt, nil-rated)
- Total inward supplies liable to reverse charge
- ITC claimed (CGST, SGST, IGST, Cess)
- Tax payable and paid
- Late fee, if applicable

**Filing Frequency**: Monthly

**Features:**
- Auto-calculation of tax liability
- ITC reconciliation with GSTR-2A/2B
- Payment challan generation
- Interest calculation on late payment

##### 3. GSTR-9 (Annual Return)
**Purpose**: Annual consolidated return

**Includes:**
- Turnover details for the financial year
- ITC claimed and reversed
- Tax paid and refund claimed
- Amendments to previous returns

**Filing Frequency**: Annual (by December 31st)

#### C. GST Calculation Engine

**Automatic Calculations:**
- Output GST on sales (CGST + SGST or IGST)
- Input GST on purchases
- Net GST liability (Output GST - Input GST)
- Reverse charge mechanism
- Interest on delayed payment
- Late filing fees

**Tax Rate Management:**
- Product/service-wise tax rates
- HSN/SAC code database
- Exemption tracking
- Composition scheme calculations

#### D. Input Tax Credit (ITC) Management

**Features:**
- ITC eligibility checking
- GSTR-2A/2B reconciliation
- Blocked credit identification
- ITC reversal calculations
- Carry forward of excess ITC

**ITC Rules Compliance:**
- Time limit for claiming ITC (November of next FY)
- Matching with supplier returns
- Ineligible ITC identification
- Proportionate ITC for mixed supplies

#### E. GST Reconciliation

**Reconciliation Types:**
1. **Sales Reconciliation**: Books vs GSTR-1
2. **Purchase Reconciliation**: Books vs GSTR-2A/2B
3. **ITC Reconciliation**: Claimed vs Available
4. **Payment Reconciliation**: Liability vs Payment

**Mismatch Identification:**
- Invoice-level mismatches
- Tax amount differences
- Missing invoices
- Duplicate entries

### How to Use GST Returns

1. **Upload GST Data**
   - Navigate to GST Management page
   - Upload sales/purchase data (CSV/Excel)
   - System extracts GST-relevant information

2. **Review GST Summary**
   - View calculated GST liability
   - Check ITC available
   - Review tax rate breakup

3. **Generate GSTR-1**
   - Click "Generate GSTR-1"
   - Review invoice-wise details
   - Download JSON file for GST portal upload

4. **File GSTR-3B**
   - System auto-fills GSTR-3B form
   - Review and verify amounts
   - Download return or file directly (if API integrated)

5. **Reconcile Returns**
   - Compare filed returns with books
   - Identify and resolve mismatches
   - Generate reconciliation reports

6. **Make GST Payment**
   - View payment challan details
   - Generate challan (PMT-06)
   - Track payment status

### GST Compliance Alerts

The system alerts for:
- 📅 Upcoming return filing deadlines
- 💰 GST payment due dates
- ⚠️ ITC expiry warnings
- 🔍 Reconciliation mismatches
- 📊 Annual return due dates
- 🚨 Non-compliance penalties

### GST Reports Available

- Monthly GST liability report
- ITC utilization report
- HSN/SAC-wise summary
- Tax rate-wise breakup
- Supplier/customer-wise GST
- Reconciliation statements
- Compliance certificates

---

## 4. Banking Integration

### Overview
The Banking Integration feature connects your business bank accounts securely using Plaid API, enabling real-time transaction monitoring, cash flow tracking, and automated reconciliation.

### Key Features

#### A. Secure Bank Connection
- **Plaid Integration**: Industry-standard secure banking API
- **Multi-Bank Support**: Connect multiple bank accounts
- **Real-time Sync**: Automatic transaction updates
- **Bank-level Security**: OAuth 2.0 authentication
- **Read-only Access**: No ability to initiate transactions

#### B. Supported Banks
The integration supports 11,000+ financial institutions including:
- **Major Indian Banks**: SBI, HDFC, ICICI, Axis, Kotak, etc.
- **Private Banks**: Yes Bank, IndusInd, RBL, etc.
- **Payment Banks**: Paytm Payments Bank, Airtel Payments Bank
- **Co-operative Banks**: Regional and urban co-operative banks
- **International Banks**: For export/import businesses

#### C. Transaction Management

**Automatic Transaction Import:**
- Real-time transaction fetching
- Historical data (up to 24 months)
- Transaction categorization
- Merchant identification
- Duplicate detection

**Transaction Details Captured:**
- Date and time
- Amount (debit/credit)
- Merchant/counterparty name
- Transaction type (UPI, NEFT, RTGS, cheque, etc.)
- Balance after transaction
- Transaction ID/reference number

**Smart Categorization:**
- Revenue/Income
- Operating Expenses
- Capital Expenditure
- Loan Payments
- Tax Payments
- Salary Payments
- Vendor Payments
- Customer Receipts

#### D. Cash Flow Monitoring

**Real-time Insights:**
- Current account balance across all accounts
- Daily cash position
- Cash inflows vs outflows
- Projected cash runway
- Low balance alerts

**Cash Flow Analysis:**
- Weekly/monthly cash flow trends
- Seasonal patterns identification
- Cash conversion cycle tracking
- Working capital monitoring

**Forecasting:**
- 3-month cash flow projection
- Scenario analysis (best/worst case)
- Burn rate calculation
- Funding requirement estimation

#### E. Automated Reconciliation

**Bank Reconciliation:**
- Match bank transactions with accounting entries
- Identify unmatched transactions
- Detect duplicate entries
- Flag unusual transactions

**Invoice Matching:**
- Auto-match customer payments to invoices
- Track outstanding receivables
- Payment delay analysis
- Customer payment behavior insights

**Expense Matching:**
- Match vendor payments to bills
- Track outstanding payables
- Vendor payment terms compliance
- Early payment discount opportunities

#### F. Financial Insights

**Spending Analysis:**
- Category-wise expense breakdown
- Vendor-wise spending patterns
- Month-over-month comparisons
- Budget vs actual analysis

**Revenue Analysis:**
- Customer-wise revenue tracking
- Payment method analysis
- Revenue concentration risk
- Collection efficiency metrics

**Banking Metrics:**
- Average daily balance
- Float days
- Bank charges analysis
- Interest earned/paid

### How to Use Banking Integration

#### Step 1: Connect Your Bank Account

1. **Navigate to Banking Page**
   - Click "Banking" from dashboard
   - Click "Connect Bank Account" button

2. **Select Your Bank**
   - Search for your bank in Plaid interface
   - Select from list of supported banks

3. **Authenticate**
   - Enter your online banking credentials
   - Complete 2FA/OTP verification
   - Grant read-only access permission

4. **Select Accounts**
   - Choose which accounts to connect
   - Current accounts, savings accounts, credit cards
   - Click "Connect"

5. **Confirmation**
   - Connection successful message
   - Initial transaction sync begins
   - View connected accounts

#### Step 2: View Transactions

1. **Transaction Dashboard**
   - View all transactions across accounts
   - Filter by date range, type, category
   - Search by merchant or amount

2. **Transaction Details**
   - Click any transaction for details
   - View categorization
   - Add notes or tags
   - Attach receipts/documents

3. **Categorize Transactions**
   - Review auto-categorization
   - Manually adjust if needed
   - Create custom categories
   - Set rules for future transactions

#### Step 3: Monitor Cash Flow

1. **Cash Flow Dashboard**
   - View current balance across all accounts
   - See today's inflows and outflows
   - Check projected balance

2. **Cash Flow Chart**
   - Visual representation of cash movement
   - Identify trends and patterns
   - Compare periods

3. **Set Alerts**
   - Low balance warnings
   - Large transaction notifications
   - Unusual activity alerts
   - Daily summary emails

#### Step 4: Reconciliation

1. **Auto-Reconciliation**
   - System matches transactions automatically
   - Review matched items
   - Approve or reject matches

2. **Manual Reconciliation**
   - View unmatched transactions
   - Manually match with invoices/bills
   - Mark as reconciled
   - Add reconciliation notes

3. **Generate Reports**
   - Bank reconciliation statement
   - Unmatched items report
   - Reconciliation summary

### Banking Security

**Security Measures:**
- 🔒 256-bit SSL encryption
- 🔐 OAuth 2.0 authentication
- 👁️ Read-only access (no transaction initiation)
- 🛡️ Plaid's bank-level security
- 🔑 Encrypted token storage
- 📱 Multi-factor authentication support

**Data Privacy:**
- No storage of banking credentials
- Encrypted data transmission
- Secure token management
- Compliance with data protection regulations
- Regular security audits

**Access Control:**
- User-level access permissions
- Activity logging
- Session management
- Automatic logout on inactivity

### Troubleshooting Banking Connection

**Common Issues:**

1. **Connection Failed**
   - Verify banking credentials
   - Check if online banking is enabled
   - Ensure 2FA/OTP is working
   - Try different browser

2. **Transactions Not Syncing**
   - Check connection status
   - Reconnect account if needed
   - Verify bank account is active
   - Contact support if issue persists

3. **Incorrect Categorization**
   - Manually recategorize transactions
   - Create categorization rules
   - Train the system with corrections

4. **Account Disconnected**
   - Bank may require re-authentication
   - Click "Reconnect" button
   - Complete authentication again

### Banking Integration Benefits

✅ **Time Savings**: Eliminate manual data entry
✅ **Accuracy**: Reduce human errors in transaction recording
✅ **Real-time Visibility**: Always know your cash position
✅ **Better Decisions**: Data-driven financial decisions
✅ **Fraud Detection**: Identify unusual transactions quickly
✅ **Compliance**: Maintain accurate financial records
✅ **Cash Flow Management**: Optimize working capital
✅ **Reconciliation**: Automated matching saves hours

---

## 5. Financial Analysis

### Overview
After uploading financial data, the system generates comprehensive AI-powered analysis with actionable insights.

### Analysis Components

#### A. Financial Health Score (0-100)
Weighted composite score based on:
- Liquidity (30%): Ability to meet short-term obligations
- Profitability (25%): Earning capacity and margins
- Cash Flow (25%): Cash generation efficiency
- Debt Health (20%): Leverage and solvency

**Risk Bands:**
- 🟢 **Safe (70-100)**: Strong financial health
- 🟡 **Watch (40-69)**: Moderate concerns, needs attention
- 🔴 **Critical (0-39)**: Significant financial stress

#### B. Key Financial Metrics

**Liquidity Ratios:**
- Current Ratio: Current Assets / Current Liabilities
- Quick Ratio: (Current Assets - Inventory) / Current Liabilities
- Cash Ratio: Cash / Current Liabilities

**Profitability Ratios:**
- Gross Profit Margin: (Gross Profit / Revenue) × 100
- Net Profit Margin: (Net Profit / Revenue) × 100
- Operating Margin: (Operating Profit / Revenue) × 100
- Return on Assets (ROA): (Net Profit / Total Assets) × 100
- Return on Equity (ROE): (Net Profit / Equity) × 100

**Debt Ratios:**
- Debt to Equity: Total Debt / Equity
- Debt to Assets: (Total Debt / Total Assets) × 100
- Interest Coverage: EBIT / Interest Expense

**Cash Flow Metrics:**
- Operating Cash Flow Margin
- Cash Conversion Cycle
- Cash Flow Coverage Ratio

#### C. AI-Powered Insights
- Trend analysis and pattern recognition
- Strength and weakness identification
- Risk assessment and early warnings
- Opportunity identification
- Peer comparison insights

#### D. Actionable Recommendations
Prioritized recommendations with:
- Issue description
- Impact assessment
- Specific action steps
- Expected outcomes
- Implementation timeline

#### E. Industry Benchmarking
Compare your metrics against:
- Industry averages
- Top performers
- Similar-sized companies
- Regional benchmarks

#### F. Credit Readiness Assessment
- Credit score estimation
- Loan eligibility analysis
- Recommended financing options
- Documentation requirements
- Improvement suggestions

#### G. Cash Flow Forecasting
- 3-6 month projections
- Scenario analysis
- Funding gap identification
- Optimization opportunities

### Downloadable Reports
- Comprehensive PDF report
- Executive summary
- Detailed metric analysis
- Visualizations and charts
- Recommendations document

---

## Support & Resources

### Getting Help
- **In-app Help**: Click "?" icon for contextual help
- **Documentation**: Refer to this guide
- **Support Email**: support@yourapp.com
- **Video Tutorials**: Available on dashboard

### Best Practices
1. Upload data regularly (monthly/quarterly)
2. Review compliance status weekly
3. Reconcile bank transactions daily
4. Act on high-priority recommendations
5. Monitor cash flow daily
6. File returns before deadlines
7. Maintain proper documentation

### Data Security
- All data encrypted at rest and in transit
- Regular security audits
- Compliance with data protection laws
- Secure cloud infrastructure
- Regular backups
- Access controls and logging

---

## Conclusion

This SME Financial Health Assessment Tool provides a comprehensive suite of features to help small and medium enterprises:
- Automate financial data management
- Ensure tax and GST compliance
- Monitor cash flow in real-time
- Make data-driven decisions
- Improve financial health
- Access credit opportunities

For detailed technical documentation, refer to the README.md file.
