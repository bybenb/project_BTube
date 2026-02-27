// site/script.js

// Modal de pagamento
const modal = document.getElementById('paymentModal');

function showPaymentModal() {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Fechar modal clicando fora
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// Seleção de método de pagamento
function selectPayment(method) {
    // Esconder todos os formulários
    document.getElementById('cardForm').style.display = 'none';
    document.getElementById('paypalForm').style.display = 'none';
    document.getElementById('cryptoForm').style.display = 'none';
    
    // Remover seleção anterior
    document.querySelectorAll('.payment-option').forEach(opt => {
        opt.style.borderColor = 'var(--border)';
    });
    
    // Mostrar formulário correspondente
    switch(method) {
        case 'card':
            document.getElementById('cardForm').style.display = 'block';
            event.target.closest('.payment-option').style.borderColor = 'var(--accent-primary)';
            break;
        case 'paypal':
            document.getElementById('paypalForm').style.display = 'block';
            event.target.closest('.payment-option').style.borderColor = 'var(--accent-primary)';
            break;
        case 'crypto':
            document.getElementById('cryptoForm').style.display = 'block';
            event.target.closest('.payment-option').style.borderColor = 'var(--accent-primary)';
            break;
    }
}

// Processar pagamento
function processPayment() {
    alert('Redirecionando para gateway de pagamento...\n(Implementar integração real)');
}

function paypalRedirect() {
    alert('Redirecionando para PayPal...\n(Implementar integração real)');
}

// Download grátis
function downloadFree() {
    // Simular download
    const link = document.createElement('a');
    link.href = '#';
    link.download = 'BTube_Free_Setup.exe';
    link.click();
    
    alert('Download iniciado! Obrigado por experimentar o BTube.');
}

// Smooth scroll para links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Animação de entrada dos elementos
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .pricing-card, .faq-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// Contador de downloads (fake)
let downloadCount = 15234;
setInterval(() => {
    downloadCount += Math.floor(Math.random() * 10);
    const counters = document.querySelectorAll('.download-count');
    counters.forEach(counter => {
        if (counter) counter.textContent = downloadCount.toLocaleString();
    });
}, 5000);