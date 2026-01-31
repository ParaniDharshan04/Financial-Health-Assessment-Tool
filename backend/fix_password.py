import sys
import getpass
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

print("=" * 60)
print("PostgreSQL Password Fix Tool")
print("=" * 60)
print()

# Get password from user
password = getpass.getpass("Enter your PostgreSQL password: ")

# URL encode the password to handle special characters
encoded_password = quote_plus(password)

# Test connection
test_url = f"postgresql://postgres:{encoded_password}@localhost:5432/sme_financial_db"

try:
    print("\nTesting connection...")
    engine = create_engine(test_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Connection successful!")
    
    # Update .env file
    print("\nUpdating .env file...")
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    with open('.env', 'w') as f:
        for line in lines:
            if line.startswith('DATABASE_URL='):
                f.write(f'DATABASE_URL=postgresql://postgres:{encoded_password}@localhost:5432/sme_financial_db\n')
            else:
                f.write(line)
    
    print("✓ .env file updated!")
    print()
    print("=" * 60)
    print("✅ Password fixed! You can now start the server:")
    print("   python -m uvicorn app.main:app --reload")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Connection failed: {str(e)}")
    print("\nPlease check:")
    print("  1. PostgreSQL is running")
    print("  2. Password is correct")
    print("  3. Database 'sme_financial_db' exists")
    sys.exit(1)
