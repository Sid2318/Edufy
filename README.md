# 🎓 Edufy - AI-Powered Study Companion

**Edufy** is an intelligent, comprehensive study companion that transforms your documents into interactive learning experiences. Built with modern RAG (Retrieval-Augmented Generation) technology, Edufy helps students, researchers, and professionals extract maximum value from their documents through AI-powered Q&A, smart flashcards, and intelligent content analysis.

## 🌟 Core Features

### 📚 **Intelligent Document Processing**

- **Multi-format Support**: PDF and TXT files with automatic text extraction
- **Smart Chunking**: Advanced text splitting for optimal context preservation
- **Vector Indexing**: Semantic embedding for precise content retrieval
- **Content Validation**: Automatic file validation and error handling

### 🤖 **AI-Powered Learning Tools**

- **Interactive Q&A**: Ask natural language questions about your documents
- **Smart Flashcards**: Auto-generated flashcards for key concepts and definitions
- **Sample Questions**: AI-generated study questions based on document content
- **Enhanced Answers**: LLM-powered detailed explanations using Ollama integration

### 🔍 **Advanced Search & Retrieval**

- **Semantic Search**: Find relevant information beyond keyword matching
- **Context-Aware Responses**: Answers with proper document context
- **Domain-Specific Intelligence**: Specialized handling for different subject areas
- **Real-time Processing**: Instant responses with efficient caching

### 🎨 **Modern User Experience**

- **Responsive Design**: Beautiful React interface optimized for all devices
- **Real-time Feedback**: Live status updates and progress indicators
- **Error Boundaries**: Robust error handling with user-friendly messages
- **Accessibility**: WCAG-compliant design with keyboard navigation

## 🛠️ Tech Stack

### **Backend Architecture**

- **FastAPI**: High-performance Python web framework with automatic API documentation
- **LangChain**: Advanced LLM orchestration and RAG pipeline management
- **ChromaDB**: High-performance vector database for semantic search
- **HuggingFace Transformers**: State-of-the-art embedding models
- **Sentence Transformers**: Specialized models for semantic similarity
- **Ollama Integration**: Local LLM support for enhanced answer generation

### **Frontend Architecture**

- **React 18+**: Modern React with hooks and functional components
- **Vite**: Lightning-fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Axios**: Promise-based HTTP client with interceptors and error handling

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+** (Recommended: Python 3.10+)
- **Node.js 16+** (Recommended: Node.js 18+)
- **npm or yarn**
- **Git** for version control
- **Optional**: Ollama for enhanced AI responses

### 🔧 Backend Setup

