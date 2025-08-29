"""
Enhanced activity parser with AI integration.
"""

import re

DIST_RE = r'(?P<qty>\d+(?:\.\d+)?)\s*(?:km|kilometers?)'
COUNT_RE = r'(?P<qty>\d+)'

def parse_entry(text: str):
    """
    Parse activity entry using AI first, then fallback to regex patterns.
    
    Args:
        text: Natural language description of environmental activity
        
    Returns:
        Dictionary with parsed activity data or None
    """
    if not text:
        return None
    
    # Try AI parsing first (with safe imports)
    try:
        from .ai_parser_fixed import parse_with_ai
        ai_result = parse_with_ai(text)
        if ai_result is not None:
            return ai_result
    except Exception as e:
        print(f"AI parsing not available: {e}")
    
    # Fallback to legacy regex parsing
    return _legacy_parse_entry(text)

def _legacy_parse_entry(text: str):
    """
    Legacy regex-based parsing for backward compatibility.
    """
    if not text:
        return None
    t = text.lower().strip()

    if 'walk' in t:
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if ('instead of car' in t or 'instead of driving' in t or 'drive' in t) else None
        return {'action': 'walk', 'quantity': qty, 'unit': 'km', 'instead_of': instead}

    if 'cycle' in t or 'cycled' in t or 'bicycle' in t or 'bike' in t:
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if 'instead of car' in t else ('bus' if 'instead of bus' in t else None)
        return {'action': 'cycle', 'quantity': qty, 'unit': 'km', 'instead_of': instead}

    if 'bus' in t and ('took' in t or 'ride' in t or 'rode' in t):
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if 'instead of car' in t else None
        return {'action': 'bus', 'quantity': qty, 'unit': 'km', 'instead_of': instead}

    if ('vegetarian' in t or 'veg' in t) and 'beef' in t:
        return {'action': 'meal_swap', 'from': 'beef', 'to': 'veg', 'quantity': 1, 'unit': 'meal'}
    if ('vegetarian' in t or 'veg' in t) and 'chicken' in t:
        return {'action': 'meal_swap', 'from': 'chicken', 'to': 'veg', 'quantity': 1, 'unit': 'meal'}
    if ('meatless' in t or 'veg' in t or 'vegetarian' in t) and ('meal' in t or 'lunch' in t or 'dinner' in t):
        return {'action': 'meal_swap', 'from': 'chicken', 'to': 'veg', 'quantity': 1, 'unit': 'meal'}

    if 'bottle' in t or 'plastic bottle' in t:
        m = re.search(COUNT_RE, t)
        qty = int(m.group('qty')) if m else 1
        if 'avoid' in t or 'skipped' in t or 'reused' in t or 'refill' in t or 'refilled' in t:
            return {'action': 'plastic_bottle', 'quantity': qty, 'unit': 'count'}

    return None
