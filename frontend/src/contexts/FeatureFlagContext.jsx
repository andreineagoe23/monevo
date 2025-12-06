import React, { createContext, useContext, useMemo, useState } from "react";

const FeatureFlagContext = createContext({ flags: {} });

const DEFAULT_VARIANTS = {
  control: { feedbackDelayMs: 0, hintCost: 0, skipCost: 0 },
  experiment: { feedbackDelayMs: 1200, hintCost: 2, skipCost: 3 },
};

const VARIANT_STORAGE_KEY = "monevo:feature-variant";

const pickVariant = () => {
  if (typeof window === "undefined") return "control";
  const stored = localStorage.getItem(VARIANT_STORAGE_KEY);
  if (stored) return stored;
  const variant = Math.random() < 0.5 ? "control" : "experiment";
  localStorage.setItem(VARIANT_STORAGE_KEY, variant);
  return variant;
};

export const FeatureFlagProvider = ({ children }) => {
  const [variant] = useState(pickVariant);

  const flags = useMemo(() => {
    return { variant, ...(DEFAULT_VARIANTS[variant] || DEFAULT_VARIANTS.control) };
  }, [variant]);

  return (
    <FeatureFlagContext.Provider value={{ flags }}>
      {children}
    </FeatureFlagContext.Provider>
  );
};

export const useFeatureFlags = () => useContext(FeatureFlagContext);
