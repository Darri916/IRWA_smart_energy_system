import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentStatus
import logging

logger = logging.getLogger(__name__)


class EnergyDemandAgent(BaseAgent):
    """
    Enhanced energy demand forecasting agent with advanced patterns
    """
    
    def __init__(self, agent_id: str = "demand_001"):
        capabilities = [
            "current_demand",
            "hourly_forecast",
            "daily_forecast",
            "peak_detection",
            "anomaly_detection"
        ]
        super().__init__(agent_id, "EnergyDemandAgent", capabilities)
        
        # Demand parameters
        self.base_demand = 1000  # MW
        self.seasonal_variation = 0.2
        self.daily_variation = 0.3
        self.random_variation = 0.1
        
        # Historical pattern learning (simulated)
        self.historical_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Any]:
        """Initialize demand patterns based on typical energy consumption"""
        return {
            'weekday_hourly': [0.7, 0.65, 0.62, 0.6, 0.63, 0.75, 0.9, 1.0, 0.95, 0.85, 0.82, 0.8,
                               0.83, 0.85, 0.87, 0.9, 0.95, 1.0, 0.98, 0.92, 0.88, 0.82, 0.78, 0.73],
            'weekend_hourly': [0.68, 0.64, 0.61, 0.59, 0.6, 0.65, 0.72, 0.8, 0.85, 0.88, 0.9, 0.92,
                               0.93, 0.94, 0.93, 0.91, 0.89, 0.87, 0.84, 0.8, 0.77, 0.74, 0.72, 0.7],
            'monthly_factors': [1.0, 0.98, 0.95, 0.92, 0.9, 0.95, 1.05, 1.1, 1.08, 1.0, 0.97, 1.02],
            'special_events': []  # Can be enhanced with holiday patterns
        }
    
    def predict_current_demand(self, weather_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict current energy demand with weather influence
        
        Weather integration: Higher temps = more AC = higher demand
        """
        current_time = datetime.now()
        hour = current_time.hour
        month = current_time.month
        is_weekend = current_time.weekday() >= 5
        
        # Base demand pattern
        hourly_pattern = (self.historical_patterns['weekend_hourly'] if is_weekend 
                         else self.historical_patterns['weekday_hourly'])
        hourly_factor = hourly_pattern[hour]
        
        # Seasonal pattern (monthly variation)
        seasonal_factor = self.historical_patterns['monthly_factors'][month - 1]
        
        # Weather influence (if available)
        weather_factor = 1.0
        if weather_data:
            temp = weather_data.get('temperature', 25)
            # Higher temperatures increase cooling demand
            if temp > 28:
                weather_factor = 1.0 + (temp - 28) * 0.02
            elif temp < 18:
                weather_factor = 1.0 + (18 - temp) * 0.015  # Heating demand
        
        # Calculate predicted demand
        predicted_demand = (
            self.base_demand * 
            hourly_factor * 
            seasonal_factor * 
            weather_factor
        )
        
        # Add random variation for realism
        predicted_demand *= (1.0 + random.uniform(-self.random_variation, self.random_variation))
        
        # Calculate confidence based on data availability
        confidence = 0.85
        if weather_data and weather_data.get('real_data'):
            confidence = 0.92
        
        # Detect if this is peak demand
        is_peak = hourly_factor > 0.95
        
        result = {
            'timestamp': current_time.isoformat(),
            'predicted_demand_mw': round(predicted_demand, 2),
            'confidence': confidence,
            'is_peak_hour': is_peak,
            'factors': {
                'hourly_factor': round(hourly_factor, 3),
                'seasonal_factor': round(seasonal_factor, 3),
                'weather_factor': round(weather_factor, 3),
                'is_weekend': is_weekend
            }
        }
        
        # Log decision for explainability
        self.log_decision(
            decision=f"Current demand: {predicted_demand:.2f} MW",
            reasoning=f"Hour={hour}, Season={month}, Weather_factor={weather_factor:.2f}, Weekend={is_weekend}",
            confidence=confidence,
            input_data={'hour': hour, 'month': month, 'is_weekend': is_weekend, 
                       'weather': weather_data is not None},
            impact="high"
        )
        
        self.log_action(f"Predicted current demand: {predicted_demand:.2f} MW")
        
        return result
    
    def forecast_24h_demand(self, weather_forecast: List[Dict] = None) -> List[Dict[str, Any]]:
        """
        Generate 24-hour demand forecast with optional weather integration
        """
        forecasts = []
        current_time = datetime.now()
        
        for i in range(24):
            future_time = current_time + timedelta(hours=i)
            hour = future_time.hour
            month = future_time.month
            is_weekend = future_time.weekday() >= 5
            
            # Get hourly pattern
            hourly_pattern = (self.historical_patterns['weekend_hourly'] if is_weekend 
                             else self.historical_patterns['weekday_hourly'])
            hourly_factor = hourly_pattern[hour]
            
            # Seasonal factor
            seasonal_factor = self.historical_patterns['monthly_factors'][month - 1]
            
            # Weather influence (if forecast available)
            weather_factor = 1.0
            if weather_forecast and i < len(weather_forecast):
                temp = weather_forecast[i].get('temperature', 25)
                if temp > 28:
                    weather_factor = 1.0 + (temp - 28) * 0.02
                elif temp < 18:
                    weather_factor = 1.0 + (18 - temp) * 0.015
            
            # Calculate demand
            predicted_demand = (
                self.base_demand * 
                hourly_factor * 
                seasonal_factor * 
                weather_factor
            )
            predicted_demand *= (1.0 + random.uniform(-0.05, 0.05))
            
            forecasts.append({
                'hour': i,
                'timestamp': future_time.isoformat(),
                'predicted_demand_mw': round(predicted_demand, 2),
                'confidence': 0.88 - (i * 0.01),  # Confidence decreases over time
                'is_peak_hour': hourly_factor > 0.95
            })
        
        return forecasts
    
    def forecast_5day_demand(self, weather_forecast_5day: List[Dict] = None) -> List[Dict[str, Any]]:
        """
        Generate 5-day demand forecast aligned with weather forecast
        NEW: Extended forecasting capability
        """
        forecasts = []
        current_time = datetime.now()
        
        # Group weather forecast by day if available
        daily_weather = {}
        if weather_forecast_5day:
            for item in weather_forecast_5day:
                date = item.get('date', item.get('timestamp', '').split('T')[0])
                if date not in daily_weather:
                    daily_weather[date] = []
                daily_weather[date].append(item)
        
        for day in range(5):
            forecast_date = (current_time + timedelta(days=day)).date()
            date_str = forecast_date.isoformat()
            
            # Calculate daily average demand
            daily_demands = []
            
            for hour in range(24):
                future_time = current_time + timedelta(days=day, hours=hour)
                hour_of_day = future_time.hour
                month = future_time.month
                is_weekend = future_time.weekday() >= 5
                
                hourly_pattern = (self.historical_patterns['weekend_hourly'] if is_weekend 
                                 else self.historical_patterns['weekday_hourly'])
                hourly_factor = hourly_pattern[hour_of_day]
                seasonal_factor = self.historical_patterns['monthly_factors'][month - 1]
                
                # Weather influence for this hour
                weather_factor = 1.0
                if date_str in daily_weather and daily_weather[date_str]:
                    # Use average temperature for the day
                    temps = [w.get('temperature', 25) for w in daily_weather[date_str]]
                    avg_temp = sum(temps) / len(temps)
                    if avg_temp > 28:
                        weather_factor = 1.0 + (avg_temp - 28) * 0.02
                    elif avg_temp < 18:
                        weather_factor = 1.0 + (18 - avg_temp) * 0.015
                
                demand = self.base_demand * hourly_factor * seasonal_factor * weather_factor
                daily_demands.append(demand)
            
            # Daily statistics
            avg_demand = sum(daily_demands) / len(daily_demands)
            min_demand = min(daily_demands)
            max_demand = max(daily_demands)
            peak_hour = daily_demands.index(max_demand)
            
            forecasts.append({
                'date': date_str,
                'day_of_week': forecast_date.strftime('%A'),
                'avg_demand_mw': round(avg_demand, 2),
                'min_demand_mw': round(min_demand, 2),
                'max_demand_mw': round(max_demand, 2),
                'peak_hour': peak_hour,
                'confidence': max(0.7, 0.9 - (day * 0.04)),
                'total_energy_mwh': round(avg_demand * 24, 2)
            })
        
        return forecasts
    
    def detect_anomalies(self, current_demand: float, historical_avg: float = None) -> Dict[str, Any]:
        """
        Detect demand anomalies for alert system
        """
        if historical_avg is None:
            historical_avg = self.base_demand
        
        deviation = abs(current_demand - historical_avg) / historical_avg
        
        is_anomaly = deviation > 0.15  # 15% deviation threshold
        severity = "normal"
        
        if deviation > 0.25:
            severity = "critical"
        elif deviation > 0.15:
            severity = "warning"
        
        return {
            'is_anomaly': is_anomaly,
            'severity': severity,
            'deviation_percent': round(deviation * 100, 2),
            'expected_range': {
                'min': round(historical_avg * 0.85, 2),
                'max': round(historical_avg * 1.15, 2)
            }
        }
    
    def process_demand_forecast(self, weather_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main demand forecasting function with comprehensive analysis
        """
        self.set_status(AgentStatus.BUSY)
        self.log_action("Processing comprehensive demand forecast")
        
        try:
            # Current demand prediction
            current_prediction = self.predict_current_demand(
                weather_data.get('current_weather') if weather_data else None
            )
            
            # 24-hour forecast
            weather_24h = None
            if weather_data and 'forecast_5day_detailed' in weather_data:
                weather_24h = weather_data['forecast_5day_detailed'][:8]  # First 24 hours
            
            forecast_24h = self.forecast_24h_demand(weather_24h)
            
            # 5-day forecast
            forecast_5day = self.forecast_5day_demand(
                weather_data.get('forecast_5day_detailed') if weather_data else None
            )
            
            # Anomaly detection
            anomaly_check = self.detect_anomalies(
                current_prediction['predicted_demand_mw']
            )
            
            # Calculate peak demand statistics
            peak_stats = self._calculate_peak_statistics(forecast_24h)
            
            self.set_status(AgentStatus.IDLE)
            
            return {
                'agent_id': self.agent_id,
                'current_demand': current_prediction,
                'forecast_24h': forecast_24h,
                'forecast_5day': forecast_5day,
                'anomaly_detection': anomaly_check,
                'peak_statistics': peak_stats,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            self.log_action(f"Demand forecast failed: {str(e)}", level="error")
            return {
                'agent_id': self.agent_id,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_peak_statistics(self, forecast_24h: List[Dict]) -> Dict[str, Any]:
        """Calculate peak demand statistics"""
        demands = [f['predicted_demand_mw'] for f in forecast_24h]
        
        max_demand = max(demands)
        min_demand = min(demands)
        avg_demand = sum(demands) / len(demands)
        
        peak_hours = [f for f in forecast_24h if f['is_peak_hour']]
        
        return {
            'max_demand_mw': round(max_demand, 2),
            'min_demand_mw': round(min_demand, 2),
            'avg_demand_mw': round(avg_demand, 2),
            'peak_hour_count': len(peak_hours),
            'load_factor': round(avg_demand / max_demand, 3) if max_demand > 0 else 0
        }
