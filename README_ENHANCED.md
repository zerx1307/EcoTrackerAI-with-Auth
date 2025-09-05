# 🌱 EcoTrack AI with GEMINI Integration (Flask + Auth) — Enhanced Build

An intelligent Flask app where users **log eco-actions in natural language** using **GEMINI LLM** and instantly see **CO₂ saved**, with **login/signup**, **badges**, **leaderboard**, and a **delightfully emoji-fied UI**.

## ✨ New AI Features
- 🤖 **GEMINI LLM Integration** - Understands virtually any environmental activity description
- 🧠 **Smart Activity Recognition** - Handles complex, varied natural language input
- 📈 **Expanded Activity Categories** - Transportation, Energy, Food, Waste, Water, and more
- 🎯 **Confidence Scoring** - AI provides confidence levels for parsed activities
- 🔄 **Fallback Parsing** - Falls back to regex patterns if AI is unavailable

## 🚀 Quickstart

### 1. Environment Setup
```powershell
python -m venv venv
.env\Scripts\Activate
pip install -r requirements.txt
```

### 2. Configure GEMINI API
1. Get your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy `.env.example` to `.env`
3. Add your API key:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Initialize Database
```powershell
# (optional) seed demo users & data
python seed.py

# run the app
python app.py
```
Open http://127.0.0.1:5000

## 🎯 Supported Activities

The AI can now understand and track **hundreds** of environmental activities across categories:

### 🚗 Transportation
- Walking, cycling, public transit, carpooling
- Electric vehicles, scooters, trains
- Working from home instead of commuting
- **Examples**: *"Walked 3km to work instead of driving"*, *"Took the bus for 15km instead of my car"*

### ⚡ Energy  
- LED bulbs, solar panels, unplugging devices
- Energy-efficient appliances, air-drying clothes
- **Examples**: *"Replaced 5 incandescent bulbs with LEDs"*, *"Air-dried laundry instead of using dryer"*

### 🥗 Food
- Vegetarian/vegan meals, local/organic food
- Reducing food waste, plant-based options
- **Examples**: *"Had vegetarian lunch instead of beef"*, *"Bought local organic vegetables"*

### ♻️ Waste
- Recycling, composting, reusing items
- Avoiding single-use plastics, repairing vs replacing
- **Examples**: *"Recycled 2kg of paper"*, *"Used cloth bags instead of plastic"*

### 💧 Water
- Shorter showers, fixing leaks, rainwater collection
- Efficient appliances, water conservation
- **Examples**: *"Took 2-minute shorter shower"*, *"Fixed leaky faucet"*

### 🌱 Other
- Planting trees, sustainable fashion, green products
- **Examples**: *"Planted 3 trees in community garden"*, *"Bought sustainable clothing"*

## 🏗️ Technical Architecture

### Enhanced Components
- **`ai_parser.py`** - GEMINI LLM integration with langchain
- **`factors.py`** - Comprehensive CO2 emission factors database  
- **`calculator.py`** - Enhanced calculation engine with AI support
- **`parser.py`** - Hybrid parsing (AI-first, regex fallback)

### API Improvements
- Enhanced `/log` endpoint with AI parsing
- Better error messages and user feedback
- Confidence scoring for parsed activities

## 📊 Example Interactions

```
User: "I composted kitchen scraps today"
AI: Understands → composting 1kg organic waste
Result: 0.35 kg CO2 saved

User: "Worked from home instead of driving 25km to office"  
AI: Understands → remote work, 25km commute saved
Result: 3.0 kg CO2 saved

User: "Used a reusable water bottle instead of buying plastic ones"
AI: Understands → avoided single-use plastic
Result: 0.1 kg CO2 saved
```

## 🔧 Configuration Options

### Environment Variables
```bash
# Required for AI features
GOOGLE_API_KEY=your_google_api_key

# Flask settings
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///ecotrack.db
```

### Fallback Mode
If GOOGLE_API_KEY is not set or API is unavailable, the system automatically falls back to the original regex-based parsing for basic activities.

## 📁 Enhanced Structure
```
.
├─ app.py
├─ config.py
├─ requirements.txt           # Now includes langchain, google-generativeai
├─ .env.example              # Updated with GOOGLE_API_KEY
├─ src/
│  ├─ utils/
│  │  ├─ ai_parser.py        # 🆕 GEMINI LLM integration
│  │  ├─ factors.py          # 🔄 Expanded CO2 factors
│  │  ├─ calculator.py       # 🔄 Enhanced with AI support
│  │  └─ parser.py           # 🔄 Hybrid AI+regex parsing
│  └─ routes/
│     └─ api.py              # 🔄 Enhanced /log endpoint
└─ ... (other files unchanged)
```

## 🎮 Demo Activities to Try

Try logging these natural language activities:

- *"Took a 5-minute shorter shower today"*
- *"Biked 10km to work instead of driving"*
- *"Bought local organic tomatoes at farmer's market"*
- *"Repaired my laptop instead of buying a new one"*
- *"Used LED bulbs for 8 hours today"*
- *"Composted food scraps from dinner"*
- *"Worked from home, saved 40km commute"*

## 🚨 Troubleshooting

**AI Parsing Not Working?**
- Check your `GOOGLE_API_KEY` in `.env`
- Verify API key has proper permissions
- System will fall back to regex parsing automatically

**Installation Issues?**
- Ensure Python 3.8+ is installed
- Try: `pip install --upgrade pip` before installing requirements

## 🏅 Original Features (Still Included)
- 🔐 **Signup/Login/Logout** with Flask-Login + password hashing
- 📊 7‑day chart, **fun equivalents**, 💬 rotating **eco quotes/facts**
- 🏅 Badges (first log, streaks, milestones)
- 🏆 Leaderboard ranks **real users**
- 💾 SQLite for zero-config persistence
