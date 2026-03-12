import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';
import { FaRocket } from 'react-icons/fa';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="container">
                <Link to="/" className="logo">
                    <img src={logo} alt="BTube Logo" style={{ height: '40px' }} />
                    <span className="logo-text">BTube</span>
                    <span className="logo-badge">PRO</span>
                </Link>
                <div className="nav-links">
                    <a href="#features">Recursos</a>
                    <a href="#pricing">Preços</a>
                    <a href="#download">Download</a>
                    <a href="#faq">FAQ</a>
                </div>
                <div className="nav-actions">
                    <Link to="/" className="btn btn-primary">
                        <FaRocket style={{ marginRight: '8px' }} />
                        Começar
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;