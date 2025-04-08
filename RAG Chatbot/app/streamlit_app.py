import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface
import uuid

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! How can I help you today?"
    })

st.title("Langchain RAG Chatbot")

# Display sidebar and get selected model
with st.sidebar:
    model = display_sidebar()

# Display chat interface
display_chat_interface(model, st.session_state.session_id)
