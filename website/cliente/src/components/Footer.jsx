import React from 'react';
import { FaTwitter, FaInstagram, FaWhatsapp, FaGithub } from 'react-icons/fa';
import logo from '../assets/logo.png';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-brand">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '15px' }}>
                            <img src={logo} alt="BTube Logo" style={{ height: '35px' }} />
                            <h3 style={{ margin: 0 }}>BTube</h3>
                        </div>
                        <p>A melhor forma de experienciar o YouTube.</p>
                    </div>
                    <div className="footer-links">
                        <a href="#">Privacidade</a>
                        <a href="#">Termos</a>
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer">Github</a>
                        <a href="#">Suporte</a>
                    </div>
                    <div className="footer-social">
                        <a href="https://x.com/kcorporation" target="_blank" rel="noopener noreferrer"><FaTwitter /></a>
                        <a href="https://instagram.com/KCorp" target="_blank" rel="noopener noreferrer"><FaInstagram /></a>
                        <a href="https://wa.me/244923456789" target="_blank" rel="noopener noreferrer"><FaWhatsapp /></a>
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer"><FaGithub /></a>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>&copy; {new Date().getFullYear()} BTube Software. Um produto KCorp.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;