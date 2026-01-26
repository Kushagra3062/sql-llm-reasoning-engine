import React, { useState } from 'react';
import { MainLayout } from './components/Layout/MainLayout';
import { Sidebar } from './components/Layout/Sidebar';
import { ChatInput } from './components/Chat/ChatInput';
import { MessageBubble } from './components/Chat/MessageBubble';
import { ThinkingIndicator } from './components/Chat/ThinkingIndicator';
import { LandingPage } from './components/LandingPage/LandingPage';
import { LeadershipPage } from './components/LandingPage/LeadershipPage';
import { ConnectDbModal } from './components/LandingPage/ConnectDbModal';
import { Database } from 'lucide-react';
import { runQuery } from './api';
import './index.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showDbConfig, setShowDbConfig] = useState(false);
  const [publicPage, setPublicPage] = useState('landing'); // 'landing' | 'leadership'
  const [messages, setMessages] = useState([
    {
      role: 'system',
      content: 'Hello! I can help you query the Chinook database. Ask me anything about artists, albums, or sales.'
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [pendingQuery, setPendingQuery] = useState(null); // Store the query that triggered ambiguity

  const handleLogin = () => {
    setShowDbConfig(true);
  };

  const handleDbConnect = (dbUrl) => {
    console.log("Connected to DB:", dbUrl);
    // Here you would typically save the DB URL or configure the backend
    setShowDbConfig(false);
    setIsAuthenticated(true);
  };

  if (showDbConfig) {
    return <ConnectDbModal onConnect={handleDbConnect} />;
  }

  const handleSend = (text) => {
    // Add User Message
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    if (pendingQuery) {
      // User is answering an ambiguity
      // Treat 'text' as the choice (integer or string)
      console.log("Resuming query:", pendingQuery, "with choice:", text);

      let choice = text;
      // Try to parse as int if generic
      if (!isNaN(parseInt(text))) {
        choice = parseInt(text);
      }

      runQuery(pendingQuery, choice).then(handleResponse);
      setPendingQuery(null); // Clear pending state
    } else {
      // Normal query
      runQuery(text).then(handleResponse);
    }
  };

  const handleResponse = (response) => {
    // Logic to handle interruption
    if (response.type === 'interruption') {
      if (response.mcq_options && response.mcq_options.length > 0) {
        response.content += "\n\nOptions:\n" + response.mcq_options.map((opt, i) => `${i + 1}. ${opt}`).join("\n");
      }
      // We need to remember this query was interrupted!
      // The backend API for resume expects {"query": "original", "human_choice": ...}
      // api.js constructs payload with query.
      // So we can just pass "RESPONSED_TO_AMBIGUITY" or empty string as query, 
      // dependent on what api.js sends.
      setPendingQuery("RESUMING_AMBIGUITY");
    }
    setMessages(prev => [...prev, response]);
    setIsTyping(false);
  };

  if (!isAuthenticated) {
    if (publicPage === 'leadership') {
      return <LeadershipPage onNavigate={setPublicPage} onLogin={handleLogin} />;
    }
    return <LandingPage onNavigate={setPublicPage} onLogin={handleLogin} />;
  }

  return (
    <MainLayout sidebar={<Sidebar onQuerySelect={handleSend} />}>
      <div className="chat-container">
        {messages.length === 0 ? (
          <div style={{
            height: '100%', display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center', opacity: 0.5
          }}>
            <Database size={64} style={{ marginBottom: '1rem', color: 'var(--accent-primary)' }} />
            <h2>Start a conversation</h2>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble key={idx} message={msg} />
          ))
        )}
        {isTyping && <ThinkingIndicator />}
      </div>
      <ChatInput onSend={handleSend} disabled={isTyping} />
    </MainLayout>
  );
}

export default App;
