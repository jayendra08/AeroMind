require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { connectDatabase } = require('./config/db');
const microLocationRoutes = require('./routes/microLocationRoutes');

const app = express();
const port = Number(process.env.PORT || 5000);
const clientOrigin = process.env.CLIENT_ORIGIN || 'http://localhost:5173';

app.use(
  cors({
    origin: clientOrigin,
    credentials: true,
  })
);
app.use(express.json({ limit: '1mb' }));

app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', service: 'aqi-micro-location-api' });
});

app.use('/api/micro-location', microLocationRoutes);

app.use((error, _req, res, _next) => {
  console.error('[api] Error:', error.message);
  res.status(400).json({
    status: 'error',
    message: error.message || 'Unexpected server error',
  });
});

async function startServer() {
  await connectDatabase();
  app.listen(port, () => {
    console.log(`[api] Listening on http://localhost:${port}`);
  });
}

startServer().catch((error) => {
  console.error('[api] Failed to start server:', error.message);
  process.exit(1);
});
