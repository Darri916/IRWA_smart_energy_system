"""
Test script for enhanced agents
"""

from agents.weather_agent import WeatherAgent
from agents.demand_agent import EnergyDemandAgent
from agents.grid_agent import GridBalancerAgent
import json

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def main():
    print_section("TESTING ENHANCED AGENTS")
    
    # Test 1: Weather Agent
    print_section("1. Testing Weather Agent (5-Day Forecast)")
    weather_agent = WeatherAgent()
    weather_result = weather_agent.process_weather_request("Colombo")
    
    if weather_result['status'] == 'success':
        print(f"✓ City: {weather_result['city']}")
        print(f"✓ Current: {weather_result['current_weather']['temperature']}°C, {weather_result['current_weather']['description']}")
        print(f"✓ Solar Potential: {weather_result['solar_potential']:.1f}%")
        print(f"✓ Wind Potential: {weather_result['wind_potential']:.1f}%")
        print(f"✓ 5-Day Detailed Forecast: {len(weather_result['forecast_5day_detailed'])} data points")
        print(f"✓ 5-Day Daily Summaries: {len(weather_result['forecast_5day_daily'])} days")
        
        print("\n📅 Daily Summaries:")
        for day in weather_result['forecast_5day_daily'][:3]:  # Show first 3 days
            print(f"   {day['date']}: {day['temp_min']}°C - {day['temp_max']}°C, "
                  f"Renewable Score: {day['renewable_score']:.1f}%")
    else:
        print(f"✗ Weather agent failed: {weather_result.get('error')}")
        return
    
    # Test 2: Demand Agent
    print_section("2. Testing Demand Agent (5-Day Forecast)")
    demand_agent = EnergyDemandAgent()
    demand_result = demand_agent.process_demand_forecast(weather_result)
    
    if demand_result['status'] == 'success':
        current = demand_result['current_demand']
        print(f"✓ Current Demand: {current['predicted_demand_mw']} MW")
        print(f"✓ Confidence: {current['confidence']:.1%}")
        print(f"✓ Peak Hour: {'Yes' if current['is_peak_hour'] else 'No'}")
        print(f"✓ 24-Hour Forecast: {len(demand_result['forecast_24h'])} hours")
        print(f"✓ 5-Day Forecast: {len(demand_result['forecast_5day'])} days")
        
        print("\n📊 Peak Statistics:")
        stats = demand_result['peak_statistics']
        print(f"   Max: {stats['max_demand_mw']} MW")
        print(f"   Min: {stats['min_demand_mw']} MW")
        print(f"   Avg: {stats['avg_demand_mw']} MW")
        
        print("\n📅 5-Day Demand Forecast:")
        for day_forecast in demand_result['forecast_5day'][:3]:
            print(f"   {day_forecast['date']} ({day_forecast['day_of_week']}): "
                  f"Avg {day_forecast['avg_demand_mw']} MW, "
                  f"Peak at hour {day_forecast['peak_hour']}")
    else:
        print(f"✗ Demand agent failed: {demand_result.get('error')}")
        return
    
    # Test 3: Grid Agent
    print_section("3. Testing Grid Agent (Optimization)")
    grid_agent = GridBalancerAgent()
    grid_result = grid_agent.coordinate_with_agents(weather_result, demand_result)
    
    if grid_result['status'] == 'success':
        balance = grid_result['balancing_result']
        print(f"✓ Grid Balance: {balance['grid_balance']}")
        print(f"✓ Stability: {balance['stability']}")
        print(f"✓ Renewable: {balance['renewable_percentage']:.1f}%")
        print(f"✓ Efficiency: {balance['efficiency']:.1f}%")
        print(f"✓ Storage SOC: {balance['storage_soc_percent']:.1f}%")
        print(f"✓ Carbon Intensity: {balance['carbon_intensity_gco2_kwh']:.1f} gCO2/kWh")
        
        print("\n⚡ Energy Mix:")
        mix = balance['energy_mix']
        print(f"   Renewable: {mix['renewable_used']:.1f} MW")
        print(f"   Storage Discharge: {mix['storage_discharged']:.1f} MW")
        print(f"   Conventional: {mix['conventional_used']:.1f} MW")
        if mix['storage_charged'] > 0:
            print(f"   Storage Charging: {mix['storage_charged']:.1f} MW")
        if mix['curtailed_renewable'] > 0:
            print(f"   Curtailed: {mix['curtailed_renewable']:.1f} MW")
        
        print("\n💡 Recommendations:")
        for rec in balance['recommendations'][:3]:
            print(f"   • {rec}")
    else:
        print(f"✗ Grid agent failed: {grid_result.get('error')}")
        return
    
    # Test 4: Agent Communication & Explainability
    print_section("4. Testing Responsible AI Features")
    
    print("📝 Weather Agent Last Decision:")
    last_decision = weather_agent.explain_last_decision()
    if last_decision:
        print(f"   Decision: {last_decision['decision']}")
        print(f"   Confidence: {last_decision['confidence']:.1%}")
        print(f"   Reasoning: {last_decision['reasoning']}")
    
    print("\n📝 Grid Agent Last Decision:")
    last_decision = grid_agent.explain_last_decision()
    if last_decision:
        print(f"   Decision: {last_decision['decision']}")
        print(f"   Confidence: {last_decision['confidence']:.1%}")
    
    print("\n📊 Agent Status:")
    print(f"   Weather Agent: {weather_agent.get_status()['status']}")
    print(f"   Demand Agent: {demand_agent.get_status()['status']}")
    print(f"   Grid Agent: {grid_agent.get_status()['status']}")
    
    # Success
    print_section("✅ ALL TESTS PASSED!")
    print("\n🎉 Enhanced agents are working correctly!")
    print("   ✓ 5-day weather forecasting")
    print("   ✓ 5-day demand forecasting")
    print("   ✓ Smart grid optimization")
    print("   ✓ Energy storage management")
    print("   ✓ Explainable AI decisions")
    print("\n📋 Next: Proceed to Phase 3 for AI Services")

if __name__ == "__main__":
    main()
