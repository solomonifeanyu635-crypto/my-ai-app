import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Deep Thought Engine", 
    page_icon="🧠", 
    layout="wide"  # Wide layout accommodates long, detailed analytical answers
)

st.title("🧠 Deep Thought Engine")
st.caption("Advanced analytical interface designed for rigorous logic, precise facts, and structured problem-solving.")

# 2. Initialize Gemini Client
api_key = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 3. Memory Architecture (Persistent Multi-Turn Chat)
# Standardizes storage using the official Google Content type format
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Strict Real-World Persona Configuration
system_instruction = (
    "You are an elite, objective, and deeply analytical AI researcher. "
    "Your primary goal is to provide realistic, hyper-accurate, and deeply thought-out answers. "
    "Break down complex problems step-by-step. "
    "Do not sugarcoat facts, use fluff, or include conversational fillers. "
    "Use markdown tables, bullet points, and clean structuring to present data clearly."
)

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.2,          # Extremely low temperature forces factual accuracy and deterministic logic
    max_output_tokens=4000,   # High limit allows the model to fully flesh out deep thoughts
)

# 5. Render Historical Chat Context
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Real-Time Processing & Execution Loop
if user_prompt := st.chat_input("Enter a complex question or topic to analyze..."):
    
    # Render user prompt immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Execute Deep Thinking Pipeline
    with st.chat_message("assistant"):
        # Use st.empty to stream text dynamically into the UI
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Transform simple history dicts into official types.Content objects for the SDK
            formatted_contents = [
                types.Content(
                    role=msg["role"], 
                    parts=[types.Part.from_text(text=msg["content"])]
                ) for msg in st.session_state.chat_history
            ]
            
            # Using 'gemini-2.5-pro' for advanced reasoning and multi-step deduction
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-pro',
                contents=formatted_contents,
                config=config
            )
            
            # Stream the answer chunk by chunk
            for chunk in response_stream:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            # Final clean render without the typing cursor
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Execution Error: {e}")
