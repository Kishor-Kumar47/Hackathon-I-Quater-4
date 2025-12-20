
import React, { useState } from 'react';
import Chatbot from '../components/Chatbot'; 

export default function Root({children}) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <>
      {children}
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000,
        }}
      >
        <button
          onClick={toggleChat}
          style={{
            borderRadius: '50%',
            width: '60px',
            height: '60px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
            cursor: 'pointer',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            fontSize: '24px',
          }}
        >
          <span>&#x1F4AC;</span>
        </button>
      </div>
      {isChatOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '400px',
            height: '600px',
            border: '1px solid #ccc',
            borderRadius: '10px',
            backgroundColor: 'white',
            boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <div
            style={{
              padding: '10px',
              borderBottom: '1px solid #ccc',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <span>Chat</span>
            <button
              onClick={toggleChat}
              style={{
                border: 'none',
                background: 'transparent',
                cursor: 'pointer',
                fontSize: '16px',
              }}
            >
              &#x2715;
            </button>
          </div>
          <div style={{ flex: 1, overflow: 'auto' }}>
            <Chatbot />
          </div>
        </div>
      )}
    </>
  );
}
