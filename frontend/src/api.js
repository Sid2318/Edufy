import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // FastAPI backend

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(
      `Making ${config.method.toUpperCase()} request to ${config.url}`
    );
    return config;
  },
  (error) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log("Response received:", response.status);
    return response;
  },
  (error) => {
    console.error("Response error:", error.response?.data || error.message);

    if (error.code === "ECONNREFUSED") {
      throw new Error(
        "Cannot connect to backend server. Please make sure it's running on port 8000."
      );
    }

    if (error.response?.status === 500) {
      throw new Error("Server error. Please try again later.");
    }

    throw error;
  }
);

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const askQuestion = async (question) => {
  const response = await api.get("/query", {
    params: { question },
  });

  return response.data;
};

export const getSampleQuestions = async () => {
  const response = await api.get("/sample-questions");
  return response.data;
};

export const getStatus = async () => {
  const response = await api.get("/status");
  return response.data;
};

// Health check function
export const checkHealth = async () => {
  try {
    const response = await api.get("/");
    return response.status === 200;
  } catch (error) {
    return false;
  }
};
