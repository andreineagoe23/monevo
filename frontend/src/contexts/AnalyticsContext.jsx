import React, { createContext, useCallback, useContext, useMemo, useState } from "react";
import axios from "axios";
import { useAuth } from "contexts/AuthContext";

const AnalyticsContext = createContext({ trackEvent: () => {}, sessionId: null });

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api";
const SESSION_STORAGE_KEY = "monevo:exercise-session-id";

const generateSessionId = () => {
  if (window.crypto?.randomUUID) {
    return window.crypto.randomUUID();
  }
  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

const getOrCreateSessionId = () => {
  if (typeof window === "undefined") {
    return null;
  }
  const existing = sessionStorage.getItem(SESSION_STORAGE_KEY);
  if (existing) {
    return existing;
  }
  const next = generateSessionId();
  sessionStorage.setItem(SESSION_STORAGE_KEY, next);
  return next;
};

export const AnalyticsProvider = ({ children }) => {
  const { getAccessToken, user } = useAuth();
  const [sessionId] = useState(() => getOrCreateSessionId());

  const trackEvent = useCallback(
    async (eventType, exerciseId, metadata = {}) => {
      if (!sessionId || !exerciseId) return;

      const payload = {
        session_id: sessionId,
        exercise_id: exerciseId,
        event_type: eventType,
        metadata: { ...metadata, userId: user?.id },
      };

      try {
        await axios.post(`${BACKEND_URL}/analytics/events/`, payload, {
          headers: {
            Authorization: `Bearer ${getAccessToken()}`,
          },
        });
      } catch (error) {
        console.error("Failed to record exercise event", error);
      }
    },
    [getAccessToken, sessionId, user?.id]
  );

  const contextValue = useMemo(
    () => ({
      sessionId,
      trackEvent,
    }),
    [sessionId, trackEvent]
  );

  return (
    <AnalyticsContext.Provider value={contextValue}>
      {children}
    </AnalyticsContext.Provider>
  );
};

export const useAnalytics = () => useContext(AnalyticsContext);
