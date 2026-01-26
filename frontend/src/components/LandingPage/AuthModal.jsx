import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { X, Mail, Lock, User, ArrowRight } from 'lucide-react';

export const AuthModal = ({ isOpen, onClose, onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            setLoading(false);
            onLogin(); // complete the mock login
            onClose();
        }, 1000);
    };

    return createPortal(
        <div className="modal-overlay" onClick={onClose}>
            <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
                <button className="close-btn" onClick={onClose}>
                    <X size={20} />
                </button>

                <div className="auth-header">
                    <h2 className="auth-title">{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
                    <p className="auth-subtitle">
                        {isLogin
                            ? 'Enter your credentials to access your workspace'
                            : 'Get started with MarketWise today'
                        }
                    </p>
                </div>

                <form className="auth-form" onSubmit={handleSubmit}>
                    {!isLogin && (
                        <div className="form-group">
                            <label className="form-label">Full Name</label>
                            <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                                <User size={18} style={{ position: 'absolute', left: '12px', color: 'var(--text-muted)' }} />
                                <input
                                    type="text"
                                    className="form-input"
                                    placeholder="John Doe"
                                    style={{ paddingLeft: '40px', width: '100%' }}
                                    required
                                />
                            </div>
                        </div>
                    )}

                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                            <Mail size={18} style={{ position: 'absolute', left: '12px', color: 'var(--text-muted)' }} />
                            <input
                                type="email"
                                className="form-input"
                                placeholder="name@company.com"
                                style={{ paddingLeft: '40px', width: '100%' }}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                            <Lock size={18} style={{ position: 'absolute', left: '12px', color: 'var(--text-muted)' }} />
                            <input
                                type="password"
                                className="form-input"
                                placeholder="••••••••"
                                style={{ paddingLeft: '40px', width: '100%' }}
                                required
                            />
                        </div>
                    </div>

                    <button type="submit" className="btn-primary submit-btn flex-center" disabled={loading}>
                        {loading ? 'Processing...' : (
                            <>
                                {isLogin ? 'Sign In' : 'Create Account'}
                                <ArrowRight size={18} style={{ marginLeft: '8px' }} />
                            </>
                        )}
                    </button>
                </form>

                <div className="auth-switch">
                    {isLogin ? "Don't have an account?" : "Already have an account?"}
                    <span className="switch-link" onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? 'Sign up' : 'Log in'}
                    </span>
                </div>
            </div>
        </div>,
        document.body
    );
};
