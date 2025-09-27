import requests
import random
from datetime import datetime
from typing import Dict, Any
from .base_agent import BaseAgent
from config.settings import Config

class WeatherAgent(BaseAgent):
    """Weather data collection and renewable energy potential calculation"""
    
    def __init__(self, agent_id: str = "weather_001"):
        super().__init__(agent_id, "WeatherAgent")
        self.api_key = Config.get_weather_api_key()
        self.base_url = Config.WEATHER_BASE_URL
        
    def fetch_weather_data(self, city: str = "Colombo") -> Dict[str, Any]:
        """Fetch real weather data from OpenWeatherMap API"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'timestamp': datetime.now().isoformat(),
                    'city': city,
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'cloud_cover': data['clouds']['all'],
                    'weather_condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'pressure': data['main'].get('pressure', 1013),
                    'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
                    'real_data': True,
                    'api_source': 'OpenWeatherMap'
                }
                
                self.log_action(f"Real weather data fetched for {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C")
                return weather_info
            else:
                self.log_action(f"API Error {response.status_code}, using sample data")
                return self._generate_sample_weather(city)
                
        except Exception as e:
            self.log_action(f"Weather API error: {str(e)}, using sample data")
            return self._generate_sample_weather(city)
    
    def _generate_sample_weather(self, city: str) -> Dict[str, Any]:
        """Generate sample weather data for demonstration"""
        return {
            'timestamp': datetime.now().isoformat(),
            'city': city,
            'temperature': random.uniform(20, 35),
            'humidity': random.uniform(40, 90),
            'wind_speed': random.uniform(0, 15),
            'cloud_cover': random.uniform(0, 100),
            'weather_condition': random.choice(['Clear', 'Clouds', 'Rain', 'Sunny']),
            'description': 'sample data for demonstration',
            'pressure': random.uniform(990, 1030),
            'visibility': random.uniform(5, 15),
            'real_data': False,
            'api_source': 'Sample Generator'
        }
    
    def calculate_solar_potential(self, weather_data: Dict[str, Any]) -> float:
        """Calculate solar energy generation potential (0-100%) - FIXED"""
        temp = weather_data['temperature']
        cloud_cover = weather_data['cloud_cover']
        humidity = weather_data['humidity']
        visibility = weather_data.get('visibility', 10)
        
        # Optimal temperature range for solar panels: 15-35°C (wider range)
        if 15 <= temp <= 35:
            temp_factor = 100 - abs(temp - 25) * 1.5  # Reduced penalty
        else:
            temp_factor = max(0, 100 - abs(temp - 25) * 3)
        
        # Cloud cover impact (less harsh penalty)
        cloud_factor = max(10, 100 - cloud_cover * 0.8)  # Minimum 10% even in overcast
        
        # Humidity factor (less impact)
        humidity_factor = max(20, 100 - humidity * 0.6)  # Minimum 20%
        
        # Visibility factor
        visibility_factor = min(100, visibility * 8)
        
        # Weighted average with adjusted weights
        solar_potential = (
            temp_factor * 0.3 + 
            cloud_factor * 0.4 + 
            humidity_factor * 0.15 + 
            visibility_factor * 0.15
        )
        
        return min(100, max(5, solar_potential))  # Minimum 5% potential
    
    def calculate_wind_potential(self, weather_data: Dict[str, Any]) -> float:
        """Calculate wind energy generation potential (0-100%) - IMPROVED"""
        wind_speed = weather_data['wind_speed']
        
        # Improved wind turbine efficiency curve
        if wind_speed < 2:  # Below cut-in speed
            return 0
        elif wind_speed < 3:  # Cut-in range
            return wind_speed * 15  # Up to 45%
        elif 3 <= wind_speed <= 12:  # Optimal range
            # Progressive increase to 100%
            return 45 + (wind_speed - 3) * 6.1  # Up to ~100% at 12 m/s
        elif 12 < wind_speed <= 25:  # High wind range
            return 100  # Maximum efficiency
        else:  # Above rated speed
            return max(0, 100 - (wind_speed - 25) * 4)  # Safety cutoff
    
    def process_weather_request(self, city: str = "Colombo") -> Dict[str, Any]:
        """Main weather processing function"""
        self.log_action(f"Processing weather request for {city}")
        
        # Fetch weather data
        weather_data = self.fetch_weather_data(city)
        
        # Calculate renewable potential
        solar_potential = self.calculate_solar_potential(weather_data)
        wind_potential = self.calculate_wind_potential(weather_data)
        renewable_score = (solar_potential + wind_potential) / 2
        
        # Log the calculations for debugging
        self.log_action(f"Solar: {solar_potential:.1f}%, Wind: {wind_potential:.1f}%, Combined: {renewable_score:.1f}%")
        
        return {
            'agent_id': self.agent_id,
            'weather_data': weather_data,
            'solar_potential': solar_potential,
            'wind_potential': wind_potential,
            'renewable_score': renewable_score,
            'data_source': weather_data.get('api_source', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }