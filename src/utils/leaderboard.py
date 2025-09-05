from sqlalchemy import func
from src.models.db import db, User, Activity

def top_users(limit=10):
    rows = (db.session
            .query(User.username, func.sum(Activity.co2_saved_kg).label('total'))
            .join(Activity, Activity.user_id == User.id)
            .group_by(User.id)
            .order_by(func.sum(Activity.co2_saved_kg).desc())
            .limit(limit)
            .all())
    return [{'username': r[0], 'total_saved_kg': round(float(r[1] or 0.0), 3)} for r in rows]
