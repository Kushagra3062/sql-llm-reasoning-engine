import React from 'react';

export const Footer = ({ onNavigate }) => {
    return (
        <footer className="landing-footer">
            <div className="footer-content">
                <div className="footer-links">
                    <a onClick={() => onNavigate && onNavigate('landing')} className="footer-link">Home</a>
                    <a onClick={() => onNavigate && onNavigate('leadership')} className="footer-link">Leadership</a>
                    <a href="#about" onClick={(e) => {
                        if (onNavigate) onNavigate('landing');
                    }} className="footer-link">About Us</a>
                    <a href="#contact" className="footer-link">Contact</a>
                </div>
                <p className="copyright">&copy; {new Date().getFullYear()} DataQuery AI. All rights reserved.</p>
            </div>
        </footer>
    );
};
