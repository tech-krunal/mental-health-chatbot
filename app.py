# app.py

import streamlit as st
import datetime
import time

# --- Backend Imports ---
# This assumes you have these files in the same directory.
from chatbot import get_emotion
from gemini_bot import gemini_reply # Assuming gemini_reply can take a model_name argument
from motivational_quotes import get_random_quote
from mood_tracker import log_mood, get_mood_history
from sos import  check_for_sos_trigger, get_sos_modal_html #,display_sos_info_in_modal #, render_sos_modal # , show_sos_info, 

# --- UI Generation ---

# Page configuration
st.set_page_config(
    page_title="Aura - Mental Wellness Companion",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for Gemini-like UI and animations
def load_custom_css():
    st.markdown("""
    <style>
        /* Main App Body */
        body {
            background-color: #131314;
        }

        /* Center the main content and add padding for the fixed input */
        .block-container {
            max-width: 800px;
            padding-top: 2rem;
            padding-bottom: 8rem;
        }

        /* Main chat area */
        [data-testid="main"] {
            background-color: #131314;
        }

        /* Chat Messages Styling */
        .stChatMessage {
            border-radius: 12px;
            padding: 1em;
            margin-bottom: 1rem;
            animation: fadeInSlideUp 0.5s ease-out forwards;
            opacity: 0;
            border: none;
        }

        @keyframes fadeInSlideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Message bubble colors */
        [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-user"]) { background-color: #3c4043; }
        [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-assistant"]) { background-color: #2d2d2f; }

        /* Header styling */
        .chat-header { text-align: left; margin-bottom: 2rem; }
        .chat-header h1 { font-size: 2.5em; font-weight: 600; color: #e8eaed; margin: 0; }
        .chat-header p { font-size: 1em; color: #9aa0a6; margin: 0; }
        
        /* --- CORRECTED: Input Area Styling --- */
        /* This is the outer container for the input bar, fixed at the bottom */
        .stChatInputContainer {
            background-color: #131314;
            border-top: 1px solid #2d2d2f;
        }
        
        # /* Watermark Caption below Input Box */
        # .stChatInputContainer::after {
        #     content: 'made with ❤️ by Krunal Mehta';
        #     display: block;
        #     text-align: center;
        #     color: #9aa0a6; /* Subtle grey text */
        #     font-size: 0.8rem;
        #     padding-top: 10px; /* Space between input box and watermark */
        #     /* This ensures it's centered with the input box */
        #     max-width: 800px;
        #     margin: 0 auto;
        # }  
        
        /* This is the container that gives the pill shape */
        # div[data-testid="stChatInput"] {
        #     margin: 0 auto;
        #     max-width: 800px;
        #     background-color: #1e1f20;
        #     border: 1px solid #5f6368;
        #     border-radius: 24px;
        #     /* Padding is removed from here */
        # }
        
        # div[data-testid="stChatInput"]:hover {
        #      border-color: #9aa0a6;
        # }
        
        /* This styles the text area inside the pill box */
        div[data-testid="stChatInput"] textarea {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
            color: #e8eaed;
            background-color: transparent;
            font-size: 1rem;
            /* Your requested padding is now applied directly to the text box */
            padding: 0.5rem 1rem;
            border-radius: 24px;
            transition: background-color 0.2s ease-in-out;
        }      
        
        /* Watermark Caption Styling */
        .watermark {
            # background-color: #ffffff; /* Match the main background */
            position: fixed;
            bottom: 10px; /* Adjust this value to control distance from the bottom */
            # left: 0;
            width: 700px;
            text-align: 20px;
            color: #9aa0a6;
            font-size: 0.8rem;
            z-index: 999;
            pointer-events: none; /* Allows clicking through the watermark text */
                transform: translateX(35px);
            # padding: 5px;
            # margin-left: 20px;
            padding-left: 2.5em;
            border-radius: 24px;
        }


        # /* Watermark Footer */
        # .footer {
        #     position: fixed;
        #     right: 0;
        #     bottom: 0;
        #     width: 100%;
        #     background-color: transparent; /* Match the main background */
        #     color: #9aa0a6; /* Subtle grey text */
        #     text-align: center;
        #     padding: 10px;
        #     font-size: 0.8rem;
        #     z-index: 999; /* Keep it above chat messages but below modals */
        #     border-top: 0px solid #2d2d2f;
        # }        
        
        /* --- Sidebar Styling --- */
        [data-testid="stSidebar"] { background-color: #1e1f20; }
        
        /* Model Selector in Sidebar */
        [data-testid="stSidebar"] div[data-testid="stSelectbox"] > label {
            color: #e8eaed;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        [data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background-color: #3c4043 !important;
            border: 1px solid #5f6368 !important;
            border-radius: 8px;
            color: #e8eaed;
        }

        /* Other Sidebar elements */
        [data-testid="stSidebar"] .stButton button { background-color: #3c4043; color: #e8eaed; border-radius: 8px; width: 100%; }
        [data-testid="stSidebar"] .stButton button:hover { background-color: #5f6368; color: #e8eaed; }
        [data-testid="stSidebar"] .stRadio > label { color: #e8eaed; }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #e8eaed; }
        [data-testid="stSidebar"] .stMarkdown { color: #9aa0a6; }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Helper function to simulate streaming
def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Aura, your mental wellness companion. How are you feeling today?"}
    ]
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "models/gemini-1.5-flash-latest" # Default model

# --- Sidebar Features ---
with st.sidebar:
    st.markdown("## 🧠 AI Model")
    model_options = {
        "Gemini 1.5 Flash": "models/gemini-1.5-flash-latest",
        "Gemini 1.5 Pro": "models/gemini-1.5-pro-latest",
        "Gemini 1.0 Pro": "models/gemini-pro-vision",
        "Gemma 3 (27B)": "models/gemma-3-27b-it"
    }
    model_display_names = list(model_options.keys())
    model_technical_names = list(model_options.values())

    try:
        current_model_index = model_technical_names.index(st.session_state.selected_model)
    except ValueError:
        current_model_index = 0

    selected_model_display = st.selectbox(
        "Choose a model",
        options=model_display_names,
        index=current_model_index,
        key="model_selector"
    )
    st.session_state.selected_model = model_options[selected_model_display]
    
    st.markdown("---")

    st.markdown("## 🌟 Need a little boost?")
    if st.button("Inspire Me"):
        quote = get_random_quote()
        st.info(f"💬 *{quote}*")

    st.markdown("---")
    st.markdown("## 🆘 Need Immediate Help?")
    if st.button("Show SOS Resources"):
        st.session_state.show_sos = True
    # st.markdown("## 🆘 Need Immediate Help?")
    # if st.button("Show SOS Resources"):
    #     st.session_state.show_sos = True # This is the only line that changes here

    st.markdown("---")
    st.markdown("## 🧭 How are you feeling today?")
    mood = st.radio(
        "Select your mood",
        ["😊", "🙂", "😐", "😟", "😢"],
        horizontal=True,
        key="mood"
    )
    if st.button("Log Mood"):
        log_mood(mood)
        st.success(f"Logged today's mood as: {mood}")

    st.write("### 📊 Mood History")
    mood_data = get_mood_history()
    if mood_data:
        for date, m in mood_data.items():
            st.markdown(f"📅 {date}: {m}")
    else:
        st.markdown("_No mood history yet._")

# --- Main Chat Interface ---

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "models/gemini-1.5-flash-latest"
if "show_sos" not in st.session_state:
    st.session_state.show_sos = False

# --- NEW LOGIC: Render Modal and Reset State ---
# This logic ensures the modal is injected only once per trigger.
if st.session_state.get("show_sos", False):
    # Inject the self-contained modal HTML
    st.markdown(get_sos_modal_html(), unsafe_allow_html=True)
    # Immediately reset the state. The JavaScript will handle the visual closing.
    # On the next rerun, this block won't execute, preventing the modal from reappearing.
    st.session_state.show_sos = False

# Header
st.markdown("""
    <div class="chat-header">
        <h1>Aura</h1>
        <p>Here to listen, without judgment</p>
    </div>
""", unsafe_allow_html=True)

# Display initial welcome message if chat is empty
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="✨"):
        st.write("Hello! I'm Aura, your mental wellness companion. How are you feeling today?")

# Display chat messages from history
for message in st.session_state.messages:
    avatar = "✨" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "assistant" and "emotion" in message:
            st.caption(f"Detected Emotion: {message['emotion']} ({message['confidence']}%)")
        st.write(message["content"])
        

# Handle user input
if user_input := st.chat_input("Talk about what's on your mind..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if check_for_sos_trigger(user_input):
        st.session_state.show_sos = True
    else:
        st.session_state.messages.append({
            "role": "assistant", "content": "...", "emotion": "Thinking", "confidence": 0
        })
        
        emotion, confidence = get_emotion(user_input)
        prompt = f"""
        You are Aura, a supportive and empathetic mental health companion.
        The user seems to be feeling {emotion}.
        Respond with kindness and understanding to their message: "{user_input}"
        """
        reply = gemini_reply(prompt, model_name=st.session_state.selected_model)
        
        st.session_state.messages[-1] = {
            "role": "assistant", 
            "content": reply,
            "emotion": emotion,
            "confidence": round(confidence * 100, 2)
        }
    
    st.rerun()

# --- Footer ---
st.markdown("""
<div class="watermark">
    made with ❤️ by Krunal Mehta
</div>
""", unsafe_allow_html=True)


# # --- Main Chat Interface ---

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "selected_model" not in st.session_state:
#     st.session_state.selected_model = "models/gemini-1.5-flash-latest"
# if "show_sos" not in st.session_state:
#     st.session_state.show_sos = False

# # Header
# st.markdown("""
#     <div class="chat-header">
#         <h1>Aura</h1>
#         <p>Here to listen, without judgment</p>
#     </div>
# """, unsafe_allow_html=True)

# # Display initial welcome message if chat is empty
# if not st.session_state.messages:
#     with st.chat_message("assistant", avatar="✨"):
#         st.write("Hello! I'm Aura, your mental wellness companion. How are you feeling today?")

# # Display chat messages from history
# for message in st.session_state.messages:
#     avatar = "✨" if message["role"] == "assistant" else "🧑‍💻"
#     with st.chat_message(message["role"], avatar=avatar):
#         st.write(message["content"])
#         if message["role"] == "assistant" and "emotion" in message:
#             st.caption(f"Detected Emotion: {message['emotion']} ({message['confidence']}%)")

# # --- CORRECTED: Render SOS Modal and Hidden Button ---
# if st.session_state.get("show_sos", False):
#     # Render the HTML/CSS/JS for the modal
#     st.markdown(get_sos_modal_html(), unsafe_allow_html=True)
    
#     # Render the hidden button that the JS will click
#     # Assign a unique, identifiable key
#     if st.button("CloseModal", key="hidden_close_button_sos"):
#         st.session_state.show_sos = False
#         st.rerun()

# # Handle user input
# if user_input := st.chat_input("Talk about what's on your mind..."):
#     # Add and display user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
    
#     # Check for SOS trigger and update state
#     if check_for_sos_trigger(user_input):
#         st.session_state.show_sos = True
#     else:
#         # Add a placeholder for the bot's response
#         st.session_state.messages.append({
#             "role": "assistant", "content": "...", "emotion": "Thinking", "confidence": 0
#         })
        
#         # Get the actual response from the backend
#         emotion, confidence = get_emotion(user_input)
#         prompt = f"""
#         You are Aura, a supportive and empathetic mental health companion.
#         The user seems to be feeling {emotion}.
#         Respond with kindness and understanding to their message: "{user_input}"
#         """
#         reply = gemini_reply(prompt, model_name=st.session_state.selected_model)
        
#         # Update the placeholder with the real content
#         st.session_state.messages[-1] = {
#             "role": "assistant", 
#             "content": reply,
#             "emotion": emotion,
#             "confidence": round(confidence * 100, 2)
#         }
    
#     # Rerun the app to display the new messages and/or modal
#     st.rerun()
