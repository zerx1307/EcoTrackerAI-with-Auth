import requests
import json

def test_api_endpoint():
    """Test the /api/log endpoint"""
    url = "http://localhost:5000/api/log"
    
    test_cases = [
        {"entry": "did not used smartphone for 24 hours"},
        {"entry": "walked 2km instead of driving"},
        {"entry": "cycled to work 5km"},
        {"entry": "had a vegetarian meal"},
        {"entry": "recycled 3 bottles"},
        {"entry": "digital detox for 8 hours"}
    ]
    
    print("Testing EcoTracker API:")
    print("=" * 50)
    
    for i, data in enumerate(test_cases, 1):
        try:
            response = requests.post(url, json=data, timeout=10)
            print(f"Test {i}: {data['entry']}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"✅ Success! CO2 saved: {result.get('co2_saved_kg', 0)} kg")
                    meta = result.get('meta', {})
                    print(f"   Category: {meta.get('category', 'unknown')}")
                    print(f"   Action: {meta.get('action', 'unknown')}")
                    print(f"   Quantity: {meta.get('quantity', 0)} {meta.get('unit', '')}")
                    if 'message' in result:
                        print(f"   Message: {result['message']}")
                else:
                    print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                    if 'message' in result:
                        print(f"   Message: {result['message']}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_api_endpoint()
