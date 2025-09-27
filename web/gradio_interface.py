import sys
from pathlib import Path
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import json
from datetime import datetime
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from main import SmartEnergySystem

# Initialize the system
energy_system = SmartEnergySystem(enable_ai=True)

# Custom CSS 
custom_css = """
<style>
    .energy-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: #4CAF50; }
    .status-warning { background-color: #FF9800; }
    .status-error { background-color: #F44336; }
    
    .ai-response {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #2196F3;
    }
    
    .energy-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
</style>
"""

def create_professional_dashboard(city):
    """Create a comprehensive professional dashboard"""
    try:
        result = energy_system.run_energy_forecast(city)
        
        if result['status'] != 'success':
            return create_error_display(result.get('error', 'Unknown error'))
        
        # Extract all data
        weather_data = result['weather'].get('weather_data', {})
        demand_data = result['demand'].get('current_demand', {})
        grid_data = result['grid'].get('grid_status', {})
        grid_balance = result['grid'].get('balancing_result', {})
        ai_analysis = result.get('ai_analysis', {})
        
        # Create main dashboard
        dashboard_html = create_dashboard_html(city, weather_data, demand_data, grid_data, grid_balance, ai_analysis)
        
        # Create charts
        charts = create_advanced_charts(result)
        
        # Create data table
        summary_table = create_summary_table(result)
        
        return dashboard_html, charts[0], charts[1], charts[2], summary_table
        
    except Exception as e:
        return create_error_display(f"Dashboard creation failed: {str(e)}"), None, None, None, None

def create_dashboard_html(city, weather_data, demand_data, grid_data, grid_balance, ai_analysis):
    """Create professional HTML dashboard"""
    data_source = "Real-time API" if weather_data.get('real_data') else "Demo Data"
    ai_status = "Active" if energy_system.ai_enabled else "Inactive"
    grid_status = grid_balance.get('grid_balance', 'Unknown')
    
    # Status indicators
    data_status_class = "status-active" if weather_data.get('real_data') else "status-warning"
    ai_status_class = "status-active" if energy_system.ai_enabled else "status-error"
    grid_status_class = {
        'BALANCED': 'status-active',
        'SURPLUS': 'status-active', 
        'DEFICIT': 'status-warning'
    }.get(grid_status, 'status-error')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    html = f"""
    <div class="energy-header">
        <h1>Smart Energy Forecasting System</h1>
        <h2>Multi-Agent AI Analysis for {city}</h2>
        <p>Generated: {timestamp}</p>
    </div>
    
    <div class="energy-grid">
        <div class="metric-card">
            <h3><span class="{data_status_class} status-indicator"></span>Data Source</h3>
            <p><strong>{data_source}</strong></p>
            <small>API: {weather_data.get('api_source', 'N/A')}</small>
        </div>
        
        <div class="metric-card">
            <h3><span class="{ai_status_class} status-indicator"></span>AI System</h3>
            <p><strong>{ai_status}</strong></p>
            <small>LLM Models: {'Loaded' if energy_system.ai_enabled else 'Not Available'}</small>
        </div>
        
        <div class="metric-card">
            <h3><span class="{grid_status_class} status-indicator"></span>Grid Status</h3>
            <p><strong>{grid_status}</strong></p>
            <small>Efficiency: {grid_balance.get('efficiency', 0):.1f}%</small>
        </div>
    </div>
    
    <div class="energy-grid">
        <div class="metric-card">
            <h3>Weather Conditions</h3>
            <p><strong>{weather_data.get('temperature', 'N/A')}°C</strong></p>
            <p>Wind: {weather_data.get('wind_speed', 'N/A')} m/s</p>
            <p>Humidity: {weather_data.get('humidity', 'N/A')}%</p>
            <small>{weather_data.get('description', weather_data.get('weather_condition', 'N/A'))}</small>
        </div>
        
        <div class="metric-card">
            <h3>Energy Demand</h3>
            <p><strong>{demand_data.get('predicted_demand_mw', 'N/A')} MW</strong></p>
            <small>Confidence: {demand_data.get('confidence', 0):.1%}</small>
        </div>
        
        <div class="metric-card">
            <h3>Renewable Generation</h3>
            <p><strong>{grid_data.get('renewable_generation', 'N/A')} MW</strong></p>
            <small>Capacity: {grid_data.get('renewable_capacity', 'N/A')} MW</small>
        </div>
    </div>
    """
    
    # Add AI analysis
    if ai_analysis and ai_analysis.get('status') == 'success':
        ai_report = ai_analysis.get('report', '').replace('\n', '<br>')
        html += f"""
        <div class="ai-response">
            <h3>AI-Generated Analysis</h3>
            <div>{ai_report}</div>
        </div>
        """
    
    return custom_css + html

