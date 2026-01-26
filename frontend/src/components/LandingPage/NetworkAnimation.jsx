import React from 'react';
import './NetworkAnimation.css';

export const NetworkAnimation = () => {
    return (
        <div className="network-anim-container">
            <div className="orbit-system">
                <div className="center-core"></div>
                <div className="core-pulse"></div>

                <div className="orbit-ring ring-1" style={{ '--rx': '70deg', '--ry': '0deg' }}>
                    <div className="electron"></div>
                </div>

                <div className="orbit-ring ring-2" style={{ '--rx': '10deg', '--ry': '60deg' }}>
                    <div className="electron"></div>
                </div>

                <div className="orbit-ring ring-3" style={{ '--rx': '0deg', '--ry': '-45deg' }}>
                    <div className="electron"></div>
                </div>
            </div>

            <div className="floating-tag tag-1">Natural Language</div>
            <div className="floating-tag tag-2">SQL Generation</div>
            <div className="floating-tag tag-3">Reasoning Engine</div>
        </div>
    );
};
