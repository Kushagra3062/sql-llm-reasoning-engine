import React from 'react';
import './HeroBackground.css';

export const HeroBackground = () => {
    // Generate random particles
    const particles = Array.from({ length: 20 }).map((_, i) => ({
        id: i,
        posX: Math.random() * 100 + '%',
        delay: Math.random() * 5 + 's',
        duration: 5 + Math.random() * 10 + 's',
        size: 2 + Math.random() * 3 + 'px'
    }));

    return (
        <div className="hero-bg-container">
            <div className="perspective-grid"></div>
            <div className="floating-particles">
                {particles.map(p => (
                    <div
                        key={p.id}
                        className="bg-particle"
                        style={{
                            '--pos-x': p.posX,
                            '--delay': p.delay,
                            '--duration': p.duration,
                            '--size': p.size
                        }}
                    />
                ))}
            </div>
        </div>
    );
};
