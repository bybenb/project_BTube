import React from 'react';
import { FaWindows, FaApple, FaLinux } from 'react-icons/fa';

const Download = () => {
    return (
        <section id="download" className="download">
            <div className="container">
                <div className="download-content">
                    <h2>Pronto para <span className="highlight">começar?</span></h2>
                    <p>Baixe agora o BTube e transforme sua forma de assistir vídeos. Disponível para Windows, macOS e Linux.</p>

                    <div className="download-buttons" style={{ display: 'flex', flexDirection: 'column', gap: '20px', alignItems: 'center' }}>
                        <button className="btn btn-primary btn-large" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <FaWindows />
                            Download para Windows (x64)
                        </button>

                        <div style={{ display: 'flex', gap: '15px' }}>
                            <button className="btn btn-outline" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <FaApple /> macOS
                            </button>
                            <button className="btn btn-outline" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <FaLinux /> Linux
                            </button>
                        </div>

                        <p className="small-text">Versão estável 2.4.1 - 45MB</p>
                    </div>

                    <div className="system-requirements">
                        <h4>Requisitos Mínimos:</h4>
                        <ul>
                            <li>Windows 10 ou superior</li>
                            <li>4GB de RAM</li>
                            <li>Ligação estável à Internet</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Download;