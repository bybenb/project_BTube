// server/src/routes/payments.js
import Stripe from 'stripe';
import pool from '../config/database.js';
import { v4 as uuidv4 } from 'uuid';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function paymentRoutes(fastify) {
  // Criar sessão de checkout Stripe
  fastify.post('/create-checkout', async (request, reply) => {
    const { plan = 'pro', email, name } = request.body;
    
    const prices = {
      pro: 2990, // $29.90 em centavos
      enterprise: 9990 // $99.90
    };
    
    try {
      const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        line_items: [{
          price_data: {
            currency: 'usd',
            product_data: {
              name: `BTube ${plan === 'pro' ? 'Pro' : 'Enterprise'}`,
              description: 'Licença vitalícia com atualizações gratuitas'
            },
            unit_amount: prices[plan]
          },
          quantity: 1
        }],
        mode: 'payment',
        success_url: `${process.env.FRONTEND_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
        cancel_url: `${process.env.FRONTEND_URL}/pricing`,
        customer_email: email,
        metadata: {
          plan,
          name
        }
      });
      
      return { sessionId: session.id, url: session.url };
    } catch (error) {
      reply.status(500).send({ error: error.message });
    }
  });

  // Webhook do Stripe (quando pagamento é confirmado)
  fastify.post('/webhook', async (request, reply) => {
    const sig = request.headers['stripe-signature'];
    let event;

    try {
      event = stripe.webhooks.constructEvent(
        request.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err) {
      reply.status(400).send(`Webhook Error: ${err.message}`);
      return;
    }

    if (event.type === 'checkout.session.completed') {
      const session = event.data.object;
      
      // Gerar licença
      const licenseKey = generateLicenseKey();
      const expiresAt = new Date();
      expiresAt.setFullYear(expiresAt.getFullYear() + 1); // 1 ano
      
      // Salvar usuário e licença no banco
      const client = await pool.connect();
      try {
        await client.query('BEGIN');
        
        // Inserir usuário
        const userResult = await client.query(
          'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id',
          [session.customer_email, session.metadata.name || 'Cliente']
        );
        
        const userId = userResult.rows[0].id;
        
        // Inserir licença
        const licenseResult = await client.query(
          `INSERT INTO licenses (license_key, user_id, type, expires_at) 
           VALUES ($1, $2, $3, $4) RETURNING id`,
          [licenseKey, userId, session.metadata.plan, expiresAt]
        );
        
        const licenseId = licenseResult.rows[0].id;
        
        // Inserir pagamento
        await client.query(
          `INSERT INTO payments (user_id, license_id, amount, currency, status, payment_method, stripe_payment_id)
           VALUES ($1, $2, $3, $4, $5, $6, $7)`,
          [
            userId, 
            licenseId, 
            session.amount_total / 100, 
            session.currency, 
            'completed', 
            'stripe', 
            session.id
          ]
        );
        
        await client.query('COMMIT');
        
        // Enviar email com a licença
        await sendLicenseEmail(session.customer_email, licenseKey);
        
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erro ao salvar pagamento:', error);
      } finally {
        client.release();
      }
    }

    reply.send({ received: true });
  });

  // Verificar status do pagamento
  fastify.get('/status/:sessionId', async (request, reply) => {
    const { sessionId } = request.params;
    
    try {
      const session = await stripe.checkout.sessions.retrieve(sessionId);
      
      if (session.payment_status === 'paid') {
        // Buscar licença gerada
        const result = await pool.query(
          `SELECT l.* FROM licenses l 
           JOIN payments p ON l.id = p.license_id 
           WHERE p.stripe_payment_id = $1`,
          [sessionId]
        );
        
        if (result.rows.length > 0) {
          return {
            status: 'completed',
            licenseKey: result.rows[0].license_key
          };
        }
      }
      
      return { status: session.payment_status };
    } catch (error) {
      reply.status(500).send({ error: error.message });
    }
  });
}

function generateLicenseKey() {
  // Formato: XXXXX-XXXXX-XXXXX-XXXXX
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let key = '';
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 5; j++) {
      key += chars[Math.floor(Math.random() * chars.length)];
    }
    if (i < 3) key += '-';
  }
  return key;
}

async function sendLicenseEmail(email, licenseKey) {
  // Implementar envio de email (nodemailer, resend, etc)
  console.log(`Licença ${licenseKey} enviada para ${email}`);
}