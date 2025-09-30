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
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          📚 Upload Study Document
        </h2>
        <p className="text-gray-600 mb-2">
          Upload PDF or TXT files to create your knowledge base
        </p>
        <p className="text-sm text-orange-600 bg-orange-50 rounded-lg px-3 py-2 inline-block">
          ⚠️ Each new upload will replace the previous document
        </p>
      </div>

      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.txt"
            className="hidden"
            id="fileUpload"
          />
          <label htmlFor="fileUpload" className="cursor-pointer">
            <div className="space-y-2">
              <div className="text-4xl">📄</div>
              <div className="text-gray-600">
                {file ? file.name : "Click to select a file or drag and drop"}
              </div>
              <div className="text-sm text-gray-400">
                Supports PDF and TXT files
              </div>
            </div>
          </label>
        </div>

        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
            !file || isUploading
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-blue-600 text-white hover:bg-blue-700 transform hover:scale-105"
          }`}
        >
          {isUploading ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Uploading...
            </span>
          ) : (
            "Upload Document"
          )}
        </button>
      </div>

      {message && (
        <div
          className={`p-4 rounded-lg ${
            message.includes("✅")
              ? "bg-green-100 text-green-800"
              : "bg-red-100 text-red-800"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
};

export default Upload;
