// my-website/src/components/RAGChatbot/index.tsx

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios'; // Import axios
import styles from './styles.module.css';

interface ChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  mode?: 'Full Book Search' | 'Context from Selection';
  timestamp: Date;
  isError?: boolean;
}

const RAGChatbot: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputQuery, setInputQuery] = useState<string>('');
  const [selectedContext, setSelectedContext] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const handleTextSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().length > 0) {
        setSelectedContext(selection.toString());
      } else {
        setSelectedContext(null);
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('keyup', handleTextSelection); // For keyboard selection

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('keyup', handleTextSelection);
    };
  }, []); // Run once on mount to set up listeners

  const sendMessage = async (query: string, context: string | null = null) => {
    if (!query.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString() + '-user',
      sender: 'user',
      text: query,
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputQuery('');
    setError(null);
    setIsLoading(true);

    try {
      const payload: { query: string; context?: string } = { query };
      if (context) {
        payload.context = context;
      }

      const response = await axios.post('http://localhost:8000/api/chat', payload);
      const agentResponse: string = response.data.answer;
      const mode: 'Full Book Search' | 'Context from Selection' = context ? 'Context from Selection' : 'Full Book Search';

      const newAgentMessage: ChatMessage = {
        id: Date.now().toString() + '-agent',
        sender: 'agent',
        text: agentResponse,
        mode: mode,
        timestamp: new Date(),
      };
      setMessages((prevMessages) => [...prevMessages, newAgentMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      const errorMessage = (err as any).response?.data?.detail || 'Failed to get a response from the agent.';
      const newErrorMessage: ChatMessage = {
        id: Date.now().toString() + '-error',
        sender: 'agent',
        text: errorMessage,
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prevMessages) => [...prevMessages, newErrorMessage]);
      setError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
      setSelectedContext(null); // Clear context after sending
    }
  };

  const handleSendClick = () => {
    sendMessage(inputQuery, selectedContext);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendClick();
    }
  };

  return (
    <div className={styles.chatContainer}>
      <h3>RAG Chatbot</h3>
      {selectedContext && (
        <div className={styles.selectedContextDisplay}>
          <p>Context from selection:</p>
          <p className={styles.contextText}>{selectedContext}</p>
          <button className={styles.clearContextButton} onClick={() => setSelectedContext(null)}>Clear Context</button>
        </div>
      )}
      {/* Chat messages display area */}
      <div className={styles.messagesDisplay}>
        {messages.length === 0 ? (
          <p className={styles.systemMessage}>Start a conversation...</p>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`${styles.message} ${msg.sender === 'user' ? styles.userMessage : styles.agentMessage} ${msg.isError ? styles.messageError : ''}`}>
              <p>{msg.text}</p>
              <div className={styles.messageMeta}>
                {msg.sender === 'agent' && msg.mode && <span className={styles.messageMode}>Mode: {msg.mode} | </span>}
                <span className={styles.messageTime}>{msg.timestamp.toLocaleTimeString()}</span>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      {/* Chat input field */}
      <div className={styles.inputArea}>
        <input 
          type="text" 
          placeholder={selectedContext ? "Ask a question about the selection..." : "Ask a question..."} 
          className={styles.chatInput}
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button className={styles.sendButton} onClick={handleSendClick} disabled={isLoading}>Send</button>
      </div>
      {error && <div className={styles.errorMessage}>{error}</div>}
      {isLoading && <div className={styles.loadingMessage}>Thinking...</div>}
    </div>
  );
};

export default RAGChatbot;



