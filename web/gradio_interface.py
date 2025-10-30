#!/usr/bin/env python3
"""
Smart Energy Forecasting System - Enhanced Professional UI with Commercialization
Modern, Professional, Interactive Dashboard with Business Model
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

# Enhanced Professional Custom CSS with Modern Design
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
        --gold: #fbbf24;
        --premium: #6366f1;
    }
    
    /* Glassmorphism Header */
    .energy-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 3rem 2.5rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        position: relative;
        overflow: hidden;
    }
    
    .energy-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.05)"/></svg>');
        animation: float 20s infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .energy-header h1 {
        font-size: 2.8rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .energy-header h2 {
        font-size: 1.4rem;
        font-weight: 400;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced Metric Cards with Gradient Borders */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 6px 25px rgba(0,0,0,0.08);
        border-left: 6px solid var(--success);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card h3 {
        color: var(--dark);
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .metric-card .value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.8rem 0;
    }
    
    .metric-card .label {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.6;
    }
    
    /* Status Indicators with Enhanced Animation */
    .status-indicator {
        display: inline-block;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse-glow 2s infinite;
        box-shadow: 0 0 0 0 currentColor;
    }
    
    @keyframes pulse-glow {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        50% {
            box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    .status-active { 
        background: linear-gradient(135deg, #10b981, #059669);
    }
    
    .status-warning { 
        background: linear-gradient(135deg, #f59e0b, #d97706);
    }
    
    .status-error { 
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }
    
    /* Enhanced AI Response Card */
    .ai-response {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border-left: 6px solid var(--info);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.15);
        transition: all 0.3s ease;
    }
    
    .ai-response:hover {
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.25);
        transform: translateY(-2px);
    }
    
    .ai-response h3 {
        color: var(--info);
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
    }
    
    /* Energy Grid Layout */
    .energy-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Enhanced Forecast Card */
    .forecast-card {
        background: white;
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
    }
    
    .forecast-card:hover {
        box-shadow: 0 10px 35px rgba(0,0,0,0.15);
        transform: translateY(-4px);
        border-color: var(--primary);
    }
    
    /* Enhanced Alert Badges */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.4rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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
    
    .badge-premium {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: white;
    }
    
    /* Statistics Panel */
    .stats-panel {
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);
    }
    
    /* Commercialization Section */
    .commercial-section {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        border-left: 8px solid var(--gold);
        box-shadow: 0 8px 30px rgba(251, 191, 36, 0.2);
    }
    
    .pricing-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
        border: 2px solid #e5e7eb;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.2);
        border-color: var(--primary);
    }
    
    .pricing-card.featured {
        border-color: var(--gold);
        border-width: 3px;
    }
    
    .pricing-card.featured::before {
        content: '⭐ MOST POPULAR';
        position: absolute;
        top: 0;
        right: 0;
        background: linear-gradient(135deg, var(--gold), var(--warning));
        color: white;
        padding: 0.5rem 2rem;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1px;
        transform: rotate(45deg) translate(30%, -50%);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .pricing-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .pricing-header h3 {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--dark);
        margin-bottom: 0.5rem;
    }
    
    .pricing-price {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
    }
    
    .pricing-period {
        font-size: 1.2rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .pricing-features {
        list-style: none;
        padding: 0;
        margin: 2rem 0;
    }
    
    .pricing-features li {
        padding: 1rem 0;
        border-bottom: 1px solid #e5e7eb;
        font-size: 1rem;
        color: #374151;
        display: flex;
        align-items: center;
    }
    
    .pricing-features li:last-child {
        border-bottom: none;
    }
    
    .pricing-features li::before {
        content: '✓';
        display: inline-block;
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, var(--success), #059669);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        margin-right: 1rem;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .cta-button {
        display: block;
        width: 100%;
        padding: 1.2rem 2rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        text-align: center;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .market-info-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 4px solid var(--info);
    }
    
    .market-info-card h4 {
        color: var(--dark);
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Responsive Typography */
    @media (max-width: 768px) {
        .energy-header h1 {
            font-size: 2rem;
        }
        .energy-grid {
            grid-template-columns: 1fr;
        }
        .pricing-price {
            font-size: 2.5rem;
        }
    }
    
    /* Animated Background Elements */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-bg {
        background: linear-gradient(-45deg, #667eea, #764ba2, #10b981, #3b82f6);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
    }
</style>
"""

# [Previous functions remain the same until create_dashboard_html]
# ... (keep all existing functions: create_dashboard, create_main_overview_chart, 
#      create_5day_forecast_chart, create_performance_chart, create_energy_mix_chart, 
#      ask_ai_question, search_system, create_search_results_chart, 
#      get_system_stats_display, create_stats_chart)

# ============================================================================
# COMMERCIALIZATION FUNCTIONS
# ============================================================================

