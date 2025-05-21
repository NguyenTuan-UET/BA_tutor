import React from 'react';
import './ChatMessage.css';

const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {!isUser && (
        <div className="avatar bot-avatar">
          🤖
        </div>
      )}
      <div className="message-content">
        <p>{message}</p>
      </div>
      {isUser && (
        <div className="avatar user-avatar">
          👤
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
