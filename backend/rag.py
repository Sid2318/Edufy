import os
import glob
import shutil
import re
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage

# Simple cache to avoid multiple simultaneous AI calls
_ai_cache = {}
_ai_cache_lock = None

def get_cache_lock():
    """Get or create thread-safe lock for AI cache operations."""
    global _ai_cache_lock
    if _ai_cache_lock is None:
        import threading
        _ai_cache_lock = threading.Lock()
    return _ai_cache_lock

def clear_ai_cache():
    """Clear the AI cache to force regeneration of questions and flashcards.
    
    This should be called when a new document is uploaded to ensure that
    cached questions and flashcards don't persist across different documents.
    """
    global _ai_cache
    lock = get_cache_lock()
    with lock:
        cache_size = len(_ai_cache)
        _ai_cache.clear()
        if cache_size > 0:
            print(f"🔄 Cleared AI cache: {cache_size} cached items invalidated for new document")
        else:
            print("🔄 AI cache cleared (was already empty)")

def enhance_answer_with_ai(question, context_content, basic_answer=""):
    """Use AI model to generate enhanced, valid answers for questions."""
    try:
        # Check if Ollama is available
        import requests
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                print("⚠️ Ollama server not responding, using basic answer")
                return basic_answer if basic_answer else "Unable to generate enhanced answer - AI service unavailable"
        except:
            print("⚠️ Ollama server not available, using basic answer")
            return basic_answer if basic_answer else "Unable to generate enhanced answer - AI service unavailable"
        
        from langchain_ollama.chat_models import ChatOllama
        from langchain_core.messages import SystemMessage, HumanMessage
        
        # Initialize Ollama model
        model = ChatOllama(
            model="llama3",
            timeout=30,
            temperature=0.3
        )
        
        # Create an enhanced prompt
        prompt = f"""You are an expert educational assistant. Generate a comprehensive, accurate, and well-structured answer based on the provided context.

QUESTION: {question}

DOCUMENT CONTEXT:
{context_content[:3000]}

BASIC ANSWER (if available): {basic_answer}

INSTRUCTIONS:
1. Provide a comprehensive answer based STRICTLY on the document content
2. Make the answer educational and easy to understand
3. Structure the answer with clear explanations
4. Include specific details and examples from the document when relevant
5. If the question asks for definitions, provide complete and accurate definitions
6. If the question asks for processes or steps, explain them clearly
7. If the question asks for comparisons, highlight key differences and similarities
8. Keep the answer focused and relevant to the question
9. If information is not available in the document, clearly state that
10. Use proper formatting and organization

Generate a clear, comprehensive answer that would help a student understand the topic thoroughly:"""

        try:
            # Generate enhanced answer
            enhanced_response = model.invoke(prompt)
            
            if enhanced_response and len(enhanced_response.strip()) > 50:
                print("✅ Generated AI-enhanced answer")
                return enhanced_response.strip()
            else:
                print("⚠️ AI response too short, using basic answer")
                return basic_answer if basic_answer else "Unable to generate a comprehensive answer from the available content."
                
        except Exception as e:
            print(f"⚠️ Error generating enhanced answer: {e}")
            return basic_answer if basic_answer else "Error generating enhanced answer."
            
    except Exception as e:
        print(f"⚠️ Error with AI enhancement: {e}")
        return basic_answer if basic_answer else "Error with AI enhancement."

def enhance_flashcard_answers(flashcards, document_content):
    """Enhance flashcard answers using AI model for better quality and validity."""
    if not flashcards:
        return flashcards
    
    enhanced_flashcards = []
    
    for i, card in enumerate(flashcards):
        question = card.get("question", "")
        original_answer = card.get("answer", "")
        
        print(f"🤖 Enhancing flashcard {i+1}/{len(flashcards)}: {question[:50]}...")
        
        # Generate enhanced answer
        enhanced_answer = enhance_answer_with_ai(question, document_content, original_answer)
        
        enhanced_card = {
            "question": question,
            "answer": enhanced_answer,
            "original_answer": original_answer  # Keep original for comparison
        }
        
        # Preserve any additional fields
        for key, value in card.items():
            if key not in ["question", "answer"]:
                enhanced_card[key] = value
        
        enhanced_flashcards.append(enhanced_card)
    
    return enhanced_flashcards

def invalidate_previous_content():
    """Mark previous questions and flashcards as invalid for new document.
    
    This creates placeholder responses that indicate the content is no longer
    valid for the newly uploaded document.
    """
    return {
        "questions": [
            "🔄 Analyzing your new document...",
            "🔄 Generating fresh questions based on new content...",
            "🔄 Previous questions are no longer relevant...",
            "⏳ Please wait while we process your document...",
            "🧠 AI is reading and understanding your new material..."
        ],
        "flashcards": [
            {
                "question": "🔄 Document Updated", 
                "answer": "We're creating new flashcards based on your newly uploaded document. The previous flashcards are no longer relevant to your current material."
            },
            {
                "question": "⏳ Content Processing", 
                "answer": "Please wait while our AI analyzes your new document and generates personalized flashcards for effective studying."
            },
            {
                "question": "🧠 AI Working", 
                "answer": "Our intelligent system is reading through your document to identify the most important concepts for your flashcards."
            }
        ]
    }

