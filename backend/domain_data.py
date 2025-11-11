# domain_data.py
"""
Domain-specific data for educational content generation.
Contains hardcoded keywords, questions, and flashcards for different academic domains.
"""

# Domain keyword definitions for automatic detection
DOMAIN_KEYWORDS = {
    "computer_networks": [
        "osi model", "tcp/ip", "network", "protocol", "router", "switch", "ethernet", 
        "ip address", "subnet", "dns", "http", "https", "firewall", "bandwidth",
        "packet", "frame", "topology", "lan", "wan", "wireless", "fiber optic"
    ],
    "operating_systems": [
        "operating system", "kernel", "process", "thread", "memory management", "cpu scheduling",
        "deadlock", "semaphore", "mutex", "virtual memory", "paging", "segmentation",
        "file system", "system call", "interrupt", "context switching", "multiprogramming",
        "multitasking", "unix", "linux", "windows", "scheduling algorithm", "synchronization"
    ],
    "database": [
        "database", "sql", "nosql", "rdbms", "table", "query", "join", "index", "primary key",
        "foreign key", "normalization", "acid", "transaction", "relational", "mongodb",
        "mysql", "postgresql", "oracle", "select", "insert", "update", "delete", "schema",
        "entity relationship", "data modeling", "stored procedure", "trigger", "view"
    ],
    "computer_science": [
        "algorithm", "data structure", "programming", "coding", "software", "compiler", 
        "debugging", "array", "linked list", "stack", "queue", "tree", "graph", 
        "sorting", "searching", "complexity", "recursion", "object oriented", "inheritance"
    ],
    "software_engineering": [
        "software engineering", "sdlc", "agile", "scrum", "waterfall", "requirements", "design patterns",
        "testing", "unit test", "integration test", "version control", "git", "code review",
        "refactoring", "debugging", "maintenance", "documentation", "uml", "architecture",
        "microservices", "api", "framework", "deployment", "devops", "continuous integration"
    ],
    "electrical_engineering": [
        "electrical engineering", "circuit", "voltage", "current", "resistance", "capacitor",
        "inductor", "transistor", "diode", "amplifier", "filter", "oscillator", "power",
        "electrical power", "transformer", "motor", "generator", "control system", "signal processing",
        "electromagnetics", "electronics", "digital circuit", "analog circuit", "microprocessor"
    ],
    "mechanical_engineering": [
        "mechanical engineering", "thermodynamics", "fluid mechanics", "heat transfer", "mechanics",
        "statics", "dynamics", "materials", "strength of materials", "machine design", "manufacturing",
        "cad", "finite element", "vibration", "control system", "robotics", "automation",
        "engine", "turbine", "pump", "compressor", "gear", "bearing", "stress", "strain"
    ],
    "civil_engineering": [
        "civil engineering", "structural", "concrete", "steel", "foundation", "beam", "column",
        "bridge", "building", "construction", "surveying", "geotechnical", "soil mechanics",
        "hydraulics", "water resources", "transportation", "highway", "pavement", "earthquake",
        "seismic", "load", "stress analysis", "reinforcement", "structural analysis"
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
    ],
    "oop": [
        "object oriented programming", "class", "object", "inheritance", "polymorphism",
        "encapsulation", "abstraction", "method", "attribute", "constructor", "destructor",
        "overloading", "overriding", "interface", "abstract class", "virtual function",
        "static", "public", "private", "protected", "this", "super", "extends", "implements"
    ],
    "os": [
        "operating system", "process", "thread", "scheduling", "memory management", "virtual memory",
        "paging", "segmentation", "deadlock", "synchronization", "semaphore", "mutex", "monitor",
        "critical section", "race condition", "file system", "inode", "directory", "boot process",
        "system call", "interrupt", "context switch", "kernel", "user space", "kernel space"
    ],
    "dbms": [
        "database management system", "relational database", "sql", "nosql", "acid properties",
        "transaction", "concurrency control", "locking", "indexing", "b-tree", "hash index",
        "normalization", "denormalization", "entity relationship", "primary key", "foreign key",
        "join", "query optimization", "stored procedure", "trigger", "view", "backup", "recovery"
    ]
}

