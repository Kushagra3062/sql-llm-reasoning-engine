import React from 'react';
import { Database } from 'lucide-react';

export const Header = ({ onLoginClick, onNavigate }) => {
    return (
        <header className="landing-header">
            <div className="logo-container" onClick={() => onNavigate && onNavigate('landing')}>
                <Database className="logo-icon" size={28} />
                <span>DataQuery AI</span>
            </div>



            <div className="nav-buttons">
                <button className="btn-secondary" onClick={onLoginClick}>
                    Log in
                </button>
                <button className="btn-primary" onClick={onLoginClick}>
                    Get Started
                </button>
            </div>
        </header>
    );
};
