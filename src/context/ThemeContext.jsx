import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext({
  darkMode: true,
  toggleDarkMode: () => {},
});

export const ThemeProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem("monevo-theme");
    if (saved === "light") {
      setDarkMode(false);
    } else {
      // Dark is the intended default. Only honor a saved "light" choice.
      setDarkMode(true);
    }
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add("dark");
      localStorage.setItem("monevo-theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("monevo-theme", "light");
    }
  }, [darkMode]);

  return (
    <ThemeContext.Provider
      value={{ darkMode, toggleDarkMode: () => setDarkMode((v) => !v) }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
