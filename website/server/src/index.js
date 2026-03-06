import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import jwt from '@fastify/jwt';
import rateLimit from '@fastify/rate-limit';
import dotenv from 'dotenv';
import pool from './config/database.js';
import authRoutes from './routes/auth.js';
import paymentRoutes from './routes/payments.js';
import licenseRoutes from './routes/licenses.js';

dotenv.config();

const fastify = Fastify({
  logger: true,
  trustProxy: true
});








await fastify.register(cors, {
  origin: [process.env.FRONTEND_URL, 'http://localhost:1976'],
  credentials: true
});

await fastify.register(helmet);

await fastify.register(jwt, {
  secret: process.env.JWT_SECRET
});

await fastify.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute'
});


fastify.register(authRoutes, { prefix: '/api/auth' });
fastify.register(paymentRoutes, { prefix: '/api/payments' });
fastify.register(licenseRoutes, { prefix: '/api/licenses' });






fastify.get('/health', async (request, reply) => {
  try {
    await pool.query('SELECT 1');
    return { status: 'healthy', database: 'connected' };
  } catch (error) {
    reply.status(500).send({ status: 'unhealthy', error: error.message });
  }
});

// Rota para registrar download gratuito
fastify.post('/api/download/free', async (request, reply) => {
  const { ip, userAgent } = request.body;
  
  await pool.query(
    'INSERT INTO downloads (ip_address, user_agent, version) VALUES ($1, $2, $3)',
    [ip || request.ip, userAgent || request.headers['user-agent'], '1.0.0']
  );
  
  // Gerar link de download temporário
  const downloadUrl = 'https://storage.btube.com/BTube_Free_Setup.exe';
  
  return { success: true, downloadUrl };
});

// Iniciar servidor
const start = async () => {
  try {
    await fastify.listen({ port: 3001, host: '0.0.0.0' });
    console.log('Servidor em http://localhost:2005');
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
