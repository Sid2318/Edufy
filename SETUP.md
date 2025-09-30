# 📋 Development Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Sid2318/Edufy.git
cd Edufy
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:5174
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Usage

1. Upload a PDF or TXT document
2. Ask questions about your document
3. Get AI-powered answers with source references

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
