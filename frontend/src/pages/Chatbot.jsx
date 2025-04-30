import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./Chatbot.css";
import { FiSend, FiUser, FiMinus, FiMaximize2 } from "react-icons/fi";
import { RiRobot2Line } from "react-icons/ri";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { role: "ai", content: "Bonjour, je suis ton assistant virtuel. Comment puis-je t'aider aujourd'hui?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await api.post("/chatbot", { message: input });
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: response.data.response },
      ]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: err.response?.data?.error || "There was an error. Try again later.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`chatbot-container ${isMinimized ? "minimized" : ""}`}>
      <div className="chat-header">
        <div className="bot-icon"><RiRobot2Line /></div>
        <h3>Chatbot Assistant</h3>
        <div className="header-right">
          <div className={`status-indicator ${isLoading ? "active" : ""}`}></div>
          <button className="minimize-button" onClick={() => setIsMinimized(!isMinimized)}>
            {isMinimized ? <FiMaximize2 /> : <FiMinus />}
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="chat-window">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.role === "user" ? "user" : "ai"}`}>
                <div className="message-avatar">
                  {msg.role === "user" ? <FiUser /> : <RiRobot2Line />}
                </div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {isLoading && (
              <div className="chat-message ai">
                <div className="message-avatar"><RiRobot2Line /></div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
            />
            <button onClick={sendMessage} disabled={isLoading || !input.trim()} className="send-button">
              <FiSend />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Chatbot;
