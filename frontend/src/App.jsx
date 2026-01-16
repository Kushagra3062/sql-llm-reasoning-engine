import React, { useState } from 'react';
import { MainLayout } from './components/Layout/MainLayout';
import { Sidebar } from './components/Layout/Sidebar';
import { ChatInput } from './components/Chat/ChatInput';
import { MessageBubble } from './components/Chat/MessageBubble';
import { ThinkingIndicator } from './components/Chat/ThinkingIndicator';
import { Database } from 'lucide-react';
import { processQuery } from './analysis/mockService';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'system',
      content: 'Hello! I can help you query the Chinook database. Ask me anything about artists, albums, or sales.'
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = (text) => {
    // Add User Message
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    // Process Query
    processQuery(text).then(response => {
      setMessages(prev => [...prev, response]);
      setIsTyping(false);
    });
  };

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
