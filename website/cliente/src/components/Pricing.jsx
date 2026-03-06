import React from 'react';

const Pricing = ({ onSelectPlan }) => {
    return (
        <section id="pricing" className="pricing">
            <div className="container">
                <h2>Planos <span className="highlight">Simples</span></h2>
                <p className="section-subtitle">Escolha o que melhor se adapta às suas necessidades</p>

                <div className="pricing-grid">
                    <div className="pricing-card">
                        <div className="pricing-header">
                            <h3>Básico</h3>
                            <div className="price">Grátis</div>
                            <p className="price-period">Para sempre</p>
                        </div>
                        <ul className="features-list">
                            <li>Bloqueio de Anúncios</li>
                            <li>Modo Escuro Nativo</li>
                            <li>Download 720p</li>
                            <li style={{ textDecoration: 'line-through', opacity: 0.5 }}>PiP Mode</li>
                        </ul>
                        <button className="btn btn-outline btn-block" onClick={() => onSelectPlan('free')}>Começar Grátis</button>
                    </div>

                    <div className="pricing-card popular">
                        <div className="popular-badge">Mais Popular</div>
                        <div className="pricing-header">
                            <h3>Pro</h3>
                            <div className="price">R$ 19<small>,90</small></div>
                            <p className="price-period">Pagamento único</p>
                        </div>
                        <ul className="features-list">
                            <li>Tudo do Grátis</li>
                            <li>Downloads 4K / MP3</li>
                            <li>Background Play</li>
                            <li>Suporte Prioritário</li>
                        </ul>
                        <button className="btn btn-primary btn-block" onClick={() => onSelectPlan('pro')}>Adquirir agora</button>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Pricing;