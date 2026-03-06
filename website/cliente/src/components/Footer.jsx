import React from 'react';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-brand">
                        <h3>BTube</h3>
                        <p>A melhor forma de experienciar o YouTube.</p>
                    </div>
                    <div className="footer-links">
                        <a href="#">Privacidade</a>
                        <a href="#">Termos</a>
                        <a href="#">Github</a>
                        <a href="#">Suporte</a>
                    </div>
                    <div className="footer-social">
                        <a href="#">🐦</a>
                        <a href="#">📸</a>
                        <a href="#">💬</a>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>&copy; {new Date().getFullYear()} BTube Software. Todos os direitos reservados.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;