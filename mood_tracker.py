# mood_tracker.py

import datetime

# Dictionary to store moods per day
mood_log = {}

def log_mood(mood_emoji):
    today = datetime.date.today().isoformat()
    mood_log[today] = mood_emoji

def get_mood_history():
    return mood_log