def get_hardcoded_flashcards_by_domain(domain):
    """Return hardcoded flashcards based on document domain."""
    
    flashcards_by_domain = {
        "computer_networks": [
            {"question": "What does OSI stand for?", "answer": "Open Systems Interconnection - a conceptual framework used to describe network communications."},
            {"question": "What is TCP/IP?", "answer": "Transmission Control Protocol/Internet Protocol - the fundamental communication protocol suite for the internet."},
            {"question": "What is the difference between a hub and a switch?", "answer": "A hub broadcasts data to all ports, while a switch intelligently forwards data only to the intended recipient."},
            {"question": "What is an IP address?", "answer": "A unique numerical identifier assigned to devices on a network to enable communication."},
            {"question": "What is DNS?", "answer": "Domain Name System - translates human-readable domain names into IP addresses."}
        ],
        "computer_science": [
            {"question": "What is Big O notation?", "answer": "A mathematical notation that describes the upper bound of an algorithm's time or space complexity."},
            {"question": "What is a stack?", "answer": "A Last-In-First-Out (LIFO) data structure where elements are added and removed from the same end."},
            {"question": "What is recursion?", "answer": "A programming technique where a function calls itself to solve smaller instances of the same problem."},
            {"question": "What is object-oriented programming?", "answer": "A programming paradigm based on objects that contain data and methods to manipulate that data."},
            {"question": "What is a hash table?", "answer": "A data structure that maps keys to values using a hash function for fast data retrieval."}
        ],
        "mathematics": [
            {"question": "What is a derivative?", "answer": "The rate of change of a function with respect to its variable, representing the slope of the tangent line."},
            {"question": "What is an integral?", "answer": "The reverse of differentiation, representing the area under a curve or the accumulation of quantities."},
            {"question": "What is a matrix?", "answer": "A rectangular array of numbers arranged in rows and columns used in linear algebra."},
            {"question": "What is probability?", "answer": "The measure of the likelihood that an event will occur, expressed as a number between 0 and 1."},
            {"question": "What is a function?", "answer": "A mathematical relationship that assigns exactly one output value to each input value."}
        ],
        "physics": [
            {"question": "What is Newton's First Law?", "answer": "An object at rest stays at rest, and an object in motion stays in motion, unless acted upon by an external force."},
            {"question": "What is energy?", "answer": "The capacity to do work or cause change, existing in various forms like kinetic, potential, and thermal."},
            {"question": "What is electromagnetic radiation?", "answer": "Energy propagated through space as oscillating electric and magnetic fields, including light and radio waves."},
            {"question": "What is momentum?", "answer": "The product of an object's mass and velocity, representing its motion and resistance to stopping."},
            {"question": "What is thermodynamics?", "answer": "The branch of physics dealing with heat, temperature, energy, and their relationships."}
        ],
        "biology": [
            {"question": "What is DNA?", "answer": "Deoxyribonucleic acid - the molecule that carries genetic information in living organisms."},
            {"question": "What is photosynthesis?", "answer": "The process by which plants convert light energy into chemical energy, producing glucose and oxygen."},
            {"question": "What is mitosis?", "answer": "The process of cell division that produces two identical diploid cells from one parent cell."},
            {"question": "What is evolution?", "answer": "The process by which species change over time through natural selection and genetic variation."},
            {"question": "What is an enzyme?", "answer": "A protein that catalyzes biochemical reactions by lowering the activation energy required."}
        ],
        "chemistry": [
            {"question": "What is an atom?", "answer": "The smallest unit of matter that retains the properties of an element, consisting of protons, neutrons, and electrons."},
            {"question": "What is a chemical bond?", "answer": "The force that holds atoms together in molecules and compounds through sharing or transferring electrons."},
            {"question": "What is pH?", "answer": "A scale measuring the acidity or alkalinity of a solution, ranging from 0 to 14."},
            {"question": "What is a catalyst?", "answer": "A substance that increases the rate of a chemical reaction without being consumed in the process."},
            {"question": "What is the periodic table?", "answer": "An organized arrangement of chemical elements based on their atomic number and properties."}
        ]
    }
    
    return flashcards_by_domain.get(domain, [])

