const express = require('express');
const app = express();
require('dotenv').config();
const routes = require('./routes');
const cors = require('cors');
const path = require('path');
const queryAsync = require('./utils/db');
// const errorHandler = require('./middlewares/error.middleware');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.use((req, res, next) => {
  console.log(`\n📨 ${req.method} ${req.path}`);
  console.log('Content-Type:', req.headers['content-type']);
  next();
});

app.get('/api/health', async (req, res) => {
  try {
    await queryAsync('SELECT 1');
    res.json({ status: 'ok', database: 'connected' });
  } catch (error) {
    res.status(503).json({ status: 'error', database: 'disconnected' });
  }
});
app.use('/api/uploads', express.static(path.resolve(__dirname, '../uploads')));
app.use('/api', routes);
app.use((err, req, res, next) => {
  console.error(err.message);
  if (res.headersSent) return next(err);
  const status = err.name === 'MulterError' || err.message === 'Invalid file type' ? 400 : 500;
  res.status(status).json({ message: status === 400 ? err.message : 'Terjadi kesalahan server' });
});


// app.use(errorHandler); 

module.exports = app;
