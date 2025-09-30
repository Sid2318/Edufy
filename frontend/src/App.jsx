import React, { useState } from "react";
import Upload from "./components/Upload";
import Query from "./components/query";
import ErrorBoundary from "./components/ErrorBoundary";
import ConnectionStatus from "./components/ConnectionStatus";
import Tutorial from "./components/Tutorial";
import DocumentManager from "./components/DocumentManager";
import SampleQuestions from "./components/SampleQuestions";
import "./style.css";

function App() {
  const [selectedQuestion, setSelectedQuestion] = useState("");

  const handleSampleQuestionClick = (question) => {
    setSelectedQuestion(question);
    // Scroll to query section
    document.querySelector(".query-section")?.scrollIntoView({
      behavior: "smooth",
    });
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          <header className="text-center mb-8">
            <h1 className="text-5xl font-bold text-gray-800 mb-4">🎓 Edufy</h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-6">
              Your AI-powered study companion. Upload documents and ask
              intelligent questions to enhance your learning experience.
            </p>
            <ConnectionStatus />
          </header>

          <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6 fade-in">
              <Upload />
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6 fade-in query-section">
              <Query
                selectedQuestion={selectedQuestion}
                onQuestionChange={setSelectedQuestion}
              />
            </div>
          </div>

          <div className="max-w-6xl mx-auto">
            <SampleQuestions onQuestionClick={handleSampleQuestionClick} />
          </div>

          <footer className="text-center mt-12 text-gray-500">
            <p>Powered by FastAPI + React + LangChain</p>
            <div className="mt-2 text-sm">
              <span className="inline-block bg-gray-200 rounded-full px-3 py-1 mx-1">
                RAG
              </span>
              <span className="inline-block bg-gray-200 rounded-full px-3 py-1 mx-1">
                Vector DB
              </span>
              <span className="inline-block bg-gray-200 rounded-full px-3 py-1 mx-1">
                AI Search
              </span>
            </div>
          </footer>
        </div>

        {/* Floating Action Buttons */}
        <Tutorial />
        <DocumentManager />
      </div>
    </ErrorBoundary>
  );
}

export default App;
