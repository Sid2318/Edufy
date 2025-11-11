import React, { useState, useRef, useEffect } from "react";
import { getStatus } from "../api";
import axios from "axios";
import FlashcardViewer from "./FlashcardViewer";

const FlashcardButton = ({
  onFlashcardsGenerated,
  isActive,
  onOpen,
  onClose,
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [flashcards, setFlashcards] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");
  const [statusType, setStatusType] = useState("info"); // info | error | success
  const statusRef = useRef(null);

  useEffect(() => {
    if (statusMessage && statusRef.current) {
      // Move focus to status for screen readers when message changes
      statusRef.current.focus();
    }
  }, [statusMessage]);

  const generateFlashcards = async () => {
    setIsGenerating(true);
    setStatusType("info");
    setStatusMessage("Checking documents and generating flashcards...");
    try {
      // Check if documents are available
      const statusResponse = await getStatus();
      if (
        !statusResponse.database_ready ||
        statusResponse.documents.length === 0
      ) {
        setStatusType("error");
        setStatusMessage(
          "Please upload a document first to generate flashcards."
        );
        setIsGenerating(false);
        return;
      }

      // Call the real flashcards API
      const response = await axios.get("http://127.0.0.1:8000/flashcards");

      if (response.data.error) {
        setStatusType("error");
        setStatusMessage(response.data.error);
        setIsGenerating(false);
        return;
      }

      const generatedFlashcards = response.data.flashcards || [];

      if (generatedFlashcards.length === 0) {
        setStatusType("error");
        setStatusMessage(
          "No flashcards could be generated from the current document. Try a document with more structured content."
        );
        setIsGenerating(false);
        return;
      }

      setFlashcards(generatedFlashcards);
      setStatusType("success");
      setStatusMessage(`Generated ${generatedFlashcards.length} flashcards.`);
      onOpen(); // Notify parent component to show flashcards
      if (onFlashcardsGenerated) {
        onFlashcardsGenerated(generatedFlashcards);
      }
    } catch (error) {
      console.error("Error generating flashcards:", error);
      setStatusType("error");
      setStatusMessage(
        "Failed to generate flashcards. Please ensure a document is uploaded and try again."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCloseFlashcards = () => {
    onClose(); // Notify parent component
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Main Flashcard Interface */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        {/* Header Section */}
        <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg
                  className="w-4 h-4 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  Flashcard Generator
                </h2>
                <p className="text-sm text-gray-600">
                  Create interactive study cards from your documents
                </p>
              </div>
            </div>
            {isActive && (
              <button
                onClick={handleCloseFlashcards}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors duration-200"
                title="Close Flashcard Interface"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
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
              <div className="w-16 h-16 bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Ready to Study?
              </h3>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Transform your documents into interactive flashcards with
                AI-generated questions and answers.
              </p>
              <button
                onClick={generateFlashcards}
                disabled={isGenerating}
                className={`inline-flex items-center px-6 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isGenerating
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-purple-600 text-white hover:bg-purple-700 shadow-sm hover:shadow-md"
                }`}
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-gray-400 mr-2"></div>
                    Generating Flashcards...
                  </>
                ) : (
                  <>
                    <svg
                      className="w-4 h-4 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                      />
                    </svg>
                    Generate Flashcards
                  </>
                )}
              </button>

              {/* Status Message */}
              {statusMessage && (
                <div
                  role="status"
                  aria-live={statusType === "error" ? "assertive" : "polite"}
                  aria-atomic="true"
                  tabIndex={-1}
                  ref={statusRef}
                  className={`mt-4 mx-auto max-w-md rounded-xl px-4 py-3 text-sm ${
                    statusType === "error"
                      ? "bg-red-50 text-red-800 border border-red-200"
                      : statusType === "success"
                      ? "bg-green-50 text-green-800 border border-green-200"
                      : "bg-blue-50 text-blue-800 border border-blue-200"
                  }`}
                >
                  {statusMessage}
                </div>
              )}

              {/* Features List */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                <div className="flex items-center justify-center p-3 bg-gray-50 rounded-xl">
                  <div className="flex items-center text-gray-600">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    <span className="font-medium">AI-Generated</span>
                  </div>
                </div>
                <div className="flex items-center justify-center p-3 bg-gray-50 rounded-xl">
                  <div className="flex items-center text-gray-600">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                    <span className="font-medium">Interactive Cards</span>
                  </div>
                </div>
                <div className="flex items-center justify-center p-3 bg-gray-50 rounded-xl">
                  <div className="flex items-center text-gray-600">
                    <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
                    <span className="font-medium">Smart Navigation</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            /* Active State - Show Flashcard Interface */
            <div className="fade-in">
              <FlashcardViewer flashcards={flashcards} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlashcardButton;
