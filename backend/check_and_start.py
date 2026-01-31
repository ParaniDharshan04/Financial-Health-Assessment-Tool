"""
Pre-flight check and startup script for the backend
"""
import sys
import os
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("=" * 60)
    print("SME Financial Health Platform - Pre-flight Check")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Check 1: .env file exists
    print("1. Checking .env file...")
    if not Path(".env").exists():
        errors.append(".env file not found. Copy .env.example to .env")
    else:
        print("   ✓ .env file found")
    
    # Check 2: Load environment variables
    print("2. Checking environment variables...")
    try:
        from app.core.config import settings
        
        # Check DATABASE_URL
        if "user:password" in settings.DATABASE_URL or "YOUR_PASSWORD" in settings.DATABASE_URL:
            errors.append("DATABASE_URL still has placeholder password. Update it in .env")
        else:
            print("   ✓ DATABASE_URL configured")
        
        # Check GEMINI_API_KEY
        if "your-gemini-api-key" in settings.GEMINI_API_KEY.lower():
            errors.append("GEMINI_API_KEY not configured. Add your API key in .env")
        else:
            print("   ✓ GEMINI_API_KEY configured")
        
        # Check SECRET_KEY
        if "your-secret-key" in settings.SECRET_KEY.lower():
            warnings.append("SECRET_KEY is using default value. Consider generating a new one")
        else:
            print("   ✓ SECRET_KEY configured")
            
    except Exception as e:
        errors.append(f"Error loading configuration: {str(e)}")
    
    # Check 3: Database connection
    print("3. Checking database connection...")
    try:
        from app.db.database import engine
        with engine.connect() as conn:
            print("   ✓ Database connection successful")
    except Exception as e:
        errors.append(f"Database connection failed: {str(e)}")
        errors.append("   → Check PostgreSQL is running")
        errors.append("   → Verify database 'sme_financial_db' exists")
        errors.append("   → Check password in DATABASE_URL")
    
    # Check 4: Database tables
    print("4. Checking database tables...")
    try:
        from app.db.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['users', 'financial_data', 'analyses', 'reports']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            errors.append(f"Missing database tables: {', '.join(missing_tables)}")
            errors.append("   → Run: python init_db.py")
        else:
            print(f"   ✓ All tables exist: {', '.join(tables)}")
    except Exception as e:
        warnings.append(f"Could not check tables: {str(e)}")
    
    # Check 5: Required packages
    print("5. Checking required packages...")
    try:
        import fastapi
        import uvicorn
        import pandas
        import sqlalchemy
        import google.generativeai
        print("   ✓ All required packages installed")
    except ImportError as e:
        errors.append(f"Missing package: {str(e)}")
        errors.append("   → Run: pip install -r requirements.txt")
    
    print()
    print("=" * 60)
    
    # Display results
    if errors:
        print("❌ ERRORS FOUND:")
        print()
        for error in errors:
            print(f"   {error}")
        print()
        print("Please fix the errors above before starting the server.")
        print("=" * 60)
        return False
    
    if warnings:
        print("⚠️  WARNINGS:")
        print()
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    print("✅ ALL CHECKS PASSED!")
    print()
    print("You can now start the server with:")
    print("   uvicorn app.main:app --reload")
    print()
    print("Or run this script with --start flag:")
    print("   python check_and_start.py --start")
    print("=" * 60)
    
    return True

def start_server():
    """Start the uvicorn server"""
    import uvicorn
    print("\n🚀 Starting server...\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    if check_environment():
        if "--start" in sys.argv:
            start_server()
        else:
            print("\nRun with --start flag to start the server automatically")
