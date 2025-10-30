import requests
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import time
from .base_agent import BaseAgent, AgentStatus
from config.settings import Config

import logging
logger = logging.getLogger(__name__)


class WeatherAgent(BaseAgent):
    """
    Enhanced weather agent with 5-day forecasting and renewable energy potential
    """
    
    def __init__(self, agent_id: str = "weather_001"):
        capabilities = [
            "current_weather",
            "5day_forecast",
            "solar_potential",
            "wind_potential",
            "renewable_scoring"
        ]
        super().__init__(agent_id, "WeatherAgent", capabilities)
        
        self.api_key = Config.get_api_key('openweather')
        self.base_url = Config.WEATHER_BASE_URL
        self.cache = {}
        self.cache_ttl = Config.CACHE_TTL
    
    def fetch_current_weather(self, city: str = "Colombo") -> Dict[str, Any]:
        """Fetch current weather data from OpenWeatherMap API"""
        try:
            # Check cache first
            cache_key = f"current_{city}"
            if self._is_cache_valid(cache_key):
                self.log_action(f"Cache hit for current weather: {city}")
                return self.cache[cache_key]['data']
            
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                weather_info = {
                    'timestamp': datetime.now().isoformat(),
                    'city': city,
                    'country': data['sys'].get('country', 'N/A'),
                    'coordinates': {
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon']
                    },
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'temp_min': data['main']['temp_min'],
                    'temp_max': data['main']['temp_max'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_deg': data['wind'].get('deg', 0),
                    'cloud_cover': data['clouds']['all'],
                    'weather_condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'visibility': data.get('visibility', 10000) / 1000,
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                    'real_data': True,
                    'api_source': 'OpenWeatherMap'
                }
                
                # Cache the result
                self._cache_data(cache_key, weather_info)
                
                self.update_metrics(True, response_time)
                self.log_action(
                    f"Real weather data fetched for {city}: {weather_info['description']}, {weather_info['temperature']}°C",
                    metadata={'response_time': response_time}
                )
                
                return weather_info
            else:
                self.log_action(f"API Error {response.status_code}, using sample data", level="warning")
                self.update_metrics(False, response_time)
                return self._generate_sample_weather(city)
                
        except Exception as e:
            self.log_action(f"Weather API error: {str(e)}, using sample data", level="error")
            self.update_metrics(False, 0)
            return self._generate_sample_weather(city)
    
    def fetch_5day_forecast(self, city: str = "Colombo") -> List[Dict[str, Any]]:
        """
        Fetch 5-day weather forecast (3-hour intervals)
        This is the NEW enhanced feature!
        """
        try:
            # Check cache first
            cache_key = f"forecast_{city}"
            if self._is_cache_valid(cache_key):
                self.log_action(f"Cache hit for 5-day forecast: {city}")
                return self.cache[cache_key]['data']
            
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': 40  # 5 days * 8 (3-hour intervals)
            }
            
            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                forecast_list = []
                for item in data['list']:
                    forecast_item = {
                        'timestamp': item['dt_txt'],
                        'date': datetime.fromtimestamp(item['dt']).date().isoformat(),
                        'time': datetime.fromtimestamp(item['dt']).time().isoformat(),
                        'temperature': item['main']['temp'],
                        'feels_like': item['main']['feels_like'],
                        'temp_min': item['main']['temp_min'],
                        'temp_max': item['main']['temp_max'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure'],
                        'wind_speed': item['wind']['speed'],
                        'wind_deg': item['wind'].get('deg', 0),
                        'cloud_cover': item['clouds']['all'],
                        'weather_condition': item['weather'][0]['main'],
                        'description': item['weather'][0]['description'],
                        'pop': item.get('pop', 0) * 100,  # Probability of precipitation
                        'rain_3h': item.get('rain', {}).get('3h', 0),
                        'snow_3h': item.get('snow', {}).get('3h', 0)
                    }
                    forecast_list.append(forecast_item)
                
                # Cache the result
                self._cache_data(cache_key, forecast_list)
                
                self.update_metrics(True, response_time)
                self.log_action(
                    f"5-day forecast fetched for {city}: {len(forecast_list)} data points",
                    metadata={'response_time': response_time}
                )
                
                return forecast_list
            else:
                self.log_action(f"API Error {response.status_code}, using sample forecast", level="warning")
                self.update_metrics(False, response_time)
                return self._generate_sample_forecast(city)
                
        except Exception as e:
            self.log_action(f"Forecast API error: {str(e)}, using sample data", level="error")
            self.update_metrics(False, 0)
            return self._generate_sample_forecast(city)
    
    def get_daily_summary(self, forecast_list: List[Dict]) -> List[Dict[str, Any]]:
        """
        Aggregate 3-hour forecast into daily summaries
        """
        daily_data = {}
        
        for item in forecast_list:
            date = item['date']
            
            if date not in daily_data:
                daily_data[date] = {
                    'temperatures': [],
                    'humidity': [],
                    'wind_speed': [],
                    'cloud_cover': [],
                    'conditions': [],
                    'rain': 0,
                    'pop': []
                }
            
            daily_data[date]['temperatures'].append(item['temperature'])
            daily_data[date]['humidity'].append(item['humidity'])
            daily_data[date]['wind_speed'].append(item['wind_speed'])
            daily_data[date]['cloud_cover'].append(item['cloud_cover'])
            daily_data[date]['conditions'].append(item['weather_condition'])
            daily_data[date]['rain'] += item['rain_3h']
            daily_data[date]['pop'].append(item['pop'])
        
        # Create daily summaries
        summaries = []
        for date, data in sorted(daily_data.items()):
            summary = {
                'date': date,
                'temp_avg': round(sum(data['temperatures']) / len(data['temperatures']), 1),
                'temp_min': round(min(data['temperatures']), 1),
                'temp_max': round(max(data['temperatures']), 1),
                'humidity_avg': round(sum(data['humidity']) / len(data['humidity']), 0),
                'wind_speed_avg': round(sum(data['wind_speed']) / len(data['wind_speed']), 1),
                'wind_speed_max': round(max(data['wind_speed']), 1),
                'cloud_cover_avg': round(sum(data['cloud_cover']) / len(data['cloud_cover']), 0),
                'total_rain': round(data['rain'], 2),
                'pop_max': round(max(data['pop']), 0),
                'dominant_condition': max(set(data['conditions']), key=data['conditions'].count)
            }
            
            # Calculate renewable potential for the day
            summary['solar_potential'] = self.calculate_solar_potential({
                'temperature': summary['temp_avg'],
                'cloud_cover': summary['cloud_cover_avg'],
                'humidity': summary['humidity_avg'],
                'visibility': 10  # Assume good visibility
            })
            
            summary['wind_potential'] = self.calculate_wind_potential({
                'wind_speed': summary['wind_speed_avg']
            })
            
            summary['renewable_score'] = (summary['solar_potential'] + summary['wind_potential']) / 2
            
            summaries.append(summary)
        
        return summaries
    
    def calculate_solar_potential(self, weather_data: Dict[str, Any]) -> float:
        """Calculate solar energy generation potential (0-100%)"""
        temp = weather_data['temperature']
        cloud_cover = weather_data['cloud_cover']
        humidity = weather_data['humidity']
        visibility = weather_data.get('visibility', 10)
        
        # Optimal temperature range for solar panels: 15-35°C
        if 15 <= temp <= 35:
            temp_factor = 100 - abs(temp - 25) * 1.5
        else:
            temp_factor = max(0, 100 - abs(temp - 25) * 3)
        
        # Cloud cover impact
        cloud_factor = max(10, 100 - cloud_cover * 0.8)
        
        # Humidity factor
        humidity_factor = max(20, 100 - humidity * 0.6)
        
        # Visibility factor
        visibility_factor = min(100, visibility * 8)
        
        # Weighted average
        solar_potential = (
            temp_factor * 0.3 +
            cloud_factor * 0.4 +
            humidity_factor * 0.15 +
            visibility_factor * 0.15
        )
        
        result = min(100, max(5, solar_potential))
        
        # Log decision for explainability
        self.log_decision(
            decision=f"Solar potential: {result:.1f}%",
            reasoning=f"Based on temp ({temp}°C), clouds ({cloud_cover}%), humidity ({humidity}%)",
            confidence=0.85,
            input_data=weather_data,
            impact="high"
        )
        
        return result
    
    def calculate_wind_potential(self, weather_data: Dict[str, Any]) -> float:
        """Calculate wind energy generation potential (0-100%)"""
        wind_speed = weather_data['wind_speed']
        
        # Wind turbine efficiency curve
        if wind_speed < 2:
            potential = 0
        elif wind_speed < 3:
            potential = wind_speed * 15
        elif 3 <= wind_speed <= 12:
            potential = 45 + (wind_speed - 3) * 6.1
        elif 12 < wind_speed <= 25:
            potential = 100
        else:
            potential = max(0, 100 - (wind_speed - 25) * 4)
        
        # Log decision for explainability
        self.log_decision(
            decision=f"Wind potential: {potential:.1f}%",
            reasoning=f"Based on wind speed {wind_speed} m/s",
            confidence=0.90,
            input_data=weather_data,
            impact="high"
        )
        
        return potential
    
    def process_weather_request(self, city: str = "Colombo") -> Dict[str, Any]:
        """
        Main weather processing function with comprehensive data
        """
        self.set_status(AgentStatus.BUSY)
        self.log_action(f"Processing comprehensive weather request for {city}")
        
        try:
            # Fetch current weather
            current_weather = self.fetch_current_weather(city)
            
            # Fetch 5-day forecast
            forecast_5day = self.fetch_5day_forecast(city)
            
            # Generate daily summaries
            daily_summaries = self.get_daily_summary(forecast_5day)
            
            # Calculate current renewable potential
            solar_potential = self.calculate_solar_potential(current_weather)
            wind_potential = self.calculate_wind_potential(current_weather)
            renewable_score = (solar_potential + wind_potential) / 2
            
            self.set_status(AgentStatus.IDLE)
            
            return {
                'agent_id': self.agent_id,
                'city': city,
                'current_weather': current_weather,
                'solar_potential': solar_potential,
                'wind_potential': wind_potential,
                'renewable_score': renewable_score,
                'forecast_5day_detailed': forecast_5day,
                'forecast_5day_daily': daily_summaries,
                'data_source': current_weather.get('api_source', 'Unknown'),
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            self.log_action(f"Weather processing failed: {str(e)}", level="error")
            return {
                'agent_id': self.agent_id,
                'city': city,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_sample_weather(self, city: str) -> Dict[str, Any]:
        """Generate sample weather data for demonstration"""
        return {
            'timestamp': datetime.now().isoformat(),
            'city': city,
            'country': 'XX',
            'coordinates': {'lat': 0.0, 'lon': 0.0},
            'temperature': random.uniform(20, 35),
            'feels_like': random.uniform(20, 35),
            'temp_min': random.uniform(18, 25),
            'temp_max': random.uniform(28, 38),
            'humidity': random.uniform(40, 90),
            'pressure': random.uniform(990, 1030),
            'wind_speed': random.uniform(0, 15),
            'wind_deg': random.uniform(0, 360),
            'cloud_cover': random.uniform(0, 100),
            'weather_condition': random.choice(['Clear', 'Clouds', 'Rain', 'Sunny']),
            'description': 'sample data for demonstration',
            'visibility': random.uniform(5, 15),
            'sunrise': datetime.now().replace(hour=6, minute=0).isoformat(),
            'sunset': datetime.now().replace(hour=18, minute=30).isoformat(),
            'real_data': False,
            'api_source': 'Sample Generator'
        }
    
    def _generate_sample_forecast(self, city: str) -> List[Dict[str, Any]]:
        """Generate sample 5-day forecast"""
        forecast = []
        base_time = datetime.now()
        
        for i in range(40):  # 5 days * 8 intervals
            forecast_time = base_time + timedelta(hours=i*3)
            forecast.append({
                'timestamp': forecast_time.isoformat(),
                'date': forecast_time.date().isoformat(),
                'time': forecast_time.time().isoformat(),
                'temperature': random.uniform(20, 35),
                'feels_like': random.uniform(20, 35),
                'temp_min': random.uniform(18, 25),
                'temp_max': random.uniform(28, 38),
                'humidity': random.uniform(40, 90),
                'pressure': random.uniform(990, 1030),
                'wind_speed': random.uniform(0, 15),
                'wind_deg': random.uniform(0, 360),
                'cloud_cover': random.uniform(0, 100),
                'weather_condition': random.choice(['Clear', 'Clouds', 'Rain']),
                'description': 'sample forecast',
                'pop': random.uniform(0, 100),
                'rain_3h': random.uniform(0, 5) if random.random() > 0.7 else 0,
                'snow_3h': 0
            })
        
        return forecast
    
    def _cache_data(self, key: str, data: Any) -> None:
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]['timestamp']
        return (time.time() - cached_time) < self.cache_ttl
