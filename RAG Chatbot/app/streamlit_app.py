import streamlit as st
from api_utils import chat_with_bot, upload_document, get_documents, delete_document
from models import ModelName
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

# Sidebar with clear separation
with st.sidebar:
    # Model Selection
    st.header("Select Model")
    model = st.selectbox(
        "",  # Empty label since header is already there
        [model.value for model in ModelName],
        key="model_select"
    )
    
    # Document Upload Section
    st.header("Document Management")
    
    # File uploader with clear button
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=['pdf', 'docx', 'html'],
        help="Drag and drop your file here"
    )
    
    if uploaded_file:
        st.write(f"Selected file: {uploaded_file.name}")
        if st.button("Upload Document"):
            with st.spinner('Uploading...'):
                if upload_document(uploaded_file):
                    st.success(f"Successfully uploaded {uploaded_file.name}")
                    st.rerun()
                else:
                    st.error("Failed to upload document. Please try again.")
    
    # Document List Section
    st.subheader("Uploaded Documents")
    documents = get_documents()
    
    if documents:
        for doc in documents:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(doc['filename'])
            with col2:
                # Unique key for each delete button
                if st.button("🗑️", key=f"delete_{doc['id']}", help="Delete document"):
                    if delete_document(doc['id']):
                        st.success("Document deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete document")
    else:
        st.info("No documents uploaded yet")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
            try:
                response = chat_with_bot(
                    prompt, 
                    model,
                    session_id=st.session_state.session_id
                )
                if "429" in response or "quota" in response.lower():
                    st.warning("The API is currently rate limited. Please wait a few seconds and try again.")
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
