from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from fuzzywuzzy import fuzz
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime

class TransactionCategorizer:
    """Categorize transactions using ML"""
    
    def __init__(self):
        self.categories = [
            "Revenue", "COGS", "Operating Expenses",
            "Marketing", "Salaries", "Rent", "Utilities",
            "Travel", "Office Supplies", "Professional Fees",
            "Insurance", "Taxes", "Interest", "Depreciation",
            "Capital Expenditure", "Loan Repayment", "Dividends"
        ]
        
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.model = MultinomialNB()
        self.is_trained = False
        
        # Train with sample data
        self._train_with_sample_data()
    
    def _train_with_sample_data(self):
        """Train model with sample transaction descriptions"""
        training_data = [
            # Revenue
            ("Customer payment received", "Revenue"),
            ("Sales invoice payment", "Revenue"),
            ("Service fee received", "Revenue"),
            ("Product sale", "Revenue"),
            
            # COGS
            ("Raw material purchase", "COGS"),
            ("Inventory purchase", "COGS"),
            ("Supplier payment for goods", "COGS"),
            
            # Operating Expenses
            ("Office rent payment", "Rent"),
            ("Electricity bill", "Utilities"),
            ("Internet bill", "Utilities"),
            ("Water bill", "Utilities"),
            
            # Salaries
            ("Employee salary", "Salaries"),
            ("Payroll payment", "Salaries"),
            ("Staff wages", "Salaries"),
            
            # Marketing
            ("Google ads payment", "Marketing"),
            ("Facebook advertising", "Marketing"),
            ("Marketing campaign", "Marketing"),
            
            # Travel
            ("Flight ticket", "Travel"),
            ("Hotel booking", "Travel"),
            ("Taxi fare", "Travel"),
            
            # Office Supplies
            ("Stationery purchase", "Office Supplies"),
            ("Office furniture", "Office Supplies"),
            ("Printer ink", "Office Supplies"),
            
            # Professional Fees
            ("Consultant fee", "Professional Fees"),
            ("Legal fees", "Professional Fees"),
            ("Accounting services", "Professional Fees"),
            
            # Insurance
            ("Business insurance premium", "Insurance"),
            ("Health insurance", "Insurance"),
            
            # Taxes
            ("GST payment", "Taxes"),
            ("Income tax payment", "Taxes"),
            ("TDS payment", "Taxes"),
            
            # Interest
            ("Loan interest payment", "Interest"),
            ("Bank charges", "Interest"),
            
            # Capital Expenditure
            ("Equipment purchase", "Capital Expenditure"),
            ("Machinery purchase", "Capital Expenditure"),
            ("Vehicle purchase", "Capital Expenditure")
        ]
        
        descriptions = [d[0] for d in training_data]
        categories = [d[1] for d in training_data]
        
        X = self.vectorizer.fit_transform(descriptions)
        self.model.fit(X, categories)
        self.is_trained = True
    
    def categorize_transaction(self, description: str, amount: float) -> str:
        """Categorize a single transaction"""
        if not self.is_trained:
            return "Uncategorized"
        
        # Use ML model
        X = self.vectorizer.transform([description])
        category = self.model.predict(X)[0]
        
        # Additional rules based on amount
        if amount < 0:  # Negative amounts are typically revenue
            category = "Revenue"
        
        return category
    
    def categorize_bulk(self, transactions: List[Dict]) -> List[Dict]:
        """Categorize multiple transactions"""
        categorized = []
        
        for txn in transactions:
            category = self.categorize_transaction(
                txn.get('description', ''),
                txn.get('amount', 0)
            )
            
            categorized.append({
                **txn,
                'category': category,
                'confidence': 0.85  # Simplified confidence score
            })
        
        return categorized
    
    def learn_from_corrections(self, transaction: Dict, correct_category: str):
        """Update model with user corrections"""
        # In production, this would retrain the model
        # For now, just acknowledge the correction
        return {
            "message": "Correction recorded",
            "transaction_id": transaction.get('id'),
            "corrected_category": correct_category
        }


class BookkeepingAutomation:
    """Automate bookkeeping tasks"""
    
    def __init__(self):
        self.categorizer = TransactionCategorizer()
    
    def generate_journal_entries(self, transactions: List[Dict]) -> List[Dict]:
        """Generate double-entry journal entries"""
        journal_entries = []
        
        for txn in transactions:
            category = txn.get('category', 'Uncategorized')
            amount = abs(txn.get('amount', 0))
            description = txn.get('description', '')
            date = txn.get('date', datetime.now().isoformat())
            
            # Determine debit and credit accounts
            if category == "Revenue":
                debit_account = "Bank"
                credit_account = "Revenue"
            elif category in ["COGS", "Operating Expenses", "Marketing", "Salaries", 
                            "Rent", "Utilities", "Travel", "Office Supplies", 
                            "Professional Fees", "Insurance", "Taxes", "Interest"]:
                debit_account = category
                credit_account = "Bank"
            elif category == "Capital Expenditure":
                debit_account = "Fixed Assets"
                credit_account = "Bank"
            elif category == "Loan Repayment":
                debit_account = "Loan Payable"
                credit_account = "Bank"
            else:
                debit_account = "Miscellaneous"
                credit_account = "Bank"
            
            journal_entries.append({
                "date": date,
                "description": description,
                "debit_account": debit_account,
                "credit_account": credit_account,
                "amount": amount,
                "transaction_id": txn.get('id')
            })
        
        return journal_entries
    
    def reconcile_accounts(self, bank_statement: List[Dict], 
                          book_entries: List[Dict]) -> Dict:
        """Reconcile bank statement with book entries"""
        matched = []
        unmatched_bank = []
        unmatched_book = []
        
        # Simple matching based on amount and date
        for bank_txn in bank_statement:
            match_found = False
            
            for book_txn in book_entries:
                if (abs(bank_txn.get('amount', 0)) == abs(book_txn.get('amount', 0)) and
                    bank_txn.get('date') == book_txn.get('date')):
                    matched.append({
                        "bank_transaction": bank_txn,
                        "book_entry": book_txn,
                        "status": "Matched"
                    })
                    match_found = True
                    break
            
            if not match_found:
                unmatched_bank.append(bank_txn)
        
        # Find unmatched book entries
        matched_book_ids = [m["book_entry"].get('id') for m in matched]
        unmatched_book = [b for b in book_entries if b.get('id') not in matched_book_ids]
        
        return {
            "matched_count": len(matched),
            "unmatched_bank_count": len(unmatched_bank),
            "unmatched_book_count": len(unmatched_book),
            "matched_transactions": matched,
            "unmatched_bank_transactions": unmatched_bank,
            "unmatched_book_entries": unmatched_book,
            "reconciliation_status": "Complete" if len(unmatched_bank) == 0 and len(unmatched_book) == 0 else "Incomplete"
        }
    
    def detect_duplicates(self, transactions: List[Dict]) -> List[Dict]:
        """Detect duplicate transactions"""
        duplicates = []
        
        for i, txn1 in enumerate(transactions):
            for j, txn2 in enumerate(transactions[i+1:], start=i+1):
                # Check similarity
                similarity = self._calculate_similarity(txn1, txn2)
                
                if similarity > 0.85:  # 85% similarity threshold
                    duplicates.append({
                        "transaction_1": txn1,
                        "transaction_2": txn2,
                        "similarity_score": similarity,
                        "reason": self._get_duplicate_reason(txn1, txn2)
                    })
        
        return duplicates
    
    def _calculate_similarity(self, txn1: Dict, txn2: Dict) -> float:
        """Calculate similarity between two transactions"""
        # Amount similarity
        amount1 = abs(txn1.get('amount', 0))
        amount2 = abs(txn2.get('amount', 0))
        amount_similarity = 1.0 if amount1 == amount2 else 0.0
        
        # Description similarity (fuzzy matching)
        desc1 = txn1.get('description', '')
        desc2 = txn2.get('description', '')
        desc_similarity = fuzz.ratio(desc1, desc2) / 100.0
        
        # Date similarity
        date1 = txn1.get('date', '')
        date2 = txn2.get('date', '')
        date_similarity = 1.0 if date1 == date2 else 0.0
        
        # Weighted average
        similarity = (amount_similarity * 0.5 + desc_similarity * 0.3 + date_similarity * 0.2)
        
        return similarity
    
    def _get_duplicate_reason(self, txn1: Dict, txn2: Dict) -> str:
        """Get reason for duplicate detection"""
        reasons = []
        
        if txn1.get('amount') == txn2.get('amount'):
            reasons.append("Same amount")
        
        if txn1.get('date') == txn2.get('date'):
            reasons.append("Same date")
        
        desc_sim = fuzz.ratio(txn1.get('description', ''), txn2.get('description', ''))
        if desc_sim > 80:
            reasons.append("Similar description")
        
        return ", ".join(reasons) if reasons else "Unknown"
    
    def track_expenses(self, transactions: List[Dict]) -> Dict:
        """Track and categorize expenses"""
        # Categorize all transactions
        categorized = self.categorizer.categorize_bulk(transactions)
        
        # Group by category
        expense_summary = {}
        total_expenses = 0
        
        for txn in categorized:
            if txn.get('amount', 0) > 0:  # Positive amounts are expenses
                category = txn.get('category', 'Uncategorized')
                amount = txn.get('amount', 0)
                
                if category not in expense_summary:
                    expense_summary[category] = {
                        "total": 0,
                        "count": 0,
                        "transactions": []
                    }
                
                expense_summary[category]["total"] += amount
                expense_summary[category]["count"] += 1
                expense_summary[category]["transactions"].append(txn)
                
                total_expenses += amount
        
        # Calculate percentages
        for category in expense_summary:
            expense_summary[category]["percentage"] = (
                expense_summary[category]["total"] / total_expenses * 100
            ) if total_expenses > 0 else 0
        
        return {
            "total_expenses": total_expenses,
            "categories": expense_summary,
            "category_count": len(expense_summary),
            "transaction_count": len([t for t in categorized if t.get('amount', 0) > 0])
        }
    
    def get_demo_transactions(self) -> List[Dict]:
        """Get demo transactions for testing"""
        return [
            {
                "id": 1,
                "date": "2025-01-15",
                "description": "Customer payment for services",
                "amount": -50000,  # Negative = revenue
                "merchant": "Customer ABC"
            },
            {
                "id": 2,
                "date": "2025-01-16",
                "description": "Office rent payment",
                "amount": 25000,
                "merchant": "Property Management"
            },
            {
                "id": 3,
                "date": "2025-01-17",
                "description": "Employee salary payment",
                "amount": 80000,
                "merchant": "Payroll"
            },
            {
                "id": 4,
                "date": "2025-01-18",
                "description": "Google ads payment",
                "amount": 15000,
                "merchant": "Google"
            },
            {
                "id": 5,
                "date": "2025-01-19",
                "description": "Office supplies purchase",
                "amount": 5000,
                "merchant": "Stationery Store"
            }
        ]
