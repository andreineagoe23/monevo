import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/Chatbot.css";
import "bootstrap/dist/css/bootstrap.min.css";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isVisible, setIsVisible] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [hasGreeted, setHasGreeted] = useState(false); // ✅ Track if greeting has been shown

  const HF_API_KEY = process.env.REACT_APP_HF_API_KEY;
  const HF_MODEL = "HuggingFaceH4/zephyr-7b-alpha"; // ✅ Use a finance-friendly model

  useEffect(() => {
    if (isVisible && !hasGreeted) {
      setChatHistory((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Hello! How can I assist you with finance today?",
        },
      ]);
      setHasGreeted(true); // ✅ Ensure greeting appears only once
    }
  }, [isVisible, hasGreeted]);

  // ✅ Function to check if user asked about stock/crypto data
  const checkFinancialQuery = async (message) => {
    if (message.toLowerCase().includes("stock price")) {
      const stockSymbol = message.split(" ").pop().toUpperCase(); // Extract last word as stock symbol
      return await fetchStockPrice(stockSymbol);
    }
    if (
      message.toLowerCase().includes("crypto") ||
      message.toLowerCase().includes("bitcoin")
    ) {
      return await fetchCryptoPrice("bitcoin"); // Default to Bitcoin
    }
    return null; // No financial query detected
  };

  // ✅ Fetch stock price using CoinGecko API
  const fetchStockPrice = async (symbol) => {
    try {
      const response = await axios.get(
        `https://api.coingecko.com/api/v3/simple/price?ids=${symbol}&vs_currencies=usd`
      );
      if (response.data[symbol]) {
        return `The current price of ${symbol.toUpperCase()} is $${
          response.data[symbol].usd
        } USD.`;
      } else {
        return `Sorry, I couldn't find the stock price for ${symbol}.`;
      }
    } catch (error) {
      console.error("Error fetching stock price:", error);
      return "Sorry, I couldn't retrieve stock data.";
    }
  };

  // ✅ Fetch crypto price using CoinGecko API
  const fetchCryptoPrice = async (cryptoId) => {
    try {
      const response = await axios.get(
        `https://api.coingecko.com/api/v3/simple/price?ids=${cryptoId}&vs_currencies=usd`
      );
      return `The current price of ${cryptoId.toUpperCase()} is $${
        response.data[cryptoId].usd
      } USD.`;
    } catch (error) {
      console.error("Error fetching crypto price:", error);
      return "Sorry, I couldn't retrieve crypto data.";
    }
  };

  // ✅ AI + Financial Data Integration
  const handleMessageSend = async () => {
    if (!userInput.trim()) return;

    setChatHistory((prev) => [...prev, { sender: "user", text: userInput }]);
    setIsTyping(true);

    // ✅ Check if user is asking for stock or crypto data
    const financialResponse = await checkFinancialQuery(userInput);
    if (financialResponse) {
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: financialResponse },
      ]);
      setIsTyping(false);
      setUserInput("");
      return;
    }

    try {
      // ✅ Call AI API if no financial data request detected
      const response = await axios.post(
        `https://api-inference.huggingface.co/models/${HF_MODEL}`,
        {
          inputs: `User: ${userInput}\n\nAssistant: (respond in 2-3 sentences, be concise and clear)`,
          parameters: { max_new_tokens: 200, temperature: 0.5, top_p: 0.8 },
        },
        {
          headers: {
            Authorization: `Bearer ${HF_API_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );

      let aiResponse = response.data[0].generated_text.trim();
      aiResponse = aiResponse
        .replace("User:", "")
        .replace(userInput, "")
        .replace("Assistant:", "")
        .replace("(respond in 2-3 sentences, be concise and clear)", "")
        .trim();

      setChatHistory((prev) => [...prev, { sender: "bot", text: aiResponse }]);
    } catch (error) {
      console.error("❌ Error sending message to Hugging Face:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Error connecting to AI. Try again later." },
      ]);
    }

    setIsTyping(false);
    setUserInput("");
  };

  return (
    <div>
      <button
        className="chatbot-toggle position-fixed"
        onClick={() => setIsVisible(!isVisible)}
      >
        💬
      </button>

      {isVisible && (
        <div className="chatbot-container position-fixed">
          <div className="chatbot-header d-flex align-items-center justify-content-between px-3 py-2">
            <span>Finance Assistant</span>
            <button
              className="btn btn-sm chatbot-close"
              onClick={() => setIsVisible(false)}
            >
              ✖
            </button>
          </div>

          <div className="chat-history p-3 flex-grow-1">
            {chatHistory.map((msg, idx) => (
              <div
                key={idx}
                className={`chat-message mb-2 ${
                  msg.sender === "user" ? "chat-user" : "chat-bot"
                }`}
              >
                {msg.text}
              </div>
            ))}
            {isTyping && <p className="chat-bot">Typing...</p>}
          </div>

          <div className="chat-input-container d-flex p-2 border-top">
            <input
              type="text"
              className="form-control me-2 chat-input"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleMessageSend()}
              placeholder="Ask me about stocks or finance..."
            />
            <button className="btn chatbot-send" onClick={handleMessageSend}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
