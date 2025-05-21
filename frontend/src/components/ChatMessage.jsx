import React from 'react';
import './ChatMessage.css';
import baIcon from '../assets/BA_icon.png';

const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {!isUser && (
        <div className="avatar bot-avatar">
          <img src={baIcon} alt="BA Tutor" className="avatar-image" />
        </div>
      )}
      <div className="message-content">
        <p>{message}</p>
      </div>

      {/* {isUser && <div className="avatar user-avatar">👤</div>} */}
    </div>
  );
};

export default ChatMessage;
