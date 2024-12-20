import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import LearningPathList from "./LearningPathList";
import UserProgressBox from "./UserProgressBox";
import "../styles/Dashboard.css";
import Chatbot from "./Chatbot";

function Dashboard() {
  const [user, setUser] = useState(null); // For user info
  const [learningPaths, setLearningPaths] = useState([]);
  const [activePathId, setActivePathId] = useState(null);
  const [recommendedPath, setRecommendedPath] = useState(null);
  const [showRecommendation, setShowRecommendation] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");

    if (!accessToken) {
      navigate("/login");
    } else {
      // Fetch user info
      axios
        .get("http://localhost:8000/api/userprofile/", {
          headers: { Authorization: `Bearer ${accessToken}` },
        })
        .then((response) => setUser(response.data))
        .catch((error) => console.error("Failed to fetch user data:", error));

      // Fetch learning paths
      axios
        .get("http://localhost:8000/api/paths/", {
          headers: { Authorization: `Bearer ${accessToken}` },
        })
        .then((response) => setLearningPaths(response.data))
        .catch((error) =>
          console.error("Failed to fetch learning paths:", error)
        );

      // Fetch user profile to check if the questionnaire is completed
      axios
        .get("http://localhost:8000/api/questionnaire/", {
          headers: { Authorization: `Bearer ${accessToken}` },
        })
        .then((response) => {
          const userProfile = response.data;

          if (userProfile.is_questionnaire_completed) {
            // Skip the questionnaire fetch if completed
            return;
          }

          // If the questionnaire is not completed, fetch it
          axios
            .get("http://localhost:8000/api/questionnaire/", {
              headers: { Authorization: `Bearer ${accessToken}` },
            })
            .then((response) => {
              const { goal, experience, preferred_style } = response.data;

              // Personalized recommendation logic
              if (goal === "Save and budget effectively") {
                setRecommendedPath("Basic Finance");
              } else if (
                goal === "Start investing" &&
                experience === "Beginner"
              ) {
                setRecommendedPath("Basic Finance");
              } else if (goal === "Achieve financial independence") {
                setRecommendedPath("Real Estate");
              } else if (preferred_style === "Interactive and hands-on") {
                setRecommendedPath("Crypto");
              } else if (experience === "Advanced") {
                setRecommendedPath("Forex");
              } else {
                setRecommendedPath("General Financial Literacy");
              }

              // Hide recommendation after 10 seconds
              setTimeout(() => setShowRecommendation(false), 10000);
            })
            .catch((error) =>
              console.error("Failed to fetch questionnaire data:", error)
            );
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    }
  }, [navigate]);

  const togglePath = (pathId) => {
    setActivePathId((prevPathId) => (prevPathId === pathId ? null : pathId));
  };

  const handleCourseClick = (courseId) => {
    navigate(`/lessons/${courseId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/welcome");
  };

  return (
    <div className="dashboard">
      <div className="main-content">
        <div className="dashboard-container">
          <div className="main-section">
            <h1>Welcome to Your Dashboard</h1>
            <button onClick={handleLogout} className="btn btn-danger">
              Logout
            </button>
            {user ? <h2>Hello, {user.username}!</h2> : <h2>Loading...</h2>}

            {showRecommendation && recommendedPath && (
              <p className="recommendation-message">
                Based on your answers, we recommend starting with:{" "}
                <strong>{recommendedPath}</strong>
              </p>
            )}

            <div className="learning-path-container">
              <LearningPathList
                learningPaths={learningPaths}
                activePathId={activePathId}
                onTogglePath={togglePath}
                onCourseClick={handleCourseClick}
              />
            </div>
          </div>
        </div>
      </div>
      <div className="user-progress">
        <UserProgressBox />
        <div className="streak-section">
          <h4 className="text-muted">Streak:</h4>
          <p className="h5">{user ? user.streak || 0 : 0} days</p>
        </div>
      </div>
      <Chatbot />
    </div>
  );
}

export default Dashboard;
