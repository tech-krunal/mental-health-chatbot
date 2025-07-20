# # chatbot.py gpt

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from torch.nn.functional import softmax
# import torch

# # Load model once
# tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
# model = AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-go-emotion")

# # Emotion label map (GoEmotions simplified for mental health)
# label_map = {
#     0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance",
#     4: "approval", 5: "caring", 6: "confusion", 7: "curiosity",
#     8: "desire", 9: "disappointment", 10: "disapproval", 11: "disgust",
#     12: "embarrassment", 13: "excitement", 14: "fear", 15: "gratitude",
#     16: "grief", 17: "joy", 18: "love", 19: "nervousness",
#     20: "optimism", 21: "pride", 22: "realization", 23: "relief",
#     24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
# }

# # Map similar ones into your chatbot-friendly ones
# emotion_groups = {
#     "joy": ["joy", "love", "gratitude", "excitement", "amusement", "pride"],
#     "sadness": ["sadness", "grief", "remorse", "disappointment"],
#     "anger": ["anger", "annoyance", "disgust", "disapproval"],
#     "fear": ["fear", "nervousness"],
#     "neutral": ["neutral", "realization", "confusion", "curiosity", "approval"]
# }

# def get_emotion(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True)
#     with torch.no_grad():
#         logits = model(**inputs).logits

#     probs = softmax(logits, dim=1)[0]
#     top_scores, top_indices = torch.topk(probs, 5)  # Get top 5 scores

#     # Convert tensor values to Python
#     top_scores = top_scores.tolist()
#     top_indices = top_indices.tolist()

#     # Score accumulator for simplified emotions
#     emotion_score = {group: 0.0 for group in emotion_groups}

#     for idx, score in zip(top_indices, top_scores):
#         original_label = label_map[idx]
#         for group, terms in emotion_groups.items():
#             if original_label in terms:
#                 emotion_score[group] += score

#     # Pick the emotion group with highest score
#     final_emotion = max(emotion_score, key=emotion_score.get)
#     confidence = round(emotion_score[final_emotion], 4)

#     return final_emotion, confidence



# chatbot.py gemini

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load model once
tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
model = AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-go-emotion")

# --- NEW: Keyword dictionary for overrides ---
# This dictionary contains strong keywords that will override the AI model's prediction
# to ensure critical emotions are not missed.
EMOTION_KEYWORDS = {
    "anger": ["punch", "hate", "furious", "angry", "pissed", "kill", "fight", "stupid", "idiot"],
    "sadness": ["suicide", "depressed", "hopeless", "i want to die"],
    "fear": ["scared", "terrified", "anxious"],
}


# Emotion label map (GoEmotions simplified for mental health)
label_map = {
    0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance",
    4: "approval", 5: "caring", 6: "confusion", 7: "curiosity",
    8: "desire", 9: "disappointment", 10: "disapproval", 11: "disgust",
    12: "embarrassment", 13: "excitement", 14: "fear", 15: "gratitude",
    16: "grief", 17: "joy", 18: "love", 19: "nervousness",
    20: "optimism", 21: "pride", 22: "realization", 23: "relief",
    24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
}

# Map similar ones into your chatbot-friendly ones
emotion_groups = {
    "joy": ["joy", "love", "gratitude", "excitement", "amusement", "pride", "optimism", "admiration"],
    "sadness": ["sadness", "grief", "remorse", "disappointment", "embarrassment"],
    "anger": ["anger", "annoyance", "disgust", "disapproval"],
    "fear": ["fear", "nervousness"],
    "neutral": ["neutral", "realization", "confusion", "curiosity", "approval", "caring", "desire", "relief", "surprise"]
}

def get_emotion(text):
    """
    Detects emotion in the text.
    First, it checks for strong keywords. If none are found, it uses the AI model.
    """
    lower_text = text.lower()

    # 1. Check for strong keywords first for a more robust detection.
    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(keyword in lower_text for keyword in keywords):
            # If a strong keyword is found, return it with high confidence
            # and skip the expensive model call.
            return emotion, 0.95

    # 2. If no keywords are found, proceed with your original AI model logic.
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = softmax(logits, dim=1)[0]

        # Get top label from model
        top_index = torch.argmax(probs).item()
        top_label = label_map[top_index]
        confidence = probs[top_index].item()

        # Map to simpler emotion category
        for group, terms in emotion_groups.items():
            if top_label in terms:
                return group, confidence
        
        # Fallback if the label isn't in any group
        return "neutral", confidence

    except Exception as e:
        print(f"Error during emotion prediction: {e}")
        # Fallback in case the model fails for any reason
        return "neutral", 0.5
