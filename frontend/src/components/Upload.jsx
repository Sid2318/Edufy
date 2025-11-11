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
    try {
      const res = await uploadFile(file);
      setMessage(`✅ ${res.message}`);
      setFile(null);
      // Reset file input
      document.querySelector('input[type="file"]').value = "";
    } catch (err) {
      setMessage("❌ Upload failed! Please try again.");
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-indigo-400 hover:bg-indigo-50/40 transition-all duration-300 group">
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.txt"
            className="hidden"
            id="fileUpload"
          />
          <label htmlFor="fileUpload" className="cursor-pointer block">
            <div className="space-y-4">
              <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-blue-100 rounded-2xl flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-300">
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
                    className="w-10 h-10 text-indigo-600"
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
              : "bg-gradient-to-r from-indigo-600 to-blue-600 text-white hover:from-indigo-700 hover:to-blue-700 shadow-lg hover:shadow-xl transform hover:scale-105"
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
              : "bg-red-50 text-red-700 border-red-200"
          }`}
        >
          <div className="flex items-center space-x-2">
            {message.includes("✅") ? (
              <svg
                className="w-5 h-5 text-green-600"
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
                className="w-5 h-5 text-red-600"
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
            <span>{message.replace(/[✅❌]/g, "").trim()}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;
