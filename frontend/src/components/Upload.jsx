import React, { useState } from "react";
import { uploadFile } from "../api";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(""); // Clear previous messages
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first!");
      return;
    }

    setIsUploading(true);
    setMessage("🔄 Uploading and processing your document...");

    try {
      const res = await uploadFile(file);

      if (res.error) {
        setMessage(`❌ ${res.error}`);
      } else {
        // Show detailed success message
        setMessage(
          `✅ ${res.message}\n\n` +
            `📄 File: ${res.filename || file.name}\n` +
            `📊 Size: ${
              res.file_size
                ? Math.round(res.file_size / 1024) + " KB"
                : "Unknown"
            }\n\n` +
            `🔄 Previous documents have been completely removed.\n` +
            `💭 New smart questions and flashcards will be generated for your new document.`
        );

        setFile(null);
        // Reset file input
        document.querySelector('input[type="file"]').value = "";

        // Auto-clear success message after 8 seconds
        setTimeout(() => {
          setMessage("");
        }, 8000);
      }
    } catch (err) {
      console.error("Upload error:", err);
      setMessage(
        "❌ Upload failed! Please try again.\n\n" +
          "Make sure your file is:\n" +
          "• A valid PDF or TXT file\n" +
          "• Not empty or corrupted\n" +
          "• Under 10MB in size"
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-purple-400 hover:bg-purple-50/30 transition-all duration-300 group">
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.txt"
            className="hidden"
            id="fileUpload"
          />
          <label htmlFor="fileUpload" className="cursor-pointer block">
            <div className="space-y-4">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
                {file ? (
                  <svg
                    className="w-10 h-10 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                ) : (
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
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                  </svg>
                )}
              </div>
              <div className="space-y-2">
                <div className="text-lg font-semibold text-gray-700">
                  {file ? file.name : "Click to select a file or drag and drop"}
                </div>
                <div className="text-sm text-gray-500">
                  Supports PDF and TXT files up to 10MB
                </div>
              </div>
            </div>
          </label>
        </div>

        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-300 ${
            !file || isUploading
              ? "bg-gray-200 text-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-purple-600 to-pink-600 text-black hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl transform hover:scale-105"
          }`}
        >
          {isUploading ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-6 w-6 border-3 border-white border-t-transparent mr-3"></div>
              Uploading Document...
            </span>
          ) : (
            <span className="flex items-center justify-center">
              <svg
                className="w-6 h-6 mr-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              Upload Document
            </span>
          )}
        </button>
      </div>

      {message && (
        <div
          className={`p-4 rounded-2xl border font-medium slide-in ${
            message.includes("✅")
              ? "bg-green-50 text-green-700 border-green-200"
              : message.includes("🔄")
              ? "bg-blue-50 text-blue-700 border-blue-200"
              : "bg-red-50 text-red-700 border-red-200"
          }`}
        >
          <div className="flex items-start space-x-3">
            {message.includes("✅") ? (
              <svg
                className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            ) : message.includes("🔄") ? (
              <svg
                className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0 animate-spin"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            ) : (
              <svg
                className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            )}
            <div className="whitespace-pre-line leading-relaxed">
              {message.replace(/[✅❌🔄]/g, "").trim()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;
