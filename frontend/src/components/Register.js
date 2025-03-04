import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../styles/Register.css";
import "../styles/CustomStyles.css";
import logo from "../assets/monevo.png";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    wants_personalized_path: false,
    referral_code: "", // Add referral code field
  });
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRadioChange = (e) => {
    setFormData({
      ...formData,
      wants_personalized_path: e.target.value === "true",
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      console.log("Sending registration data:", formData); // Debug log

      // Fetch CSRF token from the backend
      const csrfResponse = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/csrf/`,
        { withCredentials: true }
      );
      const csrfToken = csrfResponse.data.csrfToken;

      // Include referral code in the registration request
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/register/`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          withCredentials: true,
        }
      );

      console.log("Registration Success:", response.data);

      // Auto-login after registration
      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/login/`,
        {
          username: formData.username,
          password: formData.password,
        },
        { withCredentials: true }
      );

      navigate(
        formData.wants_personalized_path ? "/questionnaire" : "/all-topics"
      );
    } catch (error) {
      console.error("Registration failed", error.response?.data || error);
      setErrorMessage(
        error.response?.data?.error || "An error occurred. Please try again."
      );
    }
  };

  return (
    <div className="register-container">
      <img src={logo} alt="Logo" className="logo" />
      <h2>Create Your Account</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form onSubmit={handleRegister}>
        <label>Username</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <label>Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <label>Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <label>First Name</label>
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />

        <label>Last Name</label>
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />

        <label>Referral Code (optional)</label>
        <input
          type="text"
          name="referral_code"
          value={formData.referral_code}
          onChange={handleChange}
        />

        <label>Do you want a personalized learning path?</label>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              name="wants_personalized_path"
              value="true"
              onChange={handleRadioChange}
              required
            />
            Yes
          </label>
          <label>
            <input
              type="radio"
              name="wants_personalized_path"
              value="false"
              onChange={handleRadioChange}
              required
            />
            No
          </label>
        </div>

        <div className="form-button-row">
          <button
            type="submit"
            className="button button--primary button--large"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  );
}

export default Register;
