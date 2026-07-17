import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Title
st.set_page_config(page_title="My Lovely AI Companion", page_icon="💖", layout="centered")

# Custom CSS styling to make it look clean, cozy, and ultra-friendly
st.markdown("""
    <style>
    .stApp { background-color: #fafbfc; }
    h1 { color: #ff4b4b; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: center; }
    .caption-text { text-align: center; font-size: 1.1rem; color: #555; margin-bottom: 25px; }
    .welcome-box { background-color: #fff0f2; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.write("<h1>✨ My Lovely AI Companion ✨</h1>", unsafe_allow_html=True)
st.write("<div class='caption-text'>Always here to chat, help, and keep you smiling! 😊💖</div>", unsafe_allow_html=True)

# 2. Grab your secret API key
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

# 3. Setup a very warm, polite, and human-like persona (100% FREE CONFIG)
system_instruction = (
    "You are a warm, deeply empathetic, supportive, and brilliant AI companion. "
    "Use charming emojis, be conversational, keep sentences short and easy to read, "
    "and always balance helpful facts with genuine kindness."
)
config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.8, # Slightly higher for more creative, human-like responses
)

# 4. Initialize Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Show a lovely welcome message if the chat is empty
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class='welcome-box'>
        <h3>👋 Hello there, lovely!</h3>
        <p>I am your brand new AI assistant. I'm fully set up, error-free, and ready to go! 
        Ask me anything, tell me about your day, or let's brainstorm together. What's on your mind? 🥰</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history with clean bubble layouts
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. User Input Area
if user_prompt := st.chat_input("Type a lovely message here... 💕"):
    # Show user message
    st.chat_message("user", avatar="👤").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate warm AI response
    with st.chat_message("assistant", avatar="🤖"):
        try:
            # Switched to 'gemini-3.1-flash-lite' to fix the discontinued model error
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=user_prompt,
                config=config
            )
            ai_response = response.text
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"Oh no! A tiny hitch happened: {e}. Let's try again! ✨")
