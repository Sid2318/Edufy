import React, { useState } from "react";
import Upload from "./components/Upload";
import TabNavigation from "./components/TabNavigation";
import ErrorBoundary from "./components/ErrorBoundary";
import ConnectionStatus from "./components/ConnectionStatus";
import Tutorial from "./components/Tutorial";
import DocumentManager from "./components/DocumentManager";
import SampleQuestions from "./components/SampleQuestions";


function App() {
  const [selectedQuestion, setSelectedQuestion] = useState("");

  const handleSampleQuestionClick = (question) => {
    setSelectedQuestion(question);
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-slate-100">
        {/* Header */}
        <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-40">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl flex items-center justify-center">
                  <span className="text-xl font-bold text-white">E</span>
                </div>
                <div>
                  <h1 className="text-4xl font-bold text-gray-900">Edufy</h1>
                  <p className="text-sm text-gray-600">
                    AI-powered study companion
                  </p>
                </div>
              </div>
              <ConnectionStatus />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="container mx-auto px-6 py-8">
          <div className="grid lg:grid-cols-[3fr_7fr] gap-8 min-h-[calc(100vh-220px)]">
            {/* Left Column - Upload & Sample Questions */}
            <div className="flex flex-col space-y-6 h-full">
              {/* Upload Document */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                <Upload />
              </div>

            {/* Right Column - Tabbed Interface */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden h-full w-full">
              <TabNavigation
                selectedQuestion={selectedQuestion}
                onQuestionChange={setSelectedQuestion}
              />
            </div>
          </div>
        </div>

        {/* Sample Questions Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex-1 overflow-hidden">
                <div className="h-full overflow-y-auto">
                  <SampleQuestions
                    onQuestionClick={handleSampleQuestionClick}
                  />
                </div>
              </div>
            </div>

        {/* Footer */}
        <footer className="bg-white/80 backdrop-blur-sm border-t border-gray-200 mt-auto">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-center space-x-6 text-sm text-gray-500">
              <span>Powered by FastAPI + React + LangChain</span>
              <div className="flex space-x-2">
                <span className="bg-gray-100 rounded-full px-3 py-1">RAG</span>
                <span className="bg-gray-100 rounded-full px-3 py-1">
                  Vector DB
                </span>
                <span className="bg-gray-100 rounded-full px-3 py-1">
                  AI Search
                </span>
              </div>
            </div>
          </div>
        </footer>

        {/* Floating Action Buttons */}
        <Tutorial />
        <DocumentManager />
      </div>
    </ErrorBoundary>
  );
}

export default App;
