import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load your API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# List all available models
models = genai.list_models()

for model in models:
    print(model.name)