def generate_simple_flashcards(document_chunks, max_cards=15):
    """Generate domain-specific flashcards with AI-enhanced answers."""
    if not document_chunks:
        return []
    
    # Combine content from chunks
    combined_content = "\n".join([doc.page_content for doc in document_chunks[:8]])
    
    # Create cache key from document content
    content_preview = combined_content[:500]  # First 500 chars for cache key
    cache_key = f"flashcards_{hash(content_preview)}_{max_cards}"
    
    # Check cache first
    lock = get_cache_lock()
    with lock:
        if cache_key in _ai_cache:
            print("🔄 Using cached flashcards")
            return _ai_cache[cache_key]
    
    # Detect document domain
    domain = detect_document_domain(combined_content)
    
    # Get hardcoded flashcards for the domain
    print(f"📚 Generating {domain} domain flashcards...")
    hardcoded_flashcards = get_hardcoded_flashcards_by_domain(domain)
    
    # Start with hardcoded flashcards
    flashcards = hardcoded_flashcards.copy()
    
    flashcards = []
    
    # Rule 1: Extract definitions (key concepts)
    definition_patterns = [
        r'(\w+(?:\s+\w+){0,2})\s+(?:is|are|means?|refers?\s+to|defined?\s+as)\s+([^.!?]+[.!?])',
        r'(?:the|a)\s+(\w+(?:\s+\w+){0,2})\s+(?:is|are)\s+([^.!?]+[.!?])',
    ]
    
    for pattern in definition_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                term = match[0].strip().title()
                definition = match[1].strip()
                # Keep answers short (1-3 sentences max)
                if len(term) > 2 and 10 < len(definition) < 150:
                    # Ensure answer is concise
                    sentences = definition.split('.')
                    answer = '. '.join(sentences[:2]).strip()
                    if not answer.endswith('.'):
                        answer += '.'
                    
                    flashcards.append({
                        "question": f"What is {term}?",
                        "answer": answer
                    })
    
    # Rule 2: Extract key processes and procedures
    process_patterns = [
        r'(?:steps?|process|procedure|method)(?:\s+to|\s+for|\s+of)\s+([^:]+):\s*([^.!?]+[.!?])',
        r'(?:how to|to)\s+([^:]+):\s*([^.!?]+[.!?])',
    ]
    
    for pattern in process_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                process_name = match[0].strip()
                description = match[1].strip()
                if len(process_name) > 3 and 15 < len(description) < 120:
                    flashcards.append({
                        "question": f"How to {process_name}?",
                        "answer": description
                    })
    
    # Rule 3: Extract important facts and key points
    important_patterns = [
        r'(?:important|key|crucial|essential|vital|significant)[:\s]+([^.!?]+[.!?])',
        r'(?:note|remember|keep in mind)[:\s]+([^.!?]+[.!?])',
        r'(?:it is important to|must|should always)[:\s]+([^.!?]+[.!?])',
    ]
    
    for pattern in important_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            fact = match.strip()
            if 20 < len(fact) < 120:
                # Create question based on content
                if "important" in fact.lower():
                    question = "What is an important point to remember?"
                elif "must" in fact.lower() or "should" in fact.lower():
                    question = "What should you always do?"
                else:
                    question = "What is a key fact?"
                
                flashcards.append({
                    "question": question,
                    "answer": fact
                })
    
    # Rule 4: Extract comparisons and differences
    comparison_patterns = [
        r'(?:difference between|compare)\s+([^.!?]+?)(?:\s+and\s+|\s+vs\s+)([^.!?]+?)[:\s]*([^.!?]+[.!?])',
        r'([^.!?]+?)\s+(?:differs from|compared to)\s+([^.!?]+?)[:\s]*([^.!?]+[.!?])',
    ]
    
    for pattern in comparison_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            if len(match) == 3:
                item1 = match[0].strip()
                item2 = match[1].strip()
                difference = match[2].strip()
                if len(item1) > 2 and len(item2) > 2 and 15 < len(difference) < 120:
                    flashcards.append({
                        "question": f"What is the difference between {item1} and {item2}?",
                        "answer": difference
                    })
    
    # Rule 5: Extract lists and categories (key points)
    list_patterns = [
        r'(?:types?|kinds?|categories|examples?)\s+of\s+([^:]+):\s*([^.!?]+[.!?])',
        r'([^:]+?)\s+(?:include|are|consists? of):\s*([^.!?]+[.!?])',
    ]
    
    for pattern in list_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                category = match[0].strip()
                items = match[1].strip()
                if len(category) > 3 and 20 < len(items) < 130:
                    # Keep answer concise
                    sentences = items.split('.')
                    answer = '. '.join(sentences[:2]).strip()
                    if not answer.endswith('.'):
                        answer += '.'
                    
                    flashcards.append({
                        "question": f"What are the types of {category}?",
                        "answer": answer
                    })
    
    # Rule 6: Generate concept-based questions from document structure
    # Extract sentences that contain key concepts
    sentences = [s.strip() for s in combined_content.split('.') if s.strip()]
    concept_flashcards = []
    
    for sentence in sentences:
        if 30 < len(sentence) < 150:
            # Look for sentences with definitions or explanations
            if any(word in sentence.lower() for word in ['explains', 'describes', 'shows', 'demonstrates', 'illustrates']):
                # Extract the main concept
                words = sentence.split()
                if len(words) > 5:
                    # Create a "What does X explain/show?" question
                    concept_flashcards.append({
                        "question": "What concept is explained in this statement?",
                        "answer": sentence + "."
                    })
    
    # Add concept flashcards
    flashcards.extend(concept_flashcards[:3])  # Limit to 3
    
    # Rule 7: Add generic questions if we don't have enough specific ones
    if len(flashcards) < 5:
        # Extract first meaningful paragraph for summary
        paragraphs = [p.strip() for p in combined_content.split('\n') if len(p.strip()) > 50]
        first_paragraph = paragraphs[0] if paragraphs else combined_content[:200]
        
        # Keep summary answer to 1-2 sentences
        summary_sentences = first_paragraph.split('.')[:2]
        summary = '. '.join(summary_sentences).strip()
        if not summary.endswith('.'):
            summary += '.'
        
        generic_flashcards = [
            {
                "question": "What is the main topic of this document?",
                "answer": summary
            },
            {
                "question": "What are the key concepts covered?",
                "answer": "The document covers essential definitions, processes, and important facts related to the subject matter."
            },
            {
                "question": "What should you focus on when studying this material?",
                "answer": "Focus on understanding definitions, key processes, and the relationships between different concepts."
            }
        ]
        flashcards.extend(generic_flashcards)
    
    # Remove duplicates and ensure quality
    unique_flashcards = []
    seen_questions = set()
    
    for card in flashcards:
        question_key = card["question"].lower().strip()
        answer = card["answer"].strip()
        
        # Quality check: ensure answer is 1-3 sentences max
        answer_sentences = answer.split('.')
        if len(answer_sentences) > 4:  # More than 3 sentences (accounting for empty string after last period)
            answer = '. '.join(answer_sentences[:3]).strip() + '.'
            card["answer"] = answer
        
        # Check for duplicates and quality
        if (question_key not in seen_questions and 
            len(card["answer"]) > 10 and 
            len(card["answer"]) < 200 and
            len(unique_flashcards) < max_cards):
            seen_questions.add(question_key)
            unique_flashcards.append(card)
    
    final_flashcards = unique_flashcards[:max_cards]
    
    # ENHANCED: Use AI to improve flashcard answers
    print("🤖 Enhancing flashcard answers with AI...")
    enhanced_flashcards = enhance_flashcard_answers(final_flashcards, combined_content)
    
    if enhanced_flashcards:
        print(f"✅ Enhanced {len(enhanced_flashcards)} flashcard answers with AI")
        # Cache the enhanced result
        with lock:
            _ai_cache[cache_key] = enhanced_flashcards
        return enhanced_flashcards
    else:
        print("⚠️ AI enhancement failed, returning basic flashcards")
        # Cache the basic result
        with lock:
            _ai_cache[cache_key] = final_flashcards
        return final_flashcards

