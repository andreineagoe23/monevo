import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/scss/main.scss";
import { useAuth } from "./AuthContext";

const FriendRequests = () => {
  const [requests, setRequests] = useState([]);
  const { getAccessToken } = useAuth();

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/friend-requests/`,
          {
            headers: {
              Authorization: `Bearer ${getAccessToken()}`,
            },
          }
        );
        setRequests(response.data);
      } catch (err) {
        console.error("Error fetching requests:", err);
      }
    };
    fetchRequests();
  }, [getAccessToken]);

  const handleAccept = async (requestId) => {
    try {
      await axios.put(
        `${process.env.REACT_APP_BACKEND_URL}/friend-requests/${requestId}/`,
        { action: "accept" },
        {
          headers: {
            Authorization: `Bearer ${getAccessToken()}`,
          },
        }
      );
      setRequests(requests.filter((request) => request.id !== requestId));
      alert("Friend request accepted!");
    } catch (err) {
      console.error("Error accepting request:", err);
      alert(
        "Error accepting request: " + (err.response?.data?.error || err.message)
      );
    }
  };

  const handleReject = async (requestId) => {
    try {
      await axios.put(
        `${process.env.REACT_APP_BACKEND_URL}/friend-requests/${requestId}/`,
        { action: "reject" },
        {
          headers: {
            Authorization: `Bearer ${getAccessToken()}`,
          },
        }
      );
      setRequests(requests.filter((request) => request.id !== requestId));
      alert("Friend request rejected.");
    } catch (err) {
      console.error("Error rejecting request:", err);
      alert(
        "Error rejecting request: " + (err.response?.data?.error || err.message)
      );
    }
  };

  return (
    <div className="friend-requests">
      <div className="requests-header">
        <h4>Friend Requests</h4>
        <span className="badge">{requests.length}</span>
      </div>

      {requests.length === 0 ? (
        <div className="empty-state">
          <span className="icon">📭</span>
          <p>No pending requests</p>
        </div>
      ) : (
        <div className="requests-list">
          {requests.map((request) => (
            <div key={request.id} className="request-item">
              <div className="user-info">
                <span className="user-avatar">👤</span>
                <div className="user-details">
                  <span className="username">{request.sender.username}</span>
                  <span className="request-text">wants to connect</span>
                </div>
              </div>
              <div className="action-buttons">
                <button
                  className="btn-accept"
                  onClick={() => handleAccept(request.id)}
                >
                  Accept
                </button>
                <button
                  className="btn-reject"
                  onClick={() => handleReject(request.id)}
                >
                  Decline
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FriendRequests;