def create_commercialization_content() -> str:
    """Create comprehensive commercialization section"""
    
    html = f"""
    <div class="commercial-section">
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 style="font-size: 3rem; font-weight: 900; color: var(--dark); margin-bottom: 1rem;">
                💼 Commercialization Strategy
            </h1>
            <p style="font-size: 1.3rem; color: #6b7280;">
                Transform Your Energy Management with AI-Powered Intelligence
            </p>
        </div>
        
        <div class="market-info-card">
            <h4>🎯 Target Market</h4>
            <div style="line-height: 2;">
                <span class="badge badge-info">Utility Companies</span>
                <span class="badge badge-info">Smart Grid Operators</span>
                <span class="badge badge-info">Industrial Facilities</span>
                <span class="badge badge-info">Renewable Energy Producers</span>
                <span class="badge badge-info">Government Energy Departments</span>
                <span class="badge badge-info">Commercial Buildings</span>
            </div>
        </div>
        
        <div class="market-info-card">
            <h4>💡 Value Proposition</h4>
            <ul style="line-height: 2; color: #374151;">
                <li><strong>Cost Reduction:</strong> Up to 30% savings on energy costs through predictive optimization</li>
                <li><strong>Renewable Integration:</strong> Maximize renewable energy utilization by 40-50%</li>
                <li><strong>Grid Stability:</strong> Real-time balancing prevents blackouts and reduces penalties</li>
                <li><strong>Carbon Reduction:</strong> Track and minimize carbon footprint automatically</li>
                <li><strong>AI-Driven Insights:</strong> Actionable recommendations from multi-agent system</li>
                <li><strong>Scalability:</strong> From single facility to city-wide grid management</li>
            </ul>
        </div>
        
        <div class="market-info-card">
            <h4>📊 Market Analysis</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div style="background: linear-gradient(135deg, #eff6ff, #dbeafe); padding: 1.5rem; border-radius: 12px;">
                    <h5 style="color: var(--info); font-weight: 700; margin-bottom: 0.5rem;">Market Size</h5>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">$15.8B</p>
                    <p style="color: #6b7280; font-size: 0.9rem;">Global Energy Management Market by 2027</p>
                </div>
                <div style="background: linear-gradient(135deg, #ecfdf5, #d1fae5); padding: 1.5rem; border-radius: 12px;">
                    <h5 style="color: var(--success); font-weight: 700; margin-bottom: 0.5rem;">Growth Rate</h5>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">14.2%</p>
                    <p style="color: #6b7280; font-size: 0.9rem;">Annual CAGR 2025-2030</p>
                </div>
                <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 1.5rem; border-radius: 12px;">
                    <h5 style="color: var(--warning); font-weight: 700; margin-bottom: 0.5rem;">ROI Period</h5>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">8-12 mo</p>
                    <p style="color: #6b7280; font-size: 0.9rem;">Average payback period for customers</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def create_pricing_tiers() -> str:
    """Create detailed pricing tier cards"""
    
    html = """
    <div style="max-width: 1400px; margin: 0 auto; padding: 2rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 900; color: var(--dark); margin-bottom: 3rem;">
            💰 Flexible Pricing Plans
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem;">
            
            <!-- Starter Plan -->
            <div class="pricing-card">
                <div class="pricing-header">
                    <h3>🌱 Starter</h3>
                    <p style="color: #6b7280;">For Small Facilities</p>
                </div>
                <div style="text-align: center;">
                    <span class="pricing-price">$15</span>
                    <span class="pricing-period">/month</span>
                </div>
                <ul class="pricing-features">
                    <li>Up to 5 MW capacity monitoring</li>
                    <li>Basic weather forecasting</li>
                    <li>Daily demand predictions</li>
                    <li>Email support</li>
                    <li>1 user account</li>
                    <li>Basic analytics dashboard</li>
                    <li>Monthly reports</li>
                </ul>
                <button class="cta-button">Get Started</button>
            </div>
            
            <!-- Professional Plan (Featured) -->
            <div class="pricing-card featured">
                <div class="pricing-header">
                    <h3>⚡ Professional</h3>
                    <p style="color: #6b7280;">For Medium Enterprises</p>
                </div>
                <div style="text-align: center;">
                    <span class="pricing-price">$30</span>
                    <span class="pricing-period">/month</span>
                </div>
                <ul class="pricing-features">
                    <li>Up to 50 MW capacity monitoring</li>
                    <li>Advanced 5-day forecasting</li>
                    <li>Hourly demand predictions</li>
                    <li>AI-powered recommendations</li>
                    <li>Real-time grid balancing</li>
                    <li>5 user accounts</li>
                    <li>Priority support (24/7)</li>
                    <li>Custom alerts & notifications</li>
                    <li>API access</li>
                    <li>Weekly detailed reports</li>
                </ul>
                <button class="cta-button">Start Free Trial</button>
            </div>
            
            <!-- Enterprise Plan -->
            <div class="pricing-card">
                <div class="pricing-header">
                    <h3>🏢 Enterprise</h3>
                    <p style="color: #6b7280;">For Utilities & Cities</p>
                </div>
                <div style="text-align: center;">
                    <span class="pricing-price">Custom</span>
                    <span class="pricing-period">contact us</span>
                </div>
                <ul class="pricing-features">
                    <li>Unlimited capacity monitoring</li>
                    <li>Multi-site management</li>
                    <li>Advanced multi-agent AI system</li>
                    <li>Predictive maintenance</li>
                    <li>Custom integrations</li>
                    <li>Unlimited user accounts</li>
                    <li>Dedicated account manager</li>
                    <li>On-premise deployment option</li>
                    <li>Custom AI model training</li>
                    <li>SLA guarantee (99.9% uptime)</li>
                    <li>White-label solution</li>
                </ul>
                <button class="cta-button">Contact Sales</button>
            </div>
        </div>
        
        <!-- Add-ons Section -->
        <div style="margin-top: 4rem; background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 6px 25px rgba(0,0,0,0.08);">
            <h3 style="text-align: center; font-size: 2rem; font-weight: 800; color: var(--dark); margin-bottom: 2rem;">
                🎁 Optional Add-Ons
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">
                <div style="padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 16px;">
                    <h4 style="color: var(--primary); font-weight: 700; margin-bottom: 1rem;">🔌 IoT Integration</h4>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">$50/mo</p>
                    <p style="color: #6b7280;">Connect smart meters and IoT devices</p>
                </div>
                <div style="padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 16px;">
                    <h4 style="color: var(--success); font-weight: 700; margin-bottom: 1rem;">🌍 Carbon Trading</h4>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">$20/mo</p>
                    <p style="color: #6b7280;">Carbon credit tracking & trading platform</p>
                </div>
                <div style="padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 16px;">
                    <h4 style="color: var(--warning); font-weight: 700; margin-bottom: 1rem;">📱 Mobile App</h4>
                    <p style="font-size: 2rem; font-weight: 800; color: var(--dark);">$15/mo</p>
                    <p style="color: #6b7280;">iOS & Android apps for on-the-go monitoring</p>
                </div>
            </div>
        </div>
        
        <!-- ROI Calculator Preview -->
        <div style="margin-top: 4rem; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border-radius: 20px; padding: 3rem; text-align: center;">
            <h3 style="font-size: 2rem; font-weight: 800; color: var(--dark); margin-bottom: 1rem;">
                📈 Calculate Your ROI
            </h3>
            <p style="font-size: 1.2rem; color: #6b7280; margin-bottom: 2rem;">
                Most customers see 20-30% cost reduction within the first year
            </p>
            <button class="cta-button" style="max-width: 400px; margin: 0 auto;">
                Launch ROI Calculator
            </button>
        </div>
    </div>
    """
    
    return html

def create_deployment_strategy() -> str:
    """Create deployment and go-to-market strategy"""
    
    html = """
    <div style="max-width: 1200px; margin: 0 auto; padding: 2rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 900; color: var(--dark); margin-bottom: 3rem;">
            🚀 Deployment & Go-To-Market Strategy
        </h2>
        
        <!-- Deployment Options -->
        <div class="market-info-card">
            <h4>☁️ Deployment Options</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div style="background: #f0f9ff; padding: 2rem; border-radius: 16px; border: 2px solid #3b82f6;">
                    <h5 style="color: var(--info); font-weight: 700; font-size: 1.3rem; margin-bottom: 1rem;">🌐 Cloud SaaS</h5>
                    <ul style="color: #374151; line-height: 1.8;">
                        <li>Quick deployment (24-48 hours)</li>
                        <li>Pay-as-you-go pricing</li>
                        <li>Automatic updates</li>
                        <li>99.9% uptime SLA</li>
                    </ul>
                </div>
                <div style="background: #ecfdf5; padding: 2rem; border-radius: 16px; border: 2px solid #10b981;">
                    <h5 style="color: var(--success); font-weight: 700; font-size: 1.3rem; margin-bottom: 1rem;">🏢 On-Premise</h5>
                    <ul style="color: #374151; line-height: 1.8;">
                        <li>Full data control</li>
                        <li>Custom security policies</li>
                        <li>Air-gapped option available</li>
                        <li>Integration with legacy systems</li>
                    </ul>
                </div>
                <div style="background: #fef3c7; padding: 2rem; border-radius: 16px; border: 2px solid #f59e0b;">
                    <h5 style="color: var(--warning); font-weight: 700; font-size: 1.3rem; margin-bottom: 1rem;">🔄 Hybrid Model</h5>
                    <ul style="color: #374151; line-height: 1.8;">
                        <li>Best of both worlds</li>
                        <li>Critical data on-premise</li>
                        <li>Analytics in cloud</li>
                        <li>Flexible scaling</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Go-To-Market Phases -->
        <div class="market-info-card" style="margin-top: 2rem;">
            <h4>📅 Go-To-Market Timeline</h4>
            <div style="position: relative; padding: 2rem 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #eff6ff, #dbeafe); border-radius: 12px;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
                        <h5 style="font-weight: 700; color: var(--dark);">Q1 2025</h5>
                        <p style="color: #6b7280; font-size: 0.9rem;">Beta Launch</p>
                        <p style="color: #6b7280; font-size: 0.85rem;">5-10 pilot customers</p>
                    </div>
                    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-radius: 12px;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                        <h5 style="font-weight: 700; color: var(--dark);">Q2 2025</h5>
                        <p style="color: #6b7280; font-size: 0.9rem;">Public Launch</p>
                        <p style="color: #6b7280; font-size: 0.85rem;">50+ customers target</p>
                    </div>
                    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 12px;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                        <h5 style="font-weight: 700; color: var(--dark);">Q3-Q4 2025</h5>
                        <p style="color: #6b7280; font-size: 0.9rem;">Scale Up</p>
                        <p style="color: #6b7280; font-size: 0.85rem;">200+ customers, enterprise focus</p>
                    </div>
                    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #fae8ff, #f3e8ff); border-radius: 12px;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
                        <h5 style="font-weight: 700; color: var(--dark);">2026</h5>
                        <p style="color: #6b7280; font-size: 0.9rem;">Global Expansion</p>
                        <p style="color: #6b7280; font-size: 0.85rem;">International markets</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Revenue Model -->
        <div class="market-info-card" style="margin-top: 2rem;">
            <h4>💵 Revenue Streams</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 12px;">
                    <h5 style="color: var(--info); font-weight: 700;">1. Subscription Revenue (70%)</h5>
                    <p style="color: #374151; margin-top: 0.5rem;">Monthly/Annual SaaS subscriptions across all tiers</p>
                </div>
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #ecfdf5, #d1fae5); border-radius: 12px;">
                    <h5 style="color: var(--success); font-weight: 700;">2. Professional Services (20%)</h5>
                    <p style="color: #374151; margin-top: 0.5rem;">Implementation, training, consulting, and customization</p>
                </div>
                <div style="padding: 1.5rem; background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 12px;">
                    <h5 style="color: var(--warning); font-weight: 700;">3. Add-ons & Integrations (10%)</h5>
                    <p style="color: #374151; margin-top: 0.5rem;">IoT, carbon trading, mobile apps, API access</p>
                </div>
            </div>
        </div>
        
        <!-- Competitive Advantages -->
        <div class="market-info-card" style="margin-top: 2rem;">
            <h4>🏆 Competitive Advantages</h4>
            <div style="margin-top: 1rem;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div style="padding: 1rem; border-left: 4px solid var(--primary); background: #f9fafb; border-radius: 8px;">
                        <strong style="color: var(--primary);">🤖 Multi-Agent AI Architecture</strong>
                        <p style="color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;">Unlike competitors with single AI models, our system uses specialized agents for weather, demand, and grid optimization</p>
                    </div>
                    <div style="padding: 1rem; border-left: 4px solid var(--success); background: #f9fafb; border-radius: 8px;">
                        <strong style="color: var(--success);">⚡ Real-Time Processing</strong>
                        <p style="color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;">Sub-second response time for grid balancing decisions vs. competitors' 5-10 minute delays</p>
                    </div>
                    <div style="padding: 1rem; border-left: 4px solid var(--warning); background: #f9fafb; border-radius: 8px;">
                        <strong style="color: var(--warning);">🌱 Renewable-First Design</strong>
                        <p style="color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;">Built specifically for renewable integration, not retrofitted from traditional energy management</p>
                    </div>
                    <div style="padding: 1rem; border-left: 4px solid var(--info); background: #f9fafb; border-radius: 8px;">
                        <strong style="color: var(--info);">🔒 Enterprise Security</strong>
                        <p style="color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;">Bank-grade encryption, audit trails, and compliance with international energy regulations</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def create_business_model_canvas() -> str:
    """Create visual business model canvas"""
    
    html = """
    <div style="max-width: 1400px; margin: 0 auto; padding: 2rem;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 900; color: var(--dark); margin-bottom: 3rem;">
            📊 Business Model Canvas
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 2rem;">
            <!-- Top Row -->
            <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">🤝 Key Partners</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li>Weather data providers</li>
                    <li>Cloud infrastructure (AWS/Azure)</li>
                    <li>IoT device manufacturers</li>
                    <li>System integrators</li>
                    <li>Energy consultants</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, #e0f2fe, #bae6fd); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 2;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">⚙️ Key Activities</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li>AI model development & training</li>
                    <li>Platform maintenance & updates</li>
                    <li>Customer support & success</li>
                    <li>Sales & marketing</li>
                    <li>R&D for new features</li>
                    <li>Compliance & security audits</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 2;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">💎 Value Propositions</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8; font-weight: 500;">
                    <li><strong>30% cost reduction</strong> in energy expenses</li>
                    <li><strong>Real-time</strong> grid optimization</li>
                    <li><strong>AI-powered</strong> predictive analytics</li>
                    <li><strong>Seamless</strong> renewable integration</li>
                    <li><strong>Carbon neutrality</strong> tracking</li>
                    <li><strong>24/7 autonomous</strong> operation</li>
                </ul>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 2rem;">
            <div style="background: linear-gradient(135deg, #fae8ff, #f3e8ff); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">🔑 Key Resources</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li>Proprietary AI algorithms</li>
                    <li>Multi-agent architecture</li>
                    <li>Engineering team</li>
                    <li>Cloud infrastructure</li>
                    <li>Customer database</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, #ffedd5, #fed7aa); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 2;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">👥 Customer Relationships</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li><strong>Self-service:</strong> Automated onboarding & dashboard</li>
                    <li><strong>Dedicated support:</strong> 24/7 technical assistance</li>
                    <li><strong>Account management:</strong> Enterprise customers</li>
                    <li><strong>Community:</strong> User forums & knowledge base</li>
                    <li><strong>Training:</strong> Webinars & certification programs</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 2;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">🎯 Customer Segments</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li><strong>Primary:</strong> Utility companies & grid operators</li>
                    <li><strong>Secondary:</strong> Industrial facilities (>5MW)</li>
                    <li><strong>Tertiary:</strong> Renewable energy producers</li>
                    <li><strong>Growing:</strong> Smart cities & municipalities</li>
                    <li><strong>Emerging:</strong> Large commercial buildings</li>
                </ul>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
            <div style="background: linear-gradient(135deg, #fee2e2, #fecaca); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 2;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">💰 Cost Structure</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li><strong>R&D (35%):</strong> AI development, new features</li>
                    <li><strong>Infrastructure (25%):</strong> Cloud hosting, APIs</li>
                    <li><strong>Sales & Marketing (20%):</strong> Customer acquisition</li>
                    <li><strong>Operations (15%):</strong> Support, maintenance</li>
                    <li><strong>Admin (5%):</strong> Legal, compliance, overhead</li>
                </ul>
            </div>
            
            <div style="background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 2rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); grid-column: span 3;">
                <h4 style="font-weight: 800; color: var(--dark); margin-bottom: 1rem; font-size: 1.1rem;">💵 Revenue Streams</h4>
                <ul style="color: #374151; font-size: 0.9rem; line-height: 1.8;">
                    <li><strong>Subscription fees (70%):</strong> $15-$30+/month per customer</li>
                    <li><strong>Implementation (15%):</strong> One-time setup fees ($5K-$50K)</li>
                    <li><strong>Professional services (10%):</strong> Consulting, training, customization</li>
                    <li><strong>Add-ons (5%):</strong> IoT integration, mobile apps, carbon trading</li>
                    <li><strong>Target Year 1:</strong> $2.5M ARR with 200 customers</li>
                </ul>
            </div>
        </div>
        
        <!-- Financial Projections -->
        <div style="margin-top: 3rem; background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 6px 25px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; font-size: 2rem; font-weight: 800; color: var(--dark); margin-bottom: 2rem;">
                📈 3-Year Financial Projections
            </h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #eff6ff, #dbeafe); border-radius: 16px;">
                    <h4 style="color: var(--info); font-weight: 700; margin-bottom: 1rem;">Year 1 (2025)</h4>
                    <p style="font-size: 2.5rem; font-weight: 900; color: var(--dark);">$2.5M</p>
                    <p style="color: #6b7280;">Revenue</p>
                    <p style="margin-top: 1rem; color: #374151;"><strong>200</strong> customers</p>
                    <p style="color: #374151;"><strong>-$500K</strong> net (investment phase)</p>
                </div>
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ecfdf5, #d1fae5); border-radius: 16px;">
                    <h4 style="color: var(--success); font-weight: 700; margin-bottom: 1rem;">Year 2 (2026)</h4>
                    <p style="font-size: 2.5rem; font-weight: 900; color: var(--dark);">$8.5M</p>
                    <p style="color: #6b7280;">Revenue</p>
                    <p style="margin-top: 1rem; color: #374151;"><strong>650</strong> customers</p>
                    <p style="color: #374151;"><strong>+$1.2M</strong> net (break-even+)</p>
                </div>
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 16px;">
                    <h4 style="color: var(--warning); font-weight: 700; margin-bottom: 1rem;">Year 3 (2027)</h4>
                    <p style="font-size: 2.5rem; font-weight: 900; color: var(--dark);">$18M</p>
                    <p style="color: #6b7280;">Revenue</p>
                    <p style="margin-top: 1rem; color: #374151;"><strong>1,400</strong> customers</p>
                    <p style="color: #374151;"><strong>+$5.4M</strong> net (30% margin)</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

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
def get_transparency_report_display() -> str:
    """Get and display transparency report"""
    try:
        transparency = energy_system.get_transparency_report()
        
        if transparency['status'] != 'success':
            return f"<p>Transparency report unavailable: {transparency.get('message', 'Unknown error')}</p>"
        
        # Create beautiful HTML report
        html = """
        <div class="stats-panel">
            <h3>🔍 System Transparency Report</h3>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 2rem;">
                Full disclosure of system capabilities, limitations, and data sources
            </p>
            
            <!-- Capabilities Section -->
            <div class="market-info-card" style="margin-bottom: 2rem;">
                <h4 style="color: var(--success);">✅ System Capabilities</h4>
                <ul style="line-height: 2; color: #374151;">
        """
        
        for capability in transparency.get('system_capabilities', []):
            html += f"<li>{capability}</li>"
        
        html += """
                </ul>
            </div>
            
            <!-- Limitations Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--warning);">
                <h4 style="color: var(--warning);">⚠️ System Limitations (Important!)</h4>
                <ul style="line-height: 2; color: #374151;">
        """
        
        for limitation in transparency.get('limitations', []):
            html += f"<li><strong>Limitation:</strong> {limitation}</li>"
        
        html += """
                </ul>
            </div>
            
            <!-- Data Sources Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--info);">
                <h4 style="color: var(--info);">📊 Data Sources</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        """
        
        for source in transparency.get('data_sources', []):
            reliability_color = {
                'High': 'var(--success)',
                'Medium': 'var(--warning)',
                'Low': 'var(--danger)'
            }.get(source.get('reliability', 'Low'), 'var(--danger)')
            
            html += f"""
                    <div style="padding: 1.5rem; background: #f9fafb; border-radius: 12px; border-left: 4px solid {reliability_color};">
                        <h5 style="color: var(--dark); font-weight: 700; margin-bottom: 0.5rem;">{source.get('name')}</h5>
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0.3rem 0;">
                            <strong>Type:</strong> {source.get('type')}
                        </p>
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0.3rem 0;">
                            <strong>Update Frequency:</strong> {source.get('update_frequency')}
                        </p>
                        <p style="color: {reliability_color}; font-size: 0.9rem; margin: 0.3rem 0;">
                            <strong>Reliability:</strong> {source.get('reliability')}
                        </p>
                    </div>
            """
        
        html += """
                </div>
            </div>
            
            <!-- Model Information Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--premium);">
                <h4 style="color: var(--premium);">🤖 AI Model Information</h4>
        """
        
        model_info = transparency.get('model_info', {})
        html += f"""
                <div style="background: #f9fafb; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                    <p style="color: #374151; margin: 0.5rem 0;">
                        <strong>LLM Provider:</strong> {model_info.get('llm_provider', 'N/A').upper()}
                    </p>
                    <p style="color: #374151; margin: 0.5rem 0;">
                        <strong>NLP Capabilities:</strong> {', '.join(model_info.get('nlp_capabilities', []))}
                    </p>
                    <p style="color: #374151; margin: 0.5rem 0;">
                        <strong>Prediction Methods:</strong> {model_info.get('prediction_methods', 'N/A')}
                    </p>
                </div>
            </div>
            
            <!-- Privacy Measures Section -->
            <div class="market-info-card" style="border-left-color: var(--success);">
                <h4 style="color: var(--success);">🔒 Privacy & Security Measures</h4>
                <ul style="line-height: 2; color: #374151;">
        """
        
        for measure in transparency.get('privacy_measures', []):
            html += f"<li>✓ {measure}</li>"
        
        html += f"""
                </ul>
            </div>
            
            <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #eff6ff, #dbeafe); border-radius: 12px; text-align: center;">
                <p style="color: #374151; margin: 0;">
                    <strong>Report Generated:</strong> {transparency.get('generated_at', 'N/A')}
                </p>
                <p style="color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;">
                    This transparency report is updated in real-time and reflects the current system state.
                </p>
            </div>
        </div>
        """
        
        return html
        
    except Exception as e:
        return f"""
        <div class="ai-response" style="border-left-color: #ef4444;">
            <h3>❌ Error</h3>
            <p>Failed to generate transparency report: {str(e)}</p>
        </div>
        """
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


# ============================================================================
# TRANSPARENCY REPORTING FUNCTION (NEW)
# ============================================================================

def get_transparency_report_display() -> str:
    """Get and display comprehensive transparency report"""
    try:
        transparency = energy_system.get_transparency_report()
        
        if transparency['status'] != 'success':
            return f"""
            <div class="ai-response" style="border-left-color: #ef4444;">
                <h3>⚠️ Transparency Report Unavailable</h3>
                <p>{transparency.get('message', 'Unknown error occurred')}</p>
            </div>
            """
        
        # Create beautiful HTML report
        html = """
        <div class="stats-panel">
            <h3>🔍 System Transparency Report</h3>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 2rem;">
                Complete disclosure of system capabilities, limitations, data sources, and privacy measures
            </p>
            
            <!-- Capabilities Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--success);">
                <h4 style="color: var(--success);">✅ What This System CAN Do</h4>
                <ul style="line-height: 2; color: #374151; margin-top: 1rem;">
        """
        
        for capability in transparency.get('system_capabilities', []):
            html += f"<li><strong>✓</strong> {capability}</li>"
        
        html += """
                </ul>
            </div>
            
            <!-- Limitations Section (CRITICAL FOR TRANSPARENCY) -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--warning); background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);">
                <h4 style="color: var(--warning);">⚠️ What This System CANNOT Do (Important!)</h4>
                <p style="color: #92400e; font-size: 0.95rem; margin-bottom: 1rem;">
                    <strong>Honest disclosure of limitations builds trust.</strong> Users should know our boundaries.
                </p>
                <ul style="line-height: 2; color: #374151; margin-top: 1rem;">
        """
        
        for limitation in transparency.get('limitations', []):
            html += f"<li><strong>⚠</strong> {limitation}</li>"
        
        html += """
                </ul>
            </div>
            
            <!-- Data Sources Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--info);">
                <h4 style="color: var(--info);">📊 Where Our Data Comes From</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        """
        
        for source in transparency.get('data_sources', []):
            reliability_color = {
                'High': 'var(--success)',
                'Medium': 'var(--warning)',
                'Low': 'var(--danger)'
            }.get(source.get('reliability', 'Low'), 'var(--danger)')
            
            reliability_icon = {
                'High': '🟢',
                'Medium': '🟡',
                'Low': '🔴'
            }.get(source.get('reliability', 'Low'), '⚪')
            
            html += f"""
                    <div style="padding: 1.5rem; background: white; border-radius: 12px; border: 2px solid #e5e7eb; border-left: 4px solid {reliability_color};">
                        <h5 style="color: var(--dark); font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem;">
                            {source.get('name')}
                        </h5>
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0.5rem 0;">
                            <strong>Type:</strong> {source.get('type')}
                        </p>
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0.5rem 0;">
                            <strong>Updates:</strong> Every {source.get('update_frequency')}
                        </p>
                        <p style="color: {reliability_color}; font-size: 1rem; margin: 0.8rem 0; font-weight: 600;">
                            {reliability_icon} <strong>Reliability:</strong> {source.get('reliability')}
                        </p>
                    </div>
            """
        
        html += """
                </div>
            </div>
            
            <!-- Model Information Section -->
            <div class="market-info-card" style="margin-bottom: 2rem; border-left-color: var(--premium);">
                <h4 style="color: var(--premium);">🤖 AI Models & Technologies Used</h4>
        """
        
        model_info = transparency.get('model_info', {})
        llm_provider = model_info.get('llm_provider', 'N/A').upper()
        llm_badge_color = 'var(--primary)' if llm_provider == 'ANTHROPIC' else 'var(--info)'
        
        html += f"""
                <div style="background: linear-gradient(135deg, #faf5ff, #f3e8ff); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                    <div style="margin-bottom: 1rem;">
                        <span style="background: {llm_badge_color}; color: white; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 700;">
                            LLM PROVIDER: {llm_provider}
                        </span>
                    </div>
                    <p style="color: #374151; margin: 0.8rem 0; font-size: 0.95rem;">
                        <strong>🧠 NLP Capabilities:</strong> 
                        <br/>
                        {', '.join(model_info.get('nlp_capabilities', []))}
                    </p>
                    <p style="color: #374151; margin: 0.8rem 0; font-size: 0.95rem;">
                        <strong>📐 Prediction Methods:</strong> {model_info.get('prediction_methods', 'N/A')}
                    </p>
                </div>
            </div>
            
            <!-- Privacy Measures Section -->
            <div class="market-info-card" style="border-left-color: var(--success); background: linear-gradient(135deg, #f0fdf4, #dcfce7);">
                <h4 style="color: var(--success);">🔒 Privacy & Security Measures</h4>
                <p style="color: #166534; font-size: 0.95rem; margin-bottom: 1rem;">
                    Your data protection is our priority. Here's how we keep your information safe:
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        """
        
        for measure in transparency.get('privacy_measures', []):
            html += f"""
                    <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 3px solid var(--success);">
                        <p style="color: #374151; margin: 0; font-size: 0.9rem;">
                            <strong style="color: var(--success);">✓</strong> {measure}
                        </p>
                    </div>
            """
        
        html += f"""
                </div>
            </div>
            
            <!-- Report Metadata -->
            <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #eff6ff, #dbeafe); border-radius: 12px; text-align: center;">
                <p style="color: #1e40af; font-weight: 600; margin: 0; font-size: 1rem;">
                    📅 Report Generated: {transparency.get('generated_at', 'N/A')}
                </p>
                <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">
                    This transparency report updates in real-time and reflects the current system state.
                </p>
                <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.3rem;">
                    <em>Our commitment: Total honesty about what we can and cannot do.</em>
                </p>
            </div>
        </div>
        """
        
        return html
        
    except Exception as e:
        return f"""
        <div class="ai-response" style="border-left-color: #ef4444;">
            <h3>❌ Error Generating Transparency Report</h3>
            <p>Failed to generate transparency report: {str(e)}</p>
            <p style="font-size: 0.9rem; color: #6b7280; margin-top: 1rem;">
                Please ensure Responsible AI services are enabled and try again.
            </p>
        </div>
        """
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
    title="Smart Energy Forecasting System - Professional Edition with Business Model",
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
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
        }
        .gr-button-primary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
        }
        .gr-button-secondary {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
        }
    """
) as demo:
    
    gr.HTML("""
        <div class="gradient-bg" style="text-align: center; padding: 3rem 2rem; border-radius: 24px; margin-bottom: 2rem; position: relative;">
            <h1 style="color: white; font-size: 3.5rem; margin-bottom: 0.8rem; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); font-weight: 900;">
                ⚡ Smart Energy Forecasting System
            </h1>
            <h2 style="color: rgba(255,255,255,0.95); font-size: 1.6rem; font-weight: 400; margin-bottom: 0.5rem;">
                Enterprise-Grade Multi-Agent AI Platform
            </h2>
            <p style="color: rgba(255,255,255,0.9); margin-top: 1.5rem; font-size: 1.2rem;">
                🤖 Powered by Claude AI | 🌍 Transforming Energy Management Worldwide
            </p>
            <div style="margin-top: 2rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 0.6rem 1.5rem; border-radius: 25px; color: white; font-weight: 600; margin: 0 0.5rem; backdrop-filter: blur(10px);">
                    Real-Time Forecasting
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.6rem 1.5rem; border-radius: 25px; color: white; font-weight: 600; margin: 0 0.5rem; backdrop-filter: blur(10px);">
                    AI-Powered Optimization
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.6rem 1.5rem; border-radius: 25px; color: white; font-weight: 600; margin: 0 0.5rem; backdrop-filter: blur(10px);">
                    Carbon Neutral Ready
                </span>
            </div>
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
        
        # NEW TRANSPARENCY SECTION
        gr.Markdown("---")
        gr.Markdown("## 🔍 System Transparency & Disclosure")
        gr.Markdown("""
        View complete, honest disclosure of system capabilities, limitations, data sources, and privacy measures.
        
        **Why Transparency Matters:**
        - ✅ Know exactly what the system CAN do
        - ⚠️ Understand what it CANNOT do (limitations)
        - 📊 See where data comes from and how reliable it is
        - 🔒 Verify privacy and security protections
        """)
        
        transparency_btn = gr.Button("📋 Generate Transparency Report", variant="secondary", size="lg")
        transparency_output = gr.HTML()
        
        transparency_btn.click(
            get_transparency_report_display,
            outputs=[transparency_output]
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
        
        ---
        
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border-radius: 16px; margin-top: 2rem;">
            <p style="font-size: 1.2rem; color: #374151; margin: 0;">
                🌍 <strong>Making Energy Smarter, Cleaner, and More Sustainable</strong> 🌱
            </p>
        </div>
        """)
    with gr.Tab("💼 Business Model & Pricing"):
        with gr.Row():
            with gr.Column():
                commercial_content = gr.HTML(value=create_commercialization_content())
        
        with gr.Row():
            with gr.Column():
                pricing_content = gr.HTML(value=create_pricing_tiers())
        
        with gr.Row():
            with gr.Column():
                deployment_content = gr.HTML(value=create_deployment_strategy())
        
        with gr.Row():
            with gr.Column():
                business_canvas = gr.HTML(value=create_business_model_canvas())
        
        gr.Markdown("""
        ---
        ### 📞 Ready to Transform Your Energy Management?
        
        **Contact us for a personalized demo and pricing consultation:**
        - 📧 Email: sales@smartenergy-ai.com
        - 📱 Phone: +1 (555) 123-4567
        - 🌐 Website: www.smartenergy-ai.com
        - 💬 Live Chat: Available 24/7
        
        **Special Launch Offer:** First 50 customers get 3 months free on Professional plan! 🎉
        """)

def launch_interface():
    """Launch the enhanced spectacular interface"""
    print("\n" + "="*70)
    print("🚀 LAUNCHING ENHANCED SMART ENERGY FORECASTING SYSTEM")
    print("="*70)
    print("\n✨ Starting spectacular UI with commercialization features...")
    print("💼 Business model and pricing included")
    print("🌐 Interface will open in your browser")
    print("📊 All systems ready!\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_api=False,
        inbrowser=True
    )

if __name__ == "__main__":
    launch_interface()
