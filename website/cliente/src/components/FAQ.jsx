import React from 'react';

const FAQ = () => {
    const questions = [
        {
            q: "O BTube é seguro?",
            a: "Sim, o BTube é totalmente seguro e de código aberto. Não coletamos seus dados pessoais e todas as conexões são encriptadas."
        },
        {
            q: "Preciso de uma conta Google?",
            a: "Você pode usar o BTube sem logar, mas se quiser ver suas inscrições e playlists, pode fazer o login de forma segura."
        },
        {
            q: "Como funcionam as atualizações?",
            a: "O app verifica automaticamente por atualizações a cada inicialização e avisa quando uma nova versão estiver disponível."
        },
        {
            q: "Posso baixar músicas em MP3?",
            a: "Com certeza! O BTube permite extrair o áudio de qualquer vídeo em alta qualidade com apenas um clique."
        }
    ];

    return (
        <section id="faq" className="faq">
            <div className="container">
                <h2>Perguntas <span className="highlight">Frequentes</span></h2>
                <div className="faq-grid">
                    {questions.map((item, index) => (
                        <div key={index} className="faq-item">
                            <h3>{item.q}</h3>
                            <p>{item.a}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default FAQ;