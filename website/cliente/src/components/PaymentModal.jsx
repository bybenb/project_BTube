// client/src/components/PaymentModal.jsx
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import axios from 'axios';
import toast from 'react-hot-toast';
import './PaymentModal.css';

const PaymentModal = ({ plan, onClose }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('card');

  const prices = {
    pro: 29.90,
    enterprise: 99.90
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (paymentMethod === 'card') {
        // Criar sessão de checkout Stripe
        const response = await axios.post('http://localhost:3001/api/payments/create-checkout', {
          plan,
          email,
          name
        });

        // Redirecionar para Stripe
        const { url } = response.data;
        window.location.href = url;
      } else if (paymentMethod === 'crypto') {
        toast.success('Endereço para pagamento em BTC gerado!');
        // Mostrar endereço BTC
      }
    } catch (error) {
      toast.error('Erro ao processar pagamento: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      <motion.div 
        className="modal-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div 
          className="modal-content"
          initial={{ scale: 0.9, y: 20 }}
          animate={{ scale: 1, y: 0 }}
          exit={{ scale: 0.9, y: 20 }}
          onClick={e => e.stopPropagation()}
        >
          <button className="close-btn" onClick={onClose}>×</button>
          
          <h2>Finalizar Compra</h2>
          <p className="plan-name">BTube {plan === 'pro' ? 'Pro' : 'Enterprise'}</p>
          <p className="price">${prices[plan]} <span>licença vitalícia</span></p>

          <div className="payment-methods">
            <button 
              className={`method ${paymentMethod === 'card' ? 'active' : ''}`}
              onClick={() => setPaymentMethod('card')}
            >
              💳 Cartão de Crédito
            </button>
            <button 
              className={`method ${paymentMethod === 'paypal' ? 'active' : ''}`}
              onClick={() => setPaymentMethod('paypal')}
            >
              🅿️ PayPal
            </button>
            <button 
              className={`method ${paymentMethod === 'crypto' ? 'active' : ''}`}
              onClick={() => setPaymentMethod('crypto')}
            >
              ₿ Criptomoedas
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {paymentMethod === 'card' && (
              <>
                <div className="form-group">
                  <label>Email</label>
                  <input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required 
                    placeholder="seu@email.com"
                  />
                </div>

                <div className="form-group">
                  <label>Nome completo</label>
                  <input 
                    type="text" 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required 
                    placeholder="Como no cartão"
                  />
                </div>

                <div className="form-group">
                  <label>Dados do cartão</label>
                  <div className="card-element">
                    <CardElement 
                      options={{
                        style: {
                          base: {
                            fontSize: '16px',
                            color: '#ffffff',
                            '::placeholder': {
                              color: '#aab7c4'
                            }
                          }
                        }
                      }}
                    />
                  </div>
                </div>
              </>
            )}

            {paymentMethod === 'paypal' && (
              <div className="paypal-info">
                <p>Você será redirecionado para o PayPal para concluir o pagamento.</p>
              </div>
            )}

            {paymentMethod === 'crypto' && (
              <div className="crypto-info">
                <p>Endereço BTC para pagamento:</p>
                <code>bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh</code>
                <p className="small">Envie exatamente ${prices[plan]} em BTC. A licença será enviada após 1 confirmação.</p>
              </div>
            )}

            <button 
              type="submit" 
              className="pay-btn"
              disabled={!stripe || loading}
            >
              {loading ? 'Processando...' : `Pagar $${prices[plan]}`}
            </button>
          </form>

          <div className="secure-badge">
            🔒 Pagamento 100% seguro - Dados criptografados
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default PaymentModal;