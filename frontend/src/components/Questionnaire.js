import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/Questionnaire.css";

const Questionnaire = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const [answers, setAnswers] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_BACKEND_URL}/questionnaire/`)

      .then((response) => {
        setQuestions(response.data);
      })
      .catch((error) => {
        console.error("Error fetching questions:", error);
      });
  }, []);

  if (questions.length === 0) {
    return <div>Loading questions...</div>;
  }

  const currentQuestion = questions[currentQuestionIndex];

  const handleAnswer = (questionId, answer) => {
    const updatedAnswers = { ...answers, [questionId]: answer };
    setAnswers(updatedAnswers);

    const newProgress = ((currentQuestionIndex + 1) / questions.length) * 100;
    setProgress(newProgress);

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      axios
        .post(
          "http://localhost:8000/api/questionnaire/submit/",
          { answers: updatedAnswers },
          { withCredentials: true } // ✅ Use cookies for authentication
        )
        .then(() => {
          navigate("/personalized-path");
        })
        .catch((error) => {
          console.error("Error submitting questionnaire:", error);
        });
    }
  };

  return (
    <div className="questionnaire-container">
      <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      <h2>{currentQuestion.text}</h2>
      <div>
        {currentQuestion.options.map((option, index) => (
          <button
            key={index}
            className="question-option"
            onClick={() => handleAnswer(currentQuestion.id, option)}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Questionnaire;