def create_advanced_charts(result):
    """Create advanced interactive charts"""
    try:
        # Chart 1: Comprehensive Energy Overview
        fig1 = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Energy Mix', 'Renewable Potential', 'Demand Pattern', 'Efficiency Metrics'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "indicator"}]]
        )
        
        # Energy Mix Pie Chart
        renewable_gen = result['grid']['grid_status']['renewable_generation']
        demand = result['demand']['current_demand']['predicted_demand_mw']
        conventional = max(0, demand - renewable_gen)
        
        fig1.add_trace(go.Pie(
            labels=['Renewable', 'Conventional'],
            values=[renewable_gen, conventional],
            marker_colors=['#2ecc71', '#e74c3c']
        ), row=1, col=1)
        
        # Renewable Potential Bar Chart
        solar_pot = result['weather']['solar_potential']
        wind_pot = result['weather']['wind_potential']
        
        fig1.add_trace(go.Bar(
            x=['Solar', 'Wind'],
            y=[solar_pot, wind_pot],
            marker_color=['#f39c12', '#3498db'],
            text=[f"{solar_pot:.1f}%", f"{wind_pot:.1f}%"],
            textposition='auto'
        ), row=1, col=2)
        
        # 24-hour Demand Pattern
        forecast = result['demand'].get('forecast_24h', [])[:12]
        if forecast:
            hours = [f['hour'] for f in forecast]
            demands = [f['predicted_demand_mw'] for f in forecast]
            
            fig1.add_trace(go.Scatter(
                x=hours, y=demands,
                mode='lines+markers',
                name='Demand Forecast',
                line=dict(color='#9b59b6', width=3)
            ), row=2, col=1)
        
        # Efficiency Indicator
        efficiency = result['grid']['balancing_result'].get('efficiency', 0)
        fig1.add_trace(go.Indicator(
            mode="gauge+number",
            value=efficiency,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "System Efficiency (%)"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 90}}
        ), row=2, col=2)
        
        fig1.update_layout(height=700, title_text="Comprehensive Energy System Analysis")
        
        # Chart 2: Weather Impact Analysis
        weather_data = result['weather']['weather_data']
        
        fig2 = go.Figure()
        
        # Create weather impact radar chart
        categories = ['Temperature<br>Suitability', 'Wind<br>Conditions', 'Solar<br>Irradiance', 
                     'Humidity<br>Factor', 'Overall<br>Renewable']
        
        values = [
            min(100, 100 - abs(weather_data['temperature'] - 25) * 3),  # Temperature suitability
            min(100, weather_data['wind_speed'] * 8),  # Wind conditions
            max(0, 100 - weather_data['cloud_cover']),  # Solar irradiance
            max(0, 100 - weather_data['humidity']),  # Humidity factor
            result['weather']['renewable_score']  # Overall renewable score
        ]
        
        fig2.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Weather Impact',
            line_color='green'
        ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title="Weather Conditions Impact on Renewable Energy",
            height=500
        )
        
        # Chart 3: System Performance Timeline
        fig3 = go.Figure()
        
        # Simulate historical performance data
        hours = list(range(-12, 1))  # Last 12 hours + current
        performance_data = []
        
        for h in hours:
            base_performance = 75 + 15 * np.sin(h * np.pi / 6) + np.random.normal(0, 3)
            performance_data.append(max(0, min(100, base_performance)))
        
        fig3.add_trace(go.Scatter(
            x=hours,
            y=performance_data,
            mode='lines+markers',
            name='System Performance',
            line=dict(color='blue', width=3),
            fill='tonexty',
            fillcolor='rgba(0,100,80,0.2)'
        ))
        
        # Add current performance point
        current_performance = result['grid']['balancing_result'].get('efficiency', 75)
        fig3.add_trace(go.Scatter(
            x=[0],
            y=[current_performance],
            mode='markers',
            name='Current',
            marker=dict(size=15, color='red', symbol='diamond')
        ))
        
        fig3.update_layout(
            title="System Performance Timeline (Last 12 Hours)",
            xaxis_title="Hours from Now",
            yaxis_title="Performance (%)",
            height=400,
            hovermode='x unified'
        )
        
        return fig1, fig2, fig3
        
    except Exception as e:
        # Return error charts
        error_fig = go.Figure()
        error_fig.add_annotation(text=f"Chart Error: {str(e)}", 
                               xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False)
        return error_fig, error_fig, error_fig

