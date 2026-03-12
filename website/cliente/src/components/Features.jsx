import React from 'react';
import { motion } from 'framer-motion';
import { MdBlock, MdFileDownload, MdHeadset, MdWorkspacePremium, MdFlashOn, MdSecurity } from 'react-icons/md';

const Features = () => {
    const features = [
        {
            icon: <MdBlock />,
            title: 'Sem Anúncios',
            description: 'Aproveite seus vídeos favoritos sem interrupções irritantes antes, durante ou depois.',
            color: 'var(--accent-primary)'
        },
        {
            icon: <MdFileDownload />,
            title: 'Downloads 4K',
            description: 'Baixe vídeos e playlists completas em altíssima resolução para ver offline.',
            color: 'var(--accent-blue)'
        },
        {
            icon: <MdHeadset />,
            title: 'Background Play',
            description: 'Continue ouvindo o áudio mesmo com a tela do celular desligada ou em outro app.',
            color: 'var(--accent-green)'
        },
        {
            icon: <MdWorkspacePremium />,
            title: 'Qualidade Premium',
            description: 'Acesso a recursos que você só encontraria em assinaturas caras, de forma nativa.',
            color: 'var(--accent-primary)'
        },
        {
            icon: <MdFlashOn />,
            title: 'Ultra Leve',
            description: 'Consome menos memória e bateria que o aplicativo original e o site.',
            color: 'var(--accent-blue)'
        },
        {
            icon: <MdSecurity />,
            title: 'Privacidade Total',
            description: 'Não rastreamos seu histórico de busca ou dados pessoais. Você está no controle.',
            color: 'var(--accent-green)'
        }
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
    };

    return (
        <section id="features" className="features">
            <div className="container">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                >
                    <h2>Recursos <span className="highlight">Poderosos</span></h2>
                    <p className="section-subtitle">Tudo o que você precisa para dominar o YouTube</p>
                </motion.div>

                <motion.div
                    className="features-grid"
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                >
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            className="feature-card"
                            variants={itemVariants}
                            whileHover={{ scale: 1.05, borderColor: feature.color }}
                        >
                            <div className="feature-icon" style={{ color: feature.color }}>{feature.icon}</div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};

export default Features;