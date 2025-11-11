import React, { useState } from "react";

const FlashcardViewer = ({ flashcards }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  if (!flashcards || flashcards.length === 0) {
    return null;
  }

  const currentCard = flashcards[currentIndex];

  // Safety check
  if (!currentCard) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-red-600">
          <p>Error: Flashcard data not found</p>
          <p className="text-sm">
            Index: {currentIndex}, Total: {flashcards.length}
          </p>
        </div>
      </div>
    );
  }

  // // Debug logging
  // console.log("FlashcardViewer - flashcards:", flashcards);
  // console.log("FlashcardViewer - currentIndex:", currentIndex);
  // console.log("FlashcardViewer - currentCard:", currentCard);

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % flashcards.length);
    setIsFlipped(false); // Reset flip state for new card
  };

  const handlePrevious = () => {
    setCurrentIndex(
      (prev) => (prev - 1 + flashcards.length) % flashcards.length
    );
    setIsFlipped(false); // Reset flip state for new card
  };

  return (
    <div className="flex flex-col h-full p-6">
      {/* Card counter */}
      <div className="text-center text-sm text-gray-600 mb-6">
        Card {currentIndex + 1} of {flashcards.length}
      </div>

      {/* Flashcard container */}
      <div className="flex-1 flex items-center justify-center">
        <div className="flex items-center gap-4 w-full max-w-4xl">
          {/* Previous Button */}
          <button
            onClick={handlePrevious}
            className="flex-shrink-0 p-3 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors shadow-sm"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>

          {/* Flashcard */}
          <div className="flex-1 max-w-2xl mx-4">
            <div className="w-full h-80 cursor-pointer perspective-1000" onClick={handleFlip}>
              <div
                className={`relative w-full h-full transition-transform duration-700 ease-in-out preserve-3d ${
                  isFlipped ? "rotate-y-180" : ""
                }`}
              >
                {/* Question Side */}
                <div className="absolute inset-0 w-full h-full backface-hidden">
                  <div className="w-full h-full bg-gradient-to-br from-indigo-50 to-blue-100 border-2 border-indigo-300 rounded-xl p-6 flex flex-col justify-center items-center text-center shadow-lg">
                    <div className="text-sm text-indigo-700 font-bold mb-6 uppercase tracking-wide bg-indigo-200 px-4 py-2 rounded-full">
                      📝 Question
                    </div>
                    <div className="text-lg text-gray-900 leading-relaxed mb-8 overflow-y-auto max-h-40 font-medium px-4">
                      {currentCard?.question ||
                        currentCard?.Question ||
                        "Loading question..."}
                    </div>
                    <div className="text-sm text-indigo-600 font-semibold animate-pulse">
                      👆 Click to reveal answer
                    </div>
                  </div>
                </div>

                {/* Answer Side */}
                <div className="absolute inset-0 w-full h-full backface-hidden rotate-y-180">
                  <div className="w-full h-full bg-gradient-to-br from-indigo-50 to-blue-100 border-2 border-indigo-300 rounded-xl p-6 flex flex-col justify-center items-center text-center shadow-lg">
                    <div className="text-sm text-indigo-700 font-bold mb-6 uppercase tracking-wide bg-indigo-200 px-4 py-2 rounded-full">
                      ✅ Answer
                    </div>
                    <div className="text-lg text-gray-900 leading-relaxed mb-8 overflow-y-auto max-h-40 font-medium px-4">
                      {currentCard?.answer ||
                        currentCard?.Answer ||
                        "No answer available"}
                    </div>
                    <div className="text-sm text-indigo-600 font-semibold animate-pulse">
                      👆 Click to see question
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Next Button */}
          <button
            onClick={handleNext}
            className="flex-shrink-0 p-3 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors shadow-sm"
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
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default FlashcardViewer;
