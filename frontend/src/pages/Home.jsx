import React, { useState } from "react";
import { useAuth } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { FiUpload, FiLogOut, FiCheckCircle } from "react-icons/fi";
import Chatbot from "./chatbot"; // تأكد من تطابق الاسم مع الملف

const Home = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setPrediction("");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setPrediction(response.data.result);
    } catch (error) {
      console.error("Prediction error:", error);
      setPrediction("Error during prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="home-container">
      {user ? (
        <>
          <div className="user-header">
            <h1 className="welcome-title">
              <span>🌿</span> Welcome, {user.name}!
            </h1>
            <button className="btn btn-danger" onClick={handleLogout}>
              <FiLogOut /> Logout
            </button>
          </div>

          <div className="upload-card">
            <h2 className="upload-title">Upload a Plant Leaf Image</h2>

            <label className="upload-area">
              <div className="upload-icon">
                <FiUpload />
              </div>
              <p>Click to browse or drag & drop your image</p>
              <input
                type="file"
                className="file-input"
                accept="image/*"
                onChange={handleFileChange}
              />
            </label>

            {previewUrl && (
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
              </div>
            )}

            <div style={{ textAlign: "center" }}>
              <button
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={loading || !selectedFile}
              >
                {loading ? (
                  <>
                    <span className="loading-spinner"></span> Analyzing...
                  </>
                ) : (
                  "Predict Disease"
                )}
              </button>
            </div>
          </div>

          {prediction && (
            <div className="result-card">
              <h2 className="result-title">
                <FiCheckCircle /> Prediction Result
              </h2>
              <p className="result-text">{prediction.replace(/_/g, " ")}</p>
            </div>
          )}

          <Chatbot />
        </>
      ) : (
        <div style={{ textAlign: "center", marginTop: "3rem" }}>
          <p>You are not logged in.</p>
          <div style={{ marginTop: "1rem" }}>
            <a href="/login" className="btn btn-primary">Login</a>
            <a href="/register" className="btn btn-primary" style={{ marginLeft: "1rem" }}>Register</a>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
