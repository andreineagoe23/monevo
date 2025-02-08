import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/Profile.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Chatbot from "./Chatbot";

function Profile() {
  const [profileData, setProfileData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    earned_money: 0.0,
    points: 0,
    streak: 0,
  });
  const [imageUrl, setImageUrl] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        // Fetch UserProfile data
        const profileResponse = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/userprofile/`,
          { withCredentials: true }
        );

        // Set profile data
        setProfileData({
          username: profileResponse.data.user.username || "",
          email: profileResponse.data.user.email || "",
          first_name: profileResponse.data.user.first_name || "",
          last_name: profileResponse.data.user.last_name || "",
          earned_money: parseFloat(profileResponse.data.earned_money) || 0.0,
          points: profileResponse.data.points || 0,
          streak: profileResponse.data.streak || 0,
        });

        // Fetch avatar URL
        setImageUrl(
          profileResponse.data.profile_avatar || "/default-avatar.png"
        );

        // Fetch recent activity
        const progressResponse = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/userprogress/`,
          { withCredentials: true }
        );

        // Transform progress data into activity items
        setRecentActivity(
          progressResponse.data.map((p) => ({
            id: p.id,
            activity: `Completed ${p.course.title}`,
            date: new Date(p.last_completed_date).toLocaleDateString(),
          }))
        );
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };

    fetchProfileData();
  }, []);

  return (
    <div className="container profile-container my-5">
      <div className="card p-4 shadow-sm">
        <h2 className="text-center mb-4">Profile</h2>

        <div className="text-center mb-4">
          <img
            src={imageUrl}
            alt="Avatar"
            className="rounded-circle"
            width="150"
            height="150"
          />
        </div>

        <div className="profile-details">
          <h3 className="mt-4 text-center">
            {profileData.first_name} {profileData.last_name}
          </h3>
          <p className="text-center text-muted">@{profileData.username}</p>
          <p className="text-center text-muted">{profileData.email}</p>

          <div className="stats-section">
            <div className="stat-box">
              <h4>Balance</h4>
              <p>${profileData.earned_money.toFixed(2)}</p>
            </div>
            <div className="stat-box">
              <h4>Points</h4>
              <p>{profileData.points}</p>
            </div>
            <div className="stat-box">
              <h4>Streak</h4>
              <p>{profileData.streak} days</p>
            </div>
          </div>
        </div>

        <h3 className="mt-4">Recent Activity</h3>
        <ul className="list-group">
          {recentActivity.map((activity) => (
            <li key={activity.id} className="list-group-item">
              <strong>{activity.activity}</strong>
              <span className="text-muted float-end">{activity.date}</span>
            </li>
          ))}
        </ul>
      </div>
      <Chatbot />
    </div>
  );
}

export default Profile;
