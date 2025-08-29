import random

QUOTES = [
    "Small choices, big impact 🌍",
    "Every step counts 🚶‍♀️🌱",
    "The greenest energy is the energy you don’t use 💡",
    "Progress, not perfection ✨",
    "Act locally, impact globally 🌏",
    "Your future self says thanks 🙌",
    "A better planet starts with you 🌿",
    "Today’s choices shape tomorrow 🌞",
]

FACTS = [
    "Skipping one beef burger can save up to ~3 kg CO₂ 🍔➡️🥗",
    "A single tree can absorb ~22 kg CO₂ per year 🌳",
    "Cycling 5 km instead of driving saves ~0.6 kg CO₂ 🚴",
    "Recycling one plastic bottle can power a light bulb for hours ♻️💡",
    "Public transport emits far less CO₂ per passenger-km than cars 🚌",
]

def pick_quote():
    # 50/50 quote or fact
    prob = random.random()
    
    if prob <= 0.01:
        return "LEGENDARY SPAWN OF 1% CHANCE!!!"
    
    if prob < 0.5:
        return random.choice(QUOTES)
    return random.choice(FACTS)
