"""
Test script to verify GEMINI AI integration is working.
Run this after setting up your GOOGLE_API_KEY to test the AI parser.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.ai_parser import parse_with_ai
from utils.calculator import compute_savings_with_ai
from dotenv import load_dotenv

def test_ai_integration():
    """Test the AI parsing with sample activities."""
    
    # Load environment variables
    load_dotenv()
    
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY not found in environment variables.")
        print("📝 Please add your API key to .env file:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        return
    
    print("🤖 Testing GEMINI AI Integration...")
    print("=" * 50)
    
    # Test activities
    test_activities = [
        "I walked 3km to work instead of driving",
        "Had a vegetarian lunch instead of eating beef",
        "Composted kitchen scraps from dinner",
        "Used LED bulbs for 5 hours today",
        "Took a 2-minute shorter shower",
        "Worked from home, saved 20km commute",
        "Recycled 2kg of plastic bottles",
        "Used reusable bags instead of plastic ones",
    ]
    
    for activity in test_activities:
        print(f"\n📝 Input: '{activity}'")
        
        try:
            # Test AI parsing
            parsed = parse_with_ai(activity)
            if parsed:
                print(f"   ✅ Parsed: {parsed['action']} - {parsed.get('quantity', 1)} {parsed.get('unit', 'units')}")
                print(f"   🎯 Category: {parsed.get('category')}")
                if parsed.get('confidence'):
                    print(f"   📊 Confidence: {parsed.get('confidence'):.2f}")
                
                # Test CO2 calculation
                savings, meta, _ = compute_savings_with_ai(activity)
                print(f"   💚 CO2 Saved: {savings} kg")
            else:
                print("   ❌ Could not parse activity")
                
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed! If you see parsed results above, AI integration is working.")
    print("💡 If all activities show errors, check your GOOGLE_API_KEY configuration.")

if __name__ == "__main__":
    test_ai_integration()
