from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from src.models.db import db, User, Activity
from src.utils.parser import parse_entry
from src.utils.calculator import compute_savings, compute_savings_with_ai
from src.utils.leaderboard import top_users

api_bp = Blueprint('api', __name__)

def ensure_guest():
    """Ensure guest user exists, create if not found."""
    try:
        user = User.query.filter_by(username="guest").first()
        if not user:
            from werkzeug.security import generate_password_hash
            user = User(username="guest", password_hash=generate_password_hash("guest"))
            db.session.add(user)
            db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error ensuring guest user: {e}")
        # Try to fetch existing guest user again
        return User.query.filter_by(username="guest").first()

@api_bp.route('/log', methods=['POST'])
def log():
    data = request.get_json(silent=True) or request.form
    entry = (data.get('entry') or '').strip()
    if not entry:
        return jsonify({'ok': False, 'error': 'Missing "entry"'}), 400

    user = current_user if current_user.is_authenticated else ensure_guest()

    # Try enhanced AI parsing first
    try:
        saved, meta, parsed = compute_savings_with_ai(entry)
        
        if parsed is None:
            return jsonify({
                'ok': False, 
                'parsed': None, 
                'message': 'Could not understand entry. Try describing your eco-friendly activity differently.'
            }), 200
        
        # Create activity record with proper error handling
        try:
            act = Activity(
                user_id=user.id,
                raw_entry=entry,
                category=meta.get('category'),
                quantity=meta.get('quantity'),
                unit=meta.get('unit'),
                co2_saved_kg=saved
            )
            db.session.add(act)
            db.session.commit()
        except Exception as db_error:
            db.session.rollback()
            print(f"Database error when saving activity: {db_error}")
            return jsonify({
                'ok': False, 
                'error': 'Failed to save activity to database'
            }), 500

        # Include additional metadata in response
        response_meta = meta.copy()
        if parsed:
            response_meta.update({
                'action': parsed.get('action'),
                'instead_of': parsed.get('instead_of'),
                'confidence': parsed.get('confidence')
            })

        return jsonify({
            'ok': True, 
            'co2_saved_kg': saved, 
            'meta': response_meta,
            'message': f"Great! You saved {saved} kg of CO2 by {parsed.get('action', 'your eco-friendly action')}."
        })
        
    except Exception as e:
        # Fallback to original parsing if AI fails
        print(f"AI parsing failed, using fallback: {e}")
        
        try:
            parsed = parse_entry(entry)
            if parsed is None:
                return jsonify({
                    'ok': False, 
                    'parsed': None, 
                    'message': 'Could not understand entry. Please try describing your activity more clearly.'
                }), 200

            saved, meta = compute_savings(parsed)
            
            # Database operation with error handling
            try:
                act = Activity(
                    user_id=user.id,
                    raw_entry=entry,
                    category=meta.get('category'),
                    quantity=meta.get('quantity'),
                    unit=meta.get('unit'),
                    co2_saved_kg=saved
                )
                db.session.add(act)
                db.session.commit()
            except Exception as db_error:
                db.session.rollback()
                print(f"Database error when saving activity (fallback): {db_error}")
                return jsonify({
                    'ok': False, 
                    'error': 'Failed to save activity to database'
                }), 500

            return jsonify({'ok': True, 'co2_saved_kg': saved, 'meta': meta})
            
        except Exception as fallback_error:
            print(f"Both AI and fallback parsing failed: {fallback_error}")
            return jsonify({
                'ok': False,
                'error': 'Failed to process activity entry'
            }), 500

@api_bp.route('/stats', methods=['GET'])
def stats():
    user = current_user if current_user.is_authenticated else None
    if not user:
        return jsonify({'ok': True, 'series': {}, 'total': 0})

    days = int(request.args.get('days', 30))
    end = datetime.utcnow().date()
    start = end - timedelta(days=days-1)

    rows = (db.session
            .query(func.date(Activity.created_at), func.sum(Activity.co2_saved_kg))
            .filter(Activity.user_id == user.id, Activity.created_at >= start)
            .group_by(func.date(Activity.created_at))
            .all())

    series = {str(start + timedelta(days=i)): 0.0 for i in range(days)}
    total = 0.0
    for d, s in rows:
        series[str(d)] = float(s or 0.0)
        total += float(s or 0.0)
    return jsonify({'ok': True, 'series': series, 'total': round(total, 3)})

@api_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    leaders = top_users(limit=int(request.args.get('limit', 10)))
    return jsonify({'ok': True, 'leaders': leaders})
