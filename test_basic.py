"""
Simple test script to verify basic GEMINI AI integration without full langchain.
"""

import os
import json
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv

def simple_test():
    """Test basic setup without langchain."""
    
    # Load environment variables
    load_dotenv()
    
    print("🔧 EcoTracker AI - Basic Integration Test")
    print("=" * 45)
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables.")
        print("📝 Please add your API key to .env file:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        print("\n💡 Get your key from: https://makersuite.google.com/app/apikey")
        return False
    elif api_key == "your_google_api_key_here":
        print("⚠️  Please replace the placeholder with your actual API key in .env")
        return False
    else:
        print(f"✅ API key found (ends with: ...{api_key[-6:]})")
    
    # Test basic google-generativeai import
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        print("✅ Google Generative AI configured successfully")
        
        # Try to create a model (without actually using it to avoid API calls)
        model = genai.GenerativeModel('gemini-pro')
        print("✅ GEMINI model initialized")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Configuration warning: {e}")
        print("   (This might be okay if API key is valid)")
    
    # Test enhanced factors system
    try:
        from utils.factors import get_co2_factor, FACTORS
        
        # Test a few calculations
        print("\n🧮 Testing enhanced factors system:")
        
        factor = get_co2_factor('walk', 'transportation', 'car')
        print(f"   Walking vs Car: {factor} kg CO2/km")
        
        factor = get_co2_factor('vegetarian_meal', 'food', 'beef')
        print(f"   Vegetarian vs Beef: {factor} kg CO2/meal")
        
        factor = get_co2_factor('led_bulb', 'energy', 'incandescent')
        print(f"   LED vs Incandescent: {factor} kg CO2/hour")
        
        print("✅ Enhanced factors system working")
        
    except Exception as e:
        print(f"❌ Factors system error: {e}")
        return False
    
    # Test fallback parser
    try:
        from utils.parser import parse_entry
        
        test_entry = "I walked 5km to work instead of driving"
        result = parse_entry(test_entry)
        
        if result:
            print(f"\n🔍 Testing parser with: '{test_entry}'")
            print(f"   ✅ Parsed result: {result}")
        else:
            print("⚠️  Parser returned None (this might be expected without full AI)")
            
    except Exception as e:
        print(f"❌ Parser error: {e}")
        return False
    
    print("\n" + "=" * 45)
    print("🎉 Basic integration test completed!")
    print("\nℹ️  Note: Full AI parsing requires langchain to be working properly.")
    print("   The app will fall back to regex patterns if AI is unavailable.")
    print("\n🚀 You can now run: python app.py")
    
    return True

if __name__ == "__main__":
    success = simple_test()
    if not success:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
