// client/src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import { Toaster } from 'react-hot-toast';
import './belezas/App.css';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Pricing from './components/Pricing';
import Download from './components/Download';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import Success from './components/Success';
import PaymentModal from './components/PaymentModal';

const stripePromise = loadStripe('pk_live_944452176-public_key_stripe:923');

function App() {
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState('pro');
  const [stats, setStats] = useState({
    downloads: 15234,
    users: 8765
  });

  useEffect(() => {
    // Buscar estatísticas do backend
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:3001/health');
      const data = await response.json();
      // Atualizar stats
    } catch (error) {
      console.error('Erro ao buscar stats:', error);
    }
  };

  const openPaymentModal = (plan) => {
    setSelectedPlan(plan);
    setShowPaymentModal(true);
  };

  return (
    <Router>
      <div className="App">
        <Toaster position="top-right" />
        <Navbar />
        
        <Routes>
          <Route path="/" element={
            <main>
              <Hero stats={stats} />
              <Features />
              <Pricing onSelectPlan={openPaymentModal} />
              <Download />
              <FAQ />
            </main>
          } />
          <Route path="/success" element={<Success />} />
        </Routes>

        <Footer />

        {showPaymentModal && (
          <Elements stripe={stripePromise}>
            <PaymentModal 
              plan={selectedPlan}
              onClose={() => setShowPaymentModal(false)}
            />
          </Elements>
        )}
      </div>
    </Router>
  );
}

export default App;