1. **Clone and navigate to backend directory:**

   ```bash
   git clone https://github.com/Sid2318/Edufy.git
   cd Edufy/backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI backend:**

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   ✅ Backend running at: **http://127.0.0.1:8000**

   📖 API Documentation: **http://127.0.0.1:8000/docs**

### ⚛️ Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the React development server:**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

   ✅ Frontend running at: **http://localhost:5174**

### 🎯 Usage Workflow

1. **🚀 Start both servers** (backend and frontend)
2. **🌐 Open browser** → Navigate to http://localhost:5174
3. **📄 Upload documents** → Drag & drop or click to select PDF/TXT files
4. **❓ Ask questions** → Use the Q&A tab to query your documents
5. **🃏 Generate flashcards** → Switch to flashcards tab for study materials
6. **📚 Use sample questions** → Click suggested questions for quick exploration

## 📁 Project Architecture

```
Edufy/
├── 🔙 backend/                    # Python FastAPI Backend
│   ├── main.py                   # 🚀 FastAPI application & API endpoints
│   ├── rag.py                    # 🧠 RAG implementation & AI logic
│   ├── domain_data.py            # 📚 Domain-specific data & keywords
│   ├── requirements.txt          # 📦 Python dependencies
│   ├── venv/                     # 🐍 Virtual environment
│   ├── documents/                # 📄 Uploaded document storage
│   └── db/                       # 🗄️ ChromaDB vector database
│       └── chroma_db/            # 📊 Persistent vector storage
├── 🎨 frontend/                   # React Frontend Application
│   ├── src/
│   │   ├── components/           # ⚛️ Reusable React components
│   │   │   ├── ConnectionStatus.jsx   # 🔗 Backend connection monitor
│   │   │   ├── DocumentManager.jsx    # 📋 Document management UI
│   │   │   ├── ErrorBoundary.jsx      # 🛡️ Error handling wrapper
│   │   │   ├── FlashcardViewer.jsx    # 🃏 Interactive flashcard display
│   │   │   ├── query.jsx              # ❓ Q&A interface component
│   │   │   ├── SampleQuestions.jsx    # 💡 AI-generated questions
│   │   │   ├── TabNavigation.jsx      # 🔄 Main tab switching logic
│   │   │   ├── Tutorial.jsx           # 📖 User onboarding guide
│   │   │   └── Upload.jsx             # 📤 File upload interface
│   │   ├── api.js                # 🔌 API integration & HTTP client
│   │   ├── App.jsx               # 🏠 Main application component
│   │   ├── main.jsx              # 🎯 React app entry point
│   │   └── style.css             # 🎨 Tailwind CSS styles
│   ├── public/                   # 📂 Static assets
│   ├── package.json              # 📦 Node.js dependencies
│   ├── vite.config.js            # ⚡ Vite build configuration
│   └── index.html                # 🌐 HTML entry point
├── README.md                     # 📖 This documentation
├── SETUP.md                      # 🔧 Setup instructions
└── .gitignore                    # 🚫 Git ignore rules
```

## 🔌 API Endpoints Reference

### Core Application Endpoints

| Method | Endpoint  | Description                      | Parameters         | Response                                                        |
| ------ | --------- | -------------------------------- | ------------------ | --------------------------------------------------------------- |
| `GET`  | `/`       | 🏥 Health check endpoint         | None               | `{"message": "Edufy Backend is running!", "status": "healthy"}` |
| `GET`  | `/status` | 📊 System status & document info | None               | Document count, database status, upload status                  |
| `POST` | `/upload` | 📤 Upload PDF/TXT documents      | `file: UploadFile` | Upload confirmation with file details                           |

### AI-Powered Learning Endpoints

| Method | Endpoint            | Description                         | Parameters      | Response                                     |
| ------ | ------------------- | ----------------------------------- | --------------- | -------------------------------------------- |
| `GET`  | `/query`            | ❓ Ask questions about documents    | `question: str` | AI-generated answers with source context     |
| `GET`  | `/sample-questions` | 💡 Get AI-generated study questions | None            | Array of relevant questions based on content |
| `GET`  | `/flashcards`       | 🃏 Generate flashcards for study    | None            | Question-answer pairs for memorization       |

### Response Formats

**Upload Response:**

```json
{
  "message": "✅ document.pdf uploaded successfully!",
  "details": "Previous documents deleted. New questions and flashcards will be generated.",
  "filename": "document.pdf",
  "file_size": 245760,
  "status": "ready"
}
```

**Query Response:**

```json
{
  "question": "What is machine learning?",
  "ai_response": "Machine learning is a subset of artificial intelligence...",
  "query_type": "definition",
  "k_used": 5,
  "total_sections": 3,
  "answers": [
    {
      "content": "Machine learning algorithms...",
      "source": "document.pdf"
    }
  ]
}
```

## 🔧 Core Functions & Features Deep Dive

### 🔙 Backend Functions (`main.py`)

#### 🏥 `read_root()`

**Purpose**: Health check endpoint for monitoring backend status
**Returns**: Server status and welcome message
**Usage**: Verify backend connectivity and uptime

```python
@app.get("/")
def read_root():
    return {"message": "Edufy Backend is running!", "status": "healthy"}
