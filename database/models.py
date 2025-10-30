"""
Database Models for Energy System
Stores historical forecasts, decisions, and system data
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class WeatherForecast(Base):
    """Store weather forecasts for historical analysis"""
    __tablename__ = 'weather_forecasts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    city = Column(String(100), index=True)
    
    # Current weather
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    cloud_cover = Column(Float)
    weather_condition = Column(String(50))
    
    # Renewable potential
    solar_potential = Column(Float)
    wind_potential = Column(Float)
    renewable_score = Column(Float)
    
    # Metadata
    data_source = Column(String(50))
    is_real_data = Column(Boolean, default=True)
    
    # Store full forecast as JSON
    forecast_data = Column(JSON)


class DemandForecast(Base):
    """Store demand forecasts"""
    __tablename__ = 'demand_forecasts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Current demand
    predicted_demand_mw = Column(Float)
    confidence = Column(Float)
    is_peak_hour = Column(Boolean)
    
    # Factors
    hourly_factor = Column(Float)
    seasonal_factor = Column(Float)
    weather_factor = Column(Float)
    is_weekend = Column(Boolean)
    
    # Anomaly detection
    is_anomaly = Column(Boolean, default=False)
    anomaly_severity = Column(String(20))
    
    # Store full forecast as JSON
    forecast_data = Column(JSON)


class GridBalance(Base):
    """Store grid balancing records"""
    __tablename__ = 'grid_balances'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Supply-Demand
    demand_mw = Column(Float)
    total_generation_mw = Column(Float)
    supply_demand_ratio = Column(Float)
    
    # Energy Mix
    renewable_generation = Column(Float)
    solar_generation = Column(Float)
    wind_generation = Column(Float)
    conventional_generation = Column(Float)
    storage_discharged = Column(Float)
    storage_charged = Column(Float)
    
    # Status
    grid_balance = Column(String(20), index=True)  # BALANCED, SURPLUS, DEFICIT
    stability = Column(String(20))
    renewable_percentage = Column(Float)
    storage_soc_percent = Column(Float)
    
    # Metrics
    carbon_intensity = Column(Float)
    efficiency = Column(Float)
    
    # Store full data as JSON
    full_data = Column(JSON)


class AIDecision(Base):
    """Store AI decisions for audit trail"""
    __tablename__ = 'ai_decisions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Decision details
    agent_id = Column(String(50), index=True)
    decision_type = Column(String(50), index=True)
    decision = Column(Text)
    reasoning = Column(Text)
    
    # Metrics
    confidence = Column(Float)
    impact = Column(String(20))  # low, medium, high, critical
    
    # Explainability
    input_data = Column(JSON)
    explainability_score = Column(Float)
    
    # User tracking (optional)
    user_id = Column(String(50), default='system')


class SystemMetrics(Base):
    """Store system performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Agent performance
    agent_id = Column(String(50))
    total_requests = Column(Integer)
    successful_requests = Column(Integer)
    failed_requests = Column(Integer)
    average_response_time = Column(Float)
    
    # System health
    uptime_hours = Column(Float)
    error_count = Column(Integer)
    
    # Store detailed metrics
    metrics_data = Column(JSON)


class UserSession(Base):
    """Store user sessions for security tracking"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True)
    
    # Session info
    created_at = Column(DateTime, default=datetime.now)
    last_activity = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime)
    
    # User info (if authenticated)
    user_id = Column(String(50), default='anonymous')
    ip_address = Column(String(50))
    
    # Session data
    is_active = Column(Boolean, default=True)
    session_data = Column(JSON)


class ForecastAccuracy(Base):
    """Track forecast accuracy over time"""
    __tablename__ = 'forecast_accuracy'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    
    # Forecast info
    forecast_type = Column(String(50))  # weather, demand, renewable
    forecast_horizon = Column(Integer)  # hours ahead
    
    # Accuracy metrics
    predicted_value = Column(Float)
    actual_value = Column(Float)
    error_percentage = Column(Float)
    mae = Column(Float)  # Mean Absolute Error
    rmse = Column(Float)  # Root Mean Square Error
    
    # Context
    city = Column(String(100))
    conditions = Column(JSON)
