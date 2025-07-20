# gemini_bot.py gemini

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print("Gemini Key Loaded:", bool(api_key))  # Should print True
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Configure Gemini
genai.configure(api_key=api_key)

# --- REMOVED ---
# The model is no longer loaded globally. It will be loaded inside the function
# based on the user's selection.
# model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


# --- UPGRADED FUNCTION ---
# It now accepts a 'model_name' argument with a default value.
# The parameter is renamed to 'prompt' to match what app.py is sending.
def gemini_reply(prompt, model_name="models/gemini-1.5-flash-latest"):
    """
    Generates a response from the Gemini API using the specified model.
    """
    try:
        # Dynamically initialize the model based on the name passed from the UI
        model = genai.GenerativeModel(model_name)
        
        # Generate content using the passed prompt
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Gemini Error (using model {model_name}): {e}")
        return "Oops, I had trouble thinking... Please try again later."



# # 1.gemini_bot.py

# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# print("Gemini Key Loaded:", bool(api_key))  # Should print True
# if not api_key:
#     raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# # Configure Gemini
# genai.configure(api_key=api_key)

# # Load model (gemini-pro is great for text tasks)
# # model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
# model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


# def gemini_reply(user_message):
#     try:
#         response = model.generate_content(user_message)
#         return response.text
#     except Exception as e:
#         print("Gemini Error:", e)
#         return "Oops, I had trouble thinking... Please try again later."

