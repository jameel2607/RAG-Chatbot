from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record, get_db_connection, log_interaction
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma, load_and_split_document
import os
import uuid
import logging
from fastapi.middleware.cors import CORSMiddleware
import time

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/chat")
async def chat(query_input: QueryInput) -> QueryResponse:
    try:
        session_id = query_input.session_id or str(uuid.uuid4())
        logger.info(f"Received chat request - Session: {session_id}, Model: {query_input.model.value}")
        
        # Add delay between requests
        time.sleep(1)  # 1 second delay
        
        logger.info(f"Initializing RAG chain for session {session_id}")
        chain = get_rag_chain(session_id, model_name=query_input.model.value)
        
        try:
            logger.info(f"Processing question for session {session_id}: {query_input.question[:50]}...")
            result = chain({
                "question": query_input.question
            })
            answer = result.get('answer', '')
            logger.info(f"Generated response for session {session_id} - Length: {len(answer)}")
        except Exception as e:
            if "429" in str(e):
                logger.warning(f"Rate limit hit for session {session_id}")
                return QueryResponse(
                    answer="I'm currently experiencing high traffic. Please try again in a few seconds.",
                    session_id=session_id,
                    model=query_input.model
                )
            logger.error(f"Error processing question for session {session_id}: {str(e)}")
            raise

        # Log to database
        logger.info(f"Logging interaction to database for session {session_id}")
        log_interaction(
            session_id=session_id,
            user_query=query_input.question,
            gpt_response=answer,
            model=query_input.model
        )
        
        return QueryResponse(
            answer=answer,
            session_id=session_id,
            model=query_input.model
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
        # Save file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # First save to database to get file_id
            logger.info(f"Saving file record to database: {file.filename}")
            doc_id = insert_document_record(file.filename)
            
            # Index document in Chroma with file_id
            logger.info(f"Indexing document in Chroma: {file.filename}")
            index_success = index_document_to_chroma(file_path, doc_id)
            
            if not index_success:
                # If indexing fails, remove from database and raise error
                logger.error(f"Failed to index document in Chroma: {file.filename}")
                delete_document_record(doc_id)
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to index document {file.filename} in vector store"
                )
            
            # Get number of chunks
            chunks = load_and_split_document(file_path)
            num_chunks = len(chunks)
            logger.info(f"Successfully processed document into {num_chunks} chunks: {file.filename}")
            
            return {
                "message": f"Successfully uploaded and indexed {file.filename}",
                "chunks": num_chunks,
                "id": doc_id
            }
        finally:
            # Always clean up the temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
                
    except Exception as e:
        logger.error(f"Error processing upload for {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    try:
        logger.info(f"Attempting to delete document with ID: {request.file_id}")
        
        # Delete from Chroma
        chroma_delete_success = delete_doc_from_chroma(request.file_id)

        if chroma_delete_success:
            # If successfully deleted from Chroma, delete from our database
            db_delete_success = delete_document_record(request.file_id)
            if db_delete_success:
                logger.info(f"Successfully deleted document {request.file_id} from system")
                return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
            else:
                logger.warning(f"Deleted from Chroma but failed to delete from database: {request.file_id}")
                return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
        else:
            logger.error(f"Failed to delete document from Chroma: {request.file_id}")
            return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}
    except Exception as e:
        logger.error(f"Error deleting document {request.file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
