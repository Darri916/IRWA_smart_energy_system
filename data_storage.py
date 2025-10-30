"""
Enhanced Data Storage and Retrieval System
Adds proper historical data storage and search functionality
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class DataStorageManager:
    """Manages persistent storage of energy system data"""
    
    def __init__(self, db_path: str = "data/energy_system.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Weather data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                city TEXT NOT NULL,
                temperature REAL,
                wind_speed REAL,
                humidity REAL,
                cloud_cover REAL,
                weather_condition TEXT,
                description TEXT,
                solar_potential REAL,
                wind_potential REAL,
                renewable_score REAL,
                data_source TEXT
            )
        ''')
        
        # Demand data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demand_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                predicted_demand_mw REAL,
                confidence REAL,
                daily_factor REAL,
                seasonal_factor REAL,
                weekend_factor REAL
            )
        ''')
        
        # Grid balance data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grid_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                city TEXT,
                demand_mw REAL,
                renewable_generation REAL,
                conventional_needed REAL,
                grid_balance TEXT,
                efficiency REAL
            )
        ''')
        
        # System events/logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT,
                event_type TEXT,
                event_data TEXT
            )
        ''')
        
        # Create indexes for faster searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather_data(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_data(city)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_demand_timestamp ON demand_data(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_grid_timestamp ON grid_data(timestamp)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def store_weather_data(self, weather_result: Dict[str, Any]):
        """Store weather data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            weather_data = weather_result.get('weather_data', {})
            
            cursor.execute('''
                INSERT INTO weather_data 
                (timestamp, city, temperature, wind_speed, humidity, cloud_cover,
                 weather_condition, description, solar_potential, wind_potential,
                 renewable_score, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                weather_data.get('timestamp'),
                weather_data.get('city'),
                weather_data.get('temperature'),
                weather_data.get('wind_speed'),
                weather_data.get('humidity'),
                weather_data.get('cloud_cover'),
                weather_data.get('weather_condition'),
                weather_data.get('description'),
                weather_result.get('solar_potential'),
                weather_result.get('wind_potential'),
                weather_result.get('renewable_score'),
                weather_data.get('api_source')
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Stored weather data for {weather_data.get('city')}")
        except Exception as e:
            logger.error(f"Failed to store weather data: {e}")
    
    def store_demand_data(self, demand_result: Dict[str, Any]):
        """Store demand forecast data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_demand = demand_result.get('current_demand', {})
            factors = current_demand.get('factors', {})
            
            cursor.execute('''
                INSERT INTO demand_data 
                (timestamp, predicted_demand_mw, confidence, daily_factor,
                 seasonal_factor, weekend_factor)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                current_demand.get('timestamp'),
                current_demand.get('predicted_demand_mw'),
                current_demand.get('confidence'),
                factors.get('daily_factor'),
                factors.get('seasonal_factor'),
                factors.get('weekend_factor')
            ))
            
            conn.commit()
            conn.close()
            logger.info("Stored demand data")
        except Exception as e:
            logger.error(f"Failed to store demand data: {e}")
    
    def store_grid_data(self, grid_result: Dict[str, Any], city: str):
        """Store grid balancing data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            balancing = grid_result.get('balancing_result', {})
            
            cursor.execute('''
                INSERT INTO grid_data 
                (timestamp, city, demand_mw, renewable_generation,
                 conventional_needed, grid_balance, efficiency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                grid_result.get('timestamp'),
                city,
                balancing.get('demand_mw'),
                balancing.get('renewable_generation'),
                balancing.get('conventional_needed'),
                balancing.get('grid_balance'),
                balancing.get('efficiency')
            ))
            
            conn.commit()
            conn.close()
            logger.info("Stored grid data")
        except Exception as e:
            logger.error(f"Failed to store grid data: {e}")
    
    def search_data(self, query: str, days: int = 7, 
                   search_type: str = 'all') -> Dict[str, Any]:
        """Search historical data"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            results = []
            
            # Search weather data
            if search_type in ['all', 'weather']:
                cursor.execute('''
                    SELECT * FROM weather_data 
                    WHERE timestamp >= ? 
                    AND (city LIKE ? OR weather_condition LIKE ? OR description LIKE ?)
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''', (start_date, f'%{query}%', f'%{query}%', f'%{query}%'))
                
                weather_results = cursor.fetchall()
                for row in weather_results:
                    results.append({
                        'type': 'Weather',
                        'relevance': 2,  # Calculate proper relevance score
                        'data': dict(row),
                        'timestamp': row['timestamp']
                    })
            
            # Search demand data
            if search_type in ['all', 'demand']:
                cursor.execute('''
                    SELECT * FROM demand_data 
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''', (start_date,))
                
                demand_results = cursor.fetchall()
                for row in demand_results:
                    results.append({
                        'type': 'Demand',
                        'relevance': 2,
                        'data': dict(row),
                        'timestamp': row['timestamp']
                    })
            
            # Search grid data
            if search_type in ['all', 'grid']:
                cursor.execute('''
                    SELECT * FROM grid_data 
                    WHERE timestamp >= ?
                    AND (city LIKE ? OR grid_balance LIKE ?)
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''', (start_date, f'%{query}%', f'%{query}%'))
                
                grid_results = cursor.fetchall()
                for row in grid_results:
                    results.append({
                        'type': 'Grid',
                        'relevance': 2,
                        'data': dict(row),
                        'timestamp': row['timestamp']
                    })
            
            conn.close()
            
            return {
                'query': query,
                'results': results,
                'total_count': len(results),
                'timeframe_days': days
            }
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                'query': query,
                'results': [],
                'total_count': 0,
                'error': str(e)
            }
    
    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get system statistics for dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Get average renewable score
            cursor.execute('''
                SELECT AVG(renewable_score) as avg_renewable,
                       AVG(solar_potential) as avg_solar,
                       AVG(wind_potential) as avg_wind
                FROM weather_data
                WHERE timestamp >= ?
            ''', (start_date,))
            renewable_stats = cursor.fetchone()
            
            # Get average efficiency
            cursor.execute('''
                SELECT AVG(efficiency) as avg_efficiency
                FROM grid_data
                WHERE timestamp >= ?
            ''', (start_date,))
            efficiency_stats = cursor.fetchone()
            
            # Get total records
            cursor.execute('''
                SELECT COUNT(*) FROM weather_data WHERE timestamp >= ?
            ''', (start_date,))
            total_weather = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM demand_data WHERE timestamp >= ?
            ''', (start_date,))
            total_demand = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM grid_data WHERE timestamp >= ?
            ''', (start_date,))
            total_grid = cursor.fetchone()[0]
            
            # Get grid balance distribution
            cursor.execute('''
                SELECT grid_balance, COUNT(*) as count
                FROM grid_data
                WHERE timestamp >= ?
                GROUP BY grid_balance
            ''', (start_date,))
            balance_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'average_renewable': renewable_stats[0] or 0.0,
                'average_solar': renewable_stats[1] or 0.0,
                'average_wind': renewable_stats[2] or 0.0,
                'average_efficiency': efficiency_stats[0] or 0.0,
                'total_records': total_weather + total_demand + total_grid,
                'weather_records': total_weather,
                'demand_records': total_demand,
                'grid_records': total_grid,
                'balance_distribution': balance_distribution,
                'timeframe_days': days
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                'error': str(e),
                'average_renewable': 0.0,
                'average_efficiency': 0.0,
                'total_records': 0
            }
    
    def cleanup_old_data(self, days: int = 30):
        """Remove data older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute('DELETE FROM weather_data WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM demand_data WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM grid_data WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM system_events WHERE timestamp < ?', (cutoff_date,))
            
            conn.commit()
            conn.close()
            logger.info(f"Cleaned up data older than {days} days")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
