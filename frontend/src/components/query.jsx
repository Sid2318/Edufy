import React, { useState, useEffect } from "react";
import { askQuestion } from "../api";

const Query = ({ selectedQuestion, onQuestionChange }) => {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState([]);
  const [aiResponse, setAiResponse] = useState("");
  const [queryMetadata, setQueryMetadata] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [showSources, setShowSources] = useState(false);

  // Handle selected question from sample questions
  useEffect(() => {
    if (selectedQuestion && selectedQuestion !== question) {
      setQuestion(selectedQuestion);
      // Clear the selected question after setting it
      onQuestionChange("");
    }
  }, [selectedQuestion, question, onQuestionChange]);

  const handleAsk = async () => {
    if (!question.trim()) {
      alert("Please enter a question!");
      return;
    }

    setIsLoading(true);
    setHasSearched(true);
    setShowSources(false); // Reset sources dropdown for new query

    try {
      const res = await askQuestion(question);
      setAnswers(res.answers || []);
      setAiResponse(res.ai_response || "");
      setQueryMetadata({
        queryType: res.query_type || "general",
        kUsed: res.k_used || 0,
        totalSections: res.total_sections || 0,
      });
    } catch (err) {
      console.error(err);
      setAnswers([]);
      setAiResponse("");
      setQueryMetadata({});
      alert(
        "Failed to get answers. Make sure you've uploaded documents first!"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          🤖 Ask Questions
        </h2>
        <p className="text-gray-600">
          Ask anything about your uploaded documents
        </p>
      </div>

      <div className="space-y-4">
        <div className="relative">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="What would you like to know about your documents? (Press Enter to search)"
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows="3"
          />
          {question && (
            <button
              onClick={() => setQuestion("")}
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 text-xl"
              title="Clear question"
            >
              ×
            </button>
          )}
        </div>

        <button
          onClick={handleAsk}
          disabled={!question.trim() || isLoading}
          className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
            !question.trim() || isLoading
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-green-600 text-white hover:bg-green-700 transform hover:scale-105"
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Searching...
            </span>
          ) : (
            "🔍 Ask Question"
          )}
        </button>
      </div>

      {hasSearched && (
        <div className="space-y-6">
          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-pulse">
                <div className="text-gray-500">
                  🤖 AI is analyzing your documents...
                </div>
              </div>
            </div>
          ) : aiResponse || answers.length > 0 ? (
            <div className="space-y-6">
              {/* Query Analysis Metadata */}
              {queryMetadata.queryType && (
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-4">
                      <span className="text-gray-600">
                        🔍 Query Type:
                        <span className="ml-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                          {queryMetadata.queryType}
                        </span>
                      </span>
                      <span className="text-gray-600">
                        📊 Retrieved:
                        <span className="ml-1 px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                          {queryMetadata.kUsed} sections
                        </span>
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      Smart retrieval system
                    </div>
                  </div>
                </div>
              )}

              {/* AI Generated Response */}
              {aiResponse && (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
                  <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center">
                    🤖 AI Response
                    {queryMetadata.queryType && (
                      <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                        {queryMetadata.queryType}
                      </span>
                    )}
                  </h3>
                  <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {aiResponse}
                  </div>
                </div>
              )}

              {/* Source Documents */}
              {answers.length > 0 && (
                <div>
                  <button
                    onClick={() => setShowSources(!showSources)}
                    className="w-full text-left p-4 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors duration-200"
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm mr-3">
                          {answers.length}
                        </span>
                        📚 Source Document{answers.length > 1 ? "s" : ""}
                      </h3>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500">
                          {showSources ? "Hide" : "Show"} sources
                        </span>
                        <svg
                          className={`w-5 h-5 text-gray-500 transition-transform duration-200 ${
                            showSources ? "rotate-180" : ""
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 9l-7 7-7-7"
                          />
                        </svg>
                      </div>
                    </div>
                  </button>
                  
                  {/* Collapsible Content */}
                  {showSources && (
                    <div className="mt-4 fade-in">
                      <div className="space-y-4">
                        {answers.map((ans, idx) => (
                          <div
                            key={idx}
                            className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200"
                          >
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex items-center text-sm text-gray-500">
                                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                                  📄 {ans.source}
                                </span>
                                <span className="ml-2 text-xs text-gray-400">
                                  Section {idx + 1}
                                </span>
                              </div>
                            </div>
                            <p className="text-gray-700 leading-relaxed text-sm">
                              {ans.content}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="text-yellow-600">
                <div className="text-2xl mb-2">🤔</div>
                <div>No relevant information found.</div>
                <div className="text-sm mt-2">
                  Try rephrasing your question or upload more documents.
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Query;
