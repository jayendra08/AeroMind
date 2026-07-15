const mongoose = require('mongoose');

async function connectDatabase() {
  const mongoUri = process.env.MONGO_URI;

  if (!mongoUri) {
    console.warn('[mongo] MONGO_URI is not set. Prediction persistence will be skipped.');
    return null;
  }

  try {
    await mongoose.connect(mongoUri, {
      dbName: process.env.MONGO_DB_NAME || undefined,
    });
    console.log('[mongo] Connected');
    return mongoose.connection;
  } catch (error) {
    console.error('[mongo] Connection failed:', error.message);
    return null;
  }
}

module.exports = { connectDatabase };
