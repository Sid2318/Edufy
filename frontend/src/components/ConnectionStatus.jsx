import React, { useState, useEffect } from "react";

const ConnectionStatus = () => {
  const [isConnected, setIsConnected] = useState(true);
  const [isChecking, setIsChecking] = useState(false);

  const checkConnection = async () => {
    setIsChecking(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/", {
        method: "GET",
        mode: "cors",
      });
      setIsConnected(response.ok);
    } catch (error) {
      setIsConnected(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (isConnected) {
    return (
      <div className="flex items-center space-x-2 text-green-600 text-sm">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span>Connected to backend</span>
      </div>
    );
  }

  return (
    <div className="bg-red-100 border border-red-300 rounded-lg p-4 mb-6">
      <div className="flex items-center space-x-2 text-red-700">
        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
        <span className="font-semibold">Backend connection lost</span>
        {isChecking && (
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-500"></div>
        )}
      </div>
      <p className="text-red-600 text-sm mt-2">
        Make sure the backend server is running on http://127.0.0.1:8000
      </p>
      <button
        onClick={checkConnection}
        disabled={isChecking}
        className="mt-2 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 disabled:opacity-50"
      >
        {isChecking ? "Checking..." : "Retry Connection"}
      </button>
    </div>
  );
};

export default ConnectionStatus;
