import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.ai_parser_simple import parse_with_ai

# Test the simple parser
test_entries = [
    "walked 2km instead of driving",
    "cycled to work 5km",
    "had a vegetarian meal",
    "recycled 3 bottles",
    "used LED bulbs"
]

print("Testing Simple AI Parser:")
print("=" * 40)

for entry in test_entries:
    result = parse_with_ai(entry)
    print(f"Input: '{entry}'")
    print(f"Result: {result}")
    print("-" * 40)
