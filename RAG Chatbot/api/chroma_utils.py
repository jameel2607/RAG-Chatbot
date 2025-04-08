from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from typing import List, Tuple
from langchain_core.documents import Document

# Define supported file types and their loaders
SUPPORTED_FORMATS = {
    '.pdf': PyPDFLoader,
    '.docx': Docx2txtLoader,
    '.html': UnstructuredHTMLLoader,
}

# Create vectorstore instance
embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

# Text splitter configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def get_vectorstore():
    """Get the Chroma vectorstore instance"""
    return vectorstore

def validate_file(file_path: str) -> Tuple[bool, str]:
    """Validate if the file exists and is of supported format"""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in SUPPORTED_FORMATS:
        return False, f"Unsupported file format: {file_ext}. Supported formats: {', '.join(SUPPORTED_FORMATS.keys())}"
    
    if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB limit
        return False, f"File too large: {os.path.basename(file_path)}. Maximum size: 10MB"
    
    return True, ""

def load_and_split_document(file_path: str) -> List[Document]:
    """Load and split a document into chunks"""
    # Validate file
    is_valid, error_message = validate_file(file_path)
    if not is_valid:
        raise ValueError(error_message)

    try:
        # Get appropriate loader based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        loader_class = SUPPORTED_FORMATS[file_ext]
        loader = loader_class(file_path)
        
        # Load and split the document
        documents = loader.load()
        return text_splitter.split_documents(documents)
    except Exception as e:
        raise ValueError(f"Error loading document {file_path}: {str(e)}")

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    """Index a document to Chroma with proper error handling"""
    try:
        # Load and split the document
        splits = load_and_split_document(file_path)
        
        if not splits:
            raise ValueError(f"No content extracted from {file_path}")
        
        # Add metadata to each split
        for split in splits:
            split.metadata['file_id'] = file_id
        
        # Add to vectorstore
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int) -> bool:
    """Delete a document from Chroma with proper error handling"""
    try:
        # Check if document exists
        docs = vectorstore.get(where={"file_id": file_id})
        if not docs['ids']:
            print(f"No documents found with file_id {file_id}")
            return True
            
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        
        # Delete all chunks with matching file_id
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
