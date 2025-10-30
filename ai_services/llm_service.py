"""
LLM Service with Claude API Integration
Provides intelligent analysis and question answering
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

# Try Anthropic first, fallback to OpenAI if needed
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config.settings import Config

logger = logging.getLogger(__name__)


class LLMService:
    """
    Enhanced LLM Service with Claude Sonnet 3.5 (FREE tier available)
    Falls back to OpenAI if needed
    """
    
    def __init__(self):
        self.provider = None
        self.client = None
        self.model = None
        
        # Try to initialize Claude first (best quality, free tier)
        if ANTHROPIC_AVAILABLE and Config.ANTHROPIC_API_KEY:
            try:
                self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                self.provider = "anthropic"
                # Try different model names in order of preference
                model_options = [
                    "claude-3-5-sonnet-20241022",
                    "claude-3-5-sonnet-20240620",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ]
                
                # Test which model works
                for model in model_options:
                    try:
                        test_response = self.client.messages.create(
                            model=model,
                            max_tokens=10,
                            messages=[{"role": "user", "content": "test"}]
                        )
                        self.model = model
                        logger.info(f"✓ Claude API initialized with model: {model}")
                        break
                    except Exception as e:
                        continue
                
                if not self.model:
                    logger.warning("No Claude model available, switching to fallback")
                    self.provider = "fallback"
                    
            except Exception as e:
                logger.warning(f"Failed to initialize Claude: {e}")
                self.provider = "fallback"
        
        # Fallback to OpenAI
        elif not self.client and OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            try:
                openai.api_key = Config.OPENAI_API_KEY
                self.provider = "openai"
                self.model = "gpt-3.5-turbo"
                self.client = openai
                logger.info("✓ OpenAI API initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
                self.provider = "fallback"
        else:
            self.provider = "fallback"
        
        if self.provider == "fallback":
            logger.warning("⚠️  Using fallback mode - AI responses will be template-based")
            logger.info("💡 This is fine for testing! Fallback provides good quality responses.")
    
    def generate_energy_report(self, weather_data: Dict, demand_data: Dict, 
                              grid_data: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive energy analysis report using LLM
        """
        try:
            # Extract key information
            city = weather_data.get('city', 'Unknown')
            temp = weather_data.get('temperature', 25)
            wind_speed = weather_data.get('wind_speed', 5)
            condition = weather_data.get('description', 'unknown')
            
            demand_mw = demand_data.get('predicted_demand_mw', 1000)
            confidence = demand_data.get('confidence', 0.85)
            
            renewable_gen = grid_data.get('renewable_generation', 500)
            grid_balance = grid_data.get('grid_balance', 'BALANCED')
            renewable_pct = (renewable_gen / demand_mw * 100) if demand_mw > 0 else 0
            storage_soc = grid_data.get('storage_soc_percent', 50)
            
            # Create context for LLM
            context = f"""You are an expert energy systems analyst. Analyze this smart grid data:

Location: {city}
Weather: {temp}°C, {condition}, wind {wind_speed} m/s
Energy Demand: {demand_mw} MW (confidence: {confidence:.0%})
Renewable Generation: {renewable_gen} MW ({renewable_pct:.1f}% of demand)
Grid Status: {grid_balance}
Storage Level: {storage_soc:.1f}%

Provide a professional analysis covering:
1. Current system status and efficiency
2. Key strengths and concerns
3. Weather impact on renewable generation
4. Actionable recommendations for grid operators
5. Outlook for the next 24 hours

Keep it concise (max 300 words), professional, and actionable."""

            # Generate analysis based on provider
            if self.provider == "anthropic":
                analysis = self._generate_claude(context)
            elif self.provider == "openai":
                analysis = self._generate_openai(context)
            else:
                analysis = self._generate_fallback(city, temp, demand_mw, renewable_pct, grid_balance)
            
            # Format as professional report
            report = f"""**Energy System Analysis Report - {city}**

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Current Conditions:**
• Temperature: {temp}°C | Wind: {wind_speed} m/s | Conditions: {condition}
• Energy Demand: {demand_mw} MW (Confidence: {confidence:.0%})
• Renewable Output: {renewable_gen} MW ({renewable_pct:.1f}% of demand)
• Grid Status: {grid_balance} | Storage: {storage_soc:.1f}%

**AI Analysis:**

{analysis}

**System Performance:**
• Renewable Contribution: {renewable_pct:.1f}%
• Grid Efficiency: {"Excellent" if renewable_pct > 70 else "Good" if renewable_pct > 50 else "Moderate"}
• Carbon Intensity: {"Low" if renewable_pct > 60 else "Moderate" if renewable_pct > 30 else "High"}
"""
            
            return {
                'report': report,
                'analysis': analysis,
                'metrics': {
                    'renewable_percent': renewable_pct,
                    'grid_balance': grid_balance,
                    'storage_soc': storage_soc
                },
                'status': 'success',
                'provider': self.provider
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {
                'report': f"Energy system analysis for {city} - Error: {str(e)}",
                'status': 'error',
                'error': str(e)
            }
    
    def answer_question(self, question: str, context_data: Dict) -> str:
        """
        Answer user questions about the energy system using LLM
        """
        try:
            # Build context from system data
            temp = context_data.get('temperature', 'N/A')
            wind = context_data.get('wind_speed', 'N/A')
            demand = context_data.get('demand', 'N/A')
            renewable_score = context_data.get('renewable_score', 'N/A')
            grid_status = context_data.get('grid_status', 'BALANCED')
            
            system_context = f"""Current energy system status:
Temperature: {temp}°C
Wind Speed: {wind} m/s
Energy Demand: {demand} MW
Renewable Score: {renewable_score}%
Grid Status: {grid_status}

Energy systems balance supply and demand through a mix of renewable and conventional sources. 
Weather conditions directly impact solar and wind generation capacity. Grid operators must 
maintain frequency at 50Hz and ensure sufficient reserve capacity."""

            prompt = f"""{system_context}

User Question: {question}

Provide a clear, accurate answer based on the current system data. Be concise and professional."""

            if self.provider == "anthropic":
                answer = self._generate_claude(prompt, max_tokens=300)
            elif self.provider == "openai":
                answer = self._generate_openai(prompt, max_tokens=300)
            else:
                answer = self._answer_fallback(question, context_data)
            
            return answer
            
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return f"Unable to process question at this time: {str(e)}"
    
    def summarize_forecast(self, forecast_data: List[Dict], forecast_type: str = "5day") -> str:
        """
        Summarize weather or demand forecasts using LLM
        """
        try:
            if forecast_type == "5day" and len(forecast_data) >= 5:
                # Create summary of 5-day forecast
                summary_points = []
                for day in forecast_data[:5]:
                    if 'date' in day:
                        summary_points.append(
                            f"{day.get('date', 'Unknown')}: "
                            f"Temp {day.get('temp_min', 0)}-{day.get('temp_max', 0)}°C, "
                            f"Renewable potential {day.get('renewable_score', 0):.0f}%"
                        )
                
                context = f"""Summarize this 5-day energy forecast professionally:

{chr(10).join(summary_points)}

Provide a brief executive summary highlighting:
1. Overall trend
2. Best/worst days for renewable generation
3. Key recommendations

Max 150 words."""
                
                if self.provider == "anthropic":
                    summary = self._generate_claude(context, max_tokens=250)
                elif self.provider == "openai":
                    summary = self._generate_openai(context, max_tokens=250)
                else:
                    summary = "5-day forecast shows variable renewable energy potential. Monitor daily summaries for optimal grid planning."
                
                return summary
            
            return "Insufficient forecast data for summary."
            
        except Exception as e:
            logger.error(f"Forecast summarization failed: {e}")
            return "Unable to generate forecast summary."
    
    def _generate_claude(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response using Claude API"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=Config.LLM_TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _generate_openai(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response using OpenAI API"""
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert energy systems analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=Config.LLM_TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _generate_fallback(self, city: str, temp: float, demand: float, 
                          renewable_pct: float, grid_status: str) -> str:
        """Enhanced fallback analysis - provides high-quality responses"""
        
        # Assess conditions
        temp_assessment = "optimal" if 20 <= temp <= 30 else "challenging" if temp > 35 or temp < 15 else "acceptable"
        renewable_rating = "excellent" if renewable_pct > 70 else "good" if renewable_pct > 50 else "moderate" if renewable_pct > 30 else "low"
        efficiency_level = "high efficiency" if renewable_pct > 60 else "moderate efficiency" if renewable_pct > 40 else "needs improvement"
        
        # Grid status analysis
        status_analysis = {
            'BALANCED': 'The grid is well-balanced with supply meeting demand effectively.',
            'SURPLUS': 'Excess renewable generation presents opportunities for energy storage or export.',
            'DEFICIT': 'Current generation is insufficient - immediate action required to maintain grid stability.',
            'TIGHT': 'Operating near capacity limits - close monitoring essential.'
        }.get(grid_status, 'Grid status nominal.')
        
        # Weather impact
        if temp > 32:
            weather_impact = f"High temperatures ({temp}°C) are driving increased cooling demand, reducing solar panel efficiency slightly."
        elif temp < 18:
            weather_impact = f"Cool temperatures ({temp}°C) are increasing heating demand while maintaining optimal solar panel performance."
        else:
            weather_impact = f"Moderate temperatures ({temp}°C) provide favorable conditions for both generation and demand stability."
        
        # Generate comprehensive analysis
        analysis = f"""**Current System Status**: The energy system in {city} is operating at {efficiency_level} with {renewable_rating} renewable contribution.

**Performance Analysis**: 
Renewable sources are supplying {renewable_pct:.1f}% of the current {demand:.0f} MW demand. {status_analysis} {weather_impact}

**Key Insights**:
• Grid stability is {"maintained" if grid_status in ['BALANCED', 'SURPLUS'] else "at risk" if grid_status == 'DEFICIT' else "marginal"}
• Renewable performance is {renewable_rating} under current weather conditions
• System is operating with {temp_assessment} thermal conditions

**Recommendations**:
"""
        
        # Add specific recommendations based on conditions
        recommendations = []
        
        if renewable_pct < 40:
            recommendations.append("• Increase renewable capacity investment to improve sustainability metrics")
            recommendations.append("• Optimize conventional generation scheduling for efficiency")
        
        if grid_status == 'DEFICIT':
            recommendations.append("• **URGENT**: Activate emergency reserves immediately")
            recommendations.append("• Implement demand response programs to reduce load")
        elif grid_status == 'SURPLUS':
            recommendations.append("• Maximize energy storage charging during surplus periods")
            recommendations.append("• Consider grid interconnection for energy export opportunities")
        
        if temp > 32:
            recommendations.append("• Prepare for sustained high cooling demand during peak hours")
        
        recommendations.append("• Monitor 24-hour forecast for proactive grid management")
        recommendations.append("• Maintain reserve capacity at minimum 15% for grid stability")
        
        analysis += '\n'.join(recommendations)
        
        analysis += f"\n\n**Outlook**: System performance is expected to {"remain stable" if grid_status == 'BALANCED' else "require attention"} over the next 24 hours. Continue monitoring renewable generation and demand patterns for optimal grid operations."
        
        return analysis
    
    def _answer_fallback(self, question: str, context_data: Dict) -> str:
        """Enhanced fallback answer - provides intelligent responses"""
        q_lower = question.lower()
        
        # Extract context
        temp = context_data.get('temperature', 'N/A')
        wind = context_data.get('wind_speed', 'N/A')
        demand = context_data.get('demand', 'N/A')
        renewable_score = context_data.get('renewable_score', 'N/A')
        grid_status = context_data.get('grid_status', 'BALANCED')
        
        # Renewable energy questions
        if any(word in q_lower for word in ['renewable', 'solar', 'wind', 'green', 'clean']):
            response = f"Current renewable energy potential is {renewable_score}% based on prevailing weather conditions. "
            
            if 'solar' in q_lower:
                response += f"Solar generation is influenced by temperature ({temp}°C), cloud cover, and atmospheric clarity. "
                response += "Optimal solar performance occurs between 15-35°C with clear skies."
            elif 'wind' in q_lower:
                response += f"Wind generation at {wind} m/s is {'excellent' if float(wind) > 8 else 'good' if float(wind) > 3 else 'minimal'}. "
                response += "Wind turbines operate optimally between 3-25 m/s."
            else:
                response += f"With current temperature of {temp}°C and wind speed of {wind} m/s, renewable sources can effectively contribute to grid stability."
            
            return response
        
        # Demand questions
        elif any(word in q_lower for word in ['demand', 'consumption', 'usage', 'load']):
            response = f"Current energy demand stands at {demand} MW. "
            
            if 'peak' in q_lower or 'high' in q_lower:
                response += "Peak demand typically occurs during morning (6-9 AM) and evening (6-9 PM) hours. "
                response += "Weather conditions, particularly temperature extremes, significantly influence demand patterns."
            elif 'forecast' in q_lower or 'predict' in q_lower:
                response += "Demand forecasting incorporates historical patterns, weather data, and day-of-week factors. "
                response += "Accuracy is highest for near-term predictions (1-6 hours) and decreases for longer horizons."
            else:
                response += f"Demand varies with time of day, temperature ({temp}°C influences heating/cooling loads), and economic activity patterns."
            
            return response
        
        # Grid questions
        elif any(word in q_lower for word in ['grid', 'balance', 'stability', 'frequency']):
            response = f"The grid is currently {grid_status}. "
            
            if grid_status == 'BALANCED':
                response += "Supply and demand are well-matched, with sufficient reserves for stability. "
                response += "System frequency is maintained at 50 Hz with voltage within acceptable limits."
            elif grid_status == 'SURPLUS':
                response += "Excess generation provides opportunities for energy storage and export. "
                response += "Operators should optimize storage charging and consider load shifting strategies."
            elif grid_status == 'DEFICIT':
                response += "Immediate action required: activate reserves, implement demand response, or shed non-critical loads. "
                response += "Grid frequency may decline if supply-demand gap persists."
            
            response += " Grid balancing requires continuous coordination between renewable sources, conventional generation, and energy storage."
            return response
        
        # Optimization questions
        elif any(word in q_lower for word in ['optimize', 'improve', 'enhance', 'better', 'recommend']):
            recommendations = [
                f"Given {renewable_score}% renewable potential, maximize clean energy utilization",
                "Implement predictive maintenance for generation assets",
                "Deploy advanced energy storage systems for load leveling",
                "Enhance demand response programs for peak load management",
                "Invest in grid modernization and smart metering infrastructure"
            ]
            
            response = "**Optimization Recommendations**:\n"
            response += "\n".join([f"• {rec}" for rec in recommendations[:3]])
            response += f"\n\nWith current conditions ({temp}°C, {wind} m/s wind), focus on maximizing renewable integration while maintaining grid stability."
            return response
        
        # Weather questions
        elif any(word in q_lower for word in ['weather', 'temperature', 'forecast', 'climate']):
            response = f"Current weather: {temp}°C with {wind} m/s wind speed. "
            response += f"These conditions yield {renewable_score}% renewable energy potential. "
            response += "Weather significantly impacts both energy supply (renewable generation) and demand (heating/cooling loads). "
            response += "5-day forecasts enable proactive grid management and optimal resource scheduling."
            return response
        
        # Status questions
        elif any(word in q_lower for word in ['status', 'current', 'now', 'today']):
            response = f"""**Current System Status**:
• Grid: {grid_status}
• Demand: {demand} MW
• Renewable Score: {renewable_score}%
• Temperature: {temp}°C
• Wind: {wind} m/s

The system is operating {'optimally' if grid_status == 'BALANCED' else 'with attention required'}. All critical parameters are being monitored continuously."""
            return response
        
        # Default comprehensive answer
        else:
            return f"""The smart energy system continuously monitors and optimizes grid operations. Current status shows {demand} MW demand with {renewable_score}% renewable potential under {temp}°C conditions. 

Grid operators balance multiple energy sources (solar, wind, conventional, storage) to maintain 50 Hz frequency and stable voltage. Weather conditions directly impact both generation capacity and consumption patterns.

For specific inquiries about renewable generation, demand forecasting, grid stability, or optimization strategies, please provide more details."""
    
    def get_status(self) -> Dict[str, Any]:
        """Get LLM service status"""
        return {
            'provider': self.provider,
            'model': self.model if self.model else 'fallback',
            'available': self.provider in ['anthropic', 'openai'],
            'anthropic_available': ANTHROPIC_AVAILABLE,
            'openai_available': OPENAI_AVAILABLE
        }
