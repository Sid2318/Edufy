# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from rag import initialize_vector_store, query_documents, load_documents, clear_documents_directory, generate_questions_from_content, generate_simple_flashcards, clear_ai_cache, invalidate_previous_content, enhance_answer_with_ai
import shutil, os
import time

app = FastAPI()

# Track document state for invalidation
document_state = {
    "last_upload_time": 0,
    "current_filename": "",
    "content_generating": False
}

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

    try:
        # Save the new uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            os.remove(file_path)  # Remove empty file
            return {"error": f"The uploaded file {file.filename} is empty. Please upload a valid document."}
        
        print(f"📁 Saved file: {file.filename} ({file_size} bytes)")

        # Recreate the vector store with only the new document
        db, embeddings = initialize_vector_store(force_recreate=True)
        
        if db is None:
            return {"error": f"Failed to process {file.filename}. The document might be empty, corrupted, or contain no readable text. Please try uploading a different document."}

        # Clear AI cache so questions and flashcards regenerate for the new document
        clear_ai_cache()
        
        # Update document state to invalidate old content
        document_state["last_upload_time"] = time.time()
        document_state["current_filename"] = file.filename
        document_state["content_generating"] = True

        return {"message": f"{file.filename} uploaded successfully! Previous documents have been replaced."}
        
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        # Clean up any partially created files
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        return {"error": f"Failed to upload {file.filename}. Error: {str(e)}"}

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

@app.get("/flashcards")
def get_flashcards():
    """Generate flashcards based on the currently uploaded document."""
    if not db:
        return {"error": "No documents uploaded yet. Please upload a document first."}
    
    # Check if we're in the middle of generating content for a new document
    current_time = time.time()
    time_since_upload = current_time - document_state["last_upload_time"]
    
    # Show invalid content for first 3 seconds after upload, then generate new content
    if document_state["content_generating"] and time_since_upload < 3:
        invalid_content = invalidate_previous_content()
        return {
            "flashcards": invalid_content["flashcards"],
            "total": len(invalid_content["flashcards"]),
            "status": "regenerating",
            "message": f"Generating new flashcards for {document_state['current_filename']}..."
        }
    
    # Mark content generation as complete after delay
    if document_state["content_generating"] and time_since_upload >= 3:
        document_state["content_generating"] = False
    
    try:
        # Get document chunks for flashcard generation
        retriever = db.as_retriever(search_kwargs={"k": 10})
        sample_docs = retriever.invoke("main topics concepts definitions")
        
        if not sample_docs:
            return {"flashcards": []}
        
        # Generate flashcards from the content
        flashcards = generate_simple_flashcards(sample_docs)
        
        return {"flashcards": flashcards, "total": len(flashcards)}
        
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return {"flashcards": [], "error": "Failed to generate flashcards"}

@app.get("/sample-questions")
def get_sample_questions():
    """Generate sample questions based on the currently uploaded document."""
    if not db:
        return {"error": "No documents uploaded yet. Please upload a document first."}
    
    # Check if we're in the middle of generating content for a new document
    current_time = time.time()
    time_since_upload = current_time - document_state["last_upload_time"]
    
    # Show invalid content for first 3 seconds after upload, then generate new content
    if document_state["content_generating"] and time_since_upload < 3:
        invalid_content = invalidate_previous_content()
        return {
            "questions": invalid_content["questions"],
            "status": "regenerating",
            "message": f"Generating new questions for {document_state['current_filename']}..."
        }
    
    # Mark content generation as complete after delay
    if document_state["content_generating"] and time_since_upload >= 3:
        document_state["content_generating"] = False
    
    # Get document chunks with diverse content for comprehensive analysis
    try:
        # Use multiple queries to get diverse content chunks
        retriever = db.as_retriever(search_kwargs={"k": 15})  # Get more chunks for better analysis
        
        # Multiple targeted queries to capture different aspects of the document
        queries = [
            "main concepts definitions important terms",
            "key topics processes methods procedures", 
            "examples applications case studies",
            "principles fundamentals basics overview"
        ]
        
        all_docs = []
        for query in queries:
            docs = retriever.invoke(query)
            all_docs.extend(docs[:4])  # Take top 4 from each query
        
        # Remove duplicates based on content
        unique_docs = []
        seen_content = set()
        for doc in all_docs:
            content_hash = hash(doc.page_content[:100])  # Use first 100 chars as identifier
            if content_hash not in seen_content:
                unique_docs.append(doc)
                seen_content.add(content_hash)
        
        sample_docs = unique_docs[:12]  # Use up to 12 diverse chunks
        
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
        # New format with LLM response and metadata
        return {
            "question": question,
            "ai_response": results["ai_response"],
            "query_type": results.get("query_type", "general"),
            "k_used": results.get("k_used", 3),
            "total_sections": len(results["source_documents"]),
            "answers": [
                {"content": doc.page_content, "source": os.path.basename(doc.metadata.get("source", "unknown"))}
                for doc in results["source_documents"]
            ]
        }
    elif isinstance(results, list):
        # Old format (fallback)
        return {
            "question": question,
            "query_type": "general",
            "k_used": len(results),
            "total_sections": len(results),
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
            "query_type": "general",
            "k_used": 0,
            "total_sections": 0,
            "answers": []
        }
