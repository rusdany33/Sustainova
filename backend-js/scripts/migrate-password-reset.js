const mysql = require('mysql2/promise');
const fs = require('node:fs');
const path = require('node:path');
const { db } = require('../src/config/env');
(async () => {
  const c = await mysql.createConnection({ host: db.host, port: db.port, user: db.user, password: db.password, database: db.name });
  try {
    const [columns] = await c.query("SHOW COLUMNS FROM users LIKE 'session_version'");
    if (!columns.length) await c.query('ALTER TABLE users ADD COLUMN session_version INT NOT NULL DEFAULT 0');
    await c.query(fs.readFileSync(path.resolve(__dirname, '../../db/migration_password_reset.sql'), 'utf8'));
    console.log('Password reset migration ready.');
  } finally { await c.end(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
