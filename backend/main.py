# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from rag import initialize_vector_store, query_documents, load_documents, clear_documents_directory, generate_questions_from_content
import shutil, os

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["http://localhost:3000"] in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB & embeddings globally (will be None initially)
db, embeddings = None, None

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Edufy Backend is running!", "status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF/TXT file and replace all previous documents."""
    global db, embeddings
    
    # Clear all previous documents first
    clear_documents_directory()
    
    # Create documents directory
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    os.makedirs(docs_dir, exist_ok=True)
    file_path = os.path.join(docs_dir, file.filename)

    # Save the new uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Recreate the vector store with only the new document
    db, embeddings = initialize_vector_store(force_recreate=True)
    
    if db is None:
        return {"error": f"Failed to process {file.filename}. Please check the file format."}

    return {"message": f"{file.filename} uploaded successfully! Previous documents have been replaced."}

@app.get("/status")
def get_status():
    """Get the current status of the document database."""
    current_dir = os.path.dirname(__file__)
    documents_dir = os.path.join(current_dir, "documents")
    
    if not os.path.exists(documents_dir):
        return {
            "status": "no_documents",
            "message": "No documents directory found",
            "documents": [],
            "database_ready": False
        }
    
    # Get list of uploaded documents
    documents = []
    for filename in os.listdir(documents_dir):
        if filename.endswith(('.pdf', '.txt')):
            file_path = os.path.join(documents_dir, filename)
            file_size = os.path.getsize(file_path)
            documents.append({
                "name": filename,
                "size": file_size,
                "size_formatted": f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
            })
    
    return {
        "status": "ready" if documents and db else "no_documents",
        "message": f"Found {len(documents)} document(s)" if documents else "No documents uploaded",
        "documents": documents,
        "database_ready": db is not None
    }

@app.get("/sample-questions")
def get_sample_questions():
    """Generate sample questions based on the currently uploaded document."""
    if not db:
        return {"error": "No documents uploaded yet. Please upload a document first."}
    
    # Get some sample document chunks to analyze
    try:
        # Get all documents from the vector store
        retriever = db.as_retriever(search_kwargs={"k": 10})  # Get more chunks for analysis
        sample_docs = retriever.invoke("content summary main topics")  # Generic query to get diverse content
        
        if not sample_docs:
            return {"questions": []}
        
        # Extract key topics and concepts from the documents
        sample_questions = generate_questions_from_content(sample_docs)
        
        return {"questions": sample_questions}
        
    except Exception as e:
        print(f"Error generating sample questions: {e}")
        return {"questions": []}

@app.get("/query")
def query(question: str):
    """Ask a question based on the currently uploaded document."""
    if not db:
        return {"error": "No documents uploaded yet. Please upload a document first to ask questions."}
    
    results = query_documents(db, question, use_llm=True)
    
    # Handle both old format (list of documents) and new format (dict with ai_response)
    if isinstance(results, dict) and "ai_response" in results:
        # New format with LLM response
        return {
            "question": question,
            "ai_response": results["ai_response"],
            "answers": [
                {"content": doc.page_content, "source": os.path.basename(doc.metadata.get("source", "unknown"))}
                for doc in results["source_documents"]
            ]
        }
    elif isinstance(results, list):
        # Old format (fallback)
        return {
            "question": question,
            "answers": [
                {"content": doc.page_content, "source": os.path.basename(doc.metadata.get("source", "unknown"))}
                for doc in results
            ]
        }
    else:
        # Error case
        return {
            "question": question,
            "error": "No relevant information found in the uploaded documents.",
            "answers": []
        }