def detect_document_domain(content):
    """Detect the domain/subject of the document based on keywords."""
    content_lower = content.lower()
    
    # Define domain keywords
    domains = {
        "computer_networks": [
            "osi model", "tcp/ip", "network", "protocol", "router", "switch", "ethernet", 
            "ip address", "subnet", "dns", "http", "https", "firewall", "bandwidth",
            "packet", "frame", "topology", "lan", "wan", "wireless", "fiber optic"
        ],
        "computer_science": [
            "algorithm", "data structure", "programming", "coding", "software", "database",
            "operating system", "compiler", "debugging", "array", "linked list", "stack",
            "queue", "tree", "graph", "sorting", "searching", "complexity", "recursion"
        ],
        "mathematics": [
            "equation", "function", "derivative", "integral", "matrix", "vector", "calculus",
            "algebra", "geometry", "probability", "statistics", "theorem", "proof", "formula",
            "trigonometry", "logarithm", "polynomial", "linear", "quadratic"
        ],
        "physics": [
            "force", "energy", "momentum", "velocity", "acceleration", "mass", "gravity",
            "electric", "magnetic", "wave", "frequency", "amplitude", "quantum", "particle",
            "thermodynamics", "mechanics", "optics", "relativity", "nuclear"
        ],
        "biology": [
            "cell", "dna", "rna", "protein", "enzyme", "chromosome", "gene", "evolution",
            "photosynthesis", "mitosis", "meiosis", "organism", "species", "ecosystem",
            "metabolism", "respiration", "reproduction", "heredity", "mutation"
        ],
        "chemistry": [
            "atom", "molecule", "element", "compound", "reaction", "bond", "acid", "base",
            "ion", "electron", "proton", "neutron", "periodic table", "catalyst", "solution",
            "ph", "oxidation", "reduction", "organic", "inorganic"
        ],
        "business": [
            "management", "marketing", "finance", "accounting", "strategy", "profit", "revenue",
            "investment", "stock", "market", "customer", "competition", "supply chain",
            "human resources", "leadership", "entrepreneur", "budget", "analysis"
        ],
        "literature": [
            "author", "character", "plot", "theme", "setting", "narrative", "metaphor",
            "symbolism", "poetry", "novel", "drama", "prose", "verse", "literary",
            "fiction", "non-fiction", "genre", "style", "analysis"
        ]
    }
    
    # Count keyword matches for each domain
    domain_scores = {}
    for domain, keywords in domains.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            domain_scores[domain] = score
    
    # Return the domain with highest score
    if domain_scores:
        best_domain = max(domain_scores, key=domain_scores.get)
        print(f"🎯 Detected domain: {best_domain} (score: {domain_scores[best_domain]})")
        return best_domain
    
    print("🎯 Domain: general (no specific domain detected)")
    return "general"

def get_hardcoded_questions_by_domain(domain, content_preview=""):
    """Return hardcoded smart questions based on document domain."""
    
    questions_by_domain = {
        "computer_networks": [
            "What are the seven layers of the OSI model and their functions?",
            "How does TCP/IP protocol suite work?",
            "What is the difference between a router and a switch?",
            "How does DNS resolution work?",
            "What are the different network topologies and their advantages?",
            "How does Ethernet protocol function?",
            "What is the difference between IPv4 and IPv6?",
            "How do firewalls protect networks?",
            "What is subnetting and why is it important?",
            "How does wireless networking work?"
        ],
        "computer_science": [
            "What are the fundamental data structures and when to use each?",
            "How do different sorting algorithms compare in terms of time complexity?",
            "What is the difference between stack and heap memory?",
            "How does recursion work and when should it be used?",
            "What are the principles of object-oriented programming?",
            "How do hash tables work and what are their applications?",
            "What is Big O notation and why is it important?",
            "How do different tree traversal algorithms work?",
            "What are the key concepts in database design?",
            "How does garbage collection work in programming languages?"
        ],
        "mathematics": [
            "What are the fundamental concepts of calculus?",
            "How do you solve systems of linear equations?",
            "What are the properties of different types of functions?",
            "How do you calculate derivatives and integrals?",
            "What are the key principles of probability theory?",
            "How do you work with matrices and vectors?",
            "What are the different types of mathematical proofs?",
            "How do trigonometric functions relate to geometry?",
            "What are the applications of logarithms?",
            "How do you analyze statistical data?"
        ],
        "physics": [
            "What are Newton's laws of motion and their applications?",
            "How do electric and magnetic fields interact?",
            "What are the principles of thermodynamics?",
            "How does wave motion work in different media?",
            "What are the key concepts of quantum mechanics?",
            "How do you calculate work, energy, and power?",
            "What are the principles of relativity?",
            "How does light behave as both wave and particle?",
            "What are the fundamental forces in nature?",
            "How do you analyze circular and rotational motion?"
        ],
        "biology": [
            "How does cellular respiration produce energy?",
            "What are the stages of mitosis and meiosis?",
            "How does DNA replication work?",
            "What are the principles of genetics and heredity?",
            "How does photosynthesis convert light to chemical energy?",
            "What are the different types of ecosystems?",
            "How does evolution shape species over time?",
            "What are the functions of different organ systems?",
            "How do enzymes catalyze biochemical reactions?",
            "What are the principles of molecular biology?"
        ],
        "chemistry": [
            "How do chemical bonds form between atoms?",
            "What are the different types of chemical reactions?",
            "How does the periodic table organize elements?",
            "What are acids, bases, and pH?",
            "How do you balance chemical equations?",
            "What are the principles of thermochemistry?",
            "How does molecular geometry affect chemical properties?",
            "What are the differences between organic and inorganic chemistry?",
            "How do catalysts affect reaction rates?",
            "What are the states of matter and phase transitions?"
        ],
        "business": [
            "What are the key principles of strategic management?",
            "How do you analyze market competition?",
            "What are the fundamentals of financial accounting?",
            "How do you develop effective marketing strategies?",
            "What are the principles of organizational behavior?",
            "How do you evaluate investment opportunities?",
            "What are the different leadership styles?",
            "How do you manage supply chain operations?",
            "What are the key performance indicators for business?",
            "How do you conduct market research?"
        ],
        "literature": [
            "What are the major themes in this literary work?",
            "How do characters develop throughout the story?",
            "What literary devices does the author use?",
            "How does the setting influence the narrative?",
            "What is the significance of symbolism in the text?",
            "How does the author's style contribute to meaning?",
            "What are the cultural and historical contexts?",
            "How do different interpretations of the work compare?",
            "What are the moral and philosophical questions raised?",
            "How does this work relate to other literature of its time?"
        ],
        "general": [
            "What are the main topics covered in this document?",
            "What are the key concepts you should understand?",
            "How do the different sections relate to each other?",
            "What examples or case studies are provided?",
            "What are the practical applications mentioned?",
            "What are the important definitions to remember?",
            "How can you apply this knowledge?",
            "What are the key takeaways from this material?",
            "What additional resources might be helpful?",
            "How does this content build on previous knowledge?"
        ]
    }
    
    return questions_by_domain.get(domain, questions_by_domain["general"])

