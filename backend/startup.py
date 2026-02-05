"""
Startup script to initialize database tables on first run
This runs before the FastAPI app starts
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, Base
from app.db import models

def init_database():
    """Initialize database tables if they don't exist"""
    try:
        print("🔄 Checking database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables ready!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