# Domain-specific sample questions for intelligent question generation
DOMAIN_QUESTIONS = {
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
    "operating_systems": [
        "What are the main functions of an operating system?",
        "How does CPU scheduling work and what are common algorithms?",
        "What is the difference between process and thread?",
        "How does virtual memory management work?",
        "What are deadlocks and how can they be prevented?",
        "How do semaphores and mutexes provide synchronization?",
        "What are the different file system structures?",
        "How does paging differ from segmentation?",
        "What are system calls and how do they work?",
        "How does context switching occur in multitasking?"
    ],
    "database": [
        "What are the ACID properties in database transactions?",
        "How do different types of SQL joins work?",
        "What is database normalization and why is it important?",
        "What is the difference between primary and foreign keys?",
        "How do database indexes improve query performance?",
        "What are the differences between SQL and NoSQL databases?",
        "How does a relational database management system work?",
        "What are stored procedures and when should you use them?",
        "How do database transactions ensure data consistency?",
        "What are the different types of database relationships?"
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
        "What are design patterns and why are they useful?",
        "How does garbage collection work in programming languages?"
    ],
    "software_engineering": [
        "What are the phases of the Software Development Life Cycle?",
        "How does Agile methodology differ from Waterfall?",
        "What are the key principles of object-oriented design?",
        "How do you write effective unit tests?",
        "What are design patterns and when should you use them?",
        "How does version control with Git work?",
        "What are the benefits of code reviews?",
        "How do you handle software requirements gathering?",
        "What is continuous integration and deployment?",
        "How do microservices architecture compare to monolithic?"
    ],
    "electrical_engineering": [
        "What is Ohm's law and how is it applied?",
        "How do capacitors and inductors behave in AC circuits?",
        "What are the differences between analog and digital circuits?",
        "How do transistors work as switches and amplifiers?",
        "What are the principles of electromagnetic induction?",
        "How do transformers change voltage levels?",
        "What are the types of electrical motors and their applications?",
        "How do control systems maintain desired outputs?",
        "What is signal processing and its applications?",
        "How do power systems distribute electrical energy?"
    ],
    "mechanical_engineering": [
        "What are the four laws of thermodynamics?",
        "How does heat transfer occur through conduction, convection, and radiation?",
        "What are the principles of fluid mechanics?",
        "How do you analyze forces in static equilibrium?",
        "What are the different types of materials and their properties?",
        "How does stress differ from strain in materials?",
        "What are the principles of machine design?",
        "How do different manufacturing processes work?",
        "What are the applications of finite element analysis?",
        "How do control systems work in mechanical systems?"
    ],
    "civil_engineering": [
        "What are the different types of structural loads?",
        "How do you design reinforced concrete structures?",
        "What are the principles of foundation design?",
        "How do you analyze structural frames and trusses?",
        "What are the properties of construction materials?",
        "How does soil mechanics affect foundation design?",
        "What are the principles of hydraulic engineering?",
        "How do you design transportation systems?",
        "What are seismic design considerations?",
        "How do you perform structural analysis?"
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
    ],
    "oop": [
        "What are the four fundamental principles of Object-Oriented Programming?",
        "How does inheritance promote code reusability?",
        "What is the difference between method overloading and overriding?",
        "How does encapsulation provide data security?",
        "What are abstract classes and when should you use them?",
        "How does polymorphism enable flexible code design?",
        "What is the difference between composition and inheritance?",
        "How do constructors and destructors work?",
        "What are design patterns in OOP?",
        "How do access modifiers control visibility in classes?"
    ],
    "os": [
        "What are the main functions of an operating system?",
        "How does process scheduling work in operating systems?",
        "What is the difference between processes and threads?",
        "How does virtual memory management work?",
        "What are deadlocks and how can they be prevented?",
        "How do semaphores and mutexes provide synchronization?",
        "What are the different file system structures?",
        "How does the boot process work in operating systems?",
        "What are system calls and how do they work?",
        "How does memory allocation work in operating systems?"
    ],
    "dbms": [
        "What are the ACID properties in database transactions?",
        "How do different types of database joins work?",
        "What is database normalization and its normal forms?",
        "How do database indexes improve query performance?",
        "What are the differences between SQL and NoSQL databases?",
        "How does concurrency control work in databases?",
        "What are stored procedures and their advantages?",
        "How does query optimization work in DBMS?",
        "What are the different types of database relationships?",
        "How do backup and recovery mechanisms work in databases?"
    ]
}

