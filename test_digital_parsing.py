#!/usr/bin/env python3
"""
Test script for digital activity parsing
"""

from src.utils.calculator import compute_savings_with_ai

def test_digital_activities():
    test_entries = [
        'did not used smartphone for 24 hours',
        'didnt use phone for 8 hours', 
        'digital detox 12 hours',
        'avoided using smartphone for 6 hours',
        'phone free for 3 hours',
        'screen free for 2 hours',
        'did not use phone for 1 hour'
    ]

    print('Testing enhanced digital activity parsing:')
    print('=' * 50)
    
    for entry in test_entries:
        result = compute_savings_with_ai(entry)
        parsed = result[2]
        if parsed:
            print(f'✓ "{entry}"')
            print(f'  -> {result[0]} kg CO2 saved')
            print(f'  -> Category: {result[1].get("category", "unknown")}')
            print()
        else:
            print(f'✗ "{entry}" -> Failed to parse')
            print()

if __name__ == '__main__':
    test_digital_activities()
