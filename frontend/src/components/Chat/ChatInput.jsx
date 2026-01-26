import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';
import './ChatInput.css';

export function ChatInput({ onSend, disabled }) {
    const [value, setValue] = useState('');
    const textareaRef = useRef(null);

    const adjustHeight = () => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
        }
    };

    useEffect(() => {
        adjustHeight();
    }, [value]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleSubmit = () => {
        if (value.trim() && !disabled) {
            onSend(value.trim());
            setValue('');
        }
    };

    return (
        <div className="chat-input-container">
            <div className="chat-input-wrapper">
                <textarea
                    ref={textareaRef}
                    className="chat-input-field"
                    placeholder="Ask a question about your data..."
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    rows={1}
                    disabled={disabled}
                />
                <button
                    className="send-button"
                    onClick={handleSubmit}
                    disabled={!value.trim() || disabled}
                >
                    <ArrowUp size={18} />
                </button>
            </div>
            <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
                <small className="text-muted text-xs">
                    AI can make mistakes. Please verify generated SQL.
                </small>
            </div>
        </div>
    );
}
