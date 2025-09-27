from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent

class GridBalancerAgent(BaseAgent):
    """Grid balancing and optimization agent"""
    
    def __init__(self, agent_id: str = "grid_001"):
        super().__init__(agent_id, "GridBalancerAgent")
        self.grid_status = {
            'total_capacity': 5000,  # MW
            'renewable_capacity': 2000,  # MW
            'current_load': 0,
            'renewable_generation': 0,
            'grid_frequency': 50.0  # Hz
        }
    
    def calculate_renewable_generation(self, weather_data: Dict[str, Any]) -> float:
        """Calculate renewable energy generation based on weather conditions"""
        if not weather_data:
            return 0
        
        solar_potential = weather_data.get('solar_potential', 0)
        wind_potential = weather_data.get('wind_potential', 0)
        
        # Convert potential percentages to actual generation
        # Assuming 1000 MW solar capacity and 1000 MW wind capacity
        solar_generation = (solar_potential / 100) * 1000
        wind_generation = (wind_potential / 100) * 1000
        
        total_renewable = solar_generation + wind_generation
        self.grid_status['renewable_generation'] = round(total_renewable, 2)
        
        self.log_action(f"Renewable generation calculated: {total_renewable:.2f} MW")
        return total_renewable
    
    def balance_grid(self, demand_mw: float, renewable_generation: float) -> Dict[str, Any]:
        """Balance grid supply and demand"""
        self.grid_status['current_load'] = demand_mw
        
        # Calculate shortfall or surplus
        shortfall = demand_mw - renewable_generation
        
        if shortfall > 0:
            # Need conventional power
            conventional_capacity = self.grid_status['total_capacity'] - self.grid_status['renewable_capacity']
            conventional_needed = min(shortfall, conventional_capacity)
            
            if shortfall > conventional_needed:
                grid_balance = 'DEFICIT'
                recommendations = ["Power shortage - Load shedding may be required"]
            else:
                grid_balance = 'BALANCED'
                recommendations = ["Conventional generators activated to meet demand"]
        else:
            # Surplus renewable energy
            conventional_needed = 0
            grid_balance = 'SURPLUS'
            excess = abs(shortfall)
            recommendations = [
                f"Excess renewable energy: {excess:.2f} MW",
                "Consider energy storage or export to neighboring grids"
            ]
        
        return {
            'demand_mw': demand_mw,
            'renewable_generation': renewable_generation,
            'conventional_needed': conventional_needed,
            'grid_balance': grid_balance,
            'recommendations': recommendations,
            'efficiency': (renewable_generation / demand_mw * 100) if demand_mw > 0 else 0
        }
    
    def coordinate_with_agents(self, weather_result: Dict[str, Any], 
                             demand_result: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents to balance the grid"""
        try:
            # Extract data from other agents
            weather_info = weather_result.get('weather_data', {}) if weather_result else {}
            demand_info = demand_result.get('current_demand', {}) if demand_result else {}
            
            current_demand = demand_info.get('predicted_demand_mw', 1000)
            
            # Calculate renewable generation
            renewable_gen = self.calculate_renewable_generation(weather_info)
            
            # Balance the grid
            balancing_result = self.balance_grid(current_demand, renewable_gen)
            
            self.log_action(f"Grid balanced: {balancing_result['grid_balance']}")
            
            return {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'grid_status': self.grid_status,
                'balancing_result': balancing_result,
                'status': 'success'
            }
            
        except Exception as e:
            self.log_action(f"Grid coordination failed: {str(e)}")
            return {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }