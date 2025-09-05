"""
Enhanced CO2 savings calculator with AI-powered activity recognition.
"""

from .factors import FACTORS, get_co2_factor, DEFAULT_FACTORS

def parse_with_ai_safe(raw_entry: str):
    """Safe AI parsing with fallback."""
    try:
        # Use only the simple parser to avoid NumPy issues
        from .ai_parser_simple import parse_with_ai as parse_simple
        result = parse_simple(raw_entry)
        if result:
            return result
    except Exception as e:
        print(f"Simple AI parser failed: {e}")
    
    return None

def compute_savings(parsed: dict):
    """
    Compute CO2 savings for a parsed environmental activity.
    
    Args:
        parsed: Dictionary with activity details from parser
        
    Returns:
        tuple: (co2_saved_kg, metadata)
    """
    if parsed is None:
        return 0.0, {}

    action = parsed.get('action', '')
    category = parsed.get('category', '')
    quantity = float(parsed.get('quantity', 1))
    unit = parsed.get('unit', '')
    instead_of = parsed.get('instead_of')
    subcategory = parsed.get('subcategory', '')
    
    # Get CO2 factor using the enhanced factor system
    co2_factor = get_co2_factor(action, category, instead_of)
    
    # Calculate savings
    savings = quantity * co2_factor
    
    # Create metadata
    meta = {
        'category': subcategory or f"{category}_{action}",
        'quantity': quantity,
        'unit': unit,
        'action': action,
        'instead_of': instead_of,
        'co2_factor': co2_factor
    }
    
    # Add confidence if available
    if 'confidence' in parsed:
        meta['confidence'] = parsed['confidence']
    
    return round(float(savings), 3), meta

def compute_savings_with_ai(raw_entry: str):
    """
    Parse activity using AI and compute CO2 savings.
    
    Args:
        raw_entry: Natural language description of environmental activity
        
    Returns:
        tuple: (co2_saved_kg, metadata, parsed_data)
    """
    # Try AI parsing first
    parsed = parse_with_ai_safe(raw_entry)
    
    if parsed is None:
        # Fallback to original parsing logic
        parsed = _legacy_parse(raw_entry)
    
    if parsed is None:
        return 0.0, {'error': 'Could not parse activity'}, None
    
    savings, meta = compute_savings(parsed)
    return savings, meta, parsed

def _legacy_parse(text: str):
    """
    Legacy parsing logic for backward compatibility.
    """
    if not text:
        return None
        
    import re
    
    t = text.lower().strip()
    DIST_RE = r'(?P<qty>\d+(?:\.\d+)?)\s*(?:km|kilometers?)'
    COUNT_RE = r'(?P<qty>\d+)'

    if 'walk' in t:
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if ('instead of car' in t or 'instead of driving' in t or 'drive' in t) else None
        return {
            'action': 'walk', 
            'category': 'transportation',
            'quantity': qty, 
            'unit': 'km', 
            'instead_of': instead
        }

    if 'cycle' in t or 'cycled' in t or 'bicycle' in t or 'bike' in t:
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if 'instead of car' in t else ('bus' if 'instead of bus' in t else None)
        return {
            'action': 'cycle',
            'category': 'transportation', 
            'quantity': qty, 
            'unit': 'km', 
            'instead_of': instead
        }

    if 'bus' in t and ('took' in t or 'ride' in t or 'rode' in t):
        m = re.search(DIST_RE, t)
        qty = float(m.group('qty')) if m else 1.0
        instead = 'car' if 'instead of car' in t else None
        return {
            'action': 'bus',
            'category': 'transportation',
            'quantity': qty, 
            'unit': 'km', 
            'instead_of': instead
        }

    if ('vegetarian' in t or 'veg' in t) and 'beef' in t:
        return {
            'action': 'meal_swap',
            'category': 'food', 
            'from': 'beef', 
            'to': 'veg', 
            'quantity': 1, 
            'unit': 'meal'
        }
    if ('vegetarian' in t or 'veg' in t) and 'chicken' in t:
        return {
            'action': 'meal_swap',
            'category': 'food',
            'from': 'chicken', 
            'to': 'veg', 
            'quantity': 1, 
            'unit': 'meal'
        }
    if ('meatless' in t or 'veg' in t or 'vegetarian' in t) and ('meal' in t or 'lunch' in t or 'dinner' in t):
        return {
            'action': 'meal_swap',
            'category': 'food',
            'from': 'chicken', 
            'to': 'veg', 
            'quantity': 1, 
            'unit': 'meal'
        }

    if 'bottle' in t or 'plastic bottle' in t:
        m = re.search(COUNT_RE, t)
        qty = int(m.group('qty')) if m else 1
        if 'avoid' in t or 'skipped' in t or 'reused' in t or 'refill' in t or 'refilled' in t:
            return {
                'action': 'plastic_bottle',
                'category': 'waste', 
                'quantity': qty, 
                'unit': 'count'
            }

    # Digital activities
    if ('did not use' in t or 'didnt use' in t or 'avoided using' in t) and ('phone' in t or 'smartphone' in t):
        # Extract hours from text
        hours = 24.0
        hour_match = re.search(r'(\d+(?:\.\d+)?)\s*hours?', t)
        if hour_match:
            hours = float(hour_match.group(1))
        
        return {
            'action': 'digital_detox',
            'category': 'digital',
            'quantity': hours,
            'unit': 'hours',
            'instead_of': 'normal_usage'
        }
    
    if 'digital detox' in t or 'screen free' in t or 'phone free' in t:
        hours = 24.0
        hour_match = re.search(r'(\d+(?:\.\d+)?)\s*hours?', t)
        if hour_match:
            hours = float(hour_match.group(1))
        
        return {
            'action': 'digital_detox', 
            'category': 'digital',
            'quantity': hours,
            'unit': 'hours',
            'instead_of': 'normal_usage'
        }

    return None

