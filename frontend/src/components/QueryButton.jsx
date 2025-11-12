import React, { useState, useEffect } from "react";
import { getStatus } from "../api";
import Query from "./query";

const QueryButton = ({
  selectedQuestion,
  onQuestionChange,
  isActive,
  onOpen,
  onClose,
}) => {
  const [isChecking, setIsChecking] = useState(false);

  // Auto-open query interface when a sample question is selected
  useEffect(() => {
    if (selectedQuestion && selectedQuestion.trim()) {
      handleOpenQuery();
    }
  }, [selectedQuestion]);

  const handleOpenQuery = async () => {
    setIsChecking(true);
    try {
      // Check if documents are available
      const statusResponse = await getStatus();
      if (
        !statusResponse.database_ready ||
        statusResponse.documents.length === 0
      ) {
        alert("Please upload a document first to ask questions!");
        setIsChecking(false);
        return;
      }

      onOpen(); // Notify parent component
    } catch (error) {
      console.error("Error checking status:", error);
      alert(
        "Failed to check document status. Please make sure documents are uploaded."
      );
    } finally {
      setIsChecking(false);
    }
  };

  const handleCloseQuery = () => {
    onClose(); // Notify parent component
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Main Query Interface */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        {/* Header Section */}
        <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">AI Question Assistant</h2>
                <p className="text-sm text-gray-600">Ask intelligent questions about your documents</p>
              </div>
            </div>
            {isActive && (
              <button
                onClick={handleCloseQuery}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors duration-200"
                title="Close Query Interface"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Content Section */}
        <div className="p-6">
          {!isActive ? (
            /* Initial State - Show Action Button */
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Learn?</h3>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Start asking questions about your uploaded documents and get intelligent AI-powered answers.
              </p>
              <button
                onClick={handleOpenQuery}
                disabled={isChecking}
                className={`inline-flex items-center px-6 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isChecking
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-blue-600 text-white hover:bg-blue-700 shadow-sm hover:shadow-md"
                }`}
              >
                {isChecking ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-gray-400 mr-2"></div>
                    Checking Documents...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                    Start Asking Questions
                  </>
                )}
              </button>
            </div>
          ) : (
            /* Active State - Show Query Interface */
            <div className="fade-in">
              <Query
                selectedQuestion={selectedQuestion || ""}
                onQuestionChange={onQuestionChange || (() => {})}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QueryButton;
