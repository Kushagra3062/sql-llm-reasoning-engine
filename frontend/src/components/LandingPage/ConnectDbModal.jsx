import React, { useState } from 'react';
import { Database, Link, ArrowRight } from 'lucide-react';
import './LandingPage.css';

export const ConnectDbModal = ({ onConnect }) => {
    const [dbUrl, setDbUrl] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        // Simulate connection delay
        setTimeout(() => {
            setLoading(false);
            onConnect(dbUrl);
        }, 1000);
    };

    return (
        <div className="modal-overlay">
            <div className="auth-modal">
                <div className="auth-header">
                    <div style={{
                        margin: '0 auto 1.5rem',
                        width: '64px',
                        height: '64px',
                        borderRadius: '50%',
                        background: 'rgba(139, 92, 246, 0.1)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--accent-primary)'
                    }}>
                        <Database size={32} />
                    </div>
                    <h2 className="auth-title">Connect your Database</h2>
                    <p className="auth-subtitle">
                        Enter your PostgreSQL database URL to start analyzing your data.
                    </p>
                </div>

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Database URL</label>
                        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                            <Link size={18} style={{ position: 'absolute', left: '12px', color: 'var(--text-muted)' }} />
                            <input
                                type="text"
                                className="form-input"
                                placeholder="postgresql://user:password@localhost:5432/dbname"
                                style={{ paddingLeft: '40px', width: '100%' }}
                                value={dbUrl}
                                onChange={(e) => setDbUrl(e.target.value)}
                                required
                            />
                        </div>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                            We need this to generate SQL queries for your schema.
                        </p>
                    </div>

                    <button type="submit" className="btn-primary submit-btn flex-center" disabled={loading}>
                        {loading ? 'Connecting...' : (
                            <>
                                Connect Database
                                <ArrowRight size={18} style={{ marginLeft: '8px' }} />
                            </>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};