# Legacy function to maintain backward compatibility
def compute_savings_legacy(parsed: dict):
    """
    Legacy compute_savings function for backward compatibility.
    """
    if parsed is None:
        return 0.0, {}

    action = parsed.get('action')
    meta = {}

    if action == 'walk':
        km = float(parsed.get('quantity', 0))
        instead = parsed.get('instead_of')
        saved = 0.0
        if instead == 'car':
            saved = km * (FACTORS['car_kg_per_km'] - FACTORS['walk_kg_per_km'])
        meta = {'category': 'walk', 'quantity': km, 'unit': 'km'}

    elif action == 'cycle':
        km = float(parsed.get('quantity', 0))
        instead = parsed.get('instead_of')
        if instead == 'car':
            saved = km * (FACTORS['car_kg_per_km'] - FACTORS['cycle_kg_per_km'])
        elif instead == 'bus':
            saved = km * (FACTORS['bus_kg_per_km'] - FACTORS['cycle_kg_per_km'])
        else:
            saved = km * (FACTORS['car_kg_per_km'])
        meta = {'category': 'cycle', 'quantity': km, 'unit': 'km'}

    elif action == 'bus':
        km = float(parsed.get('quantity', 0))
        instead = parsed.get('instead_of')
        if instead == 'car':
            saved = km * (FACTORS['car_kg_per_km'] - FACTORS['bus_kg_per_km'])
        else:
            saved = 0.0
        meta = {'category': 'bus_instead_car', 'quantity': km, 'unit': 'km'}

    elif action == 'meal_swap':
        from_food = parsed.get('from')
        if from_food == 'beef':
            saved = FACTORS['meal_beef_to_veg_kg']
        elif from_food == 'chicken':
            saved = FACTORS['meal_chicken_to_veg_kg']
        else:
            saved = FACTORS['meal_chicken_to_veg_kg']
        meta = {'category': f'meal_{from_food}_to_veg', 'quantity': 1, 'unit': 'meal'}

    elif action == 'plastic_bottle':
        count = int(parsed.get('quantity', 1))
        saved = count * FACTORS['plastic_bottle_kg']
        meta = {'category': 'plastic_bottle_avoided', 'quantity': count, 'unit': 'count'}
    
    elif action == 'digital_detox':
        hours = float(parsed.get('quantity', 24))
        saved = hours * FACTORS['digital_detox_per_hour']
        meta = {'category': 'digital_detox', 'quantity': hours, 'unit': 'hours'}

    else:
        saved = 0.0

    return round(float(saved), 3), meta
