from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from src.models.db import db, User, Activity
from src.utils.badges import evaluate_badges
from src.utils.leaderboard import top_users
from src.utils.quotes import pick_quote

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirect unauthenticated users to login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Resolve user context: logged-in user
    uid = current_user.id

    # Totals for this user
    total_saved = 0.0
    series = {}
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=6)
    series = {str(week_ago + timedelta(days=i)): 0.0 for i in range(7)}

    total_saved = (db.session.query(func.sum(Activity.co2_saved_kg))
                   .filter_by(user_id=uid).scalar() or 0.0)

    rows = (db.session
            .query(func.date(Activity.created_at), func.sum(Activity.co2_saved_kg))
            .filter(Activity.user_id == uid, Activity.created_at >= week_ago)
            .group_by(func.date(Activity.created_at))
            .all())
    for d, s in rows:
        series[str(d)] = float(s or 0.0)

    badges = evaluate_badges(uid)
    leaders = top_users(limit=5)
    quote = pick_quote()

    return render_template('index.html',
                           total_saved=round(total_saved, 3),
                           series=series,
                           badges=badges,
                           leaders=leaders,
                           quote=quote)


@main_bp.route('/leaderboard')
def leaderboard_page():
    leaders = top_users(limit=50)
    return render_template('leaderboard.html', leaders=leaders)


@main_bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@main_bp.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages with conversation history."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
        
        # Initialize chat history in session if not exists
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Add user message to history
        session['chat_history'].append({
            'role': 'user',
            'message': user_message,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Generate bot response using AI
        try:
            import os
            import google.generativeai as genai
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                bot_response = "I'm sorry, but I need to be configured with an API key to chat with you. Please ask an administrator to set up the GOOGLE_API_KEY environment variable. 🤖"
            else:
                # Configure and create model
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')
                
                # Create context from recent chat history
                context = ""
                recent_history = session['chat_history'][-10:]  # Last 10 messages for context
                for msg in recent_history[:-1]:  # Exclude current message
                    role = "User" if msg['role'] == 'user' else "EcoBot"
                    context += f"{role}: {msg['message']}\n"
                
                # Create the prompt using your template
                prompt = f"""You are "EcoBot-chan", a friendly and knowledgeable environmental assistant for EcoTrack AI. 
Your role is to help users with:
- Environmental activities and their carbon footprint impact
- Eco-friendly lifestyle tips and suggestions
- Understanding sustainability concepts
- Interpreting CO2 savings and environmental benefits
- Encouraging green behavior and activities

Previous conversation:
{context}

Guidelines:
- Be conversational, friendly, and encouraging
- Use emojis to make responses engaging
- Provide practical, actionable advice
- When discussing CO2 savings, use specific numbers when possible
- Relate answers to the EcoTrack AI platform when relevant
- Keep responses concise but informative (2-3 sentences max)
- If the user message is a greeting or small task, respond even if the topic is not related to environment try to make them short
- If asked about non-environmental topics, politely decline and redirect to environment topics

User message: {user_message}

Respond as EcoBot:"""
                
                # Get response from AI
                response = model.generate_content(prompt)
                bot_response = response.text
                
        except Exception as e:
            print(f"AI chat error: {e}")
            bot_response = generate_fallback_response(user_message)
        
        # Add bot response to history
        session['chat_history'].append({
            'role': 'bot',
            'message': bot_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep only last 20 messages (10 exchanges)
        if len(session['chat_history']) > 20:
            session['chat_history'] = session['chat_history'][-20:]
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'history_count': len(session['chat_history'])
        })
        
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again!'
        }), 500


def generate_fallback_response(message):
    """Generate fallback responses for common environmental queries."""
    message = message.lower()
    
    if any(word in message for word in ['cycle', 'cycling', 'bike', 'bicycle']):
        return "🚴‍♀️ Cycling is amazing for the environment! On average, cycling instead of driving saves about 0.12 kg CO2 per kilometer. Plus it's great exercise! Try logging your cycling activities in EcoTrack AI to see your impact! 🌱"
    
    elif any(word in message for word in ['walk', 'walking']):
        return "🚶‍♀️ Walking is one of the most eco-friendly ways to travel! Every kilometer you walk instead of drive saves about 0.12 kg of CO2. It's free, healthy, and helps our planet! Log your walking activities to track your green impact! 🌍"
    
    elif any(word in message for word in ['recycle', 'recycling']):
        return "♻️ Recycling is fantastic! It can save 1-2 kg CO2 per kg of material recycled. Focus on paper, plastic, and aluminum - they have the biggest impact. Remember to clean containers before recycling! 🌱"
    
    elif any(word in message for word in ['vegetarian', 'vegan', 'plant', 'meat']):
        return "🌱 Plant-based eating is super impactful! Choosing a veggie meal over beef can save about 7 kg CO2, and over chicken saves about 1.5 kg CO2. Even one meatless meal per week makes a difference! 🥗"
    
    elif any(word in message for word in ['energy', 'electricity', 'led', 'bulb']):
        return "💡 Energy efficiency rocks! LED bulbs use 75% less energy than incandescent ones. Switching to LEDs and unplugging devices can save significant CO2. Every small action adds up! ⚡"
    
    elif any(word in message for word in ['car', 'driving', 'transport']):
        return "🚗 Transportation has a big environmental impact! Consider cycling, walking, public transport, or carpooling. Even combining errands into one trip helps. Electric vehicles are also becoming more accessible! 🔋"
    
    elif any(word in message for word in ['tips', 'help', 'how', 'reduce', 'footprint']):
        return "🌟 Here are easy eco-tips: Walk/bike more, eat less meat, recycle properly, use LED bulbs, take shorter showers, and unplug devices. Small daily choices create big environmental wins! Track your progress with EcoTrack AI! 🌱"
    
    elif any(word in message for word in ['co2', 'carbon', 'footprint', 'emission']):
        return "🌍 Your carbon footprint is the total CO2 you produce. Average person emits ~4-16 tons CO2/year! Transportation, food, and energy are biggest contributors. Use EcoTrack AI to see how your green actions reduce your footprint! 📊"
    
    else:
        return "🤖 I'm here to help with all things eco-friendly! Ask me about cycling, recycling, plant-based eating, energy saving, or any green lifestyle tips. I can also explain CO2 savings from different activities! 🌱 What interests you most?"
