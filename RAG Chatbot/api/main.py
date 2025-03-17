from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record, get_db_connection, log_interaction
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma, process_document
import os
import uuid
import logging
from fastapi.middleware.cors import CORSMiddleware
import time

logging.basicConfig(filename='app.log', level=logging.INFO)
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
        
        # Add delay between requests
        time.sleep(1)  # 1 second delay
        
        chain = get_rag_chain(session_id, model_name=query_input.model.value)
        
        try:
            result = chain({
                "question": query_input.question
            })
            answer = result.get('answer', '')
        except Exception as e:
            if "429" in str(e):
                return QueryResponse(
                    answer="I'm currently experiencing high traffic. Please try again in a few seconds.",
                    session_id=session_id,
                    model=query_input.model
                )
            raise

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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document for RAG
        num_chunks = process_document(file_path)
        
        # Save to database
        doc_id = insert_document_record(file.filename)
        
        # Optionally remove the temporary file
        os.remove(file_path)
        
        return {"message": f"Successfully uploaded {file.filename}", "chunks": num_chunks, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # Delete from Chroma
    chroma_delete_success = delete_doc_from_chroma(request.file_id)

    if chroma_delete_success:
        # If successfully deleted from Chroma, delete from our database
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
        else:
            return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}
