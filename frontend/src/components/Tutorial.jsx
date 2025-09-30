import React, { useState } from "react";

const Tutorial = () => {
  const [isOpen, setIsOpen] = useState(false);

  const steps = [
    {
      icon: "📚",
      title: "Upload Documents",
      description:
        "Click the upload area and select your study materials (PDF or TXT files). The system will automatically process and index them.",
    },
    {
      icon: "🤖",
      title: "Ask Questions",
      description:
        "Type any question about your uploaded documents. Use natural language - ask about concepts, definitions, examples, or anything you want to learn.",
    },
    {
      icon: "🔍",
      title: "Get Smart Answers",
      description:
        "The AI will search through your documents and provide relevant answers with source references, helping you study more effectively.",
    },
    {
      icon: "📖",
      title: "Study Efficiently",
      description:
        "Use the answers to review key concepts, create study notes, or prepare for exams. The more documents you upload, the smarter it gets!",
    },
  ];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all hover:scale-105 z-50"
        title="How to use Edufy"
      >
        <span className="text-xl">❓</span>
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  🚀 How to Use Edufy
                </h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-6">
                {steps.map((step, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                        {step.icon}
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-800 mb-2">
                        {index + 1}. {step.title}
                      </h3>
                      <p className="text-gray-600 leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <h4 className="font-semibold text-yellow-800 mb-2">
                  💡 Pro Tips:
                </h4>
                <ul className="text-yellow-700 text-sm space-y-1">
                  <li>• Ask specific questions for better results</li>
                  <li>
                    • Upload multiple related documents for comprehensive
                    answers
                  </li>
                  <li>
                    • Try different phrasings if you don't get the answer you
                    need
                  </li>
                  <li>
                    • The system works best with well-structured documents
                  </li>
                </ul>
              </div>

              <div className="mt-6 text-center">
                <button
                  onClick={() => setIsOpen(false)}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Got it! Let's start learning
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tutorial;
