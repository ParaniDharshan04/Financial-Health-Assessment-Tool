import pdfplumber
import PyPDF2
import re
from typing import Dict, List, Optional
from io import BytesIO

class PDFParser:
    """Parse financial data from PDF documents"""
    
    def __init__(self):
        self.financial_keywords = {
            'revenue': ['revenue', 'sales', 'income', 'turnover'],
            'cogs': ['cost of goods sold', 'cogs', 'cost of sales'],
            'gross_profit': ['gross profit', 'gross margin'],
            'operating_expenses': ['operating expenses', 'opex', 'operating costs'],
            'operating_profit': ['operating profit', 'ebit', 'operating income'],
            'net_profit': ['net profit', 'net income', 'profit after tax', 'pat'],
            'current_assets': ['current assets'],
            'cash': ['cash', 'cash and equivalents', 'cash & equivalents'],
            'inventory': ['inventory', 'stock'],
            'current_liabilities': ['current liabilities'],
            'total_assets': ['total assets'],
            'total_debt': ['total debt', 'total liabilities', 'borrowings'],
            'equity': ['equity', 'shareholders equity', 'net worth'],
            'interest_expense': ['interest expense', 'interest paid', 'finance cost']
        }
    
    def extract_financial_data(self, pdf_file: bytes, data_type: str) -> Dict:
        """Extract financial data from PDF"""
        try:
            # Try pdfplumber first (better for tables)
            data = self._extract_with_pdfplumber(pdf_file, data_type)
            if data:
                return data
            
            # Fallback to PyPDF2 (better for text)
            data = self._extract_with_pypdf2(pdf_file, data_type)
            if data:
                return data
            
            raise Exception("Could not extract financial data from PDF")
            
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")
    
    def _extract_with_pdfplumber(self, pdf_file: bytes, data_type: str) -> Optional[Dict]:
        """Extract data using pdfplumber (good for tables)"""
        try:
            with pdfplumber.open(BytesIO(pdf_file)) as pdf:
                all_text = ""
                all_tables = []
                
                for page in pdf.pages:
                    # Extract text
                    all_text += page.extract_text() or ""
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                
                # Try to extract from tables first
                if all_tables:
                    data = self._parse_tables(all_tables, data_type)
                    if data:
                        return data
                
                # Fallback to text parsing
                if all_text:
                    return self._parse_text(all_text, data_type)
                
        except Exception as e:
            print(f"pdfplumber error: {str(e)}")
            return None
    
    def _extract_with_pypdf2(self, pdf_file: bytes, data_type: str) -> Optional[Dict]:
        """Extract data using PyPDF2 (good for text)"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
            all_text = ""
            
            for page in pdf_reader.pages:
                all_text += page.extract_text() or ""
            
            if all_text:
                return self._parse_text(all_text, data_type)
            
        except Exception as e:
            print(f"PyPDF2 error: {str(e)}")
            return None
    
    def _parse_tables(self, tables: List[List[List]], data_type: str) -> Optional[Dict]:
        """Parse financial data from extracted tables"""
        extracted_data = {}
        
        for table in tables:
            for row in table:
                if not row or len(row) < 2:
                    continue
                
                # Get label and value
                label = str(row[0]).lower().strip() if row[0] else ""
                value_str = str(row[1]).strip() if len(row) > 1 and row[1] else ""
                
                # Try to extract number
                value = self._extract_number(value_str)
                if value is None:
                    continue
                
                # Match to financial keywords
                for key, keywords in self.financial_keywords.items():
                    if any(keyword in label for keyword in keywords):
                        extracted_data[key] = value
                        break
        
        if extracted_data:
            return self._normalize_extracted_data(extracted_data, data_type)
        
        return None
    
    def _parse_text(self, text: str, data_type: str) -> Optional[Dict]:
        """Parse financial data from plain text"""
        extracted_data = {}
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Look for financial keywords
            for key, keywords in self.financial_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Try to find number in this line or next line
                    value = self._extract_number(line)
                    if value is None and i + 1 < len(lines):
                        value = self._extract_number(lines[i + 1])
                    
                    if value is not None:
                        extracted_data[key] = value
                        break
        
        if extracted_data:
            return self._normalize_extracted_data(extracted_data, data_type)
        
        return None
    
    def _extract_number(self, text: str) -> Optional[float]:
        """Extract numerical value from text"""
        if not text:
            return None
        
        # Remove common currency symbols and formatting
        text = text.replace('₹', '').replace('$', '').replace('€', '')
        text = text.replace(',', '').replace('(', '-').replace(')', '')
        
        # Find numbers (including decimals and negatives)
        matches = re.findall(r'-?\d+\.?\d*', text)
        
        if matches:
            try:
                # Take the first number found
                value = float(matches[0])
                
                # Check for multipliers (K, M, B, Cr, L)
                text_upper = text.upper()
                if 'CR' in text_upper or 'CRORE' in text_upper:
                    value *= 10000000  # 1 crore = 10 million
                elif 'L' in text_upper or 'LAC' in text_upper or 'LAKH' in text_upper:
                    value *= 100000  # 1 lakh = 100 thousand
                elif 'B' in text_upper or 'BILLION' in text_upper:
                    value *= 1000000000
                elif 'M' in text_upper or 'MILLION' in text_upper:
                    value *= 1000000
                elif 'K' in text_upper or 'THOUSAND' in text_upper:
                    value *= 1000
                
                return value
            except ValueError:
                return None
        
        return None
    
    def _normalize_extracted_data(self, extracted_data: Dict, data_type: str) -> Dict:
        """Normalize extracted data based on data type"""
        normalized = {}
        
        if data_type == "profit_loss":
            normalized = {
                'revenue': extracted_data.get('revenue', 0),
                'cost_of_goods_sold': extracted_data.get('cogs', 0),
                'gross_profit': extracted_data.get('gross_profit', 0),
                'operating_expenses': extracted_data.get('operating_expenses', 0),
                'operating_profit': extracted_data.get('operating_profit', 0),
                'net_profit': extracted_data.get('net_profit', 0),
                'ebit': extracted_data.get('operating_profit', 0),
                'interest_expense': extracted_data.get('interest_expense', 0),
            }
            
            # Calculate missing values
            if normalized['gross_profit'] == 0 and normalized['revenue'] > 0:
                normalized['gross_profit'] = normalized['revenue'] - normalized['cost_of_goods_sold']
            
            if normalized['ebit'] == 0 and normalized['operating_profit'] > 0:
                normalized['ebit'] = normalized['operating_profit']
        
        elif data_type == "balance_sheet":
            normalized = {
                'current_assets': extracted_data.get('current_assets', 0),
                'cash': extracted_data.get('cash', 0),
                'inventory': extracted_data.get('inventory', 0),
                'current_liabilities': extracted_data.get('current_liabilities', 0),
                'total_assets': extracted_data.get('total_assets', 0),
                'total_debt': extracted_data.get('total_debt', 0),
                'equity': extracted_data.get('equity', 0),
            }
        
        elif data_type == "cash_flow":
            normalized = {
                'operating_cash_flow': extracted_data.get('operating_cash_flow', 0),
                'investing_cash_flow': extracted_data.get('investing_cash_flow', 0),
                'financing_cash_flow': extracted_data.get('financing_cash_flow', 0),
                'net_cash_flow': extracted_data.get('net_cash_flow', 0),
                'receivables_days': 45,  # Default values
                'payables_days': 30,
                'inventory_days': 30,
            }
        
        return normalized
    
    def validate_extracted_data(self, data: Dict, data_type: str) -> bool:
        """Validate that extracted data has minimum required fields"""
        if data_type == "profit_loss":
            return data.get('revenue', 0) > 0 or data.get('net_profit', 0) != 0
        elif data_type == "balance_sheet":
            return data.get('total_assets', 0) > 0 or data.get('current_assets', 0) > 0
        elif data_type == "cash_flow":
            return data.get('operating_cash_flow', 0) != 0 or data.get('net_cash_flow', 0) != 0
        
        return False
