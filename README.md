# RAG Chatbot with Gemini and LangChain

A Retrieval-Augmented Generation (RAG) chatbot that uses Google's Gemini model and LangChain for document processing and contextual responses. The application features a FastAPI backend and Streamlit frontend.

## Features

- 🤖 Powered by Google's Gemini AI model
- 📄 Support for multiple document formats (PDF, DOCX, HTML)
- 💾 Document storage and management
- 💬 Contextual chat with memory
- 🔍 RAG implementation using LangChain
- 🎯 Session-based conversation history
- 🌐 Modern web interface with Streamlit

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite, ChromaDB (for vector storage)
- **AI/ML**: 
  - Google Gemini API
  - LangChain
  - ChromaDB for vector embeddings
- **Document Processing**: LangChain document loaders

## Project Structure
```
RAG Chatbot/
├── api/ # Backend FastAPI service
│ ├── init.py
│ ├── main.py # FastAPI endpoints
│ ├── chroma_utils.py # Vector DB utilities
│ ├── langchain_utils.py # LangChain implementation
│ ├── db_utils.py # Database operations
│ └── pydantic_models.py # Data models
├── app/ # Frontend Streamlit application
│ ├── streamlit_app.py # Main Streamlit interface
│ ├── api_utils.py # API communication
│ └── models.py # Frontend models
└── .env # Environment configuration
```

## Setup and Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd RAG-Chatbot
```

2. **Install dependencies**
```bash
pip install -r api/requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
GOOGLE_API_KEY=your-gemini-api-key


4. **Initialize the database**
```bash
cd api
python init_db.py
```

5. **Start the servers**

Backend:
```bash
cd api
uvicorn main:app --reload
```

Frontend (in a new terminal):
```bash
cd app
streamlit run streamlit_app.py
```

## Usage

1. Access the web interface at `http://localhost:8501`
2. Upload documents through the sidebar
3. Start chatting with the bot
4. The bot will provide responses based on:
   - Uploaded documents
   - Conversation history
   - Gemini's knowledge

## Features in Detail

### Document Management
- Upload PDF, DOCX, and HTML files
- Automatic text extraction and chunking
- Vector embeddings for efficient retrieval
- Document deletion capability

### Chat Interface
- Real-time responses
- Session-based memory
- Context-aware conversations
- Document-grounded responses

### RAG Implementation
- Document chunking and embedding
- Semantic search for relevant context
- LangChain for chain orchestration
- ChromaDB for vector storage

## API Endpoints

- `POST /chat`: Process chat messages
- `POST /upload-doc`: Upload documents
- `GET /list-docs`: List uploaded documents
- `POST /delete-doc`: Delete documents

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for the language model
- LangChain for the RAG implementation
- Streamlit for the web interface
- FastAPI for the backend framework