def create_summary_table(result):
    """Create detailed summary table"""
    try:
        data = []
        
        # Weather metrics
        weather = result['weather']['weather_data']
        data.extend([
            ["Weather", "Temperature", f"{weather['temperature']:.1f}°C"],
            ["Weather", "Wind Speed", f"{weather['wind_speed']:.1f} m/s"],
            ["Weather", "Humidity", f"{weather['humidity']:.0f}%"],
            ["Weather", "Cloud Cover", f"{weather['cloud_cover']:.0f}%"],
            ["Weather", "Condition", weather.get('description', weather.get('weather_condition', 'N/A'))]
        ])
        
        # Energy metrics
        demand = result['demand']['current_demand']
        grid = result['grid']['grid_status']
        balance = result['grid']['balancing_result']
        
        data.extend([
            ["Energy", "Current Demand", f"{demand['predicted_demand_mw']:.2f} MW"],
            ["Energy", "Renewable Gen", f"{grid['renewable_generation']:.2f} MW"],
            ["Energy", "Grid Balance", balance['grid_balance']],
            ["Energy", "Efficiency", f"{balance.get('efficiency', 0):.1f}%"]
        ])
        
        # Renewable potential
        data.extend([
            ["Renewable", "Solar Potential", f"{result['weather']['solar_potential']:.1f}%"],
            ["Renewable", "Wind Potential", f"{result['weather']['wind_potential']:.1f}%"],
            ["Renewable", "Overall Score", f"{result['weather']['renewable_score']:.1f}%"]
        ])
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=["Category", "Metric", "Value"])
        return df.to_html(index=False, classes='metric-table', escape=False)
        
    except Exception as e:
        return f"<p>Error creating table: {str(e)}</p>"

def create_error_display(error_msg):
    """Create error display"""
    return f"""
    <div style="color: red; padding: 20px; border: 1px solid red; border-radius: 5px;">
        <h3>System Error</h3>
        <p>{error_msg}</p>
    </div>
    """

