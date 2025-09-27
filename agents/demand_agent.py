import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent

class EnergyDemandAgent(BaseAgent):
    """Energy demand forecasting agent"""
    
    def __init__(self, agent_id: str = "demand_001"):
        super().__init__(agent_id, "EnergyDemandAgent")
    
    def predict_current_demand(self) -> Dict[str, Any]:
        """Predict current energy demand based on time patterns"""
        current_time = datetime.now()
        hour = current_time.hour
        month = current_time.month
        is_weekend = current_time.weekday() >= 5
        
        # Base demand pattern
        base_demand = 1000  # MW
        
        # Daily pattern (peak during 6-9 AM and 6-9 PM)
        daily_factor = 0.7 + 0.3 * np.sin((hour - 6) * np.pi / 12)
        
        # Seasonal pattern (higher in summer months)
        seasonal_factor = 0.8 + 0.2 * np.cos((month - 1) * np.pi / 6)
        
        # Weekend factor (lower demand on weekends)
        weekend_factor = 0.85 if is_weekend else 1.0
        
        # Calculate predicted demand with some randomness
        predicted_demand = (base_demand * daily_factor * 
                          seasonal_factor * weekend_factor)
        predicted_demand *= (0.95 + 0.1 * random.random())
        
        confidence = random.uniform(0.85, 0.95)
        
        self.log_action(f"Predicted current demand: {predicted_demand:.2f} MW")
        
        return {
            'timestamp': current_time.isoformat(),
            'predicted_demand_mw': round(predicted_demand, 2),
            'confidence': confidence,
            'factors': {
                'daily_factor': daily_factor,
                'seasonal_factor': seasonal_factor,
                'weekend_factor': weekend_factor
            }
        }
    
    def forecast_24h_demand(self) -> List[Dict[str, Any]]:
        """Generate 24-hour demand forecast"""
        forecasts = []
        current_time = datetime.now()
        
        for i in range(24):
            future_time = current_time + timedelta(hours=i)
            hour = future_time.hour
            is_weekend = future_time.weekday() >= 5
            
            # Daily pattern
            daily_factor = 0.7 + 0.3 * np.sin((hour - 6) * np.pi / 12)
            
            # Weekend adjustment
            weekend_factor = 0.85 if is_weekend else 1.0
            
            # Base demand with variation
            predicted_demand = 1000 * daily_factor * weekend_factor
            predicted_demand *= (0.95 + 0.1 * random.random())
            
            forecasts.append({
                'hour': i,
                'timestamp': future_time.isoformat(),
                'predicted_demand_mw': round(predicted_demand, 2)
            })
        
        return forecasts
    
    def process_demand_forecast(self) -> Dict[str, Any]:
        """Main demand forecasting function"""
        self.log_action("Processing demand forecast")
        
        current_prediction = self.predict_current_demand()
        forecast_24h = self.forecast_24h_demand()
        
        return {
            'agent_id': self.agent_id,
            'current_demand': current_prediction,
            'forecast_24h': forecast_24h,
            'timestamp': datetime.now().isoformat()
        }