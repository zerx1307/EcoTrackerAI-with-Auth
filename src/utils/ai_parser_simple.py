"""
Simple AI-powered parser that avoids heavy NumPy dependencies.
"""

import os
import json
import re
import warnings
from typing import Dict, Optional, Any
from dotenv import load_dotenv

# Suppress all warnings to avoid NumPy issues
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Fallback patterns for activities
ACTIVITY_PATTERNS = {
    'transportation': {
        'walk': {
            'patterns': ['walk', 'walked', 'walking', 'on foot'],
            'default_unit': 'km',
            'default_instead_of': 'car'
        },
        'cycle': {
            'patterns': ['cycle', 'cycled', 'bike', 'bicycle', 'cycling'],
            'default_unit': 'km',
            'default_instead_of': 'car'
        },
        'bus': {
            'patterns': ['bus', 'public transport', 'transit'],
            'default_unit': 'km',
            'default_instead_of': 'car'
        },
        'train': {
            'patterns': ['train', 'railway', 'rail'],
            'default_unit': 'km',
            'default_instead_of': 'car'
        },
        'carpool': {
            'patterns': ['carpool', 'rideshare', 'shared ride'],
            'default_unit': 'trips',
            'default_instead_of': 'car'
        }
    },
    'energy': {
        'led_bulb': {
            'patterns': ['led', 'led bulb', 'energy efficient bulb'],
            'default_unit': 'bulbs',
            'default_instead_of': 'incandescent'
        },
        'unplug_devices': {
            'patterns': ['unplug', 'unplugged', 'turn off', 'switched off'],
            'default_unit': 'devices',
            'default_instead_of': 'standby'
        }
    },
    'food': {
        'vegetarian_meal': {
            'patterns': ['vegetarian', 'veggie', 'plant-based', 'vegan', 'meatless'],
            'default_unit': 'meals',
            'default_instead_of': 'beef'
        },
        'local_food': {
            'patterns': ['local food', 'locally grown', 'farmers market'],
            'default_unit': 'meals',
            'default_instead_of': 'imported'
        }
    },
    'waste': {
        'recycle': {
            'patterns': ['recycle', 'recycled', 'recycling'],
            'default_unit': 'items',
            'default_instead_of': 'throw_away'
        },
        'reuse': {
            'patterns': ['reuse', 'reused', 'repurpose'],
            'default_unit': 'items',
            'default_instead_of': 'new_purchase'
        },
        'avoid_plastic': {
            'patterns': ['avoid plastic', 'no plastic', 'reusable bag', 'cloth bag'],
            'default_unit': 'items',
            'default_instead_of': 'plastic_bag'
        }
    },
    'digital': {
        'digital_detox': {
            'patterns': ['did not use', 'avoided using', 'digital detox', 'phone free', 'screen free', 'no phone', 'no smartphone', 'smartphone free', 'did not used'],
            'default_unit': 'hours',
            'default_instead_of': 'normal_usage'
        },
        'reduce_screen_time': {
            'patterns': ['reduced screen time', 'less screen time', 'limit screen time', 'screen time reduction'],
            'default_unit': 'hours',
            'default_instead_of': 'normal_usage'
        },
        'digital_minimalism': {
            'patterns': ['digital minimalism', 'minimalist tech', 'simple phone', 'basic phone'],
            'default_unit': 'days',
            'default_instead_of': 'smartphone'
        }
    }
}

class SimpleActivityParser:
    """Simple pattern-based activity parser without heavy dependencies."""
    
    def __init__(self):
        """Initialize the simple parser."""
        self.patterns = ACTIVITY_PATTERNS
    
    def parse_activity(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse an activity description using pattern matching.
        
        Args:
            text: Natural language description of environmental activity
            
        Returns:
            Dictionary with parsed activity data or None if parsing fails
        """
        if not text or not text.strip():
            return None
        
        text = text.lower().strip()
        
        # Handle special patterns first
        if ('did not use' in text or 'didnt use' in text or 'avoided using' in text) and ('smartphone' in text or 'phone' in text):
            # Extract duration
            hours = 24.0  # default
            if '24 hours' in text or '24 hour' in text:
                hours = 24.0
            elif 'hour' in text:
                hour_match = re.search(r'(\d+(?:\.\d+)?)\s*hours?', text)
                if hour_match:
                    hours = float(hour_match.group(1))
            
            return {
                'action': 'digital_detox',
                'category': 'digital',
                'quantity': hours,
                'unit': 'hours',
                'instead_of': 'normal_usage',
                'subcategory': 'digital_detox',
                'confidence': 0.9
            }
        
        # Handle other digital patterns
        if any(pattern in text for pattern in ['digital detox', 'screen free', 'phone free']):
            hours = self._extract_number(text) or 24.0
            if 'minute' in text:
                hours = hours / 60.0  # convert minutes to hours
            elif 'day' in text:
                hours = hours * 24.0  # convert days to hours
            
            return {
                'action': 'digital_detox',
                'category': 'digital',
                'quantity': hours,
                'unit': 'hours',
                'instead_of': 'normal_usage',
                'subcategory': 'digital_detox',
                'confidence': 0.8
            }
        
        # Extract quantity from text
        quantity = self._extract_number(text)
        if quantity is None:
            quantity = 1.0
        
        # Check for specific recycling patterns first
        if 'recycle' in text or 'recycling' in text:
            quantity = self._extract_number(text) or 1.0
            return {
                'action': 'recycle',
                'category': 'waste',
                'quantity': quantity,
                'unit': 'items',
                'instead_of': 'throw_away',
                'subcategory': 'waste_recycle',
                'confidence': 0.8
            }
        
        # Try to match other patterns
        for category, actions in self.patterns.items():
            for action, config in actions.items():
                if any(pattern in text for pattern in config['patterns']):
                    # Determine unit
                    unit = config['default_unit']
                    if 'km' in text or 'kilometer' in text:
                        unit = 'km'
                    elif 'mile' in text:
                        unit = 'miles'
                    elif 'hour' in text:
                        unit = 'hours'
                    elif 'trip' in text or 'time' in text:
                        unit = 'trips'
                    
                    # Determine what it replaced
                    instead_of = None
                    if 'instead of car' in text or 'drive' in text or 'driving' in text:
                        instead_of = 'car'
                    elif 'instead of bus' in text:
                        instead_of = 'bus'
                    elif 'instead of beef' in text or 'beef' in text:
                        instead_of = 'beef'
                    elif 'instead of chicken' in text or 'chicken' in text:
                        instead_of = 'chicken'
                    else:
                        instead_of = config['default_instead_of']
                    
                    return {
                        'action': action,
                        'category': category,
                        'quantity': quantity,
                        'unit': unit,
                        'instead_of': instead_of,
                        'subcategory': f"{category}_{action}",
                        'confidence': 0.8
                    }
        
        return None
    
    def _extract_number(self, text: str) -> Optional[float]:
        """Extract the first number found in the text."""
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                pass
        return None

# Try to use the full AI parser, fall back to simple parser
def get_ai_parser():
    """Get the best available parser."""
    try:
        # Try to import and use the full AI parser
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            from .ai_parser import get_ai_parser as get_full_parser
            parser = get_full_parser()
            if parser:
                return parser
    except Exception as e:
        print(f"Full AI parser not available: {e}")
    
    # Fall back to simple parser
    return SimpleActivityParser()

def parse_with_ai(text: str) -> Optional[Dict[str, Any]]:
    """
    Parse activity text using the best available parser.
    
    Args:
        text: Natural language description of environmental activity
        
    Returns:
        Parsed activity dictionary or None
    """
    parser = get_ai_parser()
    if parser is None:
        return None
    return parser.parse_activity(text)