def real_time_analysis(city, duration):
    """Perform real-time analysis over specified duration"""
    results = []
    timestamps = []
    
    for i in range(int(duration)):
        result = energy_system.run_energy_forecast(city)
        if result['status'] == 'success':
            results.append({
                'timestamp': datetime.now(),
                'renewable_score': result['weather']['renewable_score'],
                'demand': result['demand']['current_demand']['predicted_demand_mw'],
                'efficiency': result['grid']['balancing_result'].get('efficiency', 0)
            })
        time.sleep(1)  # Wait 1 second between analyses
    
    if results:
        df = pd.DataFrame(results)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(results))),
            y=df['renewable_score'],
            mode='lines+markers',
            name='Renewable Score',
            line=dict(color='green')
        ))
        
        fig.add_trace(go.Scatter(
            x=list(range(len(results))),
            y=df['efficiency'],
            mode='lines+markers',
            name='System Efficiency',
            line=dict(color='blue'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f'Real-time Analysis - {city} ({duration}s)',
            xaxis_title='Time (seconds)',
            yaxis=dict(title='Renewable Score (%)', side='left'),
            yaxis2=dict(title='Efficiency (%)', side='right', overlaying='y'),
            height=400
        )
        
        return fig, f"Completed {len(results)} data points over {duration} seconds"
    
    return None, f"No data collected for {city}"

# Enhanced Gradio Interface
with gr.Blocks(title="Smart Energy Forecasting System - Professional Edition", 
               css=custom_css, theme=gr.themes.Soft()) as demo:
    
    gr.HTML("""
        <div class="energy-header">
            <h1>🔋 Smart Energy Forecasting System</h1>
            <h2>Multi-Agent AI System with Advanced Analytics</h2>
            <p>Professional Energy Management Dashboard</p>
        </div>
    """)
    
    with gr.Tab("🏢 Executive Dashboard"):
        with gr.Row():
            city_dropdown = gr.Dropdown(
                choices=["Jaffna", "Colombo", "Kandy", "Galle", "Negombo", 
                        "London", "New York", "Tokyo", "Mumbai", "Singapore"],
                label="🌍 Select City",
                value="Jaffna",
                scale=2
            )
            refresh_btn = gr.Button("🔄 Refresh Analysis", variant="primary", scale=1)
        
        dashboard_html = gr.HTML()
        
        with gr.Row():
            comprehensive_chart = gr.Plot(label="Comprehensive Analysis")
        
        with gr.Row():
            with gr.Column():
                weather_radar = gr.Plot(label="Weather Impact Analysis")
            with gr.Column():
                performance_timeline = gr.Plot(label="Performance Timeline")
        
        summary_table = gr.HTML(label="Detailed Metrics")
        
        refresh_btn.click(
            create_professional_dashboard,
            inputs=[city_dropdown],
            outputs=[dashboard_html, comprehensive_chart, weather_radar, 
                    performance_timeline, summary_table]
        )
    
    with gr.Tab("🤖 AI Intelligence Center"):
        gr.Markdown("## Advanced AI-Powered Energy Analysis")
        
        with gr.Row():
            with gr.Column(scale=2):
                ai_question = gr.Textbox(
                    label="🔍 Ask AI about Energy Systems",
                    placeholder="e.g., What optimization strategies would you recommend for maximum renewable efficiency?",
                    lines=3
                )
            with gr.Column(scale=1):
                ai_city = gr.Dropdown(
                    choices=["Jaffna", "Colombo", "Kandy", "Galle"],
                    label="🏙️ Context City",
                    value="Jaffna"
                )
        
        ask_ai_btn = gr.Button("🧠 Get AI Analysis", variant="primary", size="lg")
        ai_response = gr.HTML()
        
        # Predefined expert questions
        gr.Examples(
            examples=[
                ["What are the optimal conditions for renewable energy generation?"],
                ["How can we improve grid stability with current weather conditions?"],
                ["What investment priorities would maximize energy efficiency?"],
                ["Analyze the correlation between weather patterns and energy demand."],
                ["What are the main risks to energy security in this region?"]
            ],
            inputs=[ai_question],
            label="💡 Expert Questions"
        )
        
        ask_ai_btn.click(
            lambda q, c: f'<div class="ai-response"><h3>🤖 AI Analysis</h3><p><strong>Question:</strong> {q}</p><p><strong>Response:</strong> {energy_system.answer_question(q, c)}</p></div>',
            inputs=[ai_question, ai_city],
            outputs=[ai_response]
        )
    
    with gr.Tab("📊 Real-Time Monitoring"):
        gr.Markdown("## Live System Performance Monitoring")
        
        with gr.Row():
            monitor_city = gr.Dropdown(
                choices=["Jaffna", "Colombo", "London"],
                label="🏙️ City to Monitor",
                value="Jaffna"
            )
            duration_slider = gr.Slider(
                minimum=5, maximum=30, value=10,
                label="⏱️ Monitoring Duration (seconds)",
                step=5
            )
            monitor_btn = gr.Button("▶️ Start Monitoring", variant="secondary")
        
        realtime_chart = gr.Plot()
        monitor_status = gr.Textbox(label="Status", interactive=False)
        
        monitor_btn.click(
            real_time_analysis,
            inputs=[monitor_city, duration_slider],
            outputs=[realtime_chart, monitor_status]
        )
    
    with gr.Tab("📈 Predictive Analytics"):
        gr.Markdown("## Advanced Forecasting and Predictions")
        
        forecast_city = gr.Dropdown(
            choices=["Jaffna", "Colombo", "Kandy", "Galle"],
            label="🏙️ City for Forecast",
            value="Jaffna"
        )
        
        forecast_btn = gr.Button("📊 Generate Forecast", variant="primary")
        
        def create_forecast_analysis(city):
            result = energy_system.run_energy_forecast(city)
            if result['status'] == 'success':
                forecast_data = result['demand']['forecast_24h']
                df = pd.DataFrame(forecast_data)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['hour'],
                    y=df['predicted_demand_mw'],
                    mode='lines+markers',
                    fill='tonexty',
                    name='Demand Forecast'
                ))
                
                fig.update_layout(
                    title=f'24-Hour Energy Demand Forecast - {city}',
                    xaxis_title='Hours from Now',
                    yaxis_title='Demand (MW)',
                    height=500
                )
                
                return fig
            return None
        
        forecast_chart = gr.Plot()
        forecast_btn.click(create_forecast_analysis, inputs=[forecast_city], outputs=[forecast_chart])

def launch_professional_interface():
    """Launch the professional interface"""
    print("🚀 Launching Professional Energy System Interface...")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True,
        show_api=False
    )

if __name__ == "__main__":
    launch_professional_interface()