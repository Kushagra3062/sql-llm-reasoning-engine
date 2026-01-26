import React from 'react';
import { Database, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import './SQLViewer.css';

export function SQLViewer({ sql }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(sql);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    // Simple syntax highlighting (naive regex based for demo)
    const highlightSQL = (text) => {
        // This is very basic, a real highlighter like Prism is better but this avoids deps
        const keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON', 'GROUP', 'BY', 'ORDER', 'LIMIT', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'AS', 'DISTINCT', 'INSERT', 'UPDATE', 'DELETE', 'IS', 'NULL', 'NOT', 'IN', 'LIKE'];

        // Split by spaces but preserve delimiters roughly
        const words = text.split(/(\s+|[,()])/);

        return words.map((word, i) => {
            if (keywords.includes(word.toUpperCase())) {
                return <span key={i} className="sql-keyword">{word}</span>;
            }
            if (/^['"].*['"]$/.test(word)) { // naive string check
                return <span key={i} className="sql-string">{word}</span>;
            }
            if (/^\d+$/.test(word)) {
                return <span key={i} className="sql-number">{word}</span>;
            }
            return word;
        });
    };

    return (
        <div className="sql-viewer">
            <div className="sql-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Database size={14} />
                    <span>Generated SQL</span>
                </div>
                <button
                    onClick={handleCopy}
                    className="text-muted hover:text-primary transition-colors"
                    style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}
                >
                    {copied ? <Check size={14} /> : <Copy size={14} />}
                    <span style={{ fontSize: '0.75rem' }}>{copied ? 'Copied' : 'Copy'}</span>
                </button>
            </div>
            <div className="sql-code-block">
                <code>
                    {highlightSQL(sql)}
                </code>
            </div>
        </div>
    );
}
