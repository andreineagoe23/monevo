import React, { useState, useEffect, useCallback } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";
import "../styles/scss/main.scss";
import Loader from "../components/Loader";

function PersonalizedPath({ onCourseClick }) {
  const [personalizedCourses, setPersonalizedCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const [paymentVerified, setPaymentVerified] = useState(false);

  // Define fetchPersonalizedPath first using useCallback
  const fetchPersonalizedPath = useCallback(async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/personalized-path/`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            "X-CSRFToken": document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || "",
          },
          withCredentials: true,
        }
      );

      if (response.status === 403) {
        if (response.data.redirect) {
          navigate(response.data.redirect);
          return;
        }
        throw new Error(response.data.error || "Access denied");
      }

      setPersonalizedCourses(
        response.data.courses.map((course) => ({
          ...course,
          image: course.image || "/fallback-course.png",
          progress: course.completed_lessons || 0,
          totalLessons: course.total_lessons || 0,
        }))
      );
      setIsLoading(false);
    } catch (error) {
      if (error.response?.status === 403) {
        const errorMessage = error.response.data?.error || "Access denied";
        if (errorMessage.includes("questionnaire")) {
          navigate("/questionnaire");
        } else if (errorMessage.includes("Payment")) {
          navigate("/payment-required");
        }
      } else {
        setError("Failed to load recommendations. Please try again later.");
      }
      setIsLoading(false);
    }
  }, [navigate]);

  // Now define useEffect that uses fetchPersonalizedPath
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const sessionId = queryParams.get("session_id");

    const verifyAuthAndPayment = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        navigate(
          `/#/login?returnUrl=${encodeURIComponent("/#/personalized-path")}`
        );
        return;
      }

      try {
        let profileRes = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/userprofile/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (!profileRes.data.has_paid) {
          if (sessionId) {
            try {
              await axios.post(
                `${process.env.REACT_APP_BACKEND_URL}/verify-session/`,
                { session_id: sessionId },
                { headers: { Authorization: `Bearer ${token}` } }
              );
            } catch (error) {
              console.error("Session verification failed:", error);
            }
          }

            const pollPaymentStatus = async (attempt = 0) => {
              try {
              const verificationRes = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL}/verify-session/`,
                { session_id: sessionId },
                { headers: { Authorization: `Bearer ${token}` } }
              );

              if (verificationRes.data.status === "verified") {
                window.history.replaceState({}, document.title, "/#/personalized-path");
                setPaymentVerified(true);
                return fetchPersonalizedPath();
              }

              // Progressive backoff: 500ms, 1s, 2s, 4s, etc.
              const delay = Math.min(500 * Math.pow(2, attempt), 8000);

              if (attempt < 8) {
                await new Promise(resolve => setTimeout(resolve, delay));
                return pollPaymentStatus(attempt + 1);
              }

              navigate("/payment-required");
              } catch (error) {
              if (attempt < 3) {
                await new Promise(resolve => setTimeout(resolve, 1000));
                return pollPaymentStatus(attempt + 1);
              }
              navigate("/payment-required");
              }
            };
          await pollPaymentStatus();
        } else {
          setPaymentVerified(true);
          fetchPersonalizedPath();
        }
      } catch (error) {
        console.error("Verification error:", error);
        localStorage.removeItem("access_token");
        navigate(`/login?returnUrl=${encodeURIComponent(location.pathname)}`);
      }
    };

    verifyAuthAndPayment();
  }, [navigate, location.pathname, location.search, fetchPersonalizedPath]);

  const handleCourseClick = (courseId) => {
    if (onCourseClick) onCourseClick(courseId);
  };

  if (!paymentVerified || isLoading) {
    return <Loader message="Verifying your access..." />;
  }

  if (error) {
    return (
      <div className="container text-center py-5">
        <div
          className="alert alert-danger mx-auto"
          style={{ maxWidth: "600px" }}
        >
          <h2 className="h4 mb-3">⚠️ Error Loading Recommendations</h2>
          <p className="mb-4">{error}</p>
          <button
            className="btn btn-primary"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="personalized-path container-lg">
      <div className="path-header text-center mb-5">
        <p className="recommendation-message display-6 mb-0">
          Your personalized learning path:
        </p>
      </div>

      <div className="path-container">
        {personalizedCourses.map((course, index) => (
          <React.Fragment key={course.id}>
            <div className={`path-item ${index % 2 === 0 ? "left" : "right"}`}>
              <div className="course-node">
                <div className="course-circle">
                  <img
                    src={course.image}
                    alt={course.title}
                    className="course-image img-fluid"
                    onError={(e) => {
                      e.target.src = "/default-course.jpg";
                    }}
                  />
                </div>
              </div>

              <motion.div
                className="course-box"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleCourseClick(course.id)}
              >
                <div className="course-tags">
                  <span className={`text-muted mt-2 d-block`}>
                    {course.path_title}
                  </span>
                </div>

                <h4 className="mb-3">{course.title}</h4>

                <div className="course-meta">
                  <div className="progress-container">
                    <div className="progress">
                      <div
                        className="progress-bar"
                        role="progressbar"
                        style={{
                          width: `${
                            (course.progress / course.totalLessons) * 100
                          }%`,
                          transition: "width 0.5s ease",
                        }}
                      ></div>
                    </div>
                    <span className="text-muted mt-2 d-block">
                      {course.progress}/{course.totalLessons} lessons
                    </span>
                  </div>

                  <div className="course-stats">
                    <div className="stat">
                      <span className="me-2">⏱️</span>
                      {course.estimated_duration || 4} hrs
                    </div>
                    <div className="stat">
                      <span className="me-2">💪</span>
                      {course.exercises || 3} exercises
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>

            {index < personalizedCourses.length - 1 && (
              <div className="vertical-connector d-none d-lg-block"></div>
            )}
          </React.Fragment>
        ))}
      </div>

      <div className="path-footer text-center mt-5 py-4">
        <p className="mb-0">
          🔁 Based on your latest questionnaire responses -{" "}
          <button
            onClick={() => navigate("/questionnaire")}
            className="btn btn-link text-decoration-none p-0"
          >
            Update Preferences
          </button>
        </p>
      </div>
    </div>
  );
}

export default PersonalizedPath;
