import os
import glob
import shutil
import re
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage

def generate_questions_from_content(document_chunks):
    """Generate sample questions based on document content."""
    if not document_chunks:
        return []
    
    # Combine content from chunks to analyze
    combined_content = "\n".join([doc.page_content for doc in document_chunks[:5]])  # Use first 5 chunks
    
    # Extract key terms, topics, and concepts using simple text analysis
    questions = []
    
    # Look for common question patterns in the text
    content_lower = combined_content.lower()
    
    # Find definitions (words followed by "is", "are", "means", etc.)
    definition_patterns = [
        r'(\w+(?:\s+\w+){0,2})\s+(?:is|are|means?|refers?\s+to|defined?\s+as)',
        r'(?:what\s+is|define)\s+(\w+(?:\s+\w+){0,2})',
    ]
    
    definitions = set()
    for pattern in definition_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            term = match.strip()
            if len(term) > 3 and len(term.split()) <= 3:  # Reasonable term length
                definitions.add(term.title())
    
    # Generate definition questions
    for term in list(definitions)[:5]:  # Limit to 5 questions
        questions.append(f"What is {term}?")
    
    # Look for lists and enumerations
    list_patterns = [
        r'types?\s+of\s+(\w+(?:\s+\w+){0,2})',
        r'kinds?\s+of\s+(\w+(?:\s+\w+){0,2})',
        r'categories\s+of\s+(\w+(?:\s+\w+){0,2})',
        r'examples?\s+of\s+(\w+(?:\s+\w+){0,2})',
    ]
    
    list_topics = set()
    for pattern in list_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            topic = match.strip()
            if len(topic) > 3:
                list_topics.add(topic.title())
    
    # Generate list questions
    for topic in list(list_topics)[:3]:  # Limit to 3 questions
        questions.append(f"What are the types of {topic}?")
    
    # Look for numbered or bulleted lists
    if re.search(r'\d+\.\s', combined_content) or re.search(r'[-•]\s', combined_content):
        questions.append("What are the main points covered in this document?")
    
    # Look for chapters, sections, or headings
    heading_patterns = [
        r'chapter\s+\d+[:\s]*(.+)',
        r'section\s+\d+[:\s]*(.+)',
        r'^\d+\.\s+(.+)$',
    ]
    
    headings = set()
    for pattern in heading_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            heading = match.strip()
            if len(heading) > 5 and len(heading) < 50:
                headings.add(heading.title())
    
    # Generate heading-based questions
    if headings:
        questions.append("What topics are covered in this document?")
        for heading in list(headings)[:2]:  # Limit to 2
            questions.append(f"Tell me about {heading}")
    
    # Add some generic questions if we don't have enough specific ones
    generic_questions = [
        "Summarize the main content of this document",
        "What are the key concepts explained here?",
        "What should I focus on when studying this material?",
        "Explain the important points from this document",
        "What examples are provided in this document?",
    ]
    
    # Fill up to 8-10 questions total
    while len(questions) < 8 and generic_questions:
        questions.append(generic_questions.pop(0))
    
    # Remove duplicates and return
    unique_questions = list(dict.fromkeys(questions))  # Preserves order while removing duplicates
    return unique_questions[:10]  # Return maximum 10 questions

def clear_documents_directory():
    """Clear all documents from the documents directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents")
    
    if os.path.exists(documents_dir):
        # Remove all files in the directory
        for filename in os.listdir(documents_dir):
            file_path = os.path.join(documents_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"✓ Removed previous document: {filename}")
            except Exception as e:
                print(f"✗ Error removing {filename}: {e}")
    else:
        os.makedirs(documents_dir)
        print(f"Created documents directory: {documents_dir}")

def load_documents():
    """Load documents from various formats (PDF, TXT) - only current uploads."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents")
    
    # Create documents directory if it doesn't exist
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)
        print(f"Created documents directory: {documents_dir}")
        return []
    
    all_documents = []
    
    # Load PDF files
    pdf_files = glob.glob(os.path.join(documents_dir, "*.pdf"))
    for pdf_file in pdf_files:
        try:
            print(f"Loading PDF: {os.path.basename(pdf_file)}")
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            all_documents.extend(documents)
            print(f"✓ Loaded {len(documents)} pages from {os.path.basename(pdf_file)}")
        except Exception as e:
            print(f"✗ Error loading {pdf_file}: {e}")
    
    # Load text files
    txt_files = glob.glob(os.path.join(documents_dir, "*.txt"))
    for txt_file in txt_files:
        try:
            print(f"Loading text file: {os.path.basename(txt_file)}")
            loader = TextLoader(txt_file, encoding='utf-8')
            documents = loader.load()
            all_documents.extend(documents)
            print(f"✓ Loaded {os.path.basename(txt_file)}")
        except Exception as e:
            print(f"✗ Error loading {txt_file}: {e}")
    
    # No sample document creation - only work with uploaded documents
    if not all_documents:
        print("No documents found. Please upload documents to get started.")
    
    return all_documents

