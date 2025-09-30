import React, { useState, useEffect } from "react";
import { getSampleQuestions, getStatus } from "../api";

const SampleQuestions = ({ onQuestionClick }) => {
  const [hasDocuments, setHasDocuments] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if documents are uploaded and fetch sample questions
    const checkDocumentsAndFetchQuestions = async () => {
      try {
        const statusResponse = await getStatus();
        const hasUploaded = statusResponse.database_ready && statusResponse.documents.length > 0;
        setHasDocuments(hasUploaded);

        if (hasUploaded) {
          setIsLoading(true);
          try {
            const questionsResponse = await getSampleQuestions();
            if (questionsResponse.questions && !questionsResponse.error) {
              setQuestions(questionsResponse.questions);
            } else {
              setQuestions([]);
            }
          } catch (error) {
            console.error('Error fetching sample questions:', error);
            setQuestions([]);
          } finally {
            setIsLoading(false);
          }
        } else {
          setQuestions([]);
        }
      } catch (error) {
        console.error('Error checking document status:', error);
        setHasDocuments(false);
        setQuestions([]);
      }
    };

    checkDocumentsAndFetchQuestions();
    // Check every 10 seconds
    const interval = setInterval(checkDocumentsAndFetchQuestions, 10000);
    return () => clearInterval(interval);
  }, []);

  if (!hasDocuments) {
    return (
      <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg p-6 mt-6 border border-orange-200">
        <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
          📋 No Documents Uploaded
        </h3>
        <p className="text-gray-600 text-center mb-4">
          Upload a document first to see suggested questions about it!
        </p>
        <div className="text-center">
          <div className="inline-flex items-center text-sm text-gray-500">
            <span className="mr-2">👆</span>
            <span>Use the upload section above to get started</span>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mt-6 border border-blue-200">
        <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
          🔍 Analyzing Your Document...
        </h3>
        <div className="flex justify-center items-center space-x-2">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <span className="text-gray-600">Generating smart questions from your content</span>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-6 mt-6 border border-gray-200">
        <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
          ❓ Questions Available
        </h3>
        <p className="text-gray-600 text-center">
          No specific questions could be generated from your document. Try asking general questions about the content.
        </p>
      </div>
    );
  }

  // Group questions into categories for better display
  const organizeQuestions = (questionList) => {
    const categories = [];
    const questionsPerCategory = Math.ceil(questionList.length / 3);
    
    for (let i = 0; i < questionList.length; i += questionsPerCategory) {
      const categoryQuestions = questionList.slice(i, i + questionsPerCategory);
      let categoryName = "📄 Content";
      
      if (i === 0) categoryName = "🔍 Key Topics";
      else if (i === questionsPerCategory) categoryName = "📚 Details";
      else categoryName = "💡 Analysis";
      
      categories.push({
        category: categoryName,
        questions: categoryQuestions
      });
    }
    
    return categories;
  };

  const questionCategories = organizeQuestions(questions);

  return (
    <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 mt-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
        💭 Smart Questions from Your Document
      </h3>
      <p className="text-gray-600 text-center mb-6 text-sm">
        These questions were generated based on your uploaded content
      </p>

      <div className="grid md:grid-cols-3 gap-4">
        {questionCategories.map((category, categoryIndex) => (
          <div key={categoryIndex} className="space-y-3">
            <h4 className="font-semibold text-gray-700 text-center">
              {category.category}
            </h4>
            <div className="space-y-2">
              {category.questions.map((question, questionIndex) => (
                <button
                  key={questionIndex}
                  onClick={() => onQuestionClick(question)}
                  className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-all text-sm text-gray-700 hover:text-purple-700"
                >
                  "{question}"
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SampleQuestions;