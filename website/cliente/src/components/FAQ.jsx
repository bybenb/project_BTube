import React from 'react';
import { motion } from 'framer-motion';

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
                <motion.h2
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >Perguntas <span className="highlight">Frequentes</span></motion.h2>
                <div className="faq-grid">
                    {questions.map((item, index) => (
                        <motion.div
                            key={index}
                            className="faq-item"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <h3>{item.q}</h3>
                            <p>{item.a}</p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default FAQ;