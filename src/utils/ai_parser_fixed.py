"""
AI-powered parser using GEMINI LLM to understand and categorize environmental activities.
"""

import os
import json
import re
from typing import Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIActivityParser:
    def __init__(self):
        """Initialize the AI parser with GEMINI model."""
        # Dynamic imports to avoid numpy issues
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            try:
                from langchain_core.prompts import PromptTemplate
            except ImportError:
                from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            import google.generativeai as genai
        except ImportError as e:
            raise ImportError(f"Required dependencies not available: {e}")
            
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Configure the GEMINI model
        genai.configure(api_key=self.api_key)
        self.model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=self.api_key,
            temperature=0.1
        )
        
        # Define the prompt template for activity parsing
        self.prompt_template = PromptTemplate(
            input_variables=["activity_text"],
            template="""
You are an expert environmental activity parser. Your job is to analyze user input about eco-friendly activities and extract structured data.

Please analyze this activity description and return a JSON object with the following structure:
{{
    "action": "specific_action_type",
    "category": "broad_category",
    "quantity": number,
    "unit": "measurement_unit",
    "instead_of": "alternative_activity_replaced",
    "subcategory": "specific_subcategory",
    "confidence": 0.0-1.0
}}

Supported action types and their categories:
1. TRANSPORTATION:
   - walk, cycle, bus, train, carpool, electric_vehicle, scooter, metro, subway
   - Units: km, miles, trips
   - instead_of: car, taxi, airplane, motorcycle

2. ENERGY:
   - led_bulb, solar_panel, energy_efficient_appliance, unplug_devices, air_dry_clothes
   - Units: hours, watts, kwh, devices, loads
   - instead_of: incandescent, fossil_fuel, regular_appliance

3. FOOD:
   - vegetarian_meal, vegan_meal, local_food, organic_food, reduce_food_waste, plant_based
   - Units: meals, kg, portions, days
   - instead_of: beef, chicken, pork, processed_food, imported_food

4. WASTE:
   - recycle, compost, reuse, avoid_plastic, refill_bottle, cloth_bag, repair
   - Units: items, kg, bottles, bags
   - instead_of: throw_away, single_use, new_purchase

5. WATER:
   - shorter_shower, fix_leak, rain_water, low_flow, efficient_dishwasher
   - Units: minutes, liters, gallons, loads
   - instead_of: long_shower, running_tap, inefficient_appliance

6. OTHER:
   - plant_tree, green_space, eco_product, sustainable_fashion, work_from_home
   - Units: trees, hours, items, days
   - instead_of: conventional_product, commute, fast_fashion

Guidelines:
- Extract numerical quantities when mentioned (default to 1 if not specified)
- Infer reasonable units based on activity type
- Identify what conventional activity was replaced
- Set confidence based on clarity of the input
- Use descriptive subcategories for specific variants

Activity to analyze: "{activity_text}"

Return only valid JSON, no explanation:
"""
        )
        
        self.chain = LLMChain(llm=self.model, prompt=self.prompt_template)
    
    def parse_activity(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse an activity description using GEMINI LLM.
        
        Args:
            text: Natural language description of environmental activity
            
        Returns:
            Dictionary with parsed activity data or None if parsing fails
        """
        if not text or not text.strip():
            return None
        
        try:
            # Get response from GEMINI
            response = self.chain.run(activity_text=text.strip())
            
            # Clean up the response (remove any markdown formatting)
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            # Parse JSON response
            parsed_data = json.loads(response.strip())
            
            # Validate required fields
            required_fields = ['action', 'category', 'quantity', 'unit']
            if not all(field in parsed_data for field in required_fields):
                return self._fallback_parse(text)
            
            # Ensure numeric quantity
            try:
                parsed_data['quantity'] = float(parsed_data['quantity'])
            except (ValueError, TypeError):
                parsed_data['quantity'] = 1.0
            
            # Set default confidence if not provided
            if 'confidence' not in parsed_data:
                parsed_data['confidence'] = 0.8
            
            return parsed_data
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"AI parsing failed: {e}")
            return self._fallback_parse(text)
    
    def _fallback_parse(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Fallback parsing using regex patterns for common activities.
        """
        text = text.lower().strip()
        
        # Transportation patterns
        if any(word in text for word in ['walk', 'walked', 'walking']):
            quantity = self._extract_number(text) or 1.0
            unit = 'km' if any(unit in text for unit in ['km', 'kilometer']) else 'trips'
            return {
                'action': 'walk',
                'category': 'transportation',
                'quantity': quantity,
                'unit': unit,
                'instead_of': 'car' if 'instead of car' in text or 'drive' in text else None,
                'confidence': 0.6
            }
        
        elif any(word in text for word in ['cycle', 'cycled', 'bike', 'bicycle']):
            quantity = self._extract_number(text) or 1.0
            unit = 'km' if any(unit in text for unit in ['km', 'kilometer']) else 'trips'
            return {
                'action': 'cycle',
                'category': 'transportation',
                'quantity': quantity,
                'unit': unit,
                'instead_of': 'car' if 'car' in text else ('bus' if 'bus' in text else None),
                'confidence': 0.6
            }
        
        # Energy patterns
        elif any(word in text for word in ['led', 'led bulb', 'energy efficient']):
            return {
                'action': 'led_bulb',
                'category': 'energy',
                'quantity': self._extract_number(text) or 1.0,
                'unit': 'bulbs',
                'instead_of': 'incandescent',
                'confidence': 0.5
            }
        
        # Food patterns
        elif any(word in text for word in ['vegetarian', 'vegan', 'plant based']):
            return {
                'action': 'vegetarian_meal',
                'category': 'food',
                'quantity': self._extract_number(text) or 1.0,
                'unit': 'meals',
                'instead_of': 'beef' if 'beef' in text else 'chicken',
                'confidence': 0.6
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

# Global instance
_ai_parser = None

def get_ai_parser() -> Optional[AIActivityParser]:
    """Get or create the global AI parser instance."""
    global _ai_parser
    if _ai_parser is None:
        try:
            _ai_parser = AIActivityParser()
        except Exception as e:
            print(f"Failed to initialize AI parser: {e}")
            return None
    return _ai_parser

def parse_with_ai(text: str) -> Optional[Dict[str, Any]]:
    """
    Parse activity text using AI.
    
    Args:
        text: Natural language description of environmental activity
        
    Returns:
        Parsed activity dictionary or None
    """
    parser = get_ai_parser()
    if parser is None:
        return None
    return parser.parse_activity(text)
