import React from 'react';
import { motion } from 'framer-motion';
import { FaUsers, FaDownload, FaShieldAlt } from 'react-icons/fa';

const Hero = ({ stats }) => {
    return (
        <section className="hero">
            <div className="container">
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <h1>Sua experiência do <span className="highlight">YouTube</span> elevada ao máximo</h1>
                    <p className="subtitle">
                        Bloqueio de anúncios, download de vídeos em 4K, reprodução em segundo plano e muito mais.
                        Tudo em um único cliente leve e poderoso.
                    </p>

                    <div className="hero-buttons">
                        <a href="#download" className="btn btn-primary btn-large">
                            <FaDownload style={{ marginRight: '10px' }} />
                            Baixar Agora
                        </a>
                        <a href="#features" className="btn btn-outline btn-large">Ver Recursos</a>
                    </div>

                    <div className="trust-badges">
                        <span><FaUsers className="icon-green" /> {stats.users.toLocaleString()} usuários ativos</span>
                        <span><FaDownload className="icon-blue" /> {stats.downloads.toLocaleString()} downloads</span>
                        <span><FaShieldAlt className="icon-red" /> 100% Seguro</span>
                    </div>
                </motion.div>
                <motion.div
                    className="hero-image"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                >
                    <img src="https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&q=80&w=800" alt="BTube App Preview" />
                </motion.div>
            </div>
        </section>
    );
};

export default Hero;