```

#### 📤 `upload_file(file: UploadFile)`

**Purpose**: Handle document upload with complete preprocessing pipeline
**Process**:

1. **File Validation**: Checks file type (PDF/TXT only) and size
2. **Cleanup**: Removes all previous documents and cached data
3. **Storage**: Saves new file to documents directory
4. **Processing**: Creates vector embeddings and initializes database
5. **State Management**: Updates document state for frontend synchronization

**Error Handling**: Comprehensive validation with user-friendly error messages
**Returns**: Upload confirmation with file metadata

#### 📊 `get_status()`

**Purpose**: Provide system status and document information
**Returns**:

- Document count and file details
- Database readiness status
- Upload completion status
- File size information

#### ❓ `query(question: str)`

**Purpose**: Process natural language questions about uploaded documents
**Process**:

1. **Validation**: Ensures documents are available
2. **Retrieval**: Uses semantic search to find relevant content
3. **Enhancement**: Optional LLM integration for improved answers
4. **Response**: Returns structured answer with source references

**Features**:

- Context-aware responses
- Source attribution
- Multiple search strategies
- AI enhancement with Ollama

#### 🃏 `get_flashcards()`

**Purpose**: Generate interactive flashcards for study
**Process**:

1. **Content Analysis**: Extracts key concepts and definitions
2. **Question Generation**: Creates question-answer pairs
3. **Formatting**: Structures flashcards for optimal learning
4. **Caching**: Implements smart caching for performance

#### 💡 `get_sample_questions()`

**Purpose**: Generate AI-powered study questions
**Process**:

1. **Content Sampling**: Retrieves diverse document sections
2. **Analysis**: Identifies key topics and concepts
3. **Question Generation**: Creates relevant study questions
4. **Diversity**: Ensures varied question types and difficulty levels

### 🧠 RAG Engine Functions (`rag.py`)

#### 🔄 `initialize_vector_store(force_recreate=False)`

**Purpose**: Set up ChromaDB vector database for semantic search
**Process**:

1. **Document Loading**: Processes PDF/TXT files
2. **Text Splitting**: Intelligent chunking for optimal context
3. **Embedding Generation**: Creates semantic vectors using HuggingFace
4. **Database Creation**: Initializes persistent ChromaDB storage

**Parameters**:

- `force_recreate`: Boolean to rebuild database from scratch
  **Returns**: Database instance and embeddings model

#### 🔍 `query_documents(db, question, use_llm=True)`

**Purpose**: Execute semantic search and generate responses
**Process**:

1. **Query Analysis**: Determines optimal search strategy
2. **Retrieval**: Finds most relevant document chunks
3. **Context Assembly**: Combines relevant information
4. **Response Generation**: Creates comprehensive answers

**Features**:

- Multiple retrieval strategies (k=3,5,10 based on query type)
- LLM enhancement with Ollama integration
- Smart caching to avoid redundant AI calls
- Context preservation and source tracking

#### ✨ `enhance_answer_with_ai(question, context, basic_answer)`

**Purpose**: Use local LLM (Ollama) to improve answer quality
**Process**:

1. **Availability Check**: Verifies Ollama server connection
2. **Prompt Engineering**: Creates optimized prompts for educational content
3. **Response Generation**: Uses llama3 model for enhanced answers
4. **Quality Control**: Validates response length and relevance

#### 🧹 `clear_ai_cache()`

**Purpose**: Invalidate cached AI responses for new documents
**Usage**: Called during document upload to ensure fresh content generation

#### 📚 `generate_questions_from_content(docs)`

**Purpose**: Create study questions from document content
**Features**:

- Domain-specific question templates
- Multiple question types (definitions, processes, comparisons)
- Content analysis for relevant topic extraction
- Intelligent question formulation

#### 🃏 `generate_simple_flashcards(docs)`

**Purpose**: Create flashcard pairs for memorization
**Process**:

1. **Concept Extraction**: Identifies key terms and definitions
2. **Pattern Matching**: Uses regex patterns for structured content
3. **Card Generation**: Creates question-answer pairs
4. **Quality Filtering**: Ensures meaningful flashcard content

### ⚛️ Frontend Components Deep Dive

#### 🏠 `App.jsx` - Main Application

**Purpose**: Root component managing global state and layout
**Features**:

- Responsive grid layout
- State management for selected questions
- Error boundary integration
- Header with branding and connection status

#### 📤 `Upload.jsx` - File Upload Interface

**Purpose**: Handle document upload with drag-and-drop functionality
**Features**:

- Drag-and-drop file upload
- File type validation (PDF/TXT)
- Upload progress indication
- Success/error message display
- File information preview

#### 🔄 `TabNavigation.jsx` - Main Interface Controller

**Purpose**: Manage tabbed interface between Q&A and Flashcards
**Features**:

- Smooth tab transitions
- Auto-generation of content when tabs are accessed
- Loading states with animations
- Smart caching of generated content

#### ❓ `query.jsx` - Q&A Interface

**Purpose**: Interactive question-answer interface
**Features**:

- Real-time question input
- Auto-suggestion from sample questions
- Response formatting with source attribution
- Loading animations during processing
- Error handling for failed queries

#### 🃏 `FlashcardViewer.jsx` - Interactive Flashcards

**Purpose**: Display and interact with generated flashcards
**Features**:

- Card flip animations
- Navigation between cards
- Progress tracking
- Responsive design for mobile/desktop

#### 💡 `SampleQuestions.jsx` - AI-Generated Questions

**Purpose**: Display relevant study questions
**Features**:

- Click-to-query functionality
- Dynamic question generation
- Loading states during generation
- Question categorization

#### 🔗 `ConnectionStatus.jsx` - Backend Monitor

**Purpose**: Monitor backend connectivity
**Features**:

- Real-time connection checking
- Visual status indicators
- Automatic reconnection attempts
- User-friendly status messages

#### 🛡️ `ErrorBoundary.jsx` - Error Handling

**Purpose**: Catch and handle React component errors
**Features**:

- Graceful error recovery
- User-friendly error messages
- Error reporting for debugging
- Fallback UI when components fail

#### 📖 `Tutorial.jsx` - User Onboarding

**Purpose**: Guide new users through app features
**Features**:

- Interactive walkthrough
- Feature highlights
- Skip/complete functionality
- Responsive design

### 🔌 API Integration (`api.js`)

#### 🌐 HTTP Client Configuration

- **Base URL**: Configurable backend endpoint
- **Timeout**: 30-second request timeout
- **Interceptors**: Request/response logging and error handling
- **Error Recovery**: Automatic retry logic for failed requests

#### 📤 `uploadFile(file)`

**Purpose**: Handle file upload with progress tracking
**Features**:

- FormData construction
- Progress callback support
- Error handling with user-friendly messages

#### ❓ `askQuestion(question)`

**Purpose**: Send questions to backend and receive answers
**Features**:

- URL parameter encoding
- Response caching
- Error handling for network issues

#### 📊 `getStatus()`

**Purpose**: Check backend status and document information
**Features**:

- Health monitoring
- Document count retrieval
- Database status checking

#### 🔍 `getSampleQuestions()`

**Purpose**: Retrieve AI-generated study questions
**Features**:

- Caching for performance
- Error handling for generation failures

#### 🏥 `checkHealth()`

**Purpose**: Basic connectivity test
**Returns**: Boolean indicating backend availability

## 🎯 Advanced Features

### 🧠 Domain Intelligence

- **Subject Recognition**: Automatically detects document domain (science, literature, etc.)
- **Specialized Processing**: Tailored question and flashcard generation
- **Context Awareness**: Domain-specific keyword recognition

### ⚡ Performance Optimizations

- **Smart Caching**: Reduces redundant AI processing
- **Chunked Processing**: Efficient handling of large documents
- **Lazy Loading**: Components load content only when needed
- **Connection Pooling**: Optimized database connections

### 🛡️ Error Handling & Resilience

- **Graceful Degradation**: App continues working with partial failures
- **User Feedback**: Clear error messages with resolution steps
- **Automatic Recovery**: Self-healing connections and retries
- **Input Validation**: Comprehensive validation at all levels

### 🔄 State Management

- **Document State Tracking**: Monitors upload and processing status
- **Cache Invalidation**: Ensures fresh content for new documents
- **UI Synchronization**: Real-time updates across components
- **Persistent Storage**: Maintains state across sessions

## 🚀 Deployment & Production

### 🏗️ Build Configuration

```bash
# Backend Production
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000

