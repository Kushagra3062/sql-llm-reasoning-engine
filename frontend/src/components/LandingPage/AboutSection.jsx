import React from 'react';
import { NetworkAnimation } from './NetworkAnimation';

export const AboutSection = () => {
    return (
        <section id="about" className="landing-section about-section">
            <div className="section-content">
                <div className="split-layout">
                    <div className="text-column">
                        <h2 className="section-title">About DataQuery AI</h2>
                        <p className="section-text">
                            Founded in 2026, DataQuery AI was born from a simple observation: organizations possess vast amounts of data, but accessing it requires improved technical skills.
                        </p>
                        <p className="section-text">
                            We are a team of data scientists, engineers, and designers dedicated to bridging the gap between human questions and database answers. By leveraging state-of-the-art Large Language Models and our proprietary reasoning engine, we turn SQL databases into conversational partners.
                        </p>
                    </div>
                    <div className="image-column">
                        <NetworkAnimation />
                    </div>
                </div>
            </div>
        </section>
    );
};
