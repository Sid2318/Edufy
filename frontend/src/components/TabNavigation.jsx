import React, { useState, useEffect } from "react";
import Query from "./query";
import FlashcardViewer from "./FlashcardViewer";
import { getStatus } from "../api";
import axios from "axios";

const TabNavigation = ({ selectedQuestion, onQuestionChange }) => {
  const [activeTab, setActiveTab] = useState("query");
  const [isGenerating, setIsGenerating] = useState(false);
  const [flashcards, setFlashcards] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");
  const [statusType, setStatusType] = useState("info");

  // Switch to query tab when a sample question is selected
  useEffect(() => {
    if (selectedQuestion && selectedQuestion.trim()) {
      setActiveTab("query");
    }
  }, [selectedQuestion]);

  // ===== FLASHCARD GENERATION LOGIC =====
  /**
   * Generate flashcards from uploaded documents
   * Process: Check document availability → Call API → Handle response
   */
  const generateFlashcards = async () => {
    // Set loading state and initial status
    setIsGenerating(true);
    setStatusType("info");
    setStatusMessage("Checking documents and generating flashcards...");

    try {
      // STEP 1: Verify documents are uploaded and database is ready
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

      // STEP 2: Call backend API to generate flashcards
      const response = await axios.get("http://127.0.0.1:8000/flashcards");

      // Handle API errors
      if (response.data.error) {
        setStatusType("error");
        setStatusMessage(response.data.error);
        setIsGenerating(false);
        return;
      }

      // STEP 3: Process the generated flashcards
      const generatedFlashcards = response.data.flashcards || [];

      // Validate that flashcards were actually generated
      if (generatedFlashcards.length === 0) {
        setStatusType("error");
        setStatusMessage(
          "No flashcards could be generated from the current document. Try a document with more structured content."
        );
        setIsGenerating(false);
        return;
      }

      // STEP 4: Success - Update state with generated flashcards
      setFlashcards(generatedFlashcards);
      setStatusType("success");
      setStatusMessage(
        `Generated ${generatedFlashcards.length} flashcards successfully!`
      );
    } catch (error) {
      // Handle network or other errors
      console.error("Error generating flashcards:", error);
      setStatusType("error");
      setStatusMessage(
        "Failed to generate flashcards. Please ensure a document is uploaded and try again."
      );
    } finally {
      // Always reset loading state
      setIsGenerating(false);
    }
  };

  // ===== TAB SWITCHING LOGIC =====
  /**
   * Handle tab switching between Query and Flashcard modes
   * Auto-generates flashcards when switching to flashcard tab for the first time
   */
  const handleTabClick = (tab) => {
    setActiveTab(tab);

    // Smart flashcard generation: Only generate if switching to flashcard tab,
    // no flashcards exist yet, and not currently generating
    if (tab === "flashcard" && flashcards.length === 0 && !isGenerating) {
      // Small delay to allow UI to update before starting generation
      setTimeout(() => generateFlashcards(), 100);
    }
  };

  // ===== RENDER COMPONENT =====
  return (
    <div>
      <div className="h-full flex flex-col bg-white">
        {/* ===== MODERN TAB NAVIGATION HEADER ===== */}
        <div className="bg-gradient-to-r from-slate-50 to-gray-50 border-b border-gray-200 backdrop-blur-sm ">
          <div className="flex relative">
            {/* QUERY TAB BUTTON */}
            <button
              onClick={() => handleTabClick("query")}
              className={`flex-2 relative px-6 py-1 text-xl font-semibold transition-all duration-300 group ${
                activeTab === "query"
                  ? "text-emerald-700 bg-white border-b-3 border-emerald-500 shadow-sm"
                  : "text-gray-600 hover:text-emerald-600 hover:bg-white/60"
              }`}
            >
              <div className="flex items-center justify-center space-x-3">
                <div
                  className={`p-2 rounded-xl transition-all duration-300 ${
                    activeTab === "query"
                      ? "bg-emerald-100 text-emerald-600 shadow-sm scale-110"
                      : "bg-gray-100 text-gray-500 group-hover:bg-emerald-50 group-hover:text-emerald-500"
                  }`}
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
                      strokeWidth={2.5}
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                    />
                  </svg>
                </div>
                <span className="font-bold tracking-wide">Ask Questions</span>
                {activeTab === "query" && (
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                )}
              </div>
            </button>

            {/* FLASHCARD TAB BUTTON */}
            <button
              onClick={() => handleTabClick("flashcard")}
              className={`flex-2 relative px-6 py-1 text-xl font-semibold transition-all duration-300 group ${
                activeTab === "flashcard"
                  ? "text-violet-700 bg-white border-b-3 border-violet-500 shadow-sm"
                  : "text-gray-600 hover:text-violet-600 hover:bg-white/60"
              }`}
            >
              <div className="flex items-center justify-center space-x-3">
                <div
                  className={`p-2 rounded-xl transition-all duration-300 ${
                    activeTab === "flashcard"
                      ? "bg-violet-100 text-violet-600 shadow-sm scale-110"
                      : "bg-gray-100 text-gray-500 group-hover:bg-violet-50 group-hover:text-violet-500"
                  }`}
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
                      strokeWidth={2.5}
                      d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                    />
                  </svg>
                </div>
                <span className="font-bold tracking-wide">Flashcards</span>
              </div>
            </button>
          </div>
        </div>
      </div>
      <div>
        {/* ===== TAB CONTENT AREA ===== */}
        {/* Dynamic content area that changes based on active tab */}
        <div className="flex-1 bg-white overflow-hidden">
          {/* QUERY TAB CONTENT */}
          {activeTab === "query" && (
            <div className="h-full py-1 px-3">
              {/* Render the Query component with selected question and change handler */}
              <Query
                selectedQuestion={selectedQuestion || ""}
                onQuestionChange={onQuestionChange || (() => {})}
              />
            </div>
          )}

          {/* FLASHCARD TAB CONTENT */}
          {activeTab === "flashcard" && (
            <div className="h-full">
              {/* ENHANCED LOADING STATE */}
              {isGenerating ? (
                <div className="h-full flex items-center justify-center bg-gradient-to-br from-violet-50 via-indigo-50 to-purple-50">
                  <div className="text-center p-12 max-w-lg">
                    <div className="relative mb-10">
                      <div className="w-24 h-24 mx-auto relative">
                        <div className="animate-spin rounded-full h-24 w-24 border-4 border-violet-200"></div>
                        <div className="animate-ping absolute inset-4 rounded-full bg-violet-300 opacity-75"></div>
                        <div className="absolute inset-6 rounded-full bg-gradient-to-br from-violet-400 to-purple-500 flex items-center justify-center">
                          <svg
                            className="w-6 h-6 text-white animate-bounce"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2.5}
                              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                            />
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-6">
                      <div className="space-y-3">
                        <h3 className="text-3xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
                          AI Magic in Progress
                        </h3>
                        <p className="text-lg text-gray-700 leading-relaxed">
                          🧠 Analyzing your document with advanced AI
                          <br />
                          ✨ Creating personalized study flashcards
                          <br />
                          🎯 Optimizing for effective learning
                        </p>
                      </div>
                      <div className="flex items-center justify-center space-x-3 text-violet-600">
                        <div className="flex space-x-1">
                          <div
                            className="w-2 h-2 bg-violet-400 rounded-full animate-bounce"
                            style={{ animationDelay: "0ms" }}
                          ></div>
                          <div
                            className="w-2 h-2 bg-violet-500 rounded-full animate-bounce"
                            style={{ animationDelay: "150ms" }}
                          ></div>
                          <div
                            className="w-2 h-2 bg-violet-600 rounded-full animate-bounce"
                            style={{ animationDelay: "300ms" }}
                          ></div>
                        </div>
                        <span className="font-medium">
                          Processing your content
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : flashcards.length > 0 ? (
                // ENHANCED FLASHCARDS DISPLAY
                <div className="h-full bg-gray-50">
                  <div className="p-4 bg-white border-b border-gray-100">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Study Flashcards
                      </h3>
                      <span className="text-sm text-gray-500">
                        {flashcards.length} cards
                      </span>
                    </div>
                  </div>
                  <div className="h-full pb-4">
                    <FlashcardViewer flashcards={flashcards} />
                  </div>
                </div>
              ) : (
                // EMPTY STATE - Professional design
                <div className="h-full flex items-center justify-center bg-gray-50">
                  <div className="text-center max-w-lg p-12">
                    <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-8 shadow-sm">
                      <svg
                        className="w-10 h-10 text-purple-600"
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

                    <div className="space-y-6">
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-3">
                          Create Study Flashcards
                        </h3>
                        <p className="text-gray-600 leading-relaxed">
                          Transform your uploaded documents into interactive
                          flashcards for effective studying. Perfect for
                          memorizing key concepts, definitions, and important
                          information.
                        </p>
                      </div>

                      <button
                        onClick={generateFlashcards}
                        disabled={isGenerating}
                        className="inline-flex items-center px-8 py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                      >
                        <svg
                          className="w-5 h-5 mr-2"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 10V3L4 14h7v7l9-11h-7z"
                          />
                        </svg>
                        Generate Flashcards
                      </button>

                      {/* STATUS MESSAGE DISPLAY */}
                      {statusMessage && (
                        <div
                          className={`p-4 rounded-xl text-sm font-medium ${
                            statusType === "error"
                              ? "bg-red-50 text-red-700 border border-red-100"
                              : statusType === "success"
                              ? "bg-green-50 text-green-700 border border-green-100"
                              : "bg-blue-50 text-blue-700 border border-blue-100"
                          }`}
                        >
                          {statusMessage}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TabNavigation;
