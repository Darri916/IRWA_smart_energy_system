#!/usr/bin/env python3
"""
Smart Energy Forecasting System
Multi-Agent AI System with LLM Integration
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import Config
from agents.weather_agent import WeatherAgent
from agents.demand_agent import EnergyDemandAgent
from agents.grid_agent import GridBalancerAgent
from models.ai_models import AIModelManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('energy_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SmartEnergySystem:
    """Main system coordinator for the Smart Energy Forecasting System"""
    
    def __init__(self, enable_ai: bool = True):
        logger.info("Initializing Smart Energy System...")
        
        # Ensure required directories exist
        Config.ensure_directories()
        
        # Initialize agents
        self.weather_agent = WeatherAgent()
        self.demand_agent = EnergyDemandAgent()
        self.grid_agent = GridBalancerAgent()
        
        # Initialize AI models
        self.ai_enabled = False
        if enable_ai:
            try:
                self.ai_manager = AIModelManager()
                self.ai_enabled = True
                logger.info("AI models loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load AI models: {e}")
                self.ai_manager = None
        else:
            self.ai_manager = None
        
        logger.info(f"System initialized - AI: {'Enabled' if self.ai_enabled else 'Disabled'}")
    
    def run_energy_forecast(self, city: str = "Colombo") -> Dict[str, Any]:
        """Run complete energy forecasting cycle"""
        logger.info(f"Running energy forecast for {city}")
        
        try:
            # Step 1: Get weather data
            weather_result = self.weather_agent.process_weather_request(city)
            
            # Step 2: Forecast energy demand
            demand_result = self.demand_agent.process_demand_forecast()
            
            # Step 3: Balance grid
            grid_result = self.grid_agent.coordinate_with_agents(
                weather_result, demand_result
            )
            
            # Step 4: Generate AI analysis (if available)
            ai_result = None
            if self.ai_enabled and self.ai_manager:
                try:
                    weather_data = weather_result.get('weather_data', {})
                    demand_data = demand_result.get('current_demand', {})
                    grid_data = grid_result.get('grid_status', {})
                    
                    ai_result = self.ai_manager.generate_energy_report(
                        weather_data, demand_data, grid_data
                    )
                except Exception as e:
                    logger.error(f"AI analysis failed: {e}")
                    ai_result = {'status': 'error', 'error': str(e)}
            
            return {
                'city': city,
                'timestamp': weather_result.get('timestamp'),
                'weather': weather_result,
                'demand': demand_result,
                'grid': grid_result,
                'ai_analysis': ai_result,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Forecast cycle failed: {e}")
            return {
                'city': city,
                'status': 'error',
                'error': str(e)
            }
    
    def answer_question(self, question: str, city: str = "Colombo") -> str:
        """Answer user questions using AI"""
        if not self.ai_enabled:
            return "AI question answering is not available."
        
        try:
            # Get current system state
            forecast_result = self.run_energy_forecast(city)
            
            if forecast_result['status'] != 'success':
                return "Unable to get current system data for question answering."
            
            # Prepare context
            weather_data = forecast_result['weather'].get('weather_data', {})
            demand_data = forecast_result['demand'].get('current_demand', {})
            
            context = {
                'temperature': weather_data.get('temperature'),
                'wind_speed': weather_data.get('wind_speed'),
                'demand': demand_data.get('predicted_demand_mw'),
                'renewable_score': forecast_result['weather'].get('renewable_score'),
                'grid_status': forecast_result['grid'].get('balancing_result', {}).get('grid_balance')
            }
            
            return self.ai_manager.answer_question(question, context)
            
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return f"Unable to process question: {str(e)}"
    
    def generate_report(self, city: str = "Colombo") -> str:
        """Generate comprehensive system report"""
        forecast_result = self.run_energy_forecast(city)
        
        if forecast_result['status'] != 'success':
            return f"Error generating report: {forecast_result.get('error', 'Unknown error')}"
        
        # Basic report
        weather_data = forecast_result['weather'].get('weather_data', {})
        demand_data = forecast_result['demand'].get('current_demand', {})
        grid_data = forecast_result['grid'].get('grid_status', {})
        
        report = f"""
# Energy System Report - {city}
**Generated**: {forecast_result.get('timestamp', 'N/A')}

## Weather Conditions
- Temperature: {weather_data.get('temperature', 'N/A')}°C
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s
- Conditions: {weather_data.get('description', weather_data.get('weather_condition', 'N/A'))}

## Energy Metrics
- Current Demand: {demand_data.get('predicted_demand_mw', 'N/A')} MW
- Renewable Generation: {grid_data.get('renewable_generation', 'N/A')} MW
- Grid Status: {forecast_result['grid'].get('balancing_result', {}).get('grid_balance', 'N/A')}

## Renewable Potential
- Solar Potential: {forecast_result['weather'].get('solar_potential', 'N/A')}%
- Wind Potential: {forecast_result['weather'].get('wind_potential', 'N/A')}%
"""
        
        # Add AI analysis if available
        if self.ai_enabled and forecast_result.get('ai_analysis'):
            ai_report = forecast_result['ai_analysis'].get('report', '')
            if ai_report:
                report += f"\n## AI Analysis\n{ai_report}"
        
        return report
    
    def display_system_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("SMART ENERGY SYSTEM STATUS")
        print("="*60)
        print(f"Weather Agent: {self.weather_agent.get_status()['status']}")
        print(f"Demand Agent: {self.demand_agent.get_status()['status']}")
        print(f"Grid Agent: {self.grid_agent.get_status()['status']}")
        print(f"AI Models: {'Active' if self.ai_enabled else 'Inactive'}")
        print("="*60)

def main():
    """Main entry point"""
    try:
        # Initialize system
        system = SmartEnergySystem(enable_ai=True)
        
        # Display status
        system.display_system_status()
        
        # Run sample forecast
        print("\nRunning sample forecast for Jaffna...")
        result = system.run_energy_forecast("Jaffna")
        
        if result['status'] == 'success':
            print("\n" + "="*50)
            print("FORECAST RESULTS")
            print("="*50)
            
            weather = result['weather']['weather_data']
            demand = result['demand']['current_demand']
            grid = result['grid']['balancing_result']
            
            print(f"City: {result['city']}")
            print(f"Weather: {weather.get('temperature', 'N/A')}°C, {weather.get('description', 'N/A')}")
            print(f"Demand: {demand.get('predicted_demand_mw', 'N/A')} MW")
            print(f"Grid Status: {grid.get('grid_balance', 'N/A')}")
            print(f"Renewable Score: {result['weather'].get('renewable_score', 'N/A')}%")
            
            if system.ai_enabled and result.get('ai_analysis'):
                print(f"\nAI Analysis Available: {result['ai_analysis']['status'] == 'success'}")
        else:
            print(f"Forecast failed: {result.get('error')}")
        
        # Test AI question answering
        if system.ai_enabled:
            print("\nTesting AI Question Answering...")
            question = "What is the current renewable energy potential?"
            answer = system.answer_question(question, "Jaffna")
            print(f"Q: {question}")
            print(f"A: {answer}")
        
    except KeyboardInterrupt:
        print("\nSystem shutdown requested.")
    except Exception as e:
        logger.error(f"System error: {e}")
        print(f"System error: {e}")

if __name__ == "__main__":
    main()