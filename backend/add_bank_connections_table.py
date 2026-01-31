"""
Add bank_connections table to database
Run this script to add the new table for Plaid banking integration
"""

from app.db.database import engine, Base
from app.db.models import BankConnection
from sqlalchemy import inspect

def add_bank_connections_table():
    """Add bank_connections table if it doesn't exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if 'bank_connections' not in existing_tables:
        print("Creating bank_connections table...")
        BankConnection.__table__.create(engine)
        print("✓ bank_connections table created successfully!")
    else:
        print("✓ bank_connections table already exists")

if __name__ == "__main__":
    print("Adding bank_connections table to database...")
    add_bank_connections_table()
    print("\nDatabase migration complete!")
