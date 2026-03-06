import React from 'react';

const Features = () => {
    const features = [
        {
            icon: '🚫',
            title: 'Sem Anúncios',
            description: 'Aproveite seus vídeos favoritos sem interrupções irritantes antes, durante ou depois.'
        },
        {
            icon: '📥',
            title: 'Downloads 4K',
            description: 'Baixe vídeos e playlists completas em altíssima resolução para ver offline.'
        },
        {
            icon: '🎧',
            title: 'Background Play',
            description: 'Continue ouvindo o áudio mesmo com a tela do celular desligada ou em outro app.'
        },
        {
            icon: '💎',
            title: 'Qualidade Premium',
            description: 'Acesso a recursos que você só encontraria em assinaturas caras, de forma nativa.'
        },
        {
            icon: '⚡',
            title: 'Ultra Leve',
            description: 'Consome menos memória e bateria que o aplicativo original e o site.'
        },
        {
            icon: '🔒',
            title: 'Privacidade Total',
            description: 'Não rastreamos seu histórico de busca ou dados pessoais. Você está no controle.'
        }
    ];

    return (
        <section id="features" className="features">
            <div className="container">
                <h2>Recursos <span className="highlight">Poderosos</span></h2>
                <p className="section-subtitle">Tudo o que você precisa para dominar o YouTube</p>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <div key={index} className="feature-card">
                            <div className="feature-icon">{feature.icon}</div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Features;