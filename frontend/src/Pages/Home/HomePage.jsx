import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from '../../components/ChatMessage';
import './HomePage.css';
import baIcon from '../../assets/BA_icon.png';

const HomePage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      isUser: true,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:3001/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: inputMessage }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      const botMessage = {
        text: data.answer,
        isUser: false,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-left">
          {' '}
          <h1 className="header-title">
            <div className="bot-icon">
              <img src={baIcon} alt="BA Tutor" className="bot-icon-image" />
            </div>
            <span>BA Tutor</span>
          </h1>
        </div>
        <div className="header-right">
          <span className="bot-status">AI Assistant Online</span>
        </div>
      </header>

      <div className="messages-container">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
        ))}
        {isTyping && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSendMessage} className="chat-input-form">
          <textarea
            className="chat-input"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={handleKeyPress} // ✅ dùng onKeyDown, không dùng onKeyPress
            placeholder="Nhập tin nhắn của bạn..."
            rows="1"
          />
          <button
            type="submit"
            className="send-button"
            disabled={!inputMessage.trim()}
          >
            Gửi
          </button>
        </form>
      </div>

      <footer className="chat-footer">
        <p>BA Tutor có thể lỗi, cần kiểm tra lại thông tin</p>
      </footer>
    </div>
  );
};

export default HomePage;
