import React, { useState } from 'react';
import { Database, Clock, ChevronRight, ChevronDown, LayoutList, Columns, LogOut } from 'lucide-react';
import { auth } from '../../firebase';
import './Sidebar.css';

// Mock schema for visualization
const SCHEMA = {
    'financial_statements': ['id', 'company_id', 'year', 'market_cap_billion', 'revenue', 'gross_profit', 'net_income', 'earning_per_share', 'ebitda', 'shareholder_equity', 'cashflow_operating', 'cashflow_investing', 'cashflow_financing', 'current_ratio', 'debt_equity_ratio', 'roe', 'roa', 'roi', 'net_profit_margin', 'free_cashflow_per_share', 'return_on_tangible_equity', 'number_of_employees', 'inflation_rate_us', 'version', 'scrape_timestamp', 'source'],
    'metadata_versions': ['version_id', 'version', 'scrape_timestamp', 'source', 'notes', 'data_type'],
    'companies': ['company_id', 'company_name', 'category', 'symbol'],
    'market_prices': ['id', 'company_id', 'date', 'open', 'high', 'low', 'close', 'volume', 'version', 'scrape_timestamp', 'source', 'daily_pct_change', 'ma_7', 'ma_30', 'volume_spike']
};

export function Sidebar({ onQuerySelect }) {
    const [expandedTable, setExpandedTable] = useState(null);

    const toggleTable = (table) => {
        setExpandedTable(expandedTable === table ? null : table);
    };

    const QUERIES = [
        "What was Apple's net income in 2023?",
        "Show me the revenue growth for Microsoft over the last 3 years.",
        "Which companies have a debt-to-equity ratio less than 0.5?",
        "Show me the closing prices for Nvidia in the last 30 days."
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div style={{
                    width: 32, height: 32,
                    background: 'var(--accent-primary)',
                    borderRadius: 8,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <Database size={18} color="white" />
                </div>
                <span>DataQuery AI</span>
            </div>

            <div className="sidebar-section">
                <h3>Sample Queries</h3>
                <div className="query-list">
                    {QUERIES.map((q, i) => (
                        <div key={i} className="nav-item" onClick={() => onQuerySelect && onQuerySelect(q)}>
                            <Clock size={16} />
                            <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={q}>
                                {q}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="sidebar-section" style={{ flex: 1, overflowY: 'auto' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingRight: '0.5rem' }}>
                    <h3>Database Schema</h3>
                </div>

                <div className="table-list">
                    {Object.keys(SCHEMA).map(table => (
                        <div key={table}>
                            <div
                                className={`table-item ${expandedTable === table ? 'active' : ''}`}
                                onClick={() => toggleTable(table)}
                            >
                                {expandedTable === table ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                                <LayoutList size={14} />
                                <span>{table}</span>
                            </div>

                            {expandedTable === table && (
                                <div style={{ paddingLeft: '2rem', display: 'flex', flexDirection: 'column', gap: '0.25rem', marginBottom: '0.5rem' }}>
                                    {SCHEMA[table].map(col => (
                                        <div key={col} style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <Columns size={12} />
                                            {col}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
            
            <div className="sidebar-section" style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem', marginTop: 'auto' }}>
                <div 
                    className="nav-item" 
                    style={{ color: 'var(--error, #ef4444)' }} 
                    onClick={() => {
                        auth.signOut().then(() => window.location.reload());
                    }}
                >
                    <LogOut size={16} />
                    <span>Logout / Reset Session</span>
                </div>
            </div>
        </div>
    );
}
