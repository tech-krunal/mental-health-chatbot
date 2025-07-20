
# # app.py gpt





# app.py gemini

import streamlit as st
import datetime
import time

# --- Backend Imports ---
# This assumes you have these files in the same directory.
from chatbot import get_emotion
from gemini_bot import gemini_reply
from motivational_quotes import get_random_quote
from mood_tracker import log_mood, get_mood_history
from sos import check_for_sos_trigger, show_sos_info

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
        transition: all 0.2s ease-in-out;
    }

    @keyframes fadeInSlideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Message bubble colors */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-user"]) {
        background-color: #3c4043;
    }

    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-assistant"]) {
        background-color: #2d2d2f;
    }

    /* Header styling */
    .chat-header {
        text-align: left;
        margin-bottom: 2rem;
    }

    .chat-header h1 {
        font-size: 2.5em;
        font-weight: 600;
        color: #e8eaed;
        margin: 0;
    }

    .chat-header p {
        font-size: 1em;
        color: #9aa0a6;
        margin: 0;
    }

    /* --- Input Area Styling --- */
    .stChatInputContainer {
        background-color: #131314;
        border-top: 0px solid #2d2d2f;
        margin: 0 auto;
        max-width: 800px;
        background-color: #1e1f20;
        border: 0px solid #5f6368;
        border-radius: 24px;
        padding: 0.5rem 1rem;
    }

    /* Remove red focus border on input and style cleanly */
    div[data-testid="stChatInput"] textarea {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
        color: #e8eaed;
        background-color: transparent;
        font-size: 1rem;
    }

    /* Additional safeguard for focus borders on BaseWeb input layers */
    div[data-baseweb="textarea"]:focus,
    div[data-baseweb="textarea"]:focus-visible,
    div[data-baseweb="textarea"]:active {
        outline: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
    }

    /* Catch known dynamic Streamlit input wrapper classes */
    .st-cf:focus,
    .st-cg:focus,
    .st-ch:focus,
    .st-ci:focus {
        border-color: transparent !important;
        box-shadow: none !important;
    }
            
    /* Kill red border & shadow on textarea directly */
div[data-testid="stChatInput"] textarea,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="textarea"] {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
    border-color: transparent !important;
    background-color: transparent !important;
    color: #e8eaed !important;
}

/* Remove any focus styles on wrappers */
div[data-baseweb="textarea"]:focus,
div[data-baseweb="textarea"]:focus-within,
div[data-testid="stChatInput"]:focus,
div[data-testid="stChatInput"]:focus-within {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
}

/* Remove from known focusable Streamlit classes */
.st-cf:focus, .st-cg:focus, .st-ch:focus, .st-ci:focus,
.st-cf:focus-within, .st-cg:focus-within, .st-ch:focus-within, .st-ci:focus-within {
    border: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
    outline: none !important;
}


    /* Optional: Add subtle hover effect to input container */
    .stChatInputContainer:hover {
        background-color: #2d2d2f;
        transition: background-color 0.3s ease;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e1f20;
    }

    [data-testid="stSidebar"] .stButton button {
        background-color: #3c4043;
        color: #e8eaed;
        border-radius: 8px;
        width: 100%;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #5f6368;
        color: #e8eaed;
    }

    [data-testid="stSidebar"] .stRadio > label {
        color: #e8eaed;
    }

    [data-testid="stSidebar"] h2 {
        color: #e8eaed;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #9aa0a6;
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Stream the response
def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

# --- Sidebar Features (Using your original backend calls) ---
with st.sidebar:
    st.markdown("## 🌟 Need a little boost?")
    if st.button("Inspire Me"):
        quote = get_random_quote()
        st.info(f"💬 *{quote}*")

    st.markdown("---")
    st.markdown("## 🆘 Need Immediate Help?")
    if st.button("Show SOS Resources"):
        # This function now needs to write to the sidebar
        st.error("It seems you might be in distress. Please reach out for help.")
        show_sos_info() # Assuming this function uses st.sidebar.info/write

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

# Header
st.markdown("""
    <div class="chat-header">
        <h1>Aura</h1>
        <p>Here to listen, without judgment</p>
    </div>
""", unsafe_allow_html=True)

# --- UPDATED SECTION ---
# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Aura, your mental wellness companion. How are you feeling today?"}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    avatar = "✨" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        # Display emotion caption if it exists for an assistant message
        if message["role"] == "assistant" and message.get("emotion"):
            st.caption(f"Detected Emotion: {message['emotion']} ({message['confidence']}%)")

# Handle user input at the bottom of the page
if user_input := st.chat_input("Talk about what's on your mind..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🤡"):
        st.write(user_input)

    # SOS auto-trigger
    if check_for_sos_trigger(user_input):
        with st.chat_message("assistant", avatar="✨"):
            st.error("⚠️ It seems you might be in distress. I've displayed emergency resources in the sidebar. Please reach out immediately.")
        show_sos_info()
    else:
        # Generate and display bot response
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Aura is thinking..."):
                # --- YOUR ORIGINAL BACKEND LOGIC ---
                emotion, confidence = get_emotion(user_input)
                prompt = f"""
                You are Aura, a supportive and empathetic mental health companion.
                The user seems to be feeling {emotion}.
                Respond with kindness and understanding to their message: "{user_input}"
                """
                reply = gemini_reply(prompt)
                # --- END OF YOUR LOGIC ---

            # # Stream the response
            # def stream_response(text):
            #     for word in text.split():
            #         yield word + " "
            #         time.sleep(0.05)
            
             # We need to re-display the caption
            st.caption(f"Detected Emotion: {emotion} ({round(confidence * 100, 2)}%)")
            full_response = st.write_stream(stream_response(reply))
            
            # Add the complete bot response to session state with emotion info
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "emotion": emotion,
                "confidence": round(confidence * 100, 2)
            })
            
           