def clear_vector_store():
    """Clear the existing vector store database."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(current_dir, "db", "chroma_db")
    
    if os.path.exists(persistent_directory):
        try:
            shutil.rmtree(persistent_directory)
            print("✓ Cleared previous vector store")
        except Exception as e:
            print(f"✗ Error clearing vector store: {e}")

def initialize_vector_store(force_recreate=False):
    """Initialize the vector store with document chunks."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(current_dir, "db", "chroma_db")
    
    # If force_recreate is True or no store exists, create new one
    if force_recreate or not os.path.exists(persistent_directory):
        if force_recreate:
            print("Force recreating vector store...")
            clear_vector_store()
        else:
            print("Persistent directory does not exist. Initializing vector store...")
        
        # Load documents from various sources
        documents = load_documents()
        
        if not documents:
            print("No documents to process. Vector store not created.")
            return None, None
        
        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        docs = text_splitter.split_documents(documents)
        
        # Display information about the split documents
        print(f"\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(docs)}")
        print(f"Total documents processed: {len(documents)}")
        if docs:
            print(f"Sample chunk preview:\n{docs[0].page_content[:300]}...\n")
        
        # Create embeddings
        print("--- Creating embeddings ---")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("--- Finished creating embeddings ---")
        
        # Create the vector store and persist it automatically
        print("--- Creating vector store ---")
        db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
        print("--- Finished creating vector store ---")
        
        return db, embeddings
    else:
        print("Vector store already exists. Loading existing store...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
        return db, embeddings

def query_documents(db, query, use_llm=True):
    """Query the vector store and use LLM to generate response based on retrieved content."""
    
    # Retrieve relevant documents based on the query
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    relevant_docs = retriever.invoke(query)
    
    if not relevant_docs:
        print("No relevant documents found for your question.")
        print(" Try rephrasing your question or using different keywords.")
        return relevant_docs
    
    # Display the relevant results
    print(f"Found {len(relevant_docs)} relevant document sections:")
    print("-" * 40)
    
    for i, doc in enumerate(relevant_docs, 1):
        print(f"\n Section {i}:")
        # Truncate long content for better readability
        content = doc.page_content
        if len(content) > 300:
            content = content[:300] + "..."
        print(f"   {content}")
        
        if doc.metadata and 'source' in doc.metadata:
            source = doc.metadata['source']
            # Show just the filename, not the full path
            filename = os.path.basename(source)
            print(f"    Source: {filename}")
    
    # Always try to use LLM to generate response based on retrieved content
    if relevant_docs:
        print(f"\nGenerating AI Response based on retrieved content:")
        print("-" * 40)
        
        # Combine the query and the relevant document contents for LLM processing
        context_content = "\n\n".join([f"Section {i+1}:\n{doc.page_content}" for i, doc in enumerate(relevant_docs)])
        
        combined_input = (
            f"Question: {query}\n\n"
            f"Context from relevant documents:\n{context_content}\n\n"
            f"Based on the above context, provide a comprehensive and accurate answer to the question. "
            f"Use only the information provided in the context. If the answer cannot be found in the "
            f"provided context, clearly state that the information is not available."
        )
        
        try:
            # Try to use ChatOllama model for LLM response
            from langchain_ollama.chat_models import ChatOllama
            model = ChatOllama(model="llama3")
            
            # Define the messages for the model
            messages = [
                SystemMessage(content="You are an intelligent study assistant. Answer questions based only on the provided document context. Be comprehensive, accurate, and cite specific information from the context. If information is not in the context, clearly state that."),
                HumanMessage(content=combined_input),
            ]
            
            # Invoke the model with the combined input
            result = model.invoke(messages)
            
            # Display the generated response
            print(f"🤖 AI Response: {result.content}")
            
            # Return the LLM response along with source documents
            return {
                "ai_response": result.content,
                "source_documents": relevant_docs
            }
            
        except ImportError:
            print("⚠️ Ollama not available. Using document-based response.")
            fallback_response = generate_fallback_response(query, relevant_docs)
            print(f"📄 Document-based Response: {fallback_response}")
            
            return {
                "ai_response": fallback_response,
                "source_documents": relevant_docs
            }
        except Exception as e:
            print(f"⚠️ LLM Error: {str(e)}")
            print("📋 Falling back to document content only:")
            
            # Fallback: return structured content from documents
            fallback_response = generate_fallback_response(query, relevant_docs)
            print(f"📄 Document-based Response: {fallback_response}")
            
            return {
                "ai_response": fallback_response,
                "source_documents": relevant_docs
            }
    
    return relevant_docs

def generate_fallback_response(query, relevant_docs):
    """Generate a structured response when LLM is not available."""
    if not relevant_docs:
        return "No relevant information found in the uploaded documents."
    
    response_parts = []
    response_parts.append(f"Based on the uploaded document, here's what I found regarding '{query}':")
    
    for i, doc in enumerate(relevant_docs, 1):
        content = doc.page_content.strip()
        source = doc.metadata.get('source', 'Unknown source')
        filename = os.path.basename(source)
        
        # Limit content length for readability
        if len(content) > 500:
            content = content[:500] + "..."
        
        response_parts.append(f"\n{i}. From {filename}:\n{content}")
    
    response_parts.append(f"\nThis information is extracted from {len(relevant_docs)} relevant section(s) of your uploaded document.")
    
    return "\n".join(response_parts)

def main():
    """Main function to run the RAG system."""
    print("=" * 60)
    print(" STUDY DOCUMENT Q&A SYSTEM")
    print("=" * 60)
    print("This system will help you ask questions about your study documents!")
    print("Supported formats: PDF, TXT")
    print("Place your study documents in the 'documents' folder.")
    print("=" * 60)
    
    try:
        # Initialize vector store
        print("\n Initializing the system...")
        db, embeddings = initialize_vector_store()
        
        if db is None:
            print(" Failed to initialize the system. Please check your documents.")
            return
        
        print("\n System ready! You can now ask questions about your study documents.")
        print("\n Tips:")
        print("- Ask specific questions about the content")
        print("- Use keywords from your documents")
        print("- Type 'quit', 'exit', or 'q' to stop")
        print("-" * 60)
        
        # Check if Ollama is available
        ollama_available = True
        try:
            model = ChatOllama(model="llama3")
            # Test with a simple query
            test_result = model.invoke([HumanMessage(content="Hello")])
            print(" AI Assistant: ON (Ollama + Llama3)")
        except Exception as e:
            ollama_available = False
            print("  AI Assistant: OFF (Ollama not available)")
            print("    Document search only mode")
            print(f"    To enable AI responses: Install Ollama and run 'ollama pull llama3'")
        
        print("-" * 60)
        
        # Interactive Q&A loop
        question_count = 0
        while True:
            try:
                user_query = input(f"\n Question {question_count + 1}: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'q', 'bye']:
                    print("\n👋 Thank you for using the Study Q&A System!")
                    break
                
                if not user_query:
                    print(" Please enter a question.")
                    continue
                
                question_count += 1
                print(f"\n Searching for: '{user_query}'")
                print("-" * 40)
                
                # Query the documents
                query_documents(db, user_query, use_llm=ollama_available)
                print("\n" + "=" * 60)
                
            except KeyboardInterrupt:
                print("\n\n Goodbye!")
                break
            except Exception as e:
                print(f"\n Error processing question: {e}")
                continue
    
    except Exception as e:
        print(f" System Error: {e}")
        print("\n Troubleshooting:")
        print("1. Make sure all required packages are installed:")
        print("   pip install langchain langchain-community langchain-chroma")
        print("   pip install langchain-huggingface pypdf sentence-transformers")
        print("2. Place your study documents (PDF/TXT) in the 'documents' folder")
        print("3. For AI responses, install Ollama and run 'ollama pull llama3'")

if __name__ == "__main__":
    main()
    