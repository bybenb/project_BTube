import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="container">
                <div className="logo">
                    <span className="logo-text">BTube</span>
                    <span className="logo-badge">PRO</span>
                </div>
                <div className="nav-links">
                    <a href="#features">Recursos</a>
                    <a href="#pricing">Preços</a>
                    <a href="#download">Download</a>
                    <a href="#faq">FAQ</a>
                </div>
                <div className="nav-actions">
                    <Link to="/" className="btn btn-primary">Começar Agora</Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;