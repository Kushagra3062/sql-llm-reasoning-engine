import React, { useState } from 'react';
import { ChevronDown, ChevronRight, BrainCircuit, CheckCircle2 } from 'lucide-react';
import './ReasoningAccordion.css';

export function ReasoningAccordion({ steps = [] }) {
    const [isOpen, setIsOpen] = useState(false);

    if (!steps || steps.length === 0) return null;

    return (
        <div className="reasoning-accordion">
            <div className="reasoning-header" onClick={() => setIsOpen(!isOpen)}>
                <div className="reasoning-title">
                    <BrainCircuit size={16} />
                    <span>Reasoning Process</span>
                </div>
                {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </div>

            {isOpen && (
                <div className="reasoning-content">
                    {steps.map((step, idx) => (
                        <div key={idx} className="reasoning-step">
                            <div className="step-icon">
                                <CheckCircle2 size={14} />
                            </div>
                            <span className="step-text">{step}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
