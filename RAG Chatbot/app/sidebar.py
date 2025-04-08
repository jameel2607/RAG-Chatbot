import streamlit as st
from api_utils import upload_document, get_documents, delete_document
from models import ModelName

def display_sidebar():
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
                if st.button("🗑️", key=f"delete_{doc['id']}", help="Delete document"):
                    if delete_document(doc['id']):
                        st.success("Document deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete document")
    else:
        st.info("No documents uploaded yet")
    
    return model  # Return selected model
