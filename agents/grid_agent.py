from datetime import datetime
from typing import Dict, Any, List, Tuple
from .base_agent import BaseAgent, AgentStatus
from config.settings import Config
import logging

logger = logging.getLogger(__name__)


class GridBalancerAgent(BaseAgent):
    """
    Enhanced grid balancing and optimization agent with smart algorithms
    """
    
    def __init__(self, agent_id: str = "grid_001"):
        capabilities = [
            "real_time_balancing",
            "load_optimization",
            "renewable_integration",
            "storage_management",
            "frequency_regulation",
            "voltage_control"
        ]
        super().__init__(agent_id, "GridBalancerAgent", capabilities)
        
        self.grid_status = {
            'total_capacity': Config.GRID_TOTAL_CAPACITY,
            'renewable_capacity': Config.GRID_RENEWABLE_CAPACITY,
            'storage_capacity': Config.STORAGE_CAPACITY,
            'current_load': 0,
            'renewable_generation': 0,
            'conventional_generation': 0,
            'storage_level': Config.STORAGE_CAPACITY * 0.5,  # Start at 50%
            'grid_frequency': 50.0,  # Hz
            'voltage_level': 1.0  # per unit
        }
        
        # Performance tracking
        self.balancing_history = []
    
    def calculate_renewable_generation(self, weather_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate renewable energy generation from weather data
        Returns breakdown by source
        """
        if not weather_data:
            return {'solar': 0, 'wind': 0, 'total': 0}
        
        solar_potential = weather_data.get('solar_potential', 0)
        wind_potential = weather_data.get('wind_potential', 0)
        
        # Convert potential percentages to actual generation
        solar_generation = (solar_potential / 100) * Config.SOLAR_CAPACITY
        wind_generation = (wind_potential / 100) * Config.WIND_CAPACITY
        
        total_renewable = solar_generation + wind_generation
        
        self.grid_status['renewable_generation'] = round(total_renewable, 2)
        
        self.log_action(
            f"Renewable generation: Solar={solar_generation:.1f}MW, Wind={wind_generation:.1f}MW, Total={total_renewable:.1f}MW"
        )
        
        return {
            'solar': round(solar_generation, 2),
            'wind': round(wind_generation, 2),
            'total': round(total_renewable, 2)
        }
    
    def optimize_energy_mix(self, demand_mw: float, renewable_available: float) -> Dict[str, Any]:
        """
        Optimize energy mix considering storage and conventional sources
        
        Priority:
        1. Use renewable energy first
        2. Use stored energy if available
        3. Use conventional generation
        4. Alert if shortfall
        """
        # Start with renewable energy
        remaining_demand = demand_mw - renewable_available
        
        # Energy sources breakdown
        energy_mix = {
            'renewable_used': min(renewable_available, demand_mw),
            'storage_discharged': 0,
            'conventional_used': 0,
            'storage_charged': 0,
            'curtailed_renewable': 0
        }
        
        if remaining_demand > 0:
            # Need more energy - check storage
            available_storage = self.grid_status['storage_level']
            storage_discharge = min(remaining_demand, available_storage * 0.8)  # Max 80% discharge rate
            
            energy_mix['storage_discharged'] = round(storage_discharge, 2)
            self.grid_status['storage_level'] -= storage_discharge
            remaining_demand -= storage_discharge
            
            if remaining_demand > 0:
                # Need conventional generation
                conventional_capacity = (
                    self.grid_status['total_capacity'] - 
                    self.grid_status['renewable_capacity']
                )
                conventional_needed = min(remaining_demand, conventional_capacity)
                energy_mix['conventional_used'] = round(conventional_needed, 2)
                self.grid_status['conventional_generation'] = conventional_needed
                remaining_demand -= conventional_needed
        
        elif remaining_demand < 0:
            # Surplus renewable energy - charge storage
            surplus = abs(remaining_demand)
            storage_capacity_available = (
                self.grid_status['storage_capacity'] - 
                self.grid_status['storage_level']
            )
            
            # Charge storage (max 80% charge rate)
            storage_charge = min(surplus, storage_capacity_available * 0.8)
            energy_mix['storage_charged'] = round(storage_charge, 2)
            self.grid_status['storage_level'] += storage_charge
            
            # Remaining surplus is curtailed or exported
            energy_mix['curtailed_renewable'] = round(surplus - storage_charge, 2)
        
        # Log optimization decision
        self.log_decision(
            decision=f"Energy mix optimized for {demand_mw:.1f} MW demand",
            reasoning=f"Renewable: {energy_mix['renewable_used']:.1f}MW, Storage: {energy_mix['storage_discharged']:.1f}MW, Conventional: {energy_mix['conventional_used']:.1f}MW",
            confidence=0.95,
            input_data={'demand': demand_mw, 'renewable': renewable_available},
            impact="critical"
        )
        
        return energy_mix
    
    def balance_grid(self, demand_mw: float, renewable_generation: Dict[str, float]) -> Dict[str, Any]:
        """
        Comprehensive grid balancing with multiple energy sources
        """
        self.grid_status['current_load'] = demand_mw
        total_renewable = renewable_generation['total']
        
        # Optimize energy mix
        energy_mix = self.optimize_energy_mix(demand_mw, total_renewable)
        
        # Calculate total generation
        total_generation = (
            energy_mix['renewable_used'] +
            energy_mix['storage_discharged'] +
            energy_mix['conventional_used']
        )
        
        # Determine grid balance status
        supply_demand_ratio = total_generation / demand_mw if demand_mw > 0 else 1.0
        
        if supply_demand_ratio >= 0.99:
            if supply_demand_ratio > 1.15:
                grid_balance = 'SURPLUS'
                stability = 'stable'
            else:
                grid_balance = 'BALANCED'
                stability = 'optimal'
        elif supply_demand_ratio >= 0.90:
            grid_balance = 'TIGHT'
            stability = 'marginal'
        else:
            grid_balance = 'DEFICIT'
            stability = 'critical'
        
        # Calculate grid metrics
        renewable_percentage = (total_renewable / demand_mw * 100) if demand_mw > 0 else 0
        storage_soc = (self.grid_status['storage_level'] / 
                      self.grid_status['storage_capacity'] * 100)
        
        # Calculate carbon intensity (approximate)
        carbon_intensity = self._calculate_carbon_intensity(energy_mix, demand_mw)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            grid_balance, energy_mix, storage_soc, renewable_percentage
        )
        
        # Calculate efficiency
        efficiency = min(100, renewable_percentage)

        stability_index = self.calculate_grid_stability_index()
        
        balancing_result = {
            'demand_mw': round(demand_mw, 2),
            'total_generation_mw': round(total_generation, 2),
            'supply_demand_ratio': round(supply_demand_ratio, 3),
            'renewable_generation': renewable_generation,
            'energy_mix': energy_mix,
            'grid_balance': grid_balance,
            'stability': stability,
            'renewable_percentage': round(renewable_percentage, 2),
            'storage_soc_percent': round(storage_soc, 2),
            'carbon_intensity_gco2_kwh': round(carbon_intensity, 2),
            'efficiency': round(efficiency, 2),
            'recommendations': recommendations,
            'grid_frequency_hz': self.grid_status['grid_frequency'],
            'stability_index': stability_index,
            'voltage_pu': self.grid_status['voltage_level']
        }
        
        # Store in history
        self.balancing_history.append({
            'timestamp': datetime.now().isoformat(),
            'result': balancing_result
        })
        
        # Keep only last 100 records
        if len(self.balancing_history) > 100:
            self.balancing_history.pop(0)
        
        return balancing_result
    
    def _calculate_carbon_intensity(self, energy_mix: Dict, demand_mw: float) -> float:
        """
        Calculate carbon intensity in gCO2/kWh
        
        Assumptions:
        - Renewable: 0 gCO2/kWh
        - Storage: 0 gCO2/kWh (charged from renewables)
        - Conventional (natural gas): 450 gCO2/kWh
        """
        if demand_mw == 0:
            return 0
        
        conventional_kwh = energy_mix['conventional_used'] * 1000  # MW to kW
        total_kwh = demand_mw * 1000
        
        carbon_emissions = conventional_kwh * 450  # gCO2
        carbon_intensity = carbon_emissions / total_kwh if total_kwh > 0 else 0
        
        return carbon_intensity
    
    def _generate_recommendations(self, grid_balance: str, energy_mix: Dict,
                                  storage_soc: float, renewable_pct: float) -> List[str]:
        """Generate actionable recommendations based on grid state"""
        recommendations = []
        
        if grid_balance == 'DEFICIT':
            recommendations.append("⚠️ CRITICAL: Power shortage detected - activate emergency reserves")
            recommendations.append("Consider demand response programs")
            if storage_soc < 20:
                recommendations.append("Storage critically low - prioritize charging")
        
        elif grid_balance == 'TIGHT':
            recommendations.append("⚡ WARNING: Operating near capacity limits")
            recommendations.append("Monitor system closely")
            if energy_mix['conventional_used'] > 0:
                recommendations.append("Conventional generators at high utilization")
        
        elif grid_balance == 'SURPLUS':
            excess = energy_mix['curtailed_renewable']
            if excess > 0:
                recommendations.append(f"✨ Excess renewable energy: {excess:.1f} MW")
            if storage_soc < 80:
                recommendations.append("Opportunity to charge energy storage")
            else:
                recommendations.append("Consider exporting excess energy to neighboring grids")
        
        else:  # BALANCED
            recommendations.append("✅ Grid operating optimally")
            if renewable_pct > 80:
                recommendations.append(f"🌱 Excellent renewable usage: {renewable_pct:.1f}%")
        
        # Storage recommendations
        if storage_soc < 20:
            recommendations.append("⚡ Low storage - charge when excess generation available")
        elif storage_soc > 90:
            recommendations.append("🔋 Storage nearly full - ready for peak demand")
        
        # Renewable recommendations
        if renewable_pct < 30:
            recommendations.append("Consider increasing renewable capacity investment")
        
        return recommendations
    
    def coordinate_with_agents(self, weather_result: Dict[str, Any], 
                               demand_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate with weather and demand agents to balance the grid
        """
        self.set_status(AgentStatus.BUSY)
        
        try:
            # Extract data from other agents
            weather_info = weather_result.get('current_weather', {}) if weather_result else {}
            demand_info = demand_result.get('current_demand', {}) if demand_result else {}
            
            current_demand = demand_info.get('predicted_demand_mw', 1000)
            
            # Calculate renewable generation
            renewable_gen = self.calculate_renewable_generation(weather_info)
            
            # Balance the grid
            balancing_result = self.balance_grid(current_demand, renewable_gen)
            
            self.log_action(f"Grid balanced: {balancing_result['grid_balance']}")
            
            self.set_status(AgentStatus.IDLE)
            
            return {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'grid_status': self.grid_status,
                'balancing_result': balancing_result,
                'status': 'success'
            }
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            self.log_action(f"Grid coordination failed: {str(e)}", level="error")
            return {
                'agent_id': self.agent_id,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get grid performance metrics over time"""
        if not self.balancing_history:
            return {'message': 'No historical data available'}
        
        recent = self.balancing_history[-24:]  # Last 24 records
        
        avg_renewable_pct = sum(
            r['result']['renewable_percentage'] for r in recent
        ) / len(recent)
        
        avg_efficiency = sum(
            r['result']['efficiency'] for r in recent
        ) / len(recent)
        
        balance_distribution = {}
        for record in recent:
            status = record['result']['grid_balance']
            balance_distribution[status] = balance_distribution.get(status, 0) + 1
        
        return {
            'period': 'last_24_records',
            'average_renewable_percentage': round(avg_renewable_pct, 2),
            'average_efficiency': round(avg_efficiency, 2),
            'balance_distribution': balance_distribution,
            'current_storage_soc': round(
                self.grid_status['storage_level'] / 
                self.grid_status['storage_capacity'] * 100, 2
            )
        }
    
    def calculate_grid_stability_index(self) -> float:
        """
        Calculate comprehensive grid stability index (0-100)
        Higher = more stable
        """
        # Frequency stability (50 Hz ± 0.2 Hz is excellent, ± 0.5 Hz is acceptable)
        freq_deviation = abs(self.grid_status['grid_frequency'] - 50.0)
        if freq_deviation <= 0.2:
            freq_score = 100
        elif freq_deviation <= 0.5:
            freq_score = 100 - ((freq_deviation - 0.2) / 0.3) * 30
        else:
            freq_score = max(0, 70 - (freq_deviation - 0.5) * 50)
        
        # Voltage stability (1.0 pu ± 0.05 is good)
        voltage_deviation = abs(self.grid_status['voltage_level'] - 1.0)
        voltage_score = max(0, 100 - (voltage_deviation / 0.05) * 100)
        
        # Storage health (optimal between 20-80%)
        storage_soc = (self.grid_status['storage_level'] / 
                    self.grid_status['storage_capacity'] * 100)
        if 20 <= storage_soc <= 80:
            storage_score = 100
        elif storage_soc < 20:
            storage_score = storage_soc * 5  # 0-20% → 0-100 score
        else:
            storage_score = max(0, 100 - (storage_soc - 80))
        
        # Recent balance performance
        if self.balancing_history:
            recent = self.balancing_history[-10:]
            balanced_count = sum(
                1 for r in recent 
                if r['result']['grid_balance'] in ['BALANCED', 'SURPLUS']
            )
            balance_score = (balanced_count / len(recent)) * 100
        else:
            balance_score = 50  # Neutral if no history
        
        # Weighted average (frequency most important)
        stability_index = (
            freq_score * 0.35 +
            voltage_score * 0.25 +
            storage_score * 0.20 +
            balance_score * 0.20
        )
        
        return round(stability_index, 2)
