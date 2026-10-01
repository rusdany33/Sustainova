const mysql = require('mysql2');
const { db } = require('./env');

const database = mysql.createPool({
  host: db.host,
  port: db.port,
  user: db.user,
  password: db.password,
  database: db.name,
  waitForConnections: true,
  connectionLimit: 10,
});

database.getConnection((err, connection) => {
  if (err) {
    console.error('Koneksi ke database gagal:', err.message);
  } else {
    connection.release();
    console.log('✅ Berhasil terkoneksi ke database MySQL');
  }
});

module.exports = database;
