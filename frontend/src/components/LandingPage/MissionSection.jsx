import React from 'react';
import { Target, Globe, Users } from 'lucide-react';

export const MissionSection = () => {
    return (
        <section id="mission" className="landing-section mission-section">
            <div className="section-content">
                <div className="section-header center-text">
                    <h2 className="section-title">Our Mission</h2>
                    <p className="section-subtitle">Empowering every organization to make data-driven decisions.</p>
                </div>

                <div className="mission-grid">
                    <div className="mission-card">
                        <div className="icon-box">
                            <Target size={32} />
                        </div>
                        <h3>Precision</h3>
                        <p>Delivering accurate, context-aware insights from your complex data structures.</p>
                    </div>
                    <div className="mission-card">
                        <div className="icon-box">
                            <Globe size={32} />
                        </div>
                        <h3>Accessibility</h3>
                        <p>Breaking down technical barriers so anyone can query databases using natural language.</p>
                    </div>
                    <div className="mission-card">
                        <div className="icon-box">
                            <Users size={32} />
                        </div>
                        <h3>Collaboration</h3>
                        <p>Fostering a culture where data insights are tailored of every team member.</p>
                    </div>
                </div>
            </div>
        </section>
    );
};