def generate_questions_from_content(document_chunks):
    """Generate intelligent sample questions based on document domain and content analysis."""
    if not document_chunks:
        return []
    
    # Use more chunks for better analysis (up to 8 chunks)
    combined_content = "\n".join([doc.page_content for doc in document_chunks[:8]])
    
    # Create cache key from document content
    content_preview = combined_content[:500]  # First 500 chars for cache key
    cache_key = f"questions_{hash(content_preview)}"
    
    # Check cache first
    lock = get_cache_lock()
    with lock:
        if cache_key in _ai_cache:
            print("🔄 Using cached smart questions")
            return _ai_cache[cache_key]
    
    # Detect document domain
    domain = detect_document_domain(combined_content)
    
    # Get hardcoded questions for the domain
    print(f"📚 Generating {domain} domain questions...")
    hardcoded_questions = get_hardcoded_questions_by_domain(domain, content_preview)
    
    # Take first 8-10 questions from the hardcoded list
    domain_questions = hardcoded_questions[:10]
    
    content_lower = combined_content.lower()
    
    questions = []
    processed_terms = set()  # Avoid duplicate concepts
    
    # 1. ENHANCED DEFINITION EXTRACTION with better filtering
    definition_patterns = [
        # Pattern: "X is defined as Y" or "X is Y"
        r'([A-Z][a-zA-Z\s]{2,25})\s+(?:is|are)\s+(?:defined\s+as\s+)?([^.!?]{20,100}[.!?])',
        # Pattern: "X means Y" or "X refers to Y"
        r'([A-Z][a-zA-Z\s]{2,25})\s+(?:means?|refers?\s+to)\s+([^.!?]{15,80}[.!?])',
        # Pattern: "The term X is Y"
        r'(?:the\s+term\s+|the\s+concept\s+of\s+)?([A-Z][a-zA-Z\s]{2,25})\s+is\s+([^.!?]{20,100}[.!?])',
        # Pattern: "X can be defined as Y"
        r'([A-Z][a-zA-Z\s]{2,25})\s+(?:can\s+be\s+)?defined\s+as\s+([^.!?]{15,80}[.!?])'
    ]
    
    important_definitions = {}
    for pattern in definition_patterns:
        matches = re.findall(pattern, combined_content, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                term = match[0].strip().title()
                definition = match[1].strip()
                
                # Filter for important terms (avoid common words)
                if (len(term.split()) <= 4 and 
                    len(term) > 3 and 
                    not any(word in term.lower() for word in ['this', 'that', 'these', 'those', 'such', 'other']) and
                    len(definition) > 20):
                    
                    # Score based on definition quality and term frequency
                    term_frequency = content_lower.count(term.lower())
                    score = term_frequency + (len(definition) / 10)
                    important_definitions[term] = score
    
    # Sort definitions by importance and generate questions
    sorted_definitions = sorted(important_definitions.items(), key=lambda x: x[1], reverse=True)
    for term, score in sorted_definitions[:4]:  # Top 4 most important definitions
        if term not in processed_terms:
            questions.append(f"What is {term}?")
            processed_terms.add(term.lower())
    
    # 2. PROCESS AND METHODOLOGY QUESTIONS - Enhanced patterns
    process_patterns = [
        # Steps, phases, stages
        r'(?:steps?|phases?|stages?|procedures?)\s+(?:of|for|in|to)\s+([^.!?]{5,30})',
        r'(?:how\s+to|process\s+of|method\s+for)\s+([^.!?]{5,40})',
        r'([^.!?]{5,30})\s+(?:process|procedure|method|approach)',
        # Sequential indicators
        r'(?:first|second|third|initially|then|next|finally)[,\s]+([^.!?]{10,50})'
    ]
    
    processes = set()
    for pattern in process_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            process = match.strip().title()
            if (len(process.split()) <= 6 and 
                len(process) > 5 and 
                not any(word in process.lower() for word in ['this', 'that', 'these', 'example'])):
                processes.add(process)
    
    # Generate process questions
    for process in list(processes)[:3]:  # Top 3 processes
        if process.lower() not in processed_terms:
            questions.append(f"What are the steps involved in {process}?")
            processed_terms.add(process.lower())
    
    # 3. CLASSIFICATION AND CATEGORIZATION QUESTIONS - Enhanced
    classification_patterns = [
        # Types, kinds, categories
        r'(?:different\s+)?(?:types?|kinds?|categories|forms?)\s+of\s+([^.!?]{3,30})',
        r'([^.!?]{3,30})\s+(?:can\s+be\s+)?(?:classified|categorized|divided)\s+into',
        r'(?:main|primary|key)\s+([^.!?]{3,30})\s+(?:include|are)',
        # Multiple items pattern
        r'(?:several|many|various|multiple)\s+([^.!?]{3,30})\s+(?:exist|are\s+available|can\s+be\s+found)'
    ]
    
    classifications = set()
    for pattern in classification_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            topic = match.strip().title()
            if (len(topic.split()) <= 4 and 
                len(topic) > 3 and 
                topic.lower() not in processed_terms):
                classifications.add(topic)
    
    # Generate classification questions
    for topic in list(classifications)[:3]:
        if topic.lower() not in processed_terms:
            questions.append(f"What are the different types of {topic}?")
            processed_terms.add(topic.lower())
    
    # 4. COMPARATIVE AND ANALYTICAL QUESTIONS
    comparison_patterns = [
        r'(?:difference|differences)\s+between\s+([^.!?]{5,40})\s+and\s+([^.!?]{5,40})',
        r'(?:compared?\s+to|versus|vs\.?)\s+([^.!?]{5,30})',
        r'(?:advantages?|benefits?|pros?)\s+(?:of|and)\s+([^.!?]{5,30})',
        r'(?:disadvantages?|drawbacks?|cons?)\s+(?:of|and)\s+([^.!?]{5,30})'
    ]
    
    comparisons = set()
    for pattern in comparison_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                for item in match:
                    comparisons.add(item.strip().title())
            else:
                comparisons.add(match.strip().title())
    
    # Generate comparison questions
    for comparison in list(comparisons)[:2]:
        if (len(comparison.split()) <= 4 and 
            comparison.lower() not in processed_terms):
            questions.append(f"What are the advantages and disadvantages of {comparison}?")
            processed_terms.add(comparison.lower())
    
    # 5. CONTEXTUAL AND APPLIED QUESTIONS
    application_patterns = [
        r'(?:used\s+for|applications?\s+of|applied\s+in)\s+([^.!?]{5,40})',
        r'(?:importance|significance|role)\s+of\s+([^.!?]{5,40})',
        r'(?:impact|effect|influence)\s+(?:of|on)\s+([^.!?]{5,40})'
    ]
    
    applications = set()
    for pattern in application_patterns:
        matches = re.findall(pattern, content_lower, re.IGNORECASE)
        for match in matches:
            app = match.strip().title()
            if (len(app.split()) <= 4 and 
                len(app) > 3 and 
                app.lower() not in processed_terms):
                applications.add(app)
    
    # Generate application questions
    for app in list(applications)[:2]:
        questions.append(f"What is the importance of {app}?")
        processed_terms.add(app.lower())
    
    # 6. ENHANCED FALLBACK QUESTIONS - More document-specific
    if len(questions) < 8:
        # Extract key topics for more specific fallback questions
        key_topics = []
        topic_patterns = [
            r'(?:chapter|section)\s+\d+[:\s]*([^.!?\n]{5,40})',
            r'(?:introduction\s+to|overview\s+of)\s+([^.!?]{5,40})',
            r'(?:understanding|learning|studying)\s+([^.!?]{5,40})'
        ]
        
        for pattern in topic_patterns:
            matches = re.findall(pattern, combined_content, re.IGNORECASE)
            for match in matches:
                topic = match.strip().title()
                if len(topic.split()) <= 5 and len(topic) > 5:
                    key_topics.append(topic)
        
        # Generate topic-specific questions
        if key_topics:
            for topic in key_topics[:2]:
                questions.append(f"Explain the key concepts related to {topic}")
        
        # Add high-quality generic questions only if needed
        smart_generics = [
            "What are the main objectives discussed in this document?",
            "What are the key takeaways from this material?",
            "What practical applications are mentioned in this document?",
            "What challenges or problems are addressed in this content?",
            "What solutions or recommendations are provided?"
        ]
        
        while len(questions) < 8 and smart_generics:
            questions.append(smart_generics.pop(0))
    
    # Combine hardcoded domain questions with content-extracted questions
    all_questions = []
    
    # Prioritize hardcoded domain questions (first 6-8 questions)
    all_questions.extend(domain_questions[:8])
    
    # Add content-extracted questions to fill gaps
    for q in questions[:4]:  # Add up to 4 content-specific questions
        if q not in all_questions:
            all_questions.append(q)
    
    # Remove duplicates while preserving order
    final_questions = []
    seen_questions = set()
    for q in all_questions:
        q_lower = q.lower()
        if q_lower not in seen_questions:
            final_questions.append(q)
            seen_questions.add(q_lower)
    
    # Limit to 10 questions
    final_questions = final_questions[:10]
    
    print(f"✅ Generated {len(final_questions)} domain-specific questions for {domain}")
    
    # Cache the result
    with lock:
        _ai_cache[cache_key] = final_questions
    
    return final_questions

def extract_key_terms_with_frequency(text):
    """Extract important terms based on frequency and context."""
    # Remove common stop words and extract meaningful terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their'}
    
    # Extract capitalized terms (likely important concepts)
    capitalized_terms = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
    
    # Count frequency of important terms
    term_frequency = {}
    for term in capitalized_terms:
        if term.lower() not in stop_words and len(term) > 3:
            term_frequency[term] = term_frequency.get(term, 0) + 1
    
    # Return terms sorted by frequency
    return sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)

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
            
            # Validate document content
            valid_documents = []
            for doc in documents:
                if doc.page_content and doc.page_content.strip():
                    valid_documents.append(doc)
            
            if valid_documents:
                all_documents.extend(valid_documents)
                print(f"✓ Loaded {len(valid_documents)} valid pages from {os.path.basename(pdf_file)}")
            else:
                print(f"⚠ Warning: {os.path.basename(pdf_file)} contains no readable text content")
                
        except Exception as e:
            print(f"✗ Error loading {pdf_file}: {e}")
    
    # Load text files
    txt_files = glob.glob(os.path.join(documents_dir, "*.txt"))
    for txt_file in txt_files:
        try:
            print(f"Loading text file: {os.path.basename(txt_file)}")
            loader = TextLoader(txt_file, encoding='utf-8')
            documents = loader.load()
            
            # Validate document content
            valid_documents = []
            for doc in documents:
                if doc.page_content and doc.page_content.strip():
                    valid_documents.append(doc)
            
            if valid_documents:
                all_documents.extend(valid_documents)
                print(f"✓ Loaded {os.path.basename(txt_file)} with valid content")
            else:
                print(f"⚠ Warning: {os.path.basename(txt_file)} is empty or contains no readable text")
                
        except Exception as e:
            print(f"✗ Error loading {txt_file}: {e}")
            # Try with different encoding
            try:
                print(f"  → Retrying with latin-1 encoding...")
                loader = TextLoader(txt_file, encoding='latin-1')
                documents = loader.load()
                valid_documents = []
                for doc in documents:
                    if doc.page_content and doc.page_content.strip():
                        valid_documents.append(doc)
                if valid_documents:
                    all_documents.extend(valid_documents)
                    print(f"✓ Loaded {os.path.basename(txt_file)} with latin-1 encoding")
            except Exception as e2:
                print(f"✗ Failed to load {txt_file} with any encoding: {e2}")
    
    # Validate final document list
    if not all_documents:
        print("❌ No valid documents found. Please check if uploaded files contain readable text.")
    else:
        print(f"📚 Successfully loaded {len(all_documents)} document pages total")
    
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
        
        # Validate that we have content after splitting
        if not docs:
            print("❌ No document chunks created after splitting. Documents might be empty or corrupted.")
            return None, None
        
        # Filter out empty chunks
        valid_docs = []
        for doc in docs:
            if doc.page_content and doc.page_content.strip():
                valid_docs.append(doc)
        
        if not valid_docs:
            print("❌ No valid document chunks found. All chunks are empty.")
            return None, None
        
        docs = valid_docs
        
        # Display information about the split documents
        print(f"\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(docs)}")
        print(f"Total documents processed: {len(documents)}")
        print(f"Sample chunk preview:\n{docs[0].page_content[:300]}...\n")
        
        # Create embeddings
        print("--- Creating embeddings ---")
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            return None, None
        print("--- Finished creating embeddings ---")
        
        # Create the vector store and persist it automatically
        print("--- Creating vector store ---")
        try:
            db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
            print("--- Finished creating vector store ---")
        except Exception as e:
            print(f"❌ Error creating vector store: {e}")
            print("This might be due to empty or invalid document content.")
            return None, None
        
        return db, embeddings
    else:
        print("Vector store already exists. Loading existing store...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
        return db, embeddings

def analyze_query_type(query):
    """Analyze the query to determine the appropriate retrieval strategy."""
    query_lower = query.lower().strip()
    
    # Broad/Summary queries - need more context
    summary_keywords = [
        'summarize', 'summary', 'overview', 'explain all', 'tell me about',
        'what is this document about', 'main points', 'key points', 'everything',
        'all about', 'complete', 'entire document', 'whole', 'comprehensive',
        'topics covered', 'what topics', 'what does this cover'
    ]
    
    # Specific/Detail queries - need focused retrieval
    specific_keywords = [
        'define', 'definition', 'what is', 'who is', 'when', 'where', 'how much',
        'specific', 'exactly', 'precisely', 'find', 'locate', 'search for',
        'one detail', 'particular', 'single', 'individual'
    ]
    
    # List/Enumeration queries - need moderate context
    list_keywords = [
        'list', 'types of', 'kinds of', 'examples of', 'categories',
        'what are the', 'how many', 'enumerate', 'steps', 'process',
        'methods', 'ways', 'approaches'
    ]
    
    # Comparison queries - need multiple contexts
    comparison_keywords = [
        'compare', 'contrast', 'difference', 'similar', 'versus', 'vs',
        'better', 'worse', 'advantages', 'disadvantages', 'pros', 'cons'
    ]
    
    # Check for query patterns
    if any(keyword in query_lower for keyword in summary_keywords):
        return "summary"  # Large k
    elif any(keyword in query_lower for keyword in specific_keywords):
        return "specific"  # Small k
    elif any(keyword in query_lower for keyword in list_keywords):
        return "list"  # Medium k
    elif any(keyword in query_lower for keyword in comparison_keywords):
        return "comparison"  # Medium-large k
    else:
        return "general"  # Default medium k

def calculate_dynamic_k(total_chunks, query_type, query_length):
    """Calculate the optimal k value based on document size, query type, and complexity."""
    
    # Base k values by query type
    k_mapping = {
        "specific": {"min": 1, "base": 2, "max": 4},
        "list": {"min": 2, "base": 4, "max": 6}, 
        "comparison": {"min": 3, "base": 5, "max": 8},
        "summary": {"min": 4, "base": 8, "max": 12},
        "general": {"min": 2, "base": 4, "max": 6}
    }
    
    k_config = k_mapping.get(query_type, k_mapping["general"])
    
    # Start with base k for the query type
    k = k_config["base"]
    
    # Adjust based on document size
    if total_chunks <= 3:
        # Very small document - take everything
        k = min(total_chunks, k_config["max"])
    elif total_chunks <= 10:
        # Small document - slightly reduce k
        k = max(k_config["min"], k - 1)
    elif total_chunks <= 25:
        # Medium document - use base k
        k = k_config["base"]
    elif total_chunks <= 50:
        # Large document - slightly increase k for summary/comparison
        if query_type in ["summary", "comparison"]:
            k = min(k + 2, k_config["max"])
    else:
        # Very large document - use max k for broad queries, min for specific
        if query_type == "specific":
            k = k_config["min"]
        elif query_type in ["summary", "comparison"]:
            k = k_config["max"]
        else:
            k = k_config["base"]
    
    # Adjust based on query complexity (length as a proxy)
    if query_length > 100:  # Complex, detailed query
        k = min(k + 1, k_config["max"])
    elif query_length < 20:  # Simple, short query
        k = max(k - 1, k_config["min"])
    
    # Ensure k doesn't exceed available chunks
    k = min(k, total_chunks)
    
    # Ensure k is at least 1
    k = max(1, k)
    
    return k

def query_documents(db, query, use_llm=True):
    """Query the vector store and use LLM to generate response based on retrieved content with dynamic k."""
    
    # Analyze query type and calculate dynamic k
    query_type = analyze_query_type(query)
    
    # Get total number of chunks in the database (approximate)
    try:
        # Get a large sample to estimate total chunks
        temp_retriever = db.as_retriever(search_kwargs={"k": 100})
        temp_results = temp_retriever.invoke("sample query for counting")
        total_chunks = len(temp_results) if temp_results else 10  # fallback estimate
        # For more accurate count, we use this as an approximation
        if len(temp_results) == 100:
            total_chunks = 100  # We hit the limit, likely more chunks
    except:
        total_chunks = 10  # Safe fallback
    
    # Calculate optimal k
    k = calculate_dynamic_k(total_chunks, query_type, len(query))
    
    print(f"🔍 Query Analysis:")
    print(f"   Type: {query_type}")
    print(f"   Document chunks: ~{total_chunks}")
    print(f"   Retrieving top {k} most relevant sections")
    print("-" * 40)
    
    # Retrieve relevant documents based on the dynamic k
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
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
        
        # Adapt the prompt based on query type
        context_content = "\n\n".join([f"Section {i+1}:\n{doc.page_content}" for i, doc in enumerate(relevant_docs)])
        
        # Customize prompt based on query type
        if query_type == "summary":
            instruction = (
                "Provide a comprehensive summary that synthesizes information from all the provided sections. "
                "Cover the main topics, key points, and important details."
            )
        elif query_type == "specific":
            instruction = (
                "Focus on providing a precise, specific answer to the question. "
                "Be direct and concise while ensuring accuracy."
            )
        elif query_type == "list":
            instruction = (
                "Organize your response as a clear, structured list or enumeration. "
                "Include relevant examples and categorize information where appropriate."
            )
        elif query_type == "comparison":
            instruction = (
                "Compare and contrast the relevant information from the provided sections. "
                "Highlight similarities, differences, and relationships between concepts."
            )
        else:
            instruction = (
                "Provide a comprehensive and accurate answer based on the provided context. "
                "Structure your response clearly and include relevant details."
            )
        
        combined_input = (
            f"Question: {query}\n\n"
            f"Context from relevant documents:\n{context_content}\n\n"
            f"{instruction} "
            f"Use only the information provided in the context. If the answer cannot be found in the "
            f"provided context, clearly state that the information is not available."
        )
        
        try:
            # Generate basic fallback response first
            fallback_response = generate_fallback_response(query, relevant_docs, query_type)
            
            # ENHANCED: Use AI to generate comprehensive answer
            print("🤖 Generating AI-enhanced response for your question...")
            enhanced_response = enhance_answer_with_ai(query, context_content, fallback_response)
            
            # Display the generated response
            print(f"🤖 Enhanced AI Response ({query_type} query, k={k}):")
            print(enhanced_response[:200] + "..." if len(enhanced_response) > 200 else enhanced_response)
            
            # Return the enhanced LLM response along with source documents
            return {
                "ai_response": enhanced_response,
                "source_documents": relevant_docs,
                "query_type": query_type,
                "k_used": k,
                "method": "ai_enhanced",
                "basic_response": fallback_response  # Keep basic response for comparison
            }
            
        except Exception as e:
            print(f"⚠️ Primary AI Error: {str(e)}")
            print("� Trying enhanced AI fallback:")
            
            # Generate basic fallback response
            fallback_response = generate_fallback_response(query, relevant_docs, query_type)
            
            # Try enhanced AI as backup
            enhanced_response = enhance_answer_with_ai(query, context_content, fallback_response)
            
            print(f"📄 Enhanced Fallback Response ({query_type} query, k={k}):")
            print(enhanced_response[:200] + "..." if len(enhanced_response) > 200 else enhanced_response)
            
            return {
                "ai_response": enhanced_response,
                "source_documents": relevant_docs,
                "query_type": query_type,
                "k_used": k,
                "method": "ai_fallback",
                "basic_response": fallback_response
            }
    
    return relevant_docs

def generate_fallback_response(query, relevant_docs, query_type="general"):
    """Generate a structured response when LLM is not available."""
    if not relevant_docs:
        return "No relevant information found in the uploaded documents."
    
    response_parts = []
    
    # Customize response based on query type
    if query_type == "summary":
        response_parts.append(f"Here's a summary based on your uploaded document regarding '{query}':")
        response_parts.append("\n📋 Main Topics Found:")
    elif query_type == "specific":
        response_parts.append(f"Here's the specific information I found regarding '{query}':")
    elif query_type == "list":
        response_parts.append(f"Here are the relevant items/points I found regarding '{query}':")
        response_parts.append("\n📝 Listed Information:")
    elif query_type == "comparison":
        response_parts.append(f"Here's comparative information I found regarding '{query}':")
        response_parts.append("\n⚖️ Comparison Points:")
    else:
        response_parts.append(f"Based on the uploaded document, here's what I found regarding '{query}':")
    
    for i, doc in enumerate(relevant_docs, 1):
        content = doc.page_content.strip()
        source = doc.metadata.get('source', 'Unknown source')
        filename = os.path.basename(source)
        
        # Adjust content length based on query type
        max_length = {
            "specific": 200,  # Shorter for specific queries
            "summary": 600,   # Longer for summaries
            "list": 400,      # Medium for lists
            "comparison": 500, # Medium-long for comparisons
            "general": 400    # Default medium
        }.get(query_type, 400)
        
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        if query_type == "list":
            response_parts.append(f"\n  {i}. {content}")
            response_parts.append(f"     📄 Source: {filename}")
        else:
            response_parts.append(f"\n{i}. From {filename}:")
            response_parts.append(f"   {content}")
    
    # Add contextual footer based on query type
    if query_type == "summary":
        response_parts.append(f"\n📊 This summary covers {len(relevant_docs)} key section(s) from your document.")
    elif query_type == "specific":
        response_parts.append(f"\n🎯 This specific information is from {len(relevant_docs)} relevant section(s).")
    else:
        response_parts.append(f"\n📚 This information is extracted from {len(relevant_docs)} relevant section(s) of your uploaded document.")
    
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
    