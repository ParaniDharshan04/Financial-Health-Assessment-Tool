from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid import ApiClient, Configuration
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os

class PlaidIntegration:
    """Integration with Plaid API for banking data"""
    
    def __init__(self):
        # Get Plaid credentials
        self.client_id = os.getenv('PLAID_CLIENT_ID', '').strip()
        self.secret = os.getenv('PLAID_SECRET', '').strip()
        self.env = os.getenv('PLAID_ENV', 'https://sandbox.plaid.com').strip()
        
        # Check if Plaid is configured
        self.is_configured = bool(self.client_id and self.secret and len(self.client_id) > 10)
        
        if not self.is_configured:
            print("⚠️  Plaid not configured - missing CLIENT_ID or SECRET")
            return
        
        # Configure Plaid client
        configuration = Configuration(
            host=self.env,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
        print(f"✅ Plaid configured - Environment: {self.env}")
    
    def create_link_token(self, user_id: int, user_email: str) -> Dict:
        """Create a link token for Plaid Link"""
        # Check if Plaid is configured
        if not self.is_configured:
            return {
                "error": "Plaid not configured. Please set PLAID_CLIENT_ID and PLAID_SECRET in .env file.",
                "link_token": None,
                "is_demo": True
            }
        
        try:
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(user_id)
                ),
                client_name="SME Financial Platform",
                products=[Products("transactions"), Products("auth")],
                country_codes=[CountryCode("US"), CountryCode("IN")],
                language="en",
                webhook="https://your-domain.com/api/banking/webhook",  # Update with your domain
            )
            
            response = self.client.link_token_create(request)
            
            return {
                "link_token": response['link_token'],
                "expiration": response['expiration'],
                "is_demo": False
            }
            
        except Exception as e:
            print(f"Error creating link token: {str(e)}")
            return {
                "error": str(e),
                "link_token": None,
                "is_demo": True
            }
    
    def exchange_public_token(self, public_token: str) -> Optional[Dict]:
        """Exchange public token for access token"""
        try:
            request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            
            response = self.client.item_public_token_exchange(request)
            access_token = response['access_token']
            item_id = response['item_id']
            
            return {
                "access_token": access_token,
                "item_id": item_id
            }
            
        except Exception as e:
            print(f"Error exchanging public token: {str(e)}")
            return None
    
    def get_accounts(self, access_token: str) -> List[Dict]:
        """Get account information"""
        try:
            request = AccountsBalanceGetRequest(
                access_token=access_token
            )
            
            response = self.client.accounts_balance_get(request)
            accounts = response['accounts']
            
            return [
                {
                    "account_id": account['account_id'],
                    "name": account['name'],
                    "type": account['type'],
                    "subtype": account['subtype'],
                    "balance": {
                        "current": account['balances']['current'],
                        "available": account['balances'].get('available'),
                        "currency": account['balances']['iso_currency_code']
                    }
                }
                for account in accounts
            ]
            
        except Exception as e:
            print(f"Error getting accounts: {str(e)}")
            return []
    
    def get_transactions(self, access_token: str, start_date: datetime = None, 
                        end_date: datetime = None) -> List[Dict]:
        """Get transaction history"""
        try:
            # Default to last 30 days
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date()
            )
            
            response = self.client.transactions_get(request)
            transactions = response['transactions']
            
            return [
                {
                    "transaction_id": txn['transaction_id'],
                    "account_id": txn['account_id'],
                    "date": txn['date'].isoformat(),
                    "name": txn['name'],
                    "amount": txn['amount'],
                    "category": txn.get('category', []),
                    "merchant_name": txn.get('merchant_name'),
                    "pending": txn['pending']
                }
                for txn in transactions
            ]
            
        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            return []
    
    def categorize_transactions(self, transactions: List[Dict]) -> Dict:
        """Categorize transactions for financial analysis"""
        categorized = {
            "revenue": [],
            "expenses": [],
            "total_revenue": 0,
            "total_expenses": 0,
            "by_category": {}
        }
        
        for txn in transactions:
            amount = abs(txn['amount'])
            categories = txn.get('category', [])
            category = categories[0] if categories else "Uncategorized"
            
            # Negative amounts are credits (revenue), positive are debits (expenses)
            if txn['amount'] < 0:
                categorized["revenue"].append(txn)
                categorized["total_revenue"] += amount
            else:
                categorized["expenses"].append(txn)
                categorized["total_expenses"] += amount
            
            # Group by category
            if category not in categorized["by_category"]:
                categorized["by_category"][category] = {
                    "count": 0,
                    "total": 0,
                    "transactions": []
                }
            
            categorized["by_category"][category]["count"] += 1
            categorized["by_category"][category]["total"] += amount
            categorized["by_category"][category]["transactions"].append(txn)
        
        return categorized
    
    def sync_to_financial_data(self, transactions: List[Dict], 
                               accounts: List[Dict]) -> Dict:
        """Convert banking data to financial data format"""
        categorized = self.categorize_transactions(transactions)
        
        # Calculate financial metrics from banking data
        total_balance = sum(acc['balance']['current'] for acc in accounts)
        
        financial_data = {
            "revenue": categorized["total_revenue"],
            "operating_expenses": categorized["total_expenses"],
            "net_profit": categorized["total_revenue"] - categorized["total_expenses"],
            "cash": total_balance,
            "current_assets": total_balance,  # Simplified
            "transaction_count": len(transactions),
            "account_count": len(accounts),
            "data_source": "plaid",
            "sync_date": datetime.now().isoformat()
        }
        
        return financial_data
    
    def get_mock_data_for_demo(self) -> Dict:
        """Get mock banking data for demo purposes (when Plaid not configured)"""
        return {
            "accounts": [
                {
                    "account_id": "demo_checking_001",
                    "name": "Business Checking",
                    "type": "depository",
                    "subtype": "checking",
                    "balance": {
                        "current": 250000,
                        "available": 245000,
                        "currency": "INR"
                    }
                },
                {
                    "account_id": "demo_savings_001",
                    "name": "Business Savings",
                    "type": "depository",
                    "subtype": "savings",
                    "balance": {
                        "current": 500000,
                        "available": 500000,
                        "currency": "INR"
                    }
                }
            ],
            "transactions": [
                {
                    "transaction_id": "demo_txn_001",
                    "date": (datetime.now() - timedelta(days=1)).isoformat(),
                    "name": "Customer Payment",
                    "amount": -50000,  # Negative = credit/revenue
                    "category": ["Payment", "Revenue"],
                    "merchant_name": "Customer ABC"
                },
                {
                    "transaction_id": "demo_txn_002",
                    "date": (datetime.now() - timedelta(days=2)).isoformat(),
                    "name": "Office Rent",
                    "amount": 25000,  # Positive = debit/expense
                    "category": ["Rent", "Operating Expense"],
                    "merchant_name": "Property Management"
                },
                {
                    "transaction_id": "demo_txn_003",
                    "date": (datetime.now() - timedelta(days=3)).isoformat(),
                    "name": "Supplier Payment",
                    "amount": 30000,
                    "category": ["Purchase", "COGS"],
                    "merchant_name": "Supplier XYZ"
                }
            ],
            "is_demo": True,
            "message": "This is demo data. Connect real bank account for actual data."
        }
