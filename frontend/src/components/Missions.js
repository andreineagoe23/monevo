import React, { useState, useEffect } from "react";
import axios from "axios";
import ProgressBar from "react-bootstrap/ProgressBar";
import "../styles/Missions.css";

function Missions() {
  const [dailyMissions, setDailyMissions] = useState([]);
  const [weeklyMissions, setWeeklyMissions] = useState([]);
  const [savingsBalance, setSavingsBalance] = useState(0);
  const [showSavingsMenu, setShowSavingsMenu] = useState(false);
  const [savingsAmount, setSavingsAmount] = useState("");
  const [financeFact, setFinanceFact] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetchMissions();
    fetchSavingsBalance();
    const financeFacts = [
      "Investing early allows your money to grow over time.",
      "A diversified portfolio reduces risk.",
      "Budgeting is key to financial freedom.",
      "Emergency funds should cover 3-6 months of expenses.",
      "Compound interest is a powerful wealth-building tool.",
    ];
    setFinanceFact(
      financeFacts[Math.floor(Math.random() * financeFacts.length)]
    );

    console.log("Fetching missions and initializing data...");

    const intervalId = setInterval(fetchMissions, 30000);
    return () => clearInterval(intervalId);
  }, []);

  const fetchMissions = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/missions/`,
        {
          withCredentials: true,
        }
      );
      console.log("Fetched missions:", response.data);
      setDailyMissions(response.data.daily_missions || []);
      setWeeklyMissions(response.data.weekly_missions || []);
    } catch (error) {
      console.error("Error fetching missions:", error);
      setErrorMessage("Failed to load missions. Please try again.");
    }
  };

  const fetchSavingsBalance = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/savings-account/`,
        { withCredentials: true }
      );
      console.log("Fetched savings balance:", response.data.balance);
      setSavingsBalance(response.data.balance);
    } catch (error) {
      console.error("Error fetching savings balance:", error);
      setErrorMessage("Failed to load savings balance. Please try again.");
    }
  };

  const handleSavingsSubmit = async () => {
    if (isNaN(savingsAmount) || savingsAmount <= 0) {
      alert("Please enter a valid amount.");
      return;
    }
    try {
      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/savings-account/`,
        { amount: parseFloat(savingsAmount) },
        { withCredentials: true }
      );
      setSavingsAmount("");
      fetchSavingsBalance();
      fetchMissions();
    } catch (error) {
      console.error("Error adding savings:", error);
      setErrorMessage("Failed to add savings. Please try again.");
    }
  };

  const markFactRead = async () => {
    try {
      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/finance-fact/`,
        {},
        { withCredentials: true }
      );
      fetchMissions();
    } catch (error) {
      console.error("Error marking fact as read:", error);
      setErrorMessage("Failed to mark fact as read. Please try again.");
    }
  };

  const renderMission = (mission) => (
    <div key={mission.id} className="mission-card">
      <div className="mission-header">
        <h5>{mission.name}</h5>
        <p>{mission.description}</p>
      </div>
      <ProgressBar
        now={mission.progress}
        label={`${mission.progress}%`}
        className="progress-bar-custom"
      />
      {mission.status === "completed" && (
        <p className="completed-badge">Completed!</p>
      )}
      {mission.status !== "completed" &&
        mission.goal_type === "add_savings" && (
          <div>
            <button
              onClick={() => setShowSavingsMenu(!showSavingsMenu)}
              className="update-progress-btn"
            >
              {showSavingsMenu ? "Hide Savings JAR" : "Show Savings JAR"}
            </button>
            {showSavingsMenu && (
              <div className="savings-menu">
                <p>Current Savings Balance: £{savingsBalance}</p>
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSavingsSubmit();
                  }}
                >
                  <input
                    type="number"
                    value={savingsAmount}
                    onChange={(e) => setSavingsAmount(e.target.value)}
                    placeholder="Enter amount (e.g., £5)"
                    className="form-control savings-input"
                  />
                  <button
                    type="submit"
                    className="update-progress-btn add-savings-btn"
                  >
                    Add to Savings
                  </button>
                </form>
              </div>
            )}
          </div>
        )}
      {mission.status !== "completed" && mission.goal_type === "read_fact" && (
        <div>
          <p>Today's Fact: {financeFact}</p>
          <button onClick={markFactRead} className="update-progress-btn">
            Mark Fact Read
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="missions-container">
      <h2 className="text-center missions-title">Daily Missions</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <div className="missions-list">
        {dailyMissions.length > 0 ? (
          dailyMissions.map(renderMission)
        ) : (
          <p>No daily missions available. Check back later!</p>
        )}
      </div>

      <h2 className="text-center missions-title">Weekly Missions</h2>
      <div className="missions-list">
        {weeklyMissions.length > 0 ? (
          weeklyMissions.map(renderMission)
        ) : (
          <p>No weekly missions available. Check back later!</p>
        )}
      </div>
    </div>
  );
}

export default Missions;
