#!/usr/bin/env python3
"""
Smart Renewable Energy Forecasting System
Complete Multi-Agent AI System with Database, Security & UI
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import Config
from agents.weather_agent import WeatherAgent
from agents.demand_agent import EnergyDemandAgent
from agents.grid_agent import GridBalancerAgent
from ai_services.llm_service import LLMService
from ai_services.nlp_service import NLPService
from ai_services.responsible_ai import ResponsibleAI
from database.db_manager import DatabaseManager
from security.security_manager import SecurityManager
from information_retrieval.ir_engine import IREngine

# Configure logging
logging.basicConfig(
    level=logging.INFO if not Config.DEBUG_MODE else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOGS_DIR / 'energy_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SmartEnergySystem:
    """
    Enhanced Main System Coordinator
    Integrates all components: Agents, AI, Database, Security, IR
    """
    
    def __init__(self, enable_ai: bool = True, enable_db: bool = True, 
                 enable_security: bool = True):
        logger.info("="*60)
        logger.info("Initializing Smart Energy Forecasting System v2.0")
        logger.info("="*60)
        
        # Ensure required directories exist
        Config.ensure_directories()
        
        # Initialize core agents
        logger.info("Loading agents...")
        self.weather_agent = WeatherAgent()
        self.demand_agent = EnergyDemandAgent()
        self.grid_agent = GridBalancerAgent()
        logger.info("✓ Agents initialized")
        
        # Initialize AI services
        self.ai_enabled = False
        self.llm_service = None
        self.nlp_service = None
        self.responsible_ai = None
        
        if enable_ai:
            try:
                logger.info("Loading AI services...")
                self.llm_service = LLMService()
                self.nlp_service = NLPService()
                self.responsible_ai = ResponsibleAI()
                self.ai_enabled = True
                logger.info("✓ AI services loaded")
            except Exception as e:
                logger.error(f"AI initialization failed: {e}")
                self.ai_enabled = False
        
        # Initialize database
        self.db_enabled = False
        self.db_manager = None
        
        if enable_db:
            try:
                logger.info("Connecting to database...")
                self.db_manager = DatabaseManager()
                self.db_enabled = True
                logger.info("✓ Database connected")
            except Exception as e:
                logger.error(f"Database initialization failed: {e}")
                self.db_enabled = False
        
        # Initialize security
        self.security_enabled = False
        self.security_manager = None
        
        if enable_security:
            try:
                logger.info("Initializing security...")
                self.security_manager = SecurityManager()
                self.security_enabled = True
                logger.info("✓ Security initialized")
            except Exception as e:
                logger.error(f"Security initialization failed: {e}")
                self.security_enabled = False
        
        # Initialize information retrieval
        self.ir_engine = None
        if self.db_enabled:
            try:
                logger.info("Loading information retrieval...")
                self.ir_engine = IREngine(db_manager=self.db_manager)
                logger.info("✓ IR engine loaded")
            except Exception as e:
                logger.error(f"IR initialization failed: {e}")
        
        logger.info("="*60)
        logger.info(f"System Ready - AI: {self.ai_enabled}, DB: {self.db_enabled}, Security: {self.security_enabled}")
        logger.info("="*60)
    
    def run_energy_forecast(self, city: str = "Colombo", session_id: str = None) -> Dict[str, Any]:
        """
        Run complete energy forecasting cycle with all enhancements
        """
        logger.info(f"Running energy forecast for {city}")
        start_time = datetime.now()
        
        try:
            # Security: Validate input
            if self.security_enabled and self.security_manager:
                city_validation = self.security_manager.validate_city_input(city)
                if not city_validation['valid']:
                    return {
                        'status': 'error',
                        'error': city_validation['error']
                    }
                city = city_validation['sanitized']
            
            # Step 1: Get weather data
            weather_result = self.weather_agent.process_weather_request(city)
            
            # Step 2: Forecast energy demand
            demand_result = self.demand_agent.process_demand_forecast(weather_result)
            
            # Step 3: Balance grid
            grid_result = self.grid_agent.coordinate_with_agents(
                weather_result, demand_result
            )
            
            # Step 4: Generate AI analysis
            ai_result = None
            if self.ai_enabled and self.llm_service:
                try:
                    weather_data = weather_result.get('current_weather', {})
                    demand_data = demand_result.get('current_demand', {})
                    grid_data = grid_result.get('balancing_result', {})
                    
                    ai_result = self.llm_service.generate_energy_report(
                        weather_data, demand_data, grid_data
                    )
                except Exception as e:
                    logger.error(f"AI analysis failed: {e}")
                    ai_result = {'status': 'error', 'error': str(e)}
            
            # Step 5: Save to database
            if self.db_enabled and self.db_manager:
                try:
                    self.db_manager.save_weather_forecast(weather_result)
                    self.db_manager.save_demand_forecast(demand_result)
                    self.db_manager.save_grid_balance(grid_result)
                except Exception as e:
                    logger.error(f"Database save failed: {e}")
            
            # Step 6: Log for responsible AI
            if self.responsible_ai:
                try:
                    self.responsible_ai.log_decision({
                        'type': 'energy_forecast',
                        'decision': f'Forecast generated for {city}',
                        'reasoning': 'Multi-agent coordination completed successfully',
                        'confidence': demand_result.get('current_demand', {}).get('confidence', 0.85),
                        'input_data': {'city': city},
                        'impact': 'high',
                        'agent_id': 'system'
                    })
                except Exception as e:
                    logger.error(f"Responsible AI logging failed: {e}")
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'city': city,
                'timestamp': weather_result.get('timestamp'),
                'weather': weather_result,
                'demand': demand_result,
                'grid': grid_result,
                'ai_analysis': ai_result,
                'execution_time': execution_time,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Forecast cycle failed: {e}")
            return {
                'city': city,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def answer_question(self, question: str, city: str = "Colombo") -> Dict[str, Any]:
        """Enhanced question answering with NLP"""
        if not self.ai_enabled:
            return {
                'answer': "AI services not available",
                'status': 'unavailable'
            }
        
        try:
            # Classify intent
            intent = None
            if self.nlp_service:
                intent = self.nlp_service.classify_intent(question)
            
            # Get current system state
            forecast_result = self.run_energy_forecast(city)
            
            if forecast_result['status'] != 'success':
                return {
                    'answer': "Unable to get current system data",
                    'status': 'error'
                }
            
            # Prepare context
            weather_data = forecast_result['weather'].get('current_weather', {})
            demand_data = forecast_result['demand'].get('current_demand', {})
            
            context = {
                'temperature': weather_data.get('temperature'),
                'wind_speed': weather_data.get('wind_speed'),
                'demand': demand_data.get('predicted_demand_mw'),
                'renewable_score': forecast_result['weather'].get('renewable_score'),
                'grid_status': forecast_result['grid'].get('balancing_result', {}).get('grid_balance')
            }
            
            answer = self.llm_service.answer_question(question, context)
            
            return {
                'question': question,
                'answer': answer,
                'intent': intent,
                'city': city,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return {
                'question': question,
                'answer': f"Unable to process question: {str(e)}",
                'status': 'error'
            }
    
    def search_history(self, query: str, filters: Dict = None) -> Dict[str, Any]:
        """Search historical data using IR engine"""
        if not self.ir_engine:
            return {
                'query': query,
                'results': [],
                'status': 'unavailable'
            }
        
        try:
            results = self.ir_engine.search(query, filters=filters)
            results['status'] = 'success'
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                'query': query,
                'error': str(e),
                'status': 'error'
            }
    
    def get_system_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        if not self.db_enabled:
            return {'status': 'unavailable'}
        
        try:
            stats = self.db_manager.get_system_statistics(days)
            stats['status'] = 'success'
            return stats
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def create_session(self, user_id: str = 'anonymous', ip_address: str = None) -> Dict[str, Any]:
        """Create user session"""
        if not self.security_enabled:
            return {'status': 'unavailable'}
        
        return self.security_manager.create_session(user_id, ip_address)
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate user session"""
        if not self.security_enabled:
            return {'valid': True}  # Allow if security disabled
        
        return self.security_manager.validate_session(session_id)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'agents': {
                'weather': self.weather_agent.get_status(),
                'demand': self.demand_agent.get_status(),
                'grid': self.grid_agent.get_status()
            },
            'services': {
                'ai_enabled': self.ai_enabled,
                'database_enabled': self.db_enabled,
                'security_enabled': self.security_enabled,
                'ir_enabled': self.ir_engine is not None
            }
        }
        
        if self.ai_enabled and self.llm_service:
            status['services']['llm_status'] = self.llm_service.get_status()
        
        if self.security_enabled and self.security_manager:
            status['services']['security_status'] = self.security_manager.get_status()
        
        return status
    
    def display_system_status(self):
        """Display system status in console"""
        print("\n" + "="*60)
        print("SMART ENERGY FORECASTING SYSTEM - STATUS")
        print("="*60)
        
        status = self.get_system_status()
        
        print(f"\n🤖 Agents:")
        for agent_name, agent_status in status['agents'].items():
            print(f"   {agent_name.title()}: {agent_status['status']}")
        
        print(f"\n⚙️  Services:")
        services = status['services']
        print(f"   AI: {'✓ Active' if services['ai_enabled'] else '✗ Inactive'}")
        print(f"   Database: {'✓ Active' if services['database_enabled'] else '✗ Inactive'}")
        print(f"   Security: {'✓ Active' if services['security_enabled'] else '✗ Inactive'}")
        print(f"   IR: {'✓ Active' if services['ir_enabled'] else '✗ Inactive'}")
        
        if services['ai_enabled'] and 'llm_status' in services:
            llm = services['llm_status']
            print(f"\n🧠 AI Status:")
            print(f"   Provider: {llm['provider']}")
            print(f"   Model: {llm['model']}")
        
        print("\n" + "="*60)


def main():
    """Main entry point"""
    try:
        # Initialize system
        system = SmartEnergySystem(
            enable_ai=True,
            enable_db=True,
            enable_security=True
        )
        
        # Display status
        system.display_system_status()
        
        # Run sample forecast
        print("\n🔄 Running sample forecast for Colombo...")
        result = system.run_energy_forecast("Colombo")
        
        if result['status'] == 'success':
            print(f"\n✅ Forecast completed in {result['execution_time']:.2f}s")
            print(f"   City: {result['city']}")
            print(f"   Renewable Score: {result['weather']['renewable_score']:.1f}%")
            print(f"   Grid Balance: {result['grid']['balancing_result']['grid_balance']}")
            
        print("\n🎨 Launch UI with: python web/gradio_interface.py")
        
    except KeyboardInterrupt:
        print("\n\nSystem shutdown requested.")
    except Exception as e:
        logger.error(f"System error: {e}")
        print(f"\n❌ System error: {e}")


if __name__ == "__main__":
    main()
