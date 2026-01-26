import React, { useState } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';
import { AuthModal } from './AuthModal';
import { User, Linkedin, Twitter } from 'lucide-react';
import './LandingPage.css';

export const LeadershipPage = ({ onNavigate, onLogin }) => {
    const [isAuthOpen, setIsAuthOpen] = useState(false);

    const openAuth = () => setIsAuthOpen(true);
    const closeAuth = () => setIsAuthOpen(false);

    const leaders = [
        {
            name: "Ameya Balange",
            role: "CEO",
            color: "var(--accent-primary)"
        },
        {
            name: "Shrut Jain",
            role: "CTO",
            color: "#3b82f6"
        },
        {
            name: "Kushagra Singh",
            role: "COO",
            color: "#10b981"
        },
        {
            name: "Rishabh Jain",
            role: "CSO",
            color: "#f59e0b"
        },
        {
            name: "Tanmay Dixit",
            role: "CHRO",
            color: "#1d9341ff"
        }
    ];

    return (
        <div className="landing-container">
            <div className="glow-effect" />

            <Header onLoginClick={openAuth} onNavigate={onNavigate} />

            <main className="landing-section leadership-section">
                <div className="section-content">
                    <div className="center-text">
                        <h1 className="hero-title" style={{ fontSize: '3rem', marginBottom: '1rem' }}>Our Leadership</h1>
                        <p className="hero-subtitle">Meet the visionaries behind DataQuery AI.</p>
                    </div>

                    <div className="leadership-grid">
                        {leaders.map((leader, idx) => (
                            <div key={idx} className="leader-card">
                                <div className="leader-avatar flex-center" style={{ borderColor: leader.color }}>
                                    <User size={64} color={leader.color} />
                                </div>
                                <h3 className="leader-name">{leader.name}</h3>
                                <p className="leader-role" style={{ color: leader.color }}>{leader.role}</p>
                                <p className="leader-bio">{leader.bio}</p>

                                <div className="leader-socials">
                                    <Linkedin size={20} className="social-icon" />
                                    <Twitter size={20} className="social-icon" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </main>

            <Footer onNavigate={onNavigate} />

            <AuthModal
                isOpen={isAuthOpen}
                onClose={closeAuth}
                onLogin={onLogin}
            />
        </div>
    );
};
