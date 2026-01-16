import React from 'react';
import { User, Sparkles } from 'lucide-react';
import { ReasoningAccordion } from '../Visualizations/ReasoningAccordion';
import { SQLViewer } from '../Visualizations/SQLViewer';
import { ResultTable } from '../Visualizations/ResultTable';
import './MessageBubble.css';

export function MessageBubble({ message }) {
    const isUser = message.role === 'user';
    const { content, reasoning, sql, data } = message;

    return (
        <div className="message-container">
            <div className={`message-avatar ${isUser ? 'avatar-user' : 'avatar-ai'}`}>
                {isUser ? <User size={18} /> : <Sparkles size={18} />}
            </div>

            <div className="message-content">
                {isUser ? (
                    <div className="user-text">
                        {content}
                    </div>
                ) : (
                    <div className="ai-content">
                        {reasoning && <ReasoningAccordion steps={reasoning} />}
                        {sql && <SQLViewer sql={sql} />}
                        {/* The main text content often summarizes the data */}
                        {content && <div className="user-text">{content}</div>}
                        {data && <ResultTable data={data} />}
                    </div>
                )}
            </div>
        </div>
    );
}
