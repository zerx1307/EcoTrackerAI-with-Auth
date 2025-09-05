from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import app
from src.models.db import db, User, Activity
from src.utils.parser import parse_entry
from src.utils.calculator import compute_savings

demo_users = [
    ("alice", "password1"),
    ("bob", "password2"),
    ("chloe", "password3"),
]

entries = [
    "walked 2 km instead of driving",
    "cycled 5 km instead of bus",
    "ate vegetarian instead of beef",
    "skipped 3 plastic bottles",
    "took bus 10 km instead of car",
]

with app.app_context():
    for u, p in demo_users:
        user = User.query.filter_by(username=u).first()
        if not user:
            user = User(username=u, password_hash=generate_password_hash(p))
            db.session.add(user)
            db.session.commit()

        base = datetime.utcnow().date() - timedelta(days=6)
        for i, e in enumerate(entries):
            when = base + timedelta(days=i % 7)
            parsed = parse_entry(e)
            if not parsed: 
                continue
            saved, meta = compute_savings(parsed)
            act = Activity(
                user_id=user.id,
                raw_entry=e,
                category=meta.get("category"),
                quantity=meta.get("quantity"),
                unit=meta.get("unit"),
                co2_saved_kg=saved,
                created_at=datetime(when.year, when.month, when.day)
            )
            db.session.add(act)
    db.session.commit()
    print("Seeded demo users and activities.")
