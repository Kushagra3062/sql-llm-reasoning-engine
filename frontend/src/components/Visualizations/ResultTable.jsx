import React from 'react';
import './ResultTable.css';

export function ResultTable({ data }) {
    if (!data || !data.columns || !data.rows) return null;

    return (
        <div className="result-table-container">
            <div className="result-table-wrapper">
                <table className="result-table">
                    <thead>
                        <tr>
                            {data.columns.map((col, idx) => (
                                <th key={idx}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.rows.map((row, rIdx) => (
                            <tr key={rIdx}>
                                {row.map((cell, cIdx) => (
                                    <td key={cIdx}>{cell}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="result-summary">
                Showing {data.rows.length} result{data.rows.length !== 1 && 's'}
            </div>
        </div>
    );
}
