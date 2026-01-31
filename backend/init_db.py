from app.db.database import engine, Base
from app.db import models
import sys

def init_database():
    """Initialize database tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - financial_data")
        print("  - analyses")
        print("  - reports")
        print("  - tax_deductions (NEW)")
        print("  - tax_compliance (NEW)")
        print("\nYou can now start the server with:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"✗ Error creating database tables: {str(e)}")
        print("\nPlease check:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'sme_financial_db' exists")
        print("  3. DATABASE_URL in .env is correct")
        print("  4. PostgreSQL password is correct")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
