from transformers import pipeline
import torch
from datetime import datetime
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class AIModelManager:
    """Simplified and optimized AI model manager"""
    
    def __init__(self, use_gpu: bool = True):
        self.device = 0 if torch.cuda.is_available() and use_gpu else -1
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load essential AI models with error handling"""
        model_configs = [
            {
                'name': 'summarizer',
                'task': 'summarization',
                'model': 'facebook/bart-large-cnn',
                'fallback': 'sshleifer/distilbart-cnn-12-6'
            },
            {
                'name': 'qa',
                'task': 'question-answering',
                'model': 'deepset/roberta-base-squad2',
                'fallback': 'distilbert-base-cased-distilled-squad'
            },
            {
                'name': 'generator',
                'task': 'text-generation',
                'model': 'gpt2',
                'fallback': 'gpt2'
            },
            {
                'name': 'sentiment',
                'task': 'sentiment-analysis',
                'model': 'nlptown/bert-base-multilingual-uncased-sentiment',
                'fallback': 'cardiffnlp/twitter-roberta-base-sentiment-latest'
            }
        ]
        
        for config in model_configs:
            try:
                logger.info(f"Loading {config['name']} model: {config['model']}")
                self.models[config['name']] = pipeline(
                    config['task'],
                    model=config['model'],
                    device=self.device
                )
                logger.info(f" {config['name']} model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load {config['model']}, trying fallback: {e}")
                try:
                    self.models[config['name']] = pipeline(
                        config['task'],
                        model=config['fallback'],
                        device=self.device
                    )
                    logger.info(f"{config['name']} fallback model loaded")
                except Exception as e2:
                    logger.error(f"Failed to load fallback model for {config['name']}: {e2}")
    
    def generate_energy_report(self, weather_data: Dict, demand_data: Dict, grid_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive energy analysis report"""
        try:
            city = weather_data.get('city', 'Unknown')
            temp = weather_data.get('temperature', 25)
            wind_speed = weather_data.get('wind_speed', 5)
            demand_mw = demand_data.get('predicted_demand_mw', 1000)
            renewable_gen = grid_data.get('renewable_generation', 500)
            grid_balance = grid_data.get('grid_balance', 'BALANCED')
            
            # Calculate key metrics
            renewable_percent = (renewable_gen / demand_mw * 100) if demand_mw > 0 else 0
            efficiency = min(100, renewable_percent)
            
            # Generate analysis using text generation model
            if 'generator' in self.models:
                prompt = f"Energy analysis for {city}: {temp}°C, {wind_speed}m/s wind, {demand_mw}MW demand, {renewable_gen}MW renewable generation. Grid status: {grid_balance}."
                
                try:
                    response = self.models['generator'](
                        prompt,
                        max_length=len(prompt.split()) + 50,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=50256
                    )
                    generated_text = response[0]['generated_text'].replace(prompt, "").strip()
                except Exception as e:
                    generated_text = "Analysis generation temporarily unavailable."
                    logger.warning(f"Text generation failed: {e}")
            else:
                generated_text = "Text generation model not available."
            
            # Format professional report
            report = f"""**Energy System Analysis Report - {city}**
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Current Conditions:**
• Temperature: {temp}°C | Wind Speed: {wind_speed} m/s
• Energy Demand: {demand_mw} MW | Renewable Output: {renewable_gen} MW
• Grid Status: {grid_balance} | Renewable Efficiency: {efficiency:.1f}%

**Analysis:**
{generated_text}

**Key Metrics:**
• Renewable contribution: {renewable_percent:.1f}% of demand
• Weather suitability: {"Excellent" if efficiency > 70 else "Good" if efficiency > 50 else "Moderate"}
• System status: Operating {"efficiently" if efficiency > 60 else "within normal parameters"}"""
            
            return {
                'report': report,
                'metrics': {
                    'renewable_percent': renewable_percent,
                    'efficiency': efficiency,
                    'grid_balance': grid_balance
                },
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {
                'report': f"Energy system report for {city} - Analysis temporarily unavailable",
                'metrics': {},
                'status': 'error',
                'error': str(e)
            }
    
    def answer_question(self, question: str, context_data: Dict) -> str:
        """Answer questions about energy system using Q&A model"""
        try:
            if 'qa' not in self.models:
                return "Question answering temporarily unavailable."
            
            # Create context from system data
            context = f"""Current energy system status:
Temperature: {context_data.get('temperature', 'N/A')}°C
Wind speed: {context_data.get('wind_speed', 'N/A')} m/s  
Energy demand: {context_data.get('demand', 'N/A')} MW
Renewable generation: {context_data.get('renewable_gen', 'N/A')} MW
Grid status: {context_data.get('grid_status', 'BALANCED')}

Energy systems require balancing supply and demand. Renewable sources depend on weather conditions. Grid operators monitor frequency and voltage continuously."""
            
            result = self.models['qa']({
                'question': question,
                'context': context
            })
            
            confidence = result['score']
            answer = result['answer']
            
            if confidence > 0.3:
                return f"{answer} (Confidence: {confidence:.1%})"
            else:
                return self._get_fallback_answer(question, context_data)
                
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return "Unable to process question at this time."
    
    def _get_fallback_answer(self, question: str, context_data: Dict) -> str:
        """Provide fallback answers based on keywords"""
        question_lower = question.lower()
        
        if 'renewable' in question_lower:
            renewable_gen = context_data.get('renewable_gen', 'N/A')
            return f"Current renewable generation is {renewable_gen} MW. Renewable potential depends on weather conditions."
        
        elif 'solar' in question_lower:
            temp = context_data.get('temperature', 25)
            return f"Solar generation efficiency at {temp}°C is {'optimal' if 20 <= temp <= 35 else 'suboptimal'}."
        
        elif 'wind' in question_lower:
            wind = context_data.get('wind_speed', 0)
            return f"Wind conditions at {wind} m/s are {'excellent' if wind > 8 else 'good' if wind > 3 else 'insufficient'} for generation."
        
        elif 'grid' in question_lower or 'balance' in question_lower:
            return f"Grid is currently {context_data.get('grid_status', 'balanced')} with renewable sources contributing to the energy mix."
        
        else:
            return "Energy system operations require continuous monitoring of generation, demand, and grid stability."
    
    def summarize_text(self, text: str, max_length: int = 130) -> str:
        """Summarize long text content"""
        try:
            if 'summarizer' not in self.models or len(text) < 100:
                return text
            
            summary = self.models['summarizer'](
                text,
                max_length=max_length,
                min_length=40,
                do_sample=False
            )
            return summary[0]['summary_text']
            
        except Exception as e:
            logger.error(f"Text summarization failed: {e}")
            # Fallback to extractive summarization
            sentences = text.split('.')[:3]
            return '. '.join(sentences).strip() + '.'