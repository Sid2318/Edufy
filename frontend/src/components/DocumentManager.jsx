import React, { useState } from "react";

const DocumentManager = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [documents] = useState([
    {
      name: "sample_study.txt",
      size: "8.2 KB",
      uploaded: "Sample document",
      type: "txt",
    },
  ]);

  const getFileIcon = (type) => {
    switch (type) {
      case "pdf":
        return "📄";
      case "txt":
        return "📝";
      default:
        return "📋";
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 left-6 bg-green-600 text-white p-4 rounded-full shadow-lg hover:bg-green-700 transition-all hover:scale-105 z-50"
        title="Manage Documents"
      >
        <span className="text-xl">📁</span>
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  📁 Your Documents
                </h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>

              {documents.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-gray-400 text-4xl mb-4">📋</div>
                  <p className="text-gray-500">No documents uploaded yet</p>
                  <p className="text-sm text-gray-400 mt-2">
                    Upload some documents to get started
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {documents.map((doc, index) => (
                    <div
                      key={index}
                      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="text-2xl">{getFileIcon(doc.type)}</div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-800 truncate">
                          {doc.name}
                        </p>
                        <p className="text-sm text-gray-500">
                          {doc.size} • {doc.uploaded}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span
                          className="w-2 h-2 bg-green-500 rounded-full"
                          title="Indexed"
                        ></span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h4 className="font-semibold text-blue-800 mb-2">
                  📊 Database Info:
                </h4>
                <ul className="text-blue-700 text-sm space-y-1">
                  <li>
                    • {documents.length} document
                    {documents.length !== 1 ? "s" : ""} indexed
                  </li>
                  <li>• Vector embeddings ready</li>
                  <li>• Search index up to date</li>
                </ul>
              </div>

              <div className="mt-6 text-center">
                <button
                  onClick={() => setIsOpen(false)}
                  className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentManager;
