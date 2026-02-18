# ⚡ Smart Renewable Energy Forecasting System

> A full-stack multi-agent AI system developed as a *group project for the module Information Retrieval and Web Analytics (IRWA)*.

An intelligent platform that predicts renewable energy generation, forecasts demand, and optimizes grid operations using autonomous agents, LLM-powered analysis (Claude/GPT), and BM25-inspired information retrieval.

### Key Statistics
- **Agents**: 3 autonomous agents (Weather, Demand, Grid Balancer)
- **LLM Models**: Claude 3.5 Sonnet + GPT-3.5 Turbo (fallback)
- **Forecast Horizon**: 24-hour + 5-day extended predictions
- **Performance**: Sub-100ms forecast generation, <50ms agent response time
- **Database**: SQLite with SQLAlchemy ORM, 6 core tables
- **Deployment**: Web-based with Gradio dashboard + REST API

---

## 🎯 Core Features

**Multi-Agent System**: 3 autonomous agents (Weather, Demand, Grid) with 300s API caching, pattern-based forecasting, priority dispatch (renewable → storage → conventional)

**AI/NLP**: Claude 3.5 Sonnet + GPT fallback, RAG-style Q&A, intent classification (Spacy), sentiment analysis (TextBlob), TF-IDF summarization

**Information Retrieval**: BM25-inspired ranking, multi-source search (weather/demand/grid/decisions), temporal filtering, 300s result caching

**Responsible AI**: Complete audit trail, bias detection, decision explainability, PII sanitization, impact scoring

**Web Dashboard**: Gradio interface with Plotly charts, 5 tabs (Dashboard/AI Chat/Analytics/Search/Metrics), real-time updates, CSV/PDF export

**Security**: JWT session management (3600s), Fernet encryption, regex input validation, audit logging

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│            Gradio Web Interface (Port 7860)         │
│       Dashboard | AI Chat | Analytics | Search      │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│          Smart Energy System Coordinator            │
│      (Orchestrates Agents, AI, DB, Security)        │
└──┬───────┬────────┬─────────┬─────────┬────────────┘
   │       │        │         │         │
┌──▼──┐ ┌─▼──┐ ┌──▼───┐ ┌───▼───┐ ┌──▼─────┐
│Multi│ │ AI │ │Data  │ │Security│ │   IR   │
│Agent│ │Svc │ │ base │ │Manager │ │ Engine │
└──┬──┘ └─┬──┘ └──┬───┘ └────────┘ └────────┘
   │      │       │
   │      │       └─ SQLite + SQLAlchemy ORM
   │      │
   │      └─ Claude API / OpenAI API
   │
   └─ OpenWeatherMap API
```

---

## 🤖 Multi-Agent System

### WeatherAgent
- Fetches OpenWeatherMap data (current + 5-day forecast)
- Calculates: solar potential = `100% - cloud_cover`, wind capacity from speed
- 300s TTL caching for rate limiting
- **Output**: Temperature, humidity, wind, cloud cover, solar/wind potentials, renewable score

### EnergyDemandAgent
- Pattern-based forecasting: `demand = base_MW × hourly × seasonal × weather × noise`
- Baseline: 1000 MW ±30% daily, ±20% seasonal variation
- Peak detection: >95% hourly factor
- **Output**: Predicted demand (MW), confidence, peak indicators

### GridBalancerAgent
- **Priority dispatch**: renewable → storage (80% max discharge) → conventional
- Grid metrics: frequency, voltage, load factor
- **Algorithm**: Use renewable first → charge/discharge storage → fill gap with conventional
- **Output**: Energy mix, grid balance, renewable %, storage level

---

## 🧠 AI & NLP Services

| Component | Technology | Purpose |
|-----------|-----------|---------|  
| **LLM Primary** | Claude 3.5 Sonnet | Energy reports, Q&A, RAG context retrieval |
| **LLM Fallback** | GPT-3.5 Turbo → Templates | Graceful degradation |
| **Intent Classification** | Rule-based patterns | Categorize queries (weather/demand/grid) |
| **NER** | Spacy `en_core_web_sm` | Extract locations, dates, values |
| **Sentiment** | TextBlob | User feedback polarity |
| **Summarization** | TF-IDF extractive | Report summaries |

## 💾 Database & Information Retrieval

**Database Schema** (SQLite + SQLAlchemy, indexed timestamp/location):
- `WeatherForecast`: city, temp, solar/wind potentials
- `DemandForecast`: demand_mw, confidence, is_peak
- `GridBalance`: renewable_pct, storage, balance
- `AIDecision`: decision, reasoning, impact
- `SystemMetrics`: agent_id, response_time, success_rate
- `UserSession`: session_id, user_id, expires_at

**IR Engine**: BM25-inspired ranking, keyword extraction, multi-source search (weather/demand/grid/decisions), temporal filtering (7d/30d/custom), 300s caching

## 🔧 Technology Stack

**Core**: Python 3.8+, Gradio 4.x, FastAPI, SQLAlchemy  
**AI/ML**: Anthropic SDK, OpenAI SDK, Transformers, Spacy, NLTK, TextBlob  
**Data**: NumPy, Pandas, SciPy, Plotly, Matplotlib  
**Security**: JWT (HS256), Fernet (AES-128 CBC), Bcrypt, regex validation, 3600s sessions  
**APIs**: OpenWeatherMap, PyOWM, Requests, Aiohttp  

**Dashboard Tabs**: Forecasting | AI Chat | Analytics | DB Search | System Metrics

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)
- API Keys (see Configuration section)

### Step 1: Clone/Download Project
```bash
git clone https://github.com/yourusername/smart-energy-system.git
cd smart-energy-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLP Models
```bash
# SpaCy English model
python -m spacy download en_core_web_sm

# NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 5: Configure Environment Variables

Create `.env` file in project root:

```env
# API Keys
OPENWEATHER_API_KEY=your_openweather_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here     # Optional
OPENAI_API_KEY=your_openai_key_here           # Optional

# Database
DATABASE_URL=sqlite:///./data/energy_system.db

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Configuration
ENVIRONMENT=development
DEBUG_MODE=True
MAX_FORECAST_DAYS=5
WEATHER_API_TIMEOUT=10
```

**Getting API Keys:**
- **OpenWeatherMap** (Required): [openweathermap.org/api](https://openweathermap.org/api) - Free tier: 1000 calls/day
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com) - For Claude AI features
- **OpenAI**: [platform.openai.com](https://platform.openai.com) - Fallback LLM option

### Step 6: Initialize Database

Database will be auto-created on first run, or manually initialize:
```bash
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

---

## 🚀 Usage Guide

### For End Users (Web Interface)

**Start the Application:**
```bash
python web/gradio_interface.py
```
Access at: `http://localhost:7860`

**Dashboard Features:**

1. **Main Tab - Energy Forecasting**
   - Enter city name (e.g., "Colombo", "New York")
   - Click "Generate Forecast" for real-time predictions
   - View weather conditions, demand forecast, grid balance
   - Download results as CSV

2. **AI Assistant Tab**
   - Ask natural language questions about energy systems
   - Example: "What's the renewable energy potential today?"
   - Get intelligent recommendations and insights
   - Export conversation as PDF

3. **Analytics Tab**
   - View historical performance metrics
   - Analyze forecast accuracy trends
   - Compare agent performance statistics
   - Interactive Plotly visualizations

4. **Database Search Tab**
   - Search historical forecasts by keywords
   - Filter by date range, city, data type
   - View detailed results with relevance scoring
   - Export search results

5. **System Metrics Tab**
   - Agent response times and success rates
   - API latency monitoring
   - Database query performance
   - Cache hit rates

### For Developers (Programmatic API)

