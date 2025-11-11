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
      {/* Input Section */}
      <div className="space-y-4">
        <div className="relative">
          <div className="relative">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask anything about your documents..."
              className="w-full p-4 pr-12 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none bg-gray-50 focus:bg-white transition-all duration-200 text-gray-900 placeholder-gray-500"
              rows="3"
            />
            {question && (
              <button
                onClick={() => setQuestion("")}
                className="absolute top-3 right-3 p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors duration-200"
                title="Clear question"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        <button
          onClick={handleAsk}
          disabled={!question.trim() || isLoading}
          className={`w-full py-3 px-6 rounded-xl font-medium text-sm transition-all duration-200 ${
            !question.trim() || isLoading
              ? "bg-gray-100 text-gray-400 cursor-not-allowed"
              : "bg-blue-600 text-white hover:bg-blue-700 shadow-sm hover:shadow-md"
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
              Analyzing...
            </span>
          ) : (
            <span className="flex items-center justify-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Ask Question
            </span>
          )}
        </button>
      </div>

      {hasSearched && (
        <div className="space-y-6">
          {isLoading ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-200 border-t-blue-600"></div>
              </div>
              <div className="text-gray-600 font-medium">AI is analyzing your documents...</div>
              <div className="text-sm text-gray-500 mt-1">This may take a few moments</div>
            </div>
          ) : aiResponse || answers.length > 0 ? (
            <div className="space-y-6">
              {/* Query Analysis Metadata */}
              {queryMetadata.queryType && (
                <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span className="text-gray-600 font-medium">Query Type:</span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-medium">
                          {queryMetadata.queryType}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-gray-600 font-medium">Retrieved:</span>
                        <span className="px-2 py-1 bg-green-100 text-green-700 rounded-lg text-xs font-medium">
                          {queryMetadata.kUsed} sections
                        </span>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500 font-medium">
                      Smart retrieval system
                    </div>
                  </div>
                </div>
              )}

              {/* AI Generated Response */}
              {aiResponse && (
                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">AI Response</h3>
                      {queryMetadata.queryType && (
                        <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-medium mt-1">
                          {queryMetadata.queryType}
                        </span>
                      )}
                    </div>
                  </div>
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
                    className="w-full text-left p-4 bg-gray-50 hover:bg-gray-100 rounded-xl border border-gray-200 transition-colors duration-200"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                          </svg>
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Source Documents</h3>
                          <p className="text-sm text-gray-600">{answers.length} document{answers.length > 1 ? "s" : ""} found</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500 font-medium">
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
                      <div className="space-y-3">
                        {answers.map((ans, idx) => (
                          <div
                            key={idx}
                            className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200"
                          >
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex items-center space-x-2">
                                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-medium">
                                  {ans.source}
                                </span>
                                <span className="text-xs text-gray-500 font-medium">
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
            <div className="text-center py-12 bg-amber-50 rounded-xl border border-amber-200">
              <div className="w-12 h-12 bg-gradient-to-br from-amber-100 to-orange-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="text-amber-800 font-semibold mb-2">No relevant information found</div>
              <div className="text-sm text-amber-700">
                Try rephrasing your question or upload more documents.
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Query;
