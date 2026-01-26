import React, { useState } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';
import { AuthModal } from './AuthModal';
import { MissionSection } from './MissionSection';
import { AboutSection } from './AboutSection';
import { Zap, Shield, BarChart2 } from 'lucide-react';
import { HeroBackground } from './HeroBackground';
import './LandingPage.css';

export const LandingPage = ({ onLogin, onNavigate }) => {
    const [isAuthOpen, setIsAuthOpen] = useState(false);

    const openAuth = () => {
        console.log("Opening Auth Modal");
        setIsAuthOpen(true);
    };
    const closeAuth = () => {
        console.log("Closing Auth Modal");
        setIsAuthOpen(false);
    };

    return (
        <div className="landing-container">
            <div className="glow-effect" />

            <Header onLoginClick={openAuth} onNavigate={onNavigate} />

            <main>
                <div className="landing-hero">
                    <HeroBackground />
                    <div className="hero-content">
                        <h1 className="hero-title">
                            Intelligent Data Analysis <br /> at Your Fingertips
                        </h1>
                        <p className="hero-subtitle">
                            Transform your SQL data into actionable insights with our advanced reasoning engine.
                            Ask questions, get answers, and visualize results instantly.
                        </p>

                        <div className="hero-actions">
                            <button className="btn-primary hero-btn-lg" onClick={openAuth}>
                                Start Analyzing Now
                            </button>
                        </div>
                    </div>
                </div>

                <section id="features" className="landing-section features-section">
                    <div className="section-content">
                        <div className="features-grid">
                            <div className="feature-card">
                                <Zap className="feature-icon" size={32} />
                                <h3 className="feature-title">Lightning Fast</h3>
                                <p className="feature-desc">
                                    Get real-time answers to complex queries without writing a single line of SQL.
                                </p>
                            </div>
                            <div className="feature-card">
                                <Shield className="feature-icon" size={32} />
                                <h3 className="feature-title">Secure by Design</h3>
                                <p className="feature-desc">
                                    Enterprise-grade security ensures your data remains protected and private.
                                </p>
                            </div>
                            <div className="feature-card">
                                <BarChart2 className="feature-icon" size={32} />
                                <h3 className="feature-title">Visual Insights</h3>
                                <p className="feature-desc">
                                    Automatically generate charts and graphs to visualize your data trends.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                <MissionSection />

                <AboutSection />
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
