# motivational_quotes.py

import random

QUOTES = [
    "You're stronger than you think.",
    "This too shall pass.",
    "You are not alone. Keep going.",
    "One step at a time is still progress.",
    "It's okay to feel what you're feeling.",
    "Every sunrise is a second chance.",
    "Take a breath. You've got this.",
    "Even the darkest night ends with a sunrise.",
    "Difficult roads often lead to beautiful destinations.",
    "You matter. More than you know.",
    "You’ve survived 100% of your bad days. That’s badass.",
    "શું થયું છે તે જરૂરી નથી, તમે કેવી રીતે આગળ વધો તે મહત્વપૂર્ણ છે.",  # Gujarati
    "हर दिन एक नई शुरुआत है।"  # Hindi
]

def get_random_quote():
    return random.choice(QUOTES)
