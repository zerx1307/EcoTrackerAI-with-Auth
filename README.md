# 🌱 EcoTrack AI (Flask + Auth) — Hackathon Build

An elegant Flask app where users **log eco-actions in natural language** and instantly see **CO₂ saved**, with **login/signup**, **badges**, **leaderboard**, and a **delightfully emoji-fied UI**.

## Quickstart
```powershell
python -m venv venv
.env\Scripts\Activate
pip install -r requirements.txt

# (optional) seed demo users & data
python seed.py

# run
python app.py
```
Open http://127.0.0.1:5000

Login: create your own account via **Sign up** (top-right).

## Highlights
- 🔐 **Signup/Login/Logout** with Flask-Login + password hashing
- 🧠 Rule-based NLP for quick parsing (no heavy ML)
- 📊 7‑day chart, **fun equivalents**, 💬 rotating **eco quotes/facts**
- 🏅 Badges (first log, streaks, milestones)
- 🏆 Leaderboard ranks **real users**
- 💾 SQLite for zero-config persistence

## Structure
```
.
├─ app.py
├─ config.py
├─ seed.py
├─ requirements.txt
├─ .env.example
├─ src
│  ├─ models
│  │  ├─ __init__.py
│  │  └─ db.py
│  ├─ routes
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  ├─ api.py
│  │  └─ auth.py
│  ├─ utils
│  │  ├─ __init__.py
│  │  ├─ factors.py
│  │  ├─ parser.py
│  │  ├─ calculator.py
│  │  ├─ equivalents.py
│  │  ├─ badges.py
│  │  ├─ leaderboard.py
│  │  └─ quotes.py
│  ├─ templates
│  │  ├─ base.html
│  │  ├─ index.html
│  │  ├─ leaderboard.html
│  │  ├─ login.html
│  │  └─ signup.html
│  └─ static
│     ├─ css/styles.css
│     └─ js/app.js
└─ .gitignore
```
