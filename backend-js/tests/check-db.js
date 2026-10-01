const mysql = require('mysql2/promise');
const { db } = require('../src/config/env');
(async () => {
  const connection = await mysql.createConnection({ host: db.host, port: db.port, user: db.user, password: db.password, database: db.name });
  try {
    const [tables] = await connection.query('SHOW TABLES');
    console.log(`Database ${db.name} terhubung (${tables.length} tabel).`);
  } finally {
    await connection.end();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
