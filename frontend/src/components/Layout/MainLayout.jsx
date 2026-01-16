import React from 'react';
import { Sidebar } from './Sidebar';
import './MainLayout.css';

export function MainLayout({ children, sidebar }) {
    return (
        <div className="main-layout">
            {sidebar || <Sidebar />}
            <main className="main-content">
                {children}
            </main>
        </div>
    );
}
