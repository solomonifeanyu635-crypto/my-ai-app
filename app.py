import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Deep Thought Engine + Live Search", 
    page_icon="🧠", 
    layout="wide"
)

st.title("🧠 Deep Thought Engine")
st.caption("Advanced analytical interface with Real-Time Google Search Grounding enabled.")

# 2. Initialize Gemini Client
api_key = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 3. Memory Architecture (Persistent Multi-Turn Chat)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Strict Real-World Persona & Real-Time Search Configuration
system_instruction = (
    "You are an elite, objective, and deeply analytical AI researcher. "
    "Your primary goal is to provide realistic, hyper-accurate, and deeply thought-out answers. "
    "Use your search tool to pull down current, real-time facts whenever needed. "
    "Break down complex problems step-by-step. "
    "Do not sugarcoat facts, use fluff, or include conversational fillers. "
    "Use markdown tables, bullet points, and clean structuring to present data clearly."
)

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.2,          # Keep temperature low for rigid factual correctness
    max_output_tokens=4000,   
    # ENABLE LIVE GOOGLE SEARCH GROUNDING NATIVELY FOR GEMINI 3.1
    tools=[types.Tool(google_search=types.GoogleSearch())]
)

# 5. Render Historical Chat Context
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Real-Time Processing & Execution Loop
if user_prompt := st.chat_input("Enter a question requiring live facts..."):
    
    # Render user prompt immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Execute Deep Thinking Pipeline with Search Grounding
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Format history data structures for the Google GenAI SDK
            formatted_contents = [
                types.Content(
                    role=msg["role"], 
                    parts=[types.Part.from_text(text=msg["content"])]
                ) for msg in st.session_state.chat_history
            ]
            
            # Reverted back to the working, free gemini-3.1-flash-lite endpoint
            response_stream = client.models.generate_content_stream(
                model='gemini-3.1-flash-lite',
                contents=formatted_contents,
                config=config
            )
            
            # Stream the answer chunk by chunk
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            # Final clean render without the typing cursor
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Execution Error: {e}")
