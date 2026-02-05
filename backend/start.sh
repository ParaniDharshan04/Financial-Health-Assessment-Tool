#!/bin/bash
# Startup script for Render deployment

echo "🚀 Starting application..."

# Initialize database tables
echo "📊 Initializing database..."
python startup.py

# Start the FastAPI application
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
