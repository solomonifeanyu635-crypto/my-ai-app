import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="My AI", page_icon="🤖")
st.title("🤖 My Custom AI Assistant")

# This automatically grabs your hidden key from the server settings
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

config = types.GenerateContentConfig(
    system_instruction="You are a helpful AI assistant. Use Google Search to verify facts.",
    tools=[{"google_search": {}}], 
    temperature=0.7,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Ask me anything..."):
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=config
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