# Frontend Production
npm run build
npm run preview
```

### 🔧 Environment Variables

```bash
# Backend
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_PATH=./db/chroma_db
OLLAMA_URL=http://localhost:11434

# Frontend
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Edufy
```

### 📊 Monitoring & Analytics

- **Health Checks**: Automated monitoring endpoints
- **Performance Metrics**: Response time and error rate tracking
- **Usage Analytics**: Document processing and query statistics
- **Resource Monitoring**: CPU, memory, and storage usage

## 🔍 Troubleshooting Guide

### 🐛 Common Issues & Solutions

#### Backend Issues

- **Port 8000 occupied**: Change port or kill existing process
- **ChromaDB errors**: Delete `./db` folder and restart
- **Missing dependencies**: Activate venv and reinstall requirements
- **Ollama not responding**: Install Ollama or disable LLM enhancement

#### Frontend Issues

- **API connection failed**: Verify backend is running on correct port
- **File upload timeout**: Check file size and network connection
- **Blank responses**: Ensure documents are properly uploaded
- **Build failures**: Clear node_modules and reinstall dependencies

#### Performance Issues

- **Slow responses**: Check document size and chunking strategy
- **High memory usage**: Restart services to clear cache
- **Database locks**: Restart backend to release ChromaDB locks

### 🛠️ Development Tips

- **Hot Reload**: Both frontend and backend support live reloading
- **API Testing**: Use `/docs` endpoint for interactive API testing
- **Component Debugging**: React DevTools recommended
- **Network Debugging**: Check browser DevTools Network tab

## 🚀 Future Roadmap

### 📋 Planned Features

- [ ] **Multi-format Support**: DOCX, PPTX, EPUB, Markdown
- [ ] **Authentication System**: User accounts and document management
- [ ] **Cloud Storage**: S3/Google Cloud integration
- [ ] **Advanced Analytics**: Learning progress tracking
- [ ] **Mobile App**: React Native companion app
- [ ] **Collaboration**: Shared documents and study groups
- [ ] **Export Options**: PDF reports, study guides
- [ ] **Integration APIs**: LMS and educational platform connectors

### 🔧 Technical Improvements

- [ ] **Microservices**: Split backend into specialized services
- [ ] **Kubernetes**: Container orchestration for scalability
- [ ] **Redis Caching**: Distributed caching layer
- [ ] **GraphQL**: More efficient API queries
- [ ] **WebSockets**: Real-time collaboration features
- [ ] **Progressive Web App**: Offline functionality

## 🤝 Contributing

### 📝 Development Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Make** your changes with proper testing
5. **Commit** with descriptive messages (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Submit** a Pull Request with detailed description

### 🧪 Testing Guidelines

- **Backend**: Write unit tests for new functions
- **Frontend**: Test components with React Testing Library
- **Integration**: Test API endpoints with actual data
- **Performance**: Benchmark critical functions

### 📐 Code Standards

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ESLint configuration, prefer functional components
- **Documentation**: Update README for new features
- **Git**: Use conventional commit messages

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- **LangChain** community for RAG framework
- **HuggingFace** for embedding models
- **ChromaDB** for vector database
- **FastAPI** for modern Python web framework
- **React** team for frontend framework
- **Tailwind CSS** for styling system

---

**📞 Support**: Create an issue on GitHub for bugs or feature requests
**📧 Contact**: [Your Email] for direct communication
**🌟 Star**: If this project helped you, please give it a star!

---

_Built with ❤️ by [Your Name] - Making learning more accessible through AI_
