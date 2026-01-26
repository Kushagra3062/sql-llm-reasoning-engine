import React, { useState } from 'react';
import { Database, Clock, ChevronRight, ChevronDown, LayoutList, Columns } from 'lucide-react';
import './Sidebar.css';

// Mock schema for visualization
const SCHEMA = {
    'Artist': ['ArtistId', 'Name'],
    'Album': ['AlbumId', 'Title', 'ArtistId'],
    'Track': ['TrackId', 'Name', 'AlbumId', 'MediaTypeId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice'],
    'Playlist': ['PlaylistId', 'Name'],
    'Genre': ['GenreId', 'Name'],
    'Customer': ['CustomerId', 'FirstName', 'LastName', 'Company', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email', 'SupportRepId'],
    'Invoice': ['InvoiceId', 'CustomerId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total'],
    'Employee': ['EmployeeId', 'LastName', 'FirstName', 'Title', 'ReportsTo', 'BirthDate', 'HireDate', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email']
};

export function Sidebar({ onQuerySelect }) {
    const [expandedTable, setExpandedTable] = useState(null);

    const toggleTable = (table) => {
        setExpandedTable(expandedTable === table ? null : table);
    };

    const QUERIES = [
        "How many customers are from Brazil?",
        "Which 5 artists have the most tracks?",
        "Which customers have never made a purchase?",
        "Show me recent orders"
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
        </div>
    );
}
