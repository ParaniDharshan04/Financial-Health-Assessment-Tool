from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    industry = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Additional profile fields
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    pan = Column(String, nullable=True)
    registration_date = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    annual_revenue = Column(String, nullable=True)
    
    financial_data = relationship("FinancialData", back_populates="user")
    analyses = relationship("Analysis", back_populates="user")

class FinancialData(Base):
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(DateTime, default=datetime.utcnow)
    data_type = Column(String)  # profit_loss, cash_flow, expenses, etc.
    raw_data = Column(JSON)
    normalized_data = Column(JSON)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    user = relationship("User", back_populates="financial_data")
    analysis = relationship("Analysis", back_populates="financial_data", uselist=False)

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    financial_data_id = Column(Integer, ForeignKey("financial_data.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Financial Health Score
    health_score = Column(Float)
    risk_band = Column(String)  # Safe, Watch, Critical
    
    # Metrics
    liquidity_score = Column(Float)
    profitability_score = Column(Float)
    cash_flow_score = Column(Float)
    debt_health_score = Column(Float)
    
    # Computed metrics
    metrics = Column(JSON)
    
    # AI Insights
    ai_insights = Column(JSON)
    recommendations = Column(JSON)
    
    # Benchmarking
    industry_comparison = Column(JSON)
    
    # Credit readiness
    credit_readiness = Column(JSON)
    
    # Forecasting
    cash_flow_forecast = Column(JSON)
    
    user = relationship("User", back_populates="analyses")
    financial_data = relationship("FinancialData", back_populates="analysis")
    report = relationship("Report", back_populates="analysis", uselist=False)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    generated_at = Column(DateTime, default=datetime.utcnow)
    report_path = Column(String)
    language = Column(String, default="en")
    
    analysis = relationship("Analysis", back_populates="report")

class TaxDeduction(Base):
    __tablename__ = "tax_deductions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    financial_year = Column(String)
    section = Column(String)  # 80C, 80D, etc.
    description = Column(String)
    amount = Column(Float)
    is_eligible = Column(Integer, default=1)  # Using Integer for SQLite compatibility
    document_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaxCompliance(Base):
    __tablename__ = "tax_compliance"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    financial_year = Column(String)
    compliance_type = Column(String)  # TDS, GST, Income Tax
    status = Column(String)  # Compliant, Non-compliant, Pending
    due_date = Column(DateTime, nullable=True)
    filed_date = Column(DateTime, nullable=True)
    compliance_metadata = Column(JSON, nullable=True)  # Renamed from metadata
    created_at = Column(DateTime, default=datetime.utcnow)

class BankConnection(Base):
    __tablename__ = "bank_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(Text, nullable=False)  # Encrypted in production
    item_id = Column(String, nullable=False)
    institution_id = Column(String, nullable=True)
    institution_name = Column(String, nullable=True)
    account_ids = Column(JSON, nullable=True)  # List of connected account IDs
    is_active = Column(Integer, default=1)  # Using Integer for SQLite compatibility
    connected_at = Column(DateTime, default=datetime.utcnow)
    last_sync = Column(DateTime, nullable=True)
    sync_status = Column(String, default="active")  # active, error, disconnected
    error_message = Column(Text, nullable=True)
