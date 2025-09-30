# 🎓 Edufy - AI-Powered Study Companion

Edufy is an intelligent study companion that helps you upload documents and ask questions about them using RAG (Retrieval-Augmented Generation) technology.

## Features

- 📚 **Document Upload**: Support for PDF and TXT files
- 🤖 **AI-Powered Q&A**: Ask questions about your documents
- 🔍 **Semantic Search**: Find relevant information quickly
- 💾 **Vector Database**: Efficient document storage and retrieval
- 🎨 **Modern UI**: Beautiful React frontend with Tailwind CSS
- ⚡ **Real-time**: Fast responses with FastAPI backend

## Tech Stack

**Backend:**

- FastAPI (Python web framework)
- LangChain (LLM framework)
- ChromaDB (Vector database)
- HuggingFace Embeddings
- Sentence Transformers

**Frontend:**

- React 19 with Vite
- Tailwind CSS
- Axios for API calls

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   The backend will be running at: http://127.0.0.1:8000

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The frontend will be running at: http://localhost:5174

## Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** and navigate to http://localhost:5174
3. **Upload documents**: Click on the upload area and select PDF or TXT files
4. **Ask questions**: Type your questions in the query box and get AI-powered answers

## Project Structure

```
BrainiFi/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag.py               # RAG implementation
│   ├── requirements.txt     # Python dependencies
│   ├── venv/               # Virtual environment
│   ├── documents/          # Uploaded documents
│   └── db/                 # Vector database storage
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── api.js         # API integration
    │   ├── App.jsx        # Main app component
    │   └── style.css      # Tailwind styles
    ├── package.json       # Node dependencies
    └── vite.config.js     # Vite configuration
```

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload document files
- `GET /query?question=...` - Ask questions about documents

## Development Notes

- The backend uses a persistent ChromaDB vector store
- Documents are automatically processed and indexed upon upload
- The frontend includes error boundaries and connection status monitoring
- CORS is configured to allow frontend-backend communication

## Troubleshooting

1. **Backend connection issues**: Make sure the backend is running on port 8000
2. **File upload failures**: Check file format (PDF/TXT only) and file size
3. **No answers found**: Ensure documents are uploaded and try rephrasing questions
4. **Python package errors**: Make sure you're in the virtual environment

## Future Enhancements

- [ ] Support for more file formats (DOCX, PPTX)
- [ ] Integration with LLM models (Ollama, OpenAI)
- [ ] User authentication and document management
- [ ] Advanced search filters and sorting
- [ ] Document preview and highlighting
- [ ] Export functionality for Q&A sessions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