**Basic Usage:**
```python
from main import SmartEnergySystem

# Initialize system with all features enabled
system = SmartEnergySystem(
    enable_ai=True,      # LLM services
    enable_db=True,      # Database logging
    enable_security=True # Security features
)

# Example 1: Run complete forecast cycle
result = system.run_energy_forecast(city="Colombo")

print(f"Demand: {result['demand']['current_demand']['predicted_demand_mw']} MW")
print(f"Renewable %: {result['grid']['balancing_result']['renewable_percentage']}%")
print(f"Solar Potential: {result['weather']['solar_potential']}%")

# Example 2: Natural language query
answer = system.answer_question(
    "What renewable sources are optimal for next 6 hours?",
    city="Colombo"
)
print(answer['answer'])

# Example 3: Database search
results = system.ir_engine.search(
    query="peak demand high load",
    filters={'date_range': '7days', 'city': 'Colombo'},
    limit=10
)
print(f"Found {results['total_results']} matching forecasts")

# Example 4: Agent-specific operations
weather = system.weather_agent.fetch_current_weather("London")
demand = system.demand_agent.predict_current_demand(weather)
grid = system.grid_agent.balance_grid(demand, weather)
```

---

## 📁 Project Structure

```
IRWA_smart_energy_system/
├── main.py                      # System orchestrator & coordinator
├── data_storage.py              # Data persistence utilities
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
│
├── agents/                      # Multi-Agent System
│   ├── __init__.py
│   ├── base_agent.py           # Abstract base class with logging
│   ├── weather_agent.py        # Weather data & forecasting
│   ├── demand_agent.py         # Energy demand prediction
│   └── grid_agent.py           # Grid balancing & optimization
│
├── ai_services/                 # AI & Machine Learning
│   ├── _init_.py
│   ├── llm_service.py          # Claude/GPT integration
│   ├── nlp_service.py          # NLP processing (intent, NER, sentiment)
│   └── responsible_ai.py       # Ethical AI framework
│
├── config/                      # Configuration
│   ├── _init_.py
│   └── settings.py             # System settings & environment config
│
├── database/                    # Database Management
│   ├── db_manager.py           # CRUD operations, query optimization
│   └── models.py               # SQLAlchemy ORM models
│
├── information_retrieval/       # Search & Retrieval
│   └── ir_engine.py            # IR engine with BM25 ranking
│
├── security/                    # Security & Authentication
│   ├── _init_.py
│   └── security_manager.py     # JWT auth, encryption, validation
│
├── web/                         # Web Interface
│   └── gradio_interface.py     # Gradio dashboard
│
├── tests/                       # Test Suite
│   ├── test_agents.py          # Agent tests
│   ├── test_ai_services.py     # AI service tests
│   └── test_phase4.py          # Integration tests
│
├── data/                        # Data Storage (auto-created)
│   └── energy_system.db        # SQLite database
│
├── logs/                        # Log Files (auto-created)
│   ├── energy_system.log
│   └── responsible_ai/         # AI audit logs
│
└── cache/                       # Cache Directory (auto-created)
```

---

## 🧪 Testing

**Run Test Suite:**
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_agents.py -v

# Coverage report
python -m pytest tests/ --cov=. --cov-report=html

# Integration tests
python -m pytest tests/test_phase4.py
```

**Test Coverage:**
- Agent Tests: Weather, Demand, Grid agents
- AI Service Tests: LLM, NLP, Responsible AI
- Integration Tests: End-to-end workflows
- Database Tests: CRUD operations
- Security Tests: Validation, encryption, JWT

---


## Team

Academic group project developed for Information Retrieval and Web Analytics coursework.

**Contributors:**
- System architecture, multi-agent coordination, LLM integration
- NLP services, responsible AI framework
- Frontend development, Gradio interface, visualization
- Database design, security implementation, testing

## �📄 License

This project is created for educational and portfolio purposes. Feel free to modify and adapt as needed.

## References

- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems*, Wiley.
- Hong, T. et al. (2016). Probabilistic energy forecasting: Global Energy Forecasting Competition 2014.
- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

<div align="center">

### ⭐ If you find this project useful, please consider starring it!

**Built with ❤️ by the IRWA Project Team**

</div>