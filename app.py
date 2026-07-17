import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Solomon Barbados AI Assistant", 
    page_icon="🧠", 
    layout="wide"
)

# 2. Main App UI Header
st.title("🧠 Solomon Barbados AI Assistant")
st.caption("Advanced analytical interface optimized to run entirely on the 100% free API tier.")

# Initialize Gemini Client
api_key = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 3. Memory Architecture (Persistent Multi-Turn Chat)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Sidebar Controls (Real-Time Ingestion)
with st.sidebar:
    st.header("⚙️ Grounding Control")
    st.write("To feed the AI real-time facts without breaking free tier limits, paste current data below:")
    context_input = st.text_area("Live Data / News Paste:", height=200, placeholder="Paste recent articles, stats, or text here...")
    
    if st.button("Clear Chat History", type="primary"):
        st.session_state.chat_history = []
        st.rerun()

# 5. Strict Real-World Persona Configuration
system_instruction = (
    "You are the Solomon Barbados AI Assistant, an elite, objective, and deeply analytical AI researcher. "
    "Your primary goal is to provide realistic, hyper-accurate, and deeply thought-out answers. "
    "Analyze any provided background context thoroughly and merge it into your logic. "
    "Break down complex problems step-by-step. "
    "Do not sugarcoat facts, use fluff, or include conversational fillers. "
    "Use markdown tables, bullet points, and clean structuring to present data clearly."
)

config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    temperature=0.2,          
    max_output_tokens=4000,   
)

# 6. Render Historical Chat Context
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Real-Time Processing & Execution Loop
if user_prompt := st.chat_input("Enter a complex question or topic to analyze..."):
    
    # Inject sidebar context explicitly into the prompt if present
    processed_prompt = user_prompt
    if context_input:
        processed_prompt = f"BACKGROUND CONTEXT:\n{context_input}\n\nUSER QUESTION:\n{user_prompt}"
    
    # Render user prompt immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Execute Deep Thinking Pipeline
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Build history blocks safely
            formatted_contents = []
            for msg in st.session_state.chat_history[:-1]:
                formatted_contents.append(
                    types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["content"])])
                )
            formatted_contents.append(
                types.Content(role="user", parts=[types.Part.from_text(text=processed_prompt)])
            )
            
            response_stream = client.models.generate_content_stream(
                model='gemini-3.1-flash-lite',
                contents=formatted_contents,
                config=config
            )
            
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Execution Error: {e}")


