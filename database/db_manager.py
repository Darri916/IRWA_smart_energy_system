"""
Database Manager
Handles all database operations with proper error handling
"""

from sqlalchemy import create_engine, desc, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

from config.settings import Config
from .models import (
    Base, WeatherForecast, DemandForecast, GridBalance, 
    AIDecision, SystemMetrics, UserSession, ForecastAccuracy
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Centralized database manager for all operations
    """
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or Config.DATABASE_URL
        self.engine = None
        self.SessionLocal = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            self.engine = create_engine(
                self.db_url,
                echo=Config.DEBUG_MODE,
                pool_pre_ping=True
            )
            
            # Create all tables
            Base.metadata.create_all(self.engine)
            
            # Create session factory
            self.SessionLocal = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            )
            
            logger.info("✓ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close database session"""
        session.close()
    
    # ==================== Weather Forecast Operations ====================
    
    def save_weather_forecast(self, weather_data: Dict[str, Any]) -> int:
        """Save weather forecast to database"""
        session = self.get_session()
        try:
            forecast = WeatherForecast(
                city=weather_data.get('city'),
                temperature=weather_data.get('current_weather', {}).get('temperature'),
                humidity=weather_data.get('current_weather', {}).get('humidity'),
                wind_speed=weather_data.get('current_weather', {}).get('wind_speed'),
                cloud_cover=weather_data.get('current_weather', {}).get('cloud_cover'),
                weather_condition=weather_data.get('current_weather', {}).get('weather_condition'),
                solar_potential=weather_data.get('solar_potential'),
                wind_potential=weather_data.get('wind_potential'),
                renewable_score=weather_data.get('renewable_score'),
                data_source=weather_data.get('data_source'),
                is_real_data=weather_data.get('current_weather', {}).get('real_data', False),
                forecast_data=weather_data
            )
            
            session.add(forecast)
            session.commit()
            
            forecast_id = forecast.id
            logger.info(f"Weather forecast saved: ID={forecast_id}")
            return forecast_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save weather forecast: {e}")
            return None
        finally:
            self.close_session(session)
    
    def get_weather_history(self, city: str, days: int = 7) -> List[Dict]:
        """Get weather history for a city"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            forecasts = session.query(WeatherForecast).filter(
                and_(
                    WeatherForecast.city == city,
                    WeatherForecast.timestamp >= cutoff_date
                )
            ).order_by(desc(WeatherForecast.timestamp)).all()
            
            return [self._weather_to_dict(f) for f in forecasts]
            
        finally:
            self.close_session(session)
    
    # ==================== Demand Forecast Operations ====================
    
    def save_demand_forecast(self, demand_data: Dict[str, Any]) -> int:
        """Save demand forecast to database"""
        session = self.get_session()
        try:
            current = demand_data.get('current_demand', {})
            anomaly = demand_data.get('anomaly_detection', {})
            
            forecast = DemandForecast(
                predicted_demand_mw=current.get('predicted_demand_mw'),
                confidence=current.get('confidence'),
                is_peak_hour=current.get('is_peak_hour'),
                hourly_factor=current.get('factors', {}).get('hourly_factor'),
                seasonal_factor=current.get('factors', {}).get('seasonal_factor'),
                weather_factor=current.get('factors', {}).get('weather_factor'),
                is_weekend=current.get('factors', {}).get('is_weekend'),
                is_anomaly=anomaly.get('is_anomaly', False),
                anomaly_severity=anomaly.get('severity'),
                forecast_data=demand_data
            )
            
            session.add(forecast)
            session.commit()
            
            forecast_id = forecast.id
            logger.info(f"Demand forecast saved: ID={forecast_id}")
            return forecast_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save demand forecast: {e}")
            return None
        finally:
            self.close_session(session)
    
    def get_demand_history(self, days: int = 7) -> List[Dict]:
        """Get demand history"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            forecasts = session.query(DemandForecast).filter(
                DemandForecast.timestamp >= cutoff_date
            ).order_by(desc(DemandForecast.timestamp)).all()
            
            return [self._demand_to_dict(f) for f in forecasts]
            
        finally:
            self.close_session(session)
    
    # ==================== Grid Balance Operations ====================
    
    def save_grid_balance(self, grid_data: Dict[str, Any]) -> int:
        """Save grid balance record"""
        session = self.get_session()
        try:
            balance_result = grid_data.get('balancing_result', {})
            energy_mix = balance_result.get('energy_mix', {})
            renewable_gen = balance_result.get('renewable_generation', {})
            
            balance = GridBalance(
                demand_mw=balance_result.get('demand_mw'),
                total_generation_mw=balance_result.get('total_generation_mw'),
                supply_demand_ratio=balance_result.get('supply_demand_ratio'),
                renewable_generation=renewable_gen.get('total'),
                solar_generation=renewable_gen.get('solar'),
                wind_generation=renewable_gen.get('wind'),
                conventional_generation=energy_mix.get('conventional_used'),
                storage_discharged=energy_mix.get('storage_discharged'),
                storage_charged=energy_mix.get('storage_charged'),
                grid_balance=balance_result.get('grid_balance'),
                stability=balance_result.get('stability'),
                renewable_percentage=balance_result.get('renewable_percentage'),
                storage_soc_percent=balance_result.get('storage_soc_percent'),
                carbon_intensity=balance_result.get('carbon_intensity_gco2_kwh'),
                efficiency=balance_result.get('efficiency'),
                full_data=grid_data
            )
            
            session.add(balance)
            session.commit()
            
            balance_id = balance.id
            logger.info(f"Grid balance saved: ID={balance_id}")
            return balance_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save grid balance: {e}")
            return None
        finally:
            self.close_session(session)
    
    def get_grid_history(self, days: int = 7) -> List[Dict]:
        """Get grid balance history"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            balances = session.query(GridBalance).filter(
                GridBalance.timestamp >= cutoff_date
            ).order_by(desc(GridBalance.timestamp)).all()
            
            return [self._grid_to_dict(b) for b in balances]
            
        finally:
            self.close_session(session)
    
    # ==================== AI Decision Operations ====================
    
    def save_ai_decision(self, decision_data: Dict[str, Any]) -> int:
        """Save AI decision for audit trail"""
        session = self.get_session()
        try:
            decision = AIDecision(
                agent_id=decision_data.get('agent_id'),
                decision_type=decision_data.get('type'),
                decision=decision_data.get('decision'),
                reasoning=decision_data.get('reasoning'),
                confidence=decision_data.get('confidence'),
                impact=decision_data.get('impact'),
                input_data=decision_data.get('input_data'),
                explainability_score=decision_data.get('explainability_score', 0.8),
                user_id=decision_data.get('user_id', 'system')
            )
            
            session.add(decision)
            session.commit()
            
            decision_id = decision.id
            return decision_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save AI decision: {e}")
            return None
        finally:
            self.close_session(session)
    
    def get_decision_history(self, agent_id: str = None, days: int = 7) -> List[Dict]:
        """Get AI decision history"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            query = session.query(AIDecision).filter(
                AIDecision.timestamp >= cutoff_date
            )
            
            if agent_id:
                query = query.filter(AIDecision.agent_id == agent_id)
            
            decisions = query.order_by(desc(AIDecision.timestamp)).all()
            
            return [self._decision_to_dict(d) for d in decisions]
            
        finally:
            self.close_session(session)
    
    # ==================== Statistics & Analytics ====================
    
    def get_system_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Grid statistics
            grid_stats = session.query(
                func.avg(GridBalance.renewable_percentage).label('avg_renewable'),
                func.avg(GridBalance.efficiency).label('avg_efficiency'),
                func.avg(GridBalance.carbon_intensity).label('avg_carbon'),
                func.count(GridBalance.id).label('total_records')
            ).filter(GridBalance.timestamp >= cutoff_date).first()
            
            # Grid balance distribution
            balance_dist = session.query(
                GridBalance.grid_balance,
                func.count(GridBalance.id).label('count')
            ).filter(GridBalance.timestamp >= cutoff_date).group_by(
                GridBalance.grid_balance
            ).all()
            
            # Anomaly count
            anomaly_count = session.query(func.count(DemandForecast.id)).filter(
                and_(
                    DemandForecast.timestamp >= cutoff_date,
                    DemandForecast.is_anomaly == True
                )
            ).scalar()
            
            # AI decisions count
            decision_count = session.query(
                AIDecision.decision_type,
                func.count(AIDecision.id).label('count')
            ).filter(AIDecision.timestamp >= cutoff_date).group_by(
                AIDecision.decision_type
            ).all()
            
            return {
                'period_days': days,
                'grid_statistics': {
                    'avg_renewable_percentage': round(grid_stats.avg_renewable or 0, 2),
                    'avg_efficiency': round(grid_stats.avg_efficiency or 0, 2),
                    'avg_carbon_intensity': round(grid_stats.avg_carbon or 0, 2),
                    'total_records': grid_stats.total_records
                },
                'balance_distribution': {
                    b.grid_balance: b.count for b in balance_dist
                },
                'anomaly_count': anomaly_count,
                'decision_distribution': {
                    d.decision_type: d.count for d in decision_count
                }
            }
            
        finally:
            self.close_session(session)
    
    def search_records(self, query: str, record_type: str = 'all', limit: int = 50) -> List[Dict]:
        """Search records by keyword (Information Retrieval)"""
        session = self.get_session()
        try:
            results = []
            
            if record_type in ['all', 'weather']:
                weather = session.query(WeatherForecast).filter(
                    WeatherForecast.city.contains(query)
                ).limit(limit).all()
                results.extend([{'type': 'weather', 'data': self._weather_to_dict(w)} for w in weather])
            
            if record_type in ['all', 'decisions']:
                decisions = session.query(AIDecision).filter(
                    AIDecision.decision.contains(query)
                ).limit(limit).all()
                results.extend([{'type': 'decision', 'data': self._decision_to_dict(d)} for d in decisions])
            
            return results
            
        finally:
            self.close_session(session)
    
    # ==================== Helper Methods ====================
    
    def _weather_to_dict(self, weather: WeatherForecast) -> Dict:
        """Convert weather record to dictionary"""
        return {
            'id': weather.id,
            'timestamp': weather.timestamp.isoformat(),
            'city': weather.city,
            'temperature': weather.temperature,
            'wind_speed': weather.wind_speed,
            'renewable_score': weather.renewable_score
        }
    
    def _demand_to_dict(self, demand: DemandForecast) -> Dict:
        """Convert demand record to dictionary"""
        return {
            'id': demand.id,
            'timestamp': demand.timestamp.isoformat(),
            'predicted_demand_mw': demand.predicted_demand_mw,
            'confidence': demand.confidence,
            'is_anomaly': demand.is_anomaly
        }
    
    def _grid_to_dict(self, grid: GridBalance) -> Dict:
        """Convert grid record to dictionary"""
        return {
            'id': grid.id,
            'timestamp': grid.timestamp.isoformat(),
            'grid_balance': grid.grid_balance,
            'renewable_percentage': grid.renewable_percentage,
            'efficiency': grid.efficiency
        }
    
    def _decision_to_dict(self, decision: AIDecision) -> Dict:
        """Convert decision record to dictionary"""
        return {
            'id': decision.id,
            'timestamp': decision.timestamp.isoformat(),
            'agent_id': decision.agent_id,
            'decision': decision.decision,
            'confidence': decision.confidence
        }
    
    def cleanup_old_records(self, days: int = 30):
        """Clean up records older than specified days"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Delete old records
            session.query(WeatherForecast).filter(
                WeatherForecast.timestamp < cutoff_date
            ).delete()
            
            session.query(DemandForecast).filter(
                DemandForecast.timestamp < cutoff_date
            ).delete()
            
            session.query(GridBalance).filter(
                GridBalance.timestamp < cutoff_date
            ).delete()
            
            session.commit()
            logger.info(f"Cleaned up records older than {days} days")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Cleanup failed: {e}")
        finally:
            self.close_session(session)
