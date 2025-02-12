import React, { useEffect, useState } from "react";
import axios from "axios";
import ForexTools from "./ForexTools";
import CryptoTools from "./CryptoTools";
import BasicFinanceTools from "./BasicFinanceTools";
import NewsCalendars from "./NewsCalendars";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/ToolsPage.css"; // New CSS file
import Chatbot from "./Chatbot";

const ToolsPage = () => {
  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTools = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/tools/`,
          { withCredentials: true } // ✅ Use cookies for authentication
        );

        // Move "Crypto Tools" to the top
        const reorderedCategories = response.data.sort((a, b) => {
          if (a.category === "Crypto Tools") return -1;
          if (b.category === "Crypto Tools") return 1;
          return 0;
        });

        setCategories(reorderedCategories);

        // Automatically expand the first category
        const defaultActiveIndex = reorderedCategories.findIndex(
          (cat) => cat.category === "Crypto Tools"
        );
        setActiveCategory(defaultActiveIndex);
      } catch (error) {
        console.error("Error fetching tools:", error);
        setError(error.message || "Error fetching tools.");
      }
    };

    fetchTools();
  }, []);

  return (
    <div className="tools-page">
      <h1 className="tools-title">Financial Tools</h1>
      {error ? (
        <div className="alert alert-danger text-center">{error}</div>
      ) : (
        <div className="accordion" id="toolsAccordion">
          {categories.map((category, index) => (
            <div key={index} className="accordion-item">
              <h2 className="accordion-header">
                <button
                  className="accordion-button"
                  type="button"
                  onClick={() => setActiveCategory(index)}
                  aria-expanded={activeCategory === index}
                >
                  {category.category}
                </button>
              </h2>
              <div
                className={`accordion-collapse collapse ${
                  activeCategory === index ? "show" : ""
                }`}
              >
                <div className="accordion-body">
                  {category.category === "Forex Tools" && <ForexTools />}
                  {category.category === "Crypto Tools" && <CryptoTools />}
                  {category.category === "News & Calendars" && (
                    <NewsCalendars />
                  )}
                  {category.category === "Basic Finance & Budgeting Tools" && (
                    <BasicFinanceTools />
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      <Chatbot />
    </div>
  );
};

export default ToolsPage;
