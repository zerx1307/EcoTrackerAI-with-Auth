from sqlalchemy import func
from datetime import datetime, timedelta
from src.models.db import db, Activity, User

def evaluate_badges(user_id: int):
    if not user_id:
        return []
    total = db.session.query(func.sum(Activity.co2_saved_kg)).filter_by(user_id=user_id).scalar() or 0.0
    count = Activity.query.filter_by(user_id=user_id).count()

    badges = []
    if count >= 1:
        badges.append({'name': 'Getting Started 🟢', 'desc': 'Logged your first eco action'})
    today = datetime.utcnow().date()
    days = set(d.date() for d, in db.session.query(Activity.created_at).filter_by(user_id=user_id).all())
    streak = 0
    cur = today
    while cur in days:
        streak += 1
        cur = cur - timedelta(days=1)
    if streak >= 7:
        badges.append({'name': 'One Week Streak 🔥', 'desc': '7 days of eco actions'})
    if total >= 1:
        badges.append({'name': 'Kilo Saver 🥉', 'desc': 'Saved 1 kg CO₂'})
    if total >= 10:
        badges.append({'name': 'Ten Kilo Hero 🥈', 'desc': 'Saved 10 kg CO₂'})
    if total >= 25:
        badges.append({'name': 'Quarter Hundred 🥇', 'desc': 'Saved 25 kg CO₂'})
    return badges