# Memory-optimized flashcards for active recall
DOMAIN_FLASHCARDS = {
    "computer_networks": [
        {"question": "💡 Quick Recall: OSI model has how many layers?", "answer": "7 layers (Physical, Data Link, Network, Transport, Session, Presentation, Application)", "difficulty": "easy", "category": "fundamentals"},
        {"question": "🔀 Compare: Hub vs Switch - which is smarter?", "answer": "Switch is smarter - it learns MAC addresses and sends data only to intended recipient. Hub broadcasts to all ports.", "difficulty": "medium", "category": "comparison"},
        {"question": "🎯 Definition: What does IP stand for and what does it do?", "answer": "Internet Protocol - provides addressing and routing to deliver packets across networks", "difficulty": "easy", "category": "definition"},
        {"question": "🔍 Process: How does DNS resolution work in 3 steps?", "answer": "1) Browser checks cache 2) Queries DNS server 3) DNS returns IP address for domain name", "difficulty": "medium", "category": "process"},
        {"question": "⚡ Quick Check: TCP vs UDP - which guarantees delivery?", "answer": "TCP (Transmission Control Protocol) guarantees delivery with error checking. UDP is faster but unreliable.", "difficulty": "easy", "category": "comparison"},
        {"question": "🧠 Think: Why do we need subnetting?", "answer": "To divide large networks into smaller segments for better performance, security, and efficient IP address usage", "difficulty": "hard", "category": "concept"},
        {"question": "📊 Layers: Name the bottom 3 layers of OSI model", "answer": "Physical (Layer 1), Data Link (Layer 2), Network (Layer 3)", "difficulty": "medium", "category": "recall"},
        {"question": "🔐 Security: What is a firewall's primary function?", "answer": "Controls incoming and outgoing network traffic based on predetermined security rules", "difficulty": "easy", "category": "definition"}
    ],
    "operating_systems": [
        {"question": "🔄 OS Functions: What are the 4 main functions of an OS?", "answer": "Process Management, Memory Management, File System Management, I/O Management", "difficulty": "easy", "category": "fundamentals"},
        {"question": "⚡ Process vs Thread: Key difference?", "answer": "Process = independent program with own memory. Thread = lightweight unit within process, shares memory", "difficulty": "medium", "category": "comparison"},
        {"question": "📊 CPU Scheduling: Name 3 common algorithms", "answer": "FCFS (First Come First Serve), SJF (Shortest Job First), Round Robin", "difficulty": "medium", "category": "algorithm"},
        {"question": "🔒 Deadlock: What are the 4 necessary conditions?", "answer": "Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait (Remember: MHNC)", "difficulty": "hard", "category": "concept"},
        {"question": "💾 Virtual Memory: What problem does it solve?", "answer": "Allows programs larger than physical RAM to run by using disk as extended memory", "difficulty": "medium", "category": "concept"},
        {"question": "🔄 Context Switch: What gets saved/restored?", "answer": "CPU registers, program counter, stack pointer, memory management info", "difficulty": "medium", "category": "process"},
        {"question": "🔐 Semaphore vs Mutex: When to use each?", "answer": "Semaphore for counting resources (n>1). Mutex for binary lock (only 1 resource)", "difficulty": "medium", "category": "synchronization"},
        {"question": "📁 File System: What does inode contain?", "answer": "File metadata: permissions, timestamps, size, disk block locations (not filename!)", "difficulty": "hard", "category": "filesystem"}
    ],
    "database": [
        {"question": "🔍 ACID Properties: What does each letter mean?", "answer": "Atomicity, Consistency, Isolation, Durability - ensures reliable database transactions", "difficulty": "medium", "category": "fundamentals"},
        {"question": "🔗 SQL Joins: INNER vs LEFT JOIN difference?", "answer": "INNER returns only matching rows. LEFT returns all left table rows + matches from right", "difficulty": "medium", "category": "query"},
        {"question": "📊 Primary vs Foreign Key: Purpose of each?", "answer": "Primary Key: Unique identifier for table row. Foreign Key: Links to primary key in another table", "difficulty": "easy", "category": "design"},
        {"question": "⚡ Database Index: How does it speed up queries?", "answer": "Creates sorted reference structure - like book index. O(log n) instead of O(n) search", "difficulty": "medium", "category": "performance"},
        {"question": "🏗️ Normalization: What is 3NF (Third Normal Form)?", "answer": "No transitive dependencies - non-key attributes depend only on primary key, not other non-key attributes", "difficulty": "hard", "category": "design"},
        {"question": "🔄 Transaction: What happens on ROLLBACK?", "answer": "Undoes all changes made in current transaction, returns database to previous consistent state", "difficulty": "medium", "category": "transaction"},
        {"question": "📈 SQL vs NoSQL: When to use NoSQL?", "answer": "Large scale, flexible schema, horizontal scaling needs. SQL for ACID compliance, complex relationships", "difficulty": "medium", "category": "comparison"},
        {"question": "🔍 SELECT Query: Basic syntax order?", "answer": "SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY", "difficulty": "easy", "category": "syntax"}
    ],
    "computer_science": [
        {"question": "⏱️ Time Complexity: O(n²) vs O(log n) - which is faster for large n?", "answer": "O(log n) is much faster! Example: For n=1000, O(log n)≈10 operations vs O(n²)=1,000,000 operations", "difficulty": "medium", "category": "complexity"},
        {"question": "🥞 Data Structure: Stack operations - what are the 2 main ones?", "answer": "PUSH (add to top) and POP (remove from top). Remember: Last In, First Out (LIFO)", "difficulty": "easy", "category": "fundamentals"},
        {"question": "🔄 Recursion Check: What are the 2 essential parts?", "answer": "1) Base case (stopping condition) 2) Recursive case (function calls itself with simpler input)", "difficulty": "medium", "category": "concept"},
        {"question": "🏗️ OOP Pillars: Name all 4 fundamental principles", "answer": "Encapsulation, Inheritance, Polymorphism, Abstraction (Remember: EIPA)", "difficulty": "hard", "category": "recall"},
        {"question": "⚡ Hash Table: Average time complexity for search/insert?", "answer": "O(1) - constant time! That's why hash tables are so fast for lookups", "difficulty": "medium", "category": "complexity"},
        {"question": "🌳 Tree Traversal: Inorder for BST gives what?", "answer": "Sorted order! Left → Root → Right visits nodes in ascending order", "difficulty": "medium", "category": "algorithm"},
        {"question": "🔍 Binary Search: What's the key requirement?", "answer": "Array must be SORTED first! Otherwise binary search won't work", "difficulty": "easy", "category": "prerequisite"},
        {"question": "💾 Memory: Stack vs Heap - where are local variables stored?", "answer": "Stack! Local variables, function calls on Stack. Dynamic allocation on Heap.", "difficulty": "medium", "category": "memory"}
    ],
    "software_engineering": [
        {"question": "🔄 SDLC Phases: Name the 6 main phases", "answer": "Requirements → Design → Implementation → Testing → Deployment → Maintenance", "difficulty": "medium", "category": "process"},
        {"question": "🏃 Agile vs Waterfall: Key difference?", "answer": "Agile: Iterative, flexible, customer collaboration. Waterfall: Sequential, fixed requirements, documentation heavy", "difficulty": "medium", "category": "methodology"},
        {"question": "🧪 Unit Testing: What should you test?", "answer": "Individual functions/methods in isolation. Test normal cases, edge cases, and error conditions", "difficulty": "medium", "category": "testing"},
        {"question": "🔀 Git: What does 'git merge' vs 'git rebase' do?", "answer": "Merge: Creates new commit combining branches. Rebase: Replays commits on target branch (cleaner history)", "difficulty": "hard", "category": "version_control"},
        {"question": "🏗️ Design Patterns: Name 3 common patterns", "answer": "Singleton (one instance), Observer (event notification), Factory (object creation)", "difficulty": "medium", "category": "design"},
        {"question": "📋 Requirements: What are functional vs non-functional?", "answer": "Functional: What system does (features). Non-functional: How system performs (speed, security, usability)", "difficulty": "medium", "category": "requirements"},
        {"question": "🔄 CI/CD: What does continuous integration do?", "answer": "Automatically builds, tests, and integrates code changes frequently to catch issues early", "difficulty": "medium", "category": "devops"},
        {"question": "🏢 Microservices vs Monolith: When to use microservices?", "answer": "Large teams, independent scaling needs, different tech stacks. Monolith for simple apps, small teams", "difficulty": "hard", "category": "architecture"}
    ],
    "electrical_engineering": [
        {"question": "⚡ Ohm's Law: What's the formula?", "answer": "V = I × R (Voltage = Current × Resistance). Power = V × I = I²R = V²/R", "difficulty": "easy", "category": "fundamentals"},
        {"question": "🔋 AC vs DC: Key differences?", "answer": "AC: Alternating current, changes direction periodically. DC: Direct current, flows in one direction", "difficulty": "easy", "category": "fundamentals"},
        {"question": "📊 Capacitor: What does it do in AC vs DC?", "answer": "DC: Blocks current after charging. AC: Allows current, reactance = 1/(2πfC)", "difficulty": "medium", "category": "components"},
        {"question": "🔧 Transistor: Two main functions?", "answer": "1) Switch (on/off for digital circuits) 2) Amplifier (increase signal strength)", "difficulty": "medium", "category": "components"},
        {"question": "🌊 Electromagnetic Induction: Faraday's Law?", "answer": "Changing magnetic field induces voltage. EMF = -N(dΦ/dt) where N=turns, Φ=magnetic flux", "difficulty": "hard", "category": "electromagnetics"},
        {"question": "🔄 Transformer: How does it change voltage?", "answer": "Uses mutual induction. Voltage ratio = turns ratio: V₂/V₁ = N₂/N₁", "difficulty": "medium", "category": "power"},
        {"question": "🎛️ Control System: What is feedback?", "answer": "Output signal fed back to input to automatically correct errors and maintain desired performance", "difficulty": "medium", "category": "control"},
        {"question": "📡 Signal Processing: Analog vs Digital signals?", "answer": "Analog: Continuous values. Digital: Discrete values (0s and 1s). Digital is noise-resistant", "difficulty": "easy", "category": "signals"}
    ],
    "mechanical_engineering": [
        {"question": "🌡️ Thermodynamics: What are the 4 laws?", "answer": "0th: Temperature equilibrium. 1st: Energy conservation. 2nd: Entropy increases. 3rd: Absolute zero entropy", "difficulty": "hard", "category": "fundamentals"},
        {"question": "🔥 Heat Transfer: Name the 3 modes", "answer": "Conduction (direct contact), Convection (fluid motion), Radiation (electromagnetic waves)", "difficulty": "medium", "category": "heat_transfer"},
        {"question": "💧 Fluid Mechanics: Bernoulli's Equation principle?", "answer": "Energy conservation in fluid flow: Pressure + Kinetic + Potential energy = constant", "difficulty": "medium", "category": "fluids"},
        {"question": "⚖️ Statics: Condition for equilibrium?", "answer": "ΣF = 0 (sum of forces = 0) and ΣM = 0 (sum of moments = 0)", "difficulty": "medium", "category": "mechanics"},
        {"question": "🔧 Stress vs Strain: What's the difference?", "answer": "Stress = Force/Area (N/m²). Strain = Change in length/Original length (dimensionless)", "difficulty": "medium", "category": "materials"},
        {"question": "⚙️ Machine Design: What is factor of safety?", "answer": "Ratio of material strength to expected maximum stress. Accounts for uncertainties and ensures safety", "difficulty": "medium", "category": "design"},
        {"question": "🏭 Manufacturing: CNC vs Conventional machining?", "answer": "CNC: Computer controlled, precise, automated. Conventional: Manual operation, operator skill dependent", "difficulty": "easy", "category": "manufacturing"},
        {"question": "📊 FEA: What does Finite Element Analysis do?", "answer": "Breaks complex geometry into small elements to solve engineering problems numerically", "difficulty": "medium", "category": "analysis"}
    ],
    "civil_engineering": [
        {"question": "🏗️ Structural Loads: Name the 3 main types", "answer": "Dead Load (permanent), Live Load (occupancy), Environmental Load (wind, earthquake, snow)", "difficulty": "medium", "category": "loads"},
        {"question": "🧱 Concrete: What is reinforced concrete?", "answer": "Concrete with steel bars/mesh. Concrete handles compression, steel handles tension", "difficulty": "easy", "category": "materials"},
        {"question": "🏛️ Foundation Types: Shallow vs Deep?", "answer": "Shallow: Spread footings, mat foundations. Deep: Piles, caissons when soil is weak", "difficulty": "medium", "category": "foundation"},
        {"question": "📐 Structural Analysis: What is a truss?", "answer": "Framework of triangular units connected at joints. Members carry only axial forces (tension/compression)", "difficulty": "medium", "category": "structures"},
        {"question": "🌍 Soil Mechanics: What is bearing capacity?", "answer": "Maximum pressure soil can support without shear failure. Critical for foundation design", "difficulty": "medium", "category": "geotechnical"},
        {"question": "💧 Hydraulics: Manning's Equation for?", "answer": "Calculates flow velocity in open channels and pipes based on roughness and slope", "difficulty": "hard", "category": "hydraulics"},
        {"question": "🛣️ Transportation: What is design speed?", "answer": "Maximum safe speed for road geometric design. Determines curve radius, sight distance, grades", "difficulty": "medium", "category": "transportation"},
        {"question": "🌊 Seismic Design: What is base isolation?", "answer": "Isolates building from ground motion using flexible bearings to reduce earthquake forces", "difficulty": "hard", "category": "earthquake"}
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
    ],
    "oop": [
        {"question": "🏗️ OOP Pillars: What are the 4 fundamental principles?", "answer": "Encapsulation, Inheritance, Polymorphism, Abstraction (Remember: EIPA)", "difficulty": "easy", "category": "fundamentals"},
        {"question": "🔒 Encapsulation: What does it achieve?", "answer": "Data hiding - bundles data and methods together, restricts direct access to internal details", "difficulty": "easy", "category": "concept"},
        {"question": "🧬 Inheritance: What is IS-A relationship?", "answer": "Child class inherits properties/methods from parent. Example: Dog IS-A Animal", "difficulty": "medium", "category": "concept"},
        {"question": "🎭 Polymorphism: Method Overriding vs Overloading?", "answer": "Overriding: Same signature, different implementation. Overloading: Same name, different parameters", "difficulty": "medium", "category": "comparison"},
        {"question": "🎯 Abstract Class vs Interface: Key difference?", "answer": "Abstract class can have concrete methods. Interface only has abstract methods (until Java 8)", "difficulty": "hard", "category": "comparison"},
        {"question": "🏗️ Constructor: What's its purpose?", "answer": "Special method called when object is created. Initializes object state and allocates memory", "difficulty": "easy", "category": "definition"},
        {"question": "👀 Access Modifiers: Public vs Private vs Protected?", "answer": "Public: accessible everywhere. Private: same class only. Protected: same package + subclasses", "difficulty": "medium", "category": "access_control"},
        {"question": "🔗 Composition vs Inheritance: When to use composition?", "answer": "Use composition for HAS-A relationships. More flexible than inheritance, avoids tight coupling", "difficulty": "hard", "category": "design"},
        {"question": "⚡ Static vs Instance: What's the difference?", "answer": "Static: belongs to class, shared by all objects. Instance: belongs to specific object", "difficulty": "medium", "category": "memory"},
        {"question": "🎨 Design Patterns: Name 3 common patterns", "answer": "Singleton (one instance), Factory (object creation), Observer (event notification)", "difficulty": "hard", "category": "patterns"}
    ],
    "os": [
        {"question": "🔄 OS Functions: What are the 4 main functions?", "answer": "Process Management, Memory Management, File System Management, I/O Management", "difficulty": "easy", "category": "fundamentals"},
        {"question": "⚡ Process vs Thread: Key differences?", "answer": "Process: independent program with own memory. Thread: lightweight unit within process, shares memory", "difficulty": "medium", "category": "comparison"},
        {"question": "📊 CPU Scheduling: Name 5 algorithms", "answer": "FCFS, SJF, Round Robin, Priority Scheduling, Multilevel Queue", "difficulty": "medium", "category": "scheduling"},
        {"question": "🔒 Deadlock: What are the 4 necessary conditions?", "answer": "Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait (Remember: MHNC)", "difficulty": "hard", "category": "deadlock"},
        {"question": "💾 Virtual Memory: What problem does it solve?", "answer": "Allows programs larger than physical RAM to run by using disk as extended memory", "difficulty": "medium", "category": "memory"},
        {"question": "🔄 Context Switch: What gets saved/restored?", "answer": "CPU registers, program counter, stack pointer, memory management info", "difficulty": "medium", "category": "process"},
        {"question": "🔐 Semaphore vs Mutex: When to use each?", "answer": "Semaphore: counting resources (n>1). Mutex: binary lock (only 1 resource)", "difficulty": "medium", "category": "synchronization"},
        {"question": "📁 File System: What does inode contain?", "answer": "File metadata: permissions, timestamps, size, disk block locations (not filename!)", "difficulty": "hard", "category": "filesystem"},
        {"question": "🏃 Race Condition: How to prevent it?", "answer": "Use synchronization mechanisms: mutex, semaphore, critical sections, atomic operations", "difficulty": "medium", "category": "synchronization"},
        {"question": "🔧 System Call vs Library Call: Difference?", "answer": "System call: kernel mode switch, OS service. Library call: user mode, no kernel involvement", "difficulty": "hard", "category": "system_calls"}
    ],
    "dbms": [
        {"question": "🔍 ACID Properties: What does each letter mean?", "answer": "Atomicity, Consistency, Isolation, Durability - ensures reliable database transactions", "difficulty": "medium", "category": "fundamentals"},
        {"question": "🔗 SQL Joins: INNER vs LEFT vs RIGHT vs FULL?", "answer": "INNER: matching rows only. LEFT: all left + matches. RIGHT: all right + matches. FULL: all rows", "difficulty": "medium", "category": "joins"},
        {"question": "📊 Normalization: What are the first 3 normal forms?", "answer": "1NF: atomic values. 2NF: no partial dependencies. 3NF: no transitive dependencies", "difficulty": "hard", "category": "normalization"},
        {"question": "⚡ Database Index: How does B-tree index work?", "answer": "Balanced tree structure. O(log n) search time. Keeps data sorted for range queries", "difficulty": "hard", "category": "indexing"},
        {"question": "🔄 Transaction: What happens on COMMIT vs ROLLBACK?", "answer": "COMMIT: makes changes permanent. ROLLBACK: undoes all changes, returns to previous state", "difficulty": "medium", "category": "transactions"},
        {"question": "🔒 Concurrency Control: 2PL vs Timestamp ordering?", "answer": "2PL: two-phase locking (acquire all locks, then release). Timestamp: order transactions by timestamps", "difficulty": "hard", "category": "concurrency"},
        {"question": "📈 SQL vs NoSQL: When to choose NoSQL?", "answer": "Large scale, flexible schema, horizontal scaling, eventual consistency acceptable", "difficulty": "medium", "category": "database_types"},
        {"question": "🏗️ ER Model: Entity vs Attribute vs Relationship?", "answer": "Entity: real-world object. Attribute: property of entity. Relationship: association between entities", "difficulty": "easy", "category": "modeling"},
        {"question": "⚙️ Query Optimization: How does cost-based optimizer work?", "answer": "Estimates cost of different execution plans, chooses plan with lowest estimated cost", "difficulty": "hard", "category": "optimization"},
        {"question": "💾 Backup Types: Full vs Incremental vs Differential?", "answer": "Full: complete backup. Incremental: changes since last backup. Differential: changes since last full backup", "difficulty": "medium", "category": "backup"}
    ]
}