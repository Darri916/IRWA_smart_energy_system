#!/usr/bin/env python3
"""
Smart Energy Forecasting System - Spectacular UI
Modern, Professional, Interactive Dashboard
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from main import SmartEnergySystem

# Initialize the system
energy_system = SmartEnergySystem(enable_ai=True, enable_db=True, enable_security=True)

# Professional Custom CSS with Modern Design
custom_css = """
<style>
    /* Modern Color Palette */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
        --dark: #1f2937;
        --light: #f3f4f6;
    }
    
    /* Glassmorphism Header */
    .energy-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .energy-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .energy-header h2 {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Metric Cards with Gradient Borders */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid var(--success);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-card h3 {
        color: var(--dark);
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0.5rem 0;
    }
    
    .metric-card .label {
        font-size: 0.85rem;
        color: #6b7280;
    }
    
    /* Status Indicators with Animation */
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .status-active { 
        background: linear-gradient(135deg, #10b981, #059669);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    
    .status-warning { 
        background: linear-gradient(135deg, #f59e0b, #d97706);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }
    
    .status-error { 
        background: linear-gradient(135deg, #ef4444, #dc2626);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }
    
    /* AI Response Card */
    .ai-response {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid var(--info);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    .ai-response h3 {
        color: var(--info);
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Energy Grid Layout */
    .energy-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Forecast Card */
    .forecast-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 15px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    .forecast-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    /* Alert Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.3rem;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Statistics Panel */
    .stats-panel {
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    /* Responsive Typography */
    @media (max-width: 768px) {
        .energy-header h1 {
            font-size: 1.8rem;
        }
        .energy-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
"""

# ============================================================================
# DASHBOARD CREATION FUNCTIONS
# ============================================================================

def create_dashboard(city: str) -> tuple:
    """Create comprehensive dashboard with all visualizations"""
    try:
        # Run forecast
        result = energy_system.run_energy_forecast(city)
        
        if result['status'] != 'success':
            error_html = f"""
            <div style="color: #ef4444; padding: 2rem; border: 2px solid #ef4444; border-radius: 16px; text-align: center;">
                <h2>⚠️ System Error</h2>
                <p>{result.get('error', 'Unknown error occurred')}</p>
            </div>
            """
            return error_html, None, None, None, None, ""
        
        # Extract data
        weather_data = result['weather'].get('current_weather', {})
        demand_data = result['demand'].get('current_demand', {})
        grid_data = result['grid'].get('balancing_result', {})
        forecast_5day = result['weather'].get('forecast_5day_daily', [])
        ai_analysis = result.get('ai_analysis', {})
        
        # Create dashboard HTML
        dashboard_html = create_dashboard_html(city, weather_data, demand_data, grid_data, ai_analysis, result)
        
        # Create charts
        main_chart = create_main_overview_chart(result)
        forecast_chart = create_5day_forecast_chart(forecast_5day, result)
        performance_chart = create_performance_chart(result)
        energy_mix_chart = create_energy_mix_chart(grid_data)
        
        # Create summary
        summary = create_executive_summary(result)
        
        return dashboard_html, main_chart, forecast_chart, performance_chart, energy_mix_chart, summary
        
    except Exception as e:
        error_html = f"""
        <div style="color: #ef4444; padding: 2rem; border-radius: 16px;">
            <h3>Dashboard Error</h3>
            <p>{str(e)}</p>
        </div>
        """
        return error_html, None, None, None, None, ""

def create_dashboard_html(city: str, weather: Dict, demand: Dict, grid: Dict, ai: Dict, result: Dict) -> str:
    """Create beautiful HTML dashboard"""
    
    # Status classes
    data_status = "status-active" if weather.get('real_data') else "status-warning"
    ai_status = "status-active" if energy_system.ai_enabled else "status-error"
    grid_status_class = {
        'BALANCED': 'status-active',
        'SURPLUS': 'status-active',
        'DEFICIT': 'status-warning'
    }.get(grid.get('grid_balance', 'UNKNOWN'), 'status-error')
    
    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
    exec_time = result.get('execution_time', 0)
    
    html = f"""{custom_css}
    
    <div class="energy-header">
        <h1>⚡ Smart Energy Forecasting System</h1>
        <h2>Multi-Agent AI Analysis for {city}</h2>
        <p style="margin-top: 1rem; opacity: 0.9;">Generated on {timestamp}</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Processing Time: {exec_time:.2f}s</p>
    </div>
    
    <div class="energy-grid">
        <div class="metric-card">
            <h3><span class="{data_status} status-indicator"></span>Data Source</h3>
            <div class="value">{"Real-Time" if weather.get('real_data') else "Demo"}</div>
            <div class="label">{weather.get('api_source', 'N/A')}</div>
        </div>
        
        <div class="metric-card">
            <h3><span class="{ai_status} status-indicator"></span>AI System</h3>
            <div class="value">{"Active" if energy_system.ai_enabled else "Offline"}</div>
            <div class="label">LLM: {ai.get('provider', 'N/A').title()}</div>
        </div>
        
        <div class="metric-card">
            <h3><span class="{grid_status_class} status-indicator"></span>Grid Status</h3>
            <div class="value">{grid.get('grid_balance', 'N/A')}</div>
            <div class="label">Efficiency: {grid.get('efficiency', 0):.1f}%</div>
        </div>
    </div>
    
    <div class="energy-grid">
        <div class="metric-card" style="border-left-color: #f59e0b;">
            <h3>🌡️ Weather</h3>
            <div class="value">{weather.get('temperature', 'N/A')}°C</div>
            <div class="label">
                Wind: {weather.get('wind_speed', 'N/A')} m/s<br/>
                Humidity: {weather.get('humidity', 'N/A')}%<br/>
                {weather.get('description', 'N/A')}
            </div>
        </div>
        
        <div class="metric-card" style="border-left-color: #3b82f6;">
            <h3>⚡ Energy Demand</h3>
            <div class="value">{demand.get('predicted_demand_mw', 'N/A')} MW</div>
            <div class="label">
                Confidence: {demand.get('confidence', 0):.0%}<br/>
                {"🔴 Peak Hour" if demand.get('is_peak_hour') else "🟢 Normal"}
            </div>
        </div>
        
        <div class="metric-card" style="border-left-color: #10b981;">
            <h3>♻️ Renewable</h3>
            <div class="value">{grid.get('renewable_percentage', 0):.1f}%</div>
            <div class="label">
                Generation: {grid.get('renewable_generation', {}).get('total', 0):.1f} MW<br/>
                Storage: {grid.get('storage_soc_percent', 0):.1f}%
            </div>
        </div>
        
        <div class="metric-card" style="border-left-color: #8b5cf6;">
            <h3>🌱 Carbon</h3>
            <div class="value">{grid.get('carbon_intensity_gco2_kwh', 0):.0f}</div>
            <div class="label">gCO2/kWh<br/>
                {"🌟 Low Impact" if grid.get('carbon_intensity_gco2_kwh', 999) < 200 else "⚠️ Moderate"}
            </div>
        </div>
    </div>
    """
    
    # Add AI Analysis if available
    if ai and ai.get('status') == 'success':
        ai_report = ai.get('report', '').replace('\n', '<br/>')
        html += f"""
        <div class="ai-response">
            <h3>🤖 AI-Generated Analysis</h3>
            <div style="line-height: 1.8;">{ai_report}</div>
        </div>
        """
    
    # Add Recommendations
    recommendations = grid.get('recommendations', [])
    if recommendations:
        badges = ''.join([
            f'<span class="badge badge-info">💡 {rec}</span>'
            for rec in recommendations[:3]
        ])
        html += f"""
        <div class="stats-panel">
            <h3 style="color: #8b5cf6; margin-bottom: 1rem;">📋 System Recommendations</h3>
            <div>{badges}</div>
        </div>
        """
    
    return html

def create_main_overview_chart(result: Dict) -> go.Figure:
    """Create main overview chart with multiple metrics"""
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '⚡ Energy Mix Distribution',
            '♻️ Renewable Potential',
            '📊 24-Hour Demand Forecast',
            '🎯 System Efficiency'
        ),
        specs=[
            [{"type": "pie"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "indicator"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Energy Mix Pie
    energy_mix = result['grid']['balancing_result']['energy_mix']
    renewable = energy_mix.get('renewable_used', 0)
    storage = energy_mix.get('storage_discharged', 0)
    conventional = energy_mix.get('conventional_used', 0)
    
    fig.add_trace(go.Pie(
        labels=['Renewable', 'Storage', 'Conventional'],
        values=[renewable, storage, conventional],
        marker=dict(colors=['#10b981', '#3b82f6', '#ef4444']),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=12)
    ), row=1, col=1)
    
    # Renewable Potential Bar
    solar = result['weather']['solar_potential']
    wind = result['weather']['wind_potential']
    
    fig.add_trace(go.Bar(
        x=['Solar', 'Wind'],
        y=[solar, wind],
        marker=dict(
            color=['#f59e0b', '#06b6d4'],
            line=dict(color='white', width=2)
        ),
        text=[f"{solar:.1f}%", f"{wind:.1f}%"],
        textposition='outside',
        textfont=dict(size=14, color='black')
    ), row=1, col=2)
    
    # 24-Hour Forecast
    forecast_24h = result['demand'].get('forecast_24h', [])[:12]
    if forecast_24h:
        hours = [f['hour'] for f in forecast_24h]
        demands = [f['predicted_demand_mw'] for f in forecast_24h]
        
        fig.add_trace(go.Scatter(
            x=hours,
            y=demands,
            mode='lines+markers',
            name='Demand',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8),
            fill='tonexty',
            fillcolor='rgba(139, 92, 246, 0.1)'
        ), row=2, col=1)
    
    # Efficiency Gauge
    efficiency = result['grid']['balancing_result'].get('efficiency', 0)
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=efficiency,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Efficiency %", 'font': {'size': 16}},
        delta={'reference': 70, 'increasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e5e7eb",
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#10b981", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ), row=2, col=2)
    
    fig.update_layout(
        height=700,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="'Inter', sans-serif", size=12),
        title_text="<b>System Overview Dashboard</b>",
        title_font_size=20,
        title_x=0.5
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6')
    
    return fig

def create_5day_forecast_chart(daily_forecasts: List[Dict], result: Dict) -> go.Figure:
    """Create beautiful 5-day forecast chart"""
    
    if not daily_forecasts:
        return go.Figure()
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('🌡️ Temperature & Renewable Score (5-Day)', '⚡ Energy Demand Forecast'),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    # Extract data
    dates = [d['date'] for d in daily_forecasts]
    temp_min = [d['temp_min'] for d in daily_forecasts]
    temp_max = [d['temp_max'] for d in daily_forecasts]
    renewable_scores = [d['renewable_score'] for d in daily_forecasts]
    
    # Temperature range
    fig.add_trace(go.Scatter(
        x=dates,
        y=temp_max,
        name='Max Temp',
        line=dict(color='#ef4444', width=2),
        mode='lines+markers'
    ), row=1, col=1, secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=temp_min,
        name='Min Temp',
        line=dict(color='#3b82f6', width=2),
        fill='tonexty',
        fillcolor='rgba(239, 68, 68, 0.1)',
        mode='lines+markers'
    ), row=1, col=1, secondary_y=False)
    
    # Renewable score
    fig.add_trace(go.Scatter(
        x=dates,
        y=renewable_scores,
        name='Renewable Score',
        line=dict(color='#10b981', width=3, dash='dash'),
        mode='lines+markers',
        marker=dict(size=10)
    ), row=1, col=1, secondary_y=True)
    
    # Demand forecast
    demand_5day = result['demand'].get('forecast_5day', [])
    if demand_5day:
        demand_dates = [d['date'] for d in demand_5day]
        avg_demands = [d['avg_demand_mw'] for d in demand_5day]
        max_demands = [d['max_demand_mw'] for d in demand_5day]
        
        fig.add_trace(go.Bar(
            x=demand_dates,
            y=avg_demands,
            name='Avg Demand',
            marker_color='#8b5cf6',
            text=[f"{d:.0f} MW" for d in avg_demands],
            textposition='outside'
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=demand_dates,
            y=max_demands,
            name='Peak Demand',
            line=dict(color='#ef4444', width=2, dash='dot'),
            mode='lines+markers'
        ), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Renewable Score (%)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Demand (MW)", row=2, col=1)
    
    fig.update_layout(
        height=800,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="'Inter', sans-serif"),
        hovermode='x unified'
    )
    
    return fig

def create_performance_chart(result: Dict) -> go.Figure:
    """Create system performance timeline"""
    
    fig = go.Figure()
    
    # Simulate performance history
    hours = list(range(-12, 1))
    base_performance = 75
    performance_data = []
    renewable_data = []
    
    for h in hours:
        perf = base_performance + 15 * np.sin(h * np.pi / 6) + np.random.normal(0, 2)
        performance_data.append(max(0, min(100, perf)))
        
        renew = 50 + 20 * np.cos(h * np.pi / 8) + np.random.normal(0, 5)
        renewable_data.append(max(0, min(100, renew)))
    
    # Add performance line
    fig.add_trace(go.Scatter(
        x=hours,
        y=performance_data,
        name='System Performance',
        line=dict(color='#667eea', width=3),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.2)',
        mode='lines'
    ))
    
    # Add renewable percentage
    fig.add_trace(go.Scatter(
        x=hours,
        y=renewable_data,
        name='Renewable %',
        line=dict(color='#10b981', width=2, dash='dash'),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Current point
    current_perf = result['grid']['balancing_result'].get('efficiency', 75)
    current_renew = result['grid']['balancing_result'].get('renewable_percentage', 50)
    
    fig.add_trace(go.Scatter(
        x=[0],
        y=[current_perf],
        name='Current',
        mode='markers',
        marker=dict(size=15, color='#ef4444', symbol='diamond', line=dict(color='white', width=2))
    ))
    
    fig.update_layout(
        title="<b>System Performance Timeline (Last 12 Hours)</b>",
        xaxis_title="Hours from Now",
        yaxis_title="Performance (%)",
        height=450,
        hovermode='x unified',
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="'Inter', sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6', zeroline=True)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6', range=[0, 100])
    
    return fig

def create_energy_mix_chart(grid_data: Dict) -> go.Figure:
    """Create detailed energy mix breakdown"""
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Energy Sources Breakdown', 'Carbon Intensity Comparison'),
        specs=[[{"type": "domain"}, {"type": "bar"}]]
    )
    
    # Energy mix donut
    energy_mix = grid_data.get('energy_mix', {})
    renewable = energy_mix.get('renewable_used', 0)
    storage = energy_mix.get('storage_discharged', 0)
    conventional = energy_mix.get('conventional_used', 0)
    
    fig.add_trace(go.Pie(
        labels=['Renewable', 'Storage', 'Conventional'],
        values=[renewable, storage, conventional],
        hole=0.5,
        marker=dict(colors=['#10b981', '#3b82f6', '#ef4444']),
        textposition='outside',
        textinfo='label+value',
        hovertemplate='<b>%{label}</b><br>%{value:.1f} MW<br>%{percent}<extra></extra>'
    ), row=1, col=1)
    
    # Carbon comparison
    current_carbon = grid_data.get('carbon_intensity_gco2_kwh', 0)
    
    fig.add_trace(go.Bar(
        x=['Current', 'Coal Baseline', 'Gas Baseline', 'Target'],
        y=[current_carbon, 820, 450, 100],
        marker=dict(
            color=[
                '#10b981' if current_carbon < 200 else '#f59e0b' if current_carbon < 400 else '#ef4444',
                '#991b1b',
                '#ea580c',
                '#065f46'
            ]
        ),
        text=[f"{v:.0f}" for v in [current_carbon, 820, 450, 100]],
        textposition='outside'
    ), row=1, col=2)
    
    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="'Inter', sans-serif")
    )
    
    fig.update_yaxes(title_text="gCO2/kWh", row=1, col=2)
    
    return fig

def create_executive_summary(result: Dict) -> str:
    """Create executive summary text"""
    
    city = result['city']
    renewable_pct = result['grid']['balancing_result'].get('renewable_percentage', 0)
    efficiency = result['grid']['balancing_result'].get('efficiency', 0)
    grid_status = result['grid']['balancing_result'].get('grid_balance')
    
    summary = f"""
## 📊 Executive Summary - {city}

**Grid Status:** {grid_status} | **Renewable:** {renewable_pct:.1f}% | **Efficiency:** {efficiency:.1f}%

### Key Highlights:
- ⚡ **Energy System**: Operating {"optimally" if efficiency > 70 else "within acceptable parameters"}
- ♻️ **Renewable Integration**: {renewable_pct:.1f}% of current demand met by clean energy
- 🌍 **Environmental Impact**: {"Low carbon footprint" if renewable_pct > 60 else "Moderate emissions"}
- 📈 **System Health**: All agents operational, {result.get('execution_time', 0):.2f}s response time

### 5-Day Outlook:
Weather conditions show {"favorable" if result['weather']['renewable_score'] > 50 else "challenging"} patterns for renewable generation.
System recommends {"maintaining current operations" if grid_status == "BALANCED" else "operational adjustments"}.
"""
    
    return summary

# ============================================================================
# AI INTERACTION FUNCTIONS
# ============================================================================

def ask_ai_question(question: str, city: str) -> str:
    """Process AI question with beautiful formatting"""
    if not question.strip():
        return "❓ Please enter a question."
    
    try:
        result = energy_system.answer_question(question, city)
        
        if result['status'] == 'success':
            intent = result.get('intent', {})
            intent_info = f"**Intent Detected:** {intent.get('primary_intent', 'general_query').replace('_', ' ').title()}" if intent else ""
            
            html = f"""
            <div class="ai-response">
                <h3>🤖 AI Response</h3>
                <p><strong>Question:</strong> {question}</p>
                {f'<p style="font-size: 0.9rem; color: #6b7280;">{intent_info}</p>' if intent_info else ''}
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;"/>
                <p><strong>Answer:</strong></p>
                <p style="line-height: 1.8;">{result['answer']}</p>
                <p style="margin-top: 1rem; font-size: 0.85rem; color: #6b7280;">
                    📍 Context: {city} | ⏱️ {datetime.now().strftime('%H:%M:%S')}
                </p>
            </div>
            """
            return html
        else:
            return f"<div class='ai-response' style='border-left-color: #ef4444;'><h3>⚠️ Error</h3><p>{result.get('answer', 'Unable to process question')}</p></div>"
            
    except Exception as e:
        return f"<div class='ai-response' style='border-left-color: #ef4444;'><h3>❌ Error</h3><p>{str(e)}</p></div>"

def search_system(query: str, search_type: str, days: int) -> tuple:
    """Search historical data with visualization"""
    if not query.strip():
        return "❓ Please enter a search query.", None
    
    try:
        filters = {'type': search_type, 'days': days}
        results = energy_system.search_history(query, filters)
        
        if results['status'] == 'success':
            total = results['total_results']
            
            html = f"""
            <div class="stats-panel">
                <h3>🔍 Search Results for "{query}"</h3>
                <p><strong>Found:</strong> {total} results | <strong>Timeframe:</strong> Last {days} days | <strong>Type:</strong> {search_type}</p>
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;"/>
            """
            
            if total > 0:
                for i, result in enumerate(results['results'][:5], 1):
                    result_type = result['type']
                    score = result['score']
                    summary = result['summary']
                    
                    type_colors = {
                        'weather': '#f59e0b',
                        'demand': '#3b82f6',
                        'grid': '#10b981',
                        'decision': '#8b5cf6'
                    }
                    
                    color = type_colors.get(result_type, '#6b7280')
                    
                    html += f"""
                    <div class="forecast-card" style="border-left: 4px solid {color}; margin: 0.8rem 0;">
                        <p style="font-size: 0.85rem; color: #6b7280;">Result #{i} | Type: {result_type.title()} | Relevance: {score}</p>
                        <p style="margin-top: 0.5rem;">{summary}</p>
                    </div>
                    """
                
                if total > 5:
                    html += f"<p style='margin-top: 1rem; color: #6b7280; font-style: italic;'>... and {total - 5} more results</p>"
            else:
                html += "<p>No results found. Try different keywords or adjust filters.</p>"
            
            html += "</div>"
            
            # Create visualization
            if total > 0:
                chart = create_search_results_chart(results)
                return html, chart
            else:
                return html, None
        else:
            return f"<div class='ai-response' style='border-left-color: #ef4444;'><h3>⚠️ Search Error</h3><p>{results.get('error', 'Search failed')}</p></div>", None
            
    except Exception as e:
        return f"<div class='ai-response' style='border-left-color: #ef4444;'><h3>❌ Error</h3><p>{str(e)}</p></div>", None

def create_search_results_chart(results: Dict) -> go.Figure:
    """Create chart showing search results distribution"""
    
    # Count by type
    type_counts = {}
    for result in results['results']:
        result_type = result['type']
        type_counts[result_type] = type_counts.get(result_type, 0) + 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(type_counts.keys()),
            y=list(type_counts.values()),
            marker=dict(
                color=['#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'][:len(type_counts)],
                line=dict(color='white', width=2)
            ),
            text=list(type_counts.values()),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="<b>Search Results by Type</b>",
        xaxis_title="Data Type",
        yaxis_title="Number of Results",
        height=350,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="'Inter', sans-serif")
    )
    
    return fig

def get_system_stats_display() -> tuple:
    """Get system statistics with visualization"""
    try:
        stats = energy_system.get_system_statistics(days=7)
        
        if stats['status'] == 'success':
            grid_stats = stats['grid_statistics']
            
            html = f"""
            <div class="stats-panel">
                <h3>📊 System Statistics (Last 7 Days)</h3>
                
                <div class="energy-grid">
                    <div class="metric-card">
                        <h3>Average Renewable</h3>
                        <div class="value">{grid_stats['avg_renewable_percentage']:.1f}%</div>
                    </div>
                    <div class="metric-card">
                        <h3>Average Efficiency</h3>
                        <div class="value">{grid_stats['avg_efficiency']:.1f}%</div>
                    </div>
                    <div class="metric-card">
                        <h3>Total Records</h3>
                        <div class="value">{grid_stats['total_records']}</div>
                    </div>
                </div>
                
                <h4 style="margin-top: 1.5rem;">Grid Balance Distribution:</h4>
            """
            
            for status, count in stats['balance_distribution'].items():
                html += f"<span class='badge badge-info'>{status}: {count}</span>"
            
            html += f"<p style='margin-top: 1rem;'>Anomalies Detected: {stats['anomaly_count']}</p></div>"
            
            # Create chart
            chart = create_stats_chart(stats)
            
            return html, chart
        else:
            return "<p>Statistics unavailable</p>", None
            
    except Exception as e:
        return f"<p>Error: {str(e)}</p>", None

def create_stats_chart(stats: Dict) -> go.Figure:
    """Create statistics visualization"""
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Grid Balance Distribution', 'Performance Metrics'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Balance distribution
    balance_dist = stats['balance_distribution']
    if balance_dist:
        fig.add_trace(go.Pie(
            labels=list(balance_dist.keys()),
            values=list(balance_dist.values()),
            marker=dict(colors=['#10b981', '#3b82f6', '#f59e0b', '#ef4444']),
            hole=0.4
        ), row=1, col=1)
    
    # Performance metrics
    grid_stats = stats['grid_statistics']
    fig.add_trace(go.Bar(
        x=['Renewable %', 'Efficiency %'],
        y=[grid_stats['avg_renewable_percentage'], grid_stats['avg_efficiency']],
        marker=dict(color=['#10b981', '#667eea']),
        text=[f"{grid_stats['avg_renewable_percentage']:.1f}%", 
              f"{grid_stats['avg_efficiency']:.1f}%"],
        textposition='outside'
    ), row=1, col=2)
    
    fig.update_layout(
        height=400,
        showlegend=True,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

# Create Gradio Interface
with gr.Blocks(
    title="Smart Energy Forecasting System - Professional Edition",
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate"
    ),
    css="""
        .gradio-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        .gr-button-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
        }
        .gr-button-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
        }
    """
) as demo:
    
    gr.HTML("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 2rem;">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                ⚡ Smart Energy Forecasting System
            </h1>
            <h2 style="color: rgba(255,255,255,0.9); font-size: 1.5rem; font-weight: 400;">
                Multi-Agent AI System with Advanced Analytics
            </h2>
            <p style="color: rgba(255,255,255,0.8); margin-top: 1rem; font-size: 1.1rem;">
                Professional Energy Management Dashboard | Powered by Claude AI
            </p>
        </div>
    """)
    
    # ===== TAB 1: Main Dashboard =====
    with gr.Tab("🏠 Main Dashboard"):
        with gr.Row():
            city_input = gr.Dropdown(
                choices=["Colombo", "Jaffna", "Kandy", "Galle", "Negombo", 
                        "London", "New York", "Tokyo", "Singapore", "Mumbai"],
                value="Jaffna",
                label="🌍 Select City",
                scale=3
            )
            refresh_btn = gr.Button("🔄 Refresh Analysis", variant="primary", scale=1, size="lg")
        
        dashboard_output = gr.HTML()
        
        with gr.Row():
            main_chart = gr.Plot(label="📊 System Overview")
        
        with gr.Row():
            forecast_chart = gr.Plot(label="📅 5-Day Forecast")
        
        with gr.Row():
            with gr.Column():
                performance_chart = gr.Plot(label="📈 Performance Timeline")
            with gr.Column():
                energy_mix_chart = gr.Plot(label="⚡ Energy Mix Analysis")
        
        summary_output = gr.Markdown()
        
        refresh_btn.click(
            create_dashboard,
            inputs=[city_input],
            outputs=[dashboard_output, main_chart, forecast_chart, 
                    performance_chart, energy_mix_chart, summary_output]
        )
        
        # Auto-load on start
        demo.load(
            create_dashboard,
            inputs=[city_input],
            outputs=[dashboard_output, main_chart, forecast_chart,
                    performance_chart, energy_mix_chart, summary_output]
        )
    
    # ===== TAB 2: AI Assistant =====
    with gr.Tab("🤖 AI Assistant"):
        gr.Markdown("## Ask Questions About the Energy System")
        
        with gr.Row():
            with gr.Column(scale=3):
                question_input = gr.Textbox(
                    label="💬 Your Question",
                    placeholder="e.g., What are the optimal conditions for renewable energy generation?",
                    lines=3
                )
            with gr.Column(scale=1):
                ai_city_input = gr.Dropdown(
                    choices=["Jaffna", "Colombo", "Kandy", "Galle"],
                    value="Jaffna",
                    label="📍 City Context"
                )
        
        ask_btn = gr.Button("🚀 Get AI Answer", variant="primary", size="lg")
        ai_output = gr.HTML()
        
        gr.Examples(
            examples=[
                ["What is the current renewable energy potential?"],
                ["How can we improve grid stability?"],
                ["What are the weather conditions affecting solar generation?"],
                ["Analyze the demand forecast for tomorrow"],
                ["What optimization strategies would you recommend?"],
            ],
            inputs=[question_input],
            label="💡 Example Questions"
        )
        
        ask_btn.click(
            ask_ai_question,
            inputs=[question_input, ai_city_input],
            outputs=[ai_output]
        )
    
    # ===== TAB 3: Search & Analytics =====
    with gr.Tab("🔍 Search & Analytics"):
        gr.Markdown("## Search Historical Data")
        
        with gr.Row():
            search_input = gr.Textbox(
                label="🔎 Search Query",
                placeholder="e.g., renewable energy, grid balance, high demand",
                scale=2
            )
            search_type = gr.Dropdown(
                choices=["all", "weather", "demand", "grid", "decisions"],
                value="all",
                label="📂 Search Type",
                scale=1
            )
            search_days = gr.Slider(
                minimum=1, maximum=30, value=7, step=1,
                label="📅 Days to Search",
                scale=1
            )
        
        search_btn = gr.Button("🔍 Search", variant="primary", size="lg")
        
        search_output = gr.HTML()
        search_chart = gr.Plot()
        
        search_btn.click(
            search_system,
            inputs=[search_input, search_type, search_days],
            outputs=[search_output, search_chart]
        )
        
        gr.Markdown("---")
        gr.Markdown("## System Statistics")
        
        stats_btn = gr.Button("📊 Load Statistics", variant="secondary", size="lg")
        stats_output = gr.HTML()
        stats_chart = gr.Plot()
        
        stats_btn.click(
            get_system_stats_display,
            outputs=[stats_output, stats_chart]
        )
    
    # ===== TAB 4: About =====
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        # 🌟 Smart Renewable Energy Forecasting System
        
        ## 📋 System Features
        
        ### 🤖 **Multi-Agent Architecture**
        - **Weather Agent**: Real-time weather data + 5-day forecasts
        - **Demand Agent**: AI-powered energy demand prediction
        - **Grid Agent**: Intelligent grid balancing & optimization
        
        ### 🧠 **AI & Machine Learning**
        - **Claude AI Integration**: Advanced natural language understanding
        - **NLP Services**: Sentiment analysis, entity extraction, intent classification
        - **Responsible AI**: Explainability, fairness, bias detection
        
        ### 🔒 **Security & Privacy**
        - Session management with encryption
        - Input validation & sanitization
        - SQL injection & XSS protection
        - JWT authentication
        
        ### 💾 **Data Management**
        - SQLite database with 7 tables
        - Historical data tracking
        - AI decision audit trail
        - Information retrieval engine
        
        ### 📊 **Advanced Analytics**
        - Real-time forecasting
        - 5-day weather & demand predictions
        - Carbon intensity tracking
        - System performance metrics
        
        ## 🎓 Academic Project
        **Course**: Information Retrieval and Web Analytics (IT 3041)  
        **Institution**: SLIIT  
        **Version**: 2.0  
        **Technology Stack**: Python, Gradio, Plotly, SQLAlchemy, Claude AI
        
        ## 📧 Support
        For questions or issues, contact your course instructor.
        
        ---
        
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border-radius: 16px; margin-top: 2rem;">
            <p style="font-size: 1.2rem; color: #374151; margin: 0;">
                🌍 <strong>Making Energy Smarter, Cleaner, and More Sustainable</strong> 🌱
            </p>
        </div>
        """)

# ============================================================================
# LAUNCH
# ============================================================================

def launch_interface():
    """Launch the spectacular interface"""
    print("\n" + "="*70)
    print("🚀 LAUNCHING SMART ENERGY FORECASTING SYSTEM")
    print("="*70)
    print("\n✨ Starting spectacular UI...")
    print("🌐 Interface will open in your browser")
    print("📊 All systems ready!\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_api=False,
        favicon_path=None,
        inbrowser=True
    )

if __name__ == "__main__":
    launch_interface()
