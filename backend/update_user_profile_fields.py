"""
Migration script to add profile fields to users table
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.database import engine

def update_database():
    print("Adding profile fields to users table...")
    print(f"Database URL: {engine.url}\n")
    
    # List of new columns to add
    new_columns = [
        ('phone', 'VARCHAR'),
        ('address', 'TEXT'),
        ('city', 'VARCHAR'),
        ('state', 'VARCHAR'),
        ('pincode', 'VARCHAR'),
        ('gstin', 'VARCHAR'),
        ('pan', 'VARCHAR'),
        ('registration_date', 'VARCHAR'),
        ('company_size', 'VARCHAR'),
        ('annual_revenue', 'VARCHAR')
    ]
    
    try:
        with engine.begin() as conn:  # Use begin() for automatic transaction management
            # Get existing columns
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """))
            existing_columns = [row[0] for row in result]
            
            print(f"Existing columns: {existing_columns}\n")
            
            # Add new columns if they don't exist
            for column_name, column_type in new_columns:
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
                        conn.execute(text(sql))
                        print(f"✓ Added column: {column_name}")
                    except Exception as e:
                        print(f"✗ Error adding column {column_name}: {e}")
                        raise
                else:
                    print(f"○ Column {column_name} already exists")
        
        print("\n✓ Database migration completed successfully!")
        print("\nPlease restart the backend server to apply changes.")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the database is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Verify you have permission to alter the table")
        return False
    
    return True

if __name__ == "__main__":
    success = update_database()
    sys.exit(0 if success else 1)
