import React from 'react';
import { Sparkles } from 'lucide-react';
import './ThinkingIndicator.css';

export function ThinkingIndicator() {
    return (
        <div className="thinking-container">
            <Sparkles size={16} className="text-muted" />
            <span>Reasoning...</span>
            <div className="thinking-dots">
                <div className="thinking-dot"></div>
                <div className="thinking-dot"></div>
                <div className="thinking-dot"></div>
            </div>
        </div>
    );
}
