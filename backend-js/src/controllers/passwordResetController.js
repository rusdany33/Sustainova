const crypto = require('node:crypto');
const bcrypt = require('bcrypt');
const nodemailer = require('nodemailer');
const query = require('../utils/db');
require('../config/env');

const responseMessage = 'Jika email terdaftar, tautan reset password akan dikirim. Periksa kotak masuk atau folder spam.';
const transport = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT || 587),
  secure: process.env.SMTP_SECURE === 'true',
  auth: process.env.SMTP_USER ? { user: process.env.SMTP_USER, pass: process.env.SMTP_PASSWORD } : undefined,
  connectionTimeout: 5000, greetingTimeout: 5000, socketTimeout: 10000,
});
const digest = token => crypto.createHash('sha256').update(token).digest('hex');

exports.requestReset = async (req, res) => {
  const startedAt = Date.now();
  const email = typeof req.body.email === 'string' ? req.body.email.trim().toLowerCase() : '';
  if (email.length > 255 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ message: 'Masukkan alamat email yang valid.' });
  }
  let hash;
  try {
    if (!process.env.SMTP_HOST || !process.env.MAIL_FROM || !process.env.FRONTEND_URL) throw new Error('Mail configuration missing');
    // Check mail availability for all addresses, including unknown accounts.
    await transport.verify();
    const users = await query('SELECT ID_user, email FROM users WHERE email = ? LIMIT 1', [email]);
    if (users.length) {
      const token = crypto.randomBytes(32).toString('hex');
      hash = digest(token);
      const user = users[0];
      // One outstanding token per user. SQL also prevents concurrent requests
      // from bypassing the per-account 60-second email cooldown.
      await query(`INSERT INTO password_reset_tokens (user_id, token_hash, expires_at, requested_at)
        VALUES (?, ?, DATE_ADD(NOW(), INTERVAL 30 MINUTE), NOW())
        ON DUPLICATE KEY UPDATE
          token_hash = IF(requested_at <= DATE_SUB(NOW(), INTERVAL 60 SECOND), VALUES(token_hash), token_hash),
          expires_at = IF(requested_at <= DATE_SUB(NOW(), INTERVAL 60 SECOND), VALUES(expires_at), expires_at),
          used_at = IF(requested_at <= DATE_SUB(NOW(), INTERVAL 60 SECOND), NULL, used_at),
          requested_at = IF(requested_at <= DATE_SUB(NOW(), INTERVAL 60 SECOND), NOW(), requested_at)`, [user.ID_user, hash]);
      const saved = await query('SELECT user_id FROM password_reset_tokens WHERE token_hash = ?', [hash]);
      if (saved.length) {
        const url = new URL('/reset-password', process.env.FRONTEND_URL);
        url.hash = `token=${token}`;
        await transport.sendMail({
          from: process.env.MAIL_FROM, to: user.email, subject: 'Reset password Sustainova',
          text: `Anda meminta reset password Sustainova. Buka tautan berikut untuk membuat password baru:\n\n${url.href}\n\nTautan berlaku selama 30 menit dan hanya dapat digunakan sekali. Jika bukan Anda yang meminta, abaikan email ini.`,
        });
      }
    }
    await new Promise(resolve => setTimeout(resolve, Math.max(0, 600 - (Date.now() - startedAt))));
    return res.json({ message: responseMessage });
  } catch (error) {
    if (hash) await query('DELETE FROM password_reset_tokens WHERE token_hash = ?', [hash]).catch(() => {});
    console.error('Password reset delivery failed:', error.code || error.name);
    return res.status(503).json({ message: 'Layanan email belum tersedia. Silakan coba lagi nanti.' });
  }
};

exports.resetPassword = async (req, res) => {
  const { token, password, confirmPassword } = req.body;
  if (typeof token !== 'string' || !/^[a-f0-9]{64}$/.test(token)) {
    return res.status(400).json({ message: 'Tautan reset tidak valid atau sudah kedaluwarsa.' });
  }
  if (typeof password !== 'string' || password.length < 8 || Buffer.byteLength(password, 'utf8') > 72) {
    return res.status(400).json({ message: 'Password minimal 8 karakter dan maksimal 72 byte.' });
  }
  if (password !== confirmPassword) return res.status(400).json({ message: 'Konfirmasi password tidak cocok.' });
  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    // Atomic consumption: only one concurrent request can use a token.
    const result = await query(`UPDATE users u JOIN password_reset_tokens r ON r.user_id = u.ID_user
      SET u.password = ?, u.session_version = u.session_version + 1, r.token_hash = NULL, r.used_at = NOW()
      WHERE r.token_hash = ? AND r.expires_at > NOW() AND r.used_at IS NULL`, [hashedPassword, digest(token)]);
    if (!result.affectedRows) return res.status(400).json({ message: 'Tautan reset tidak valid atau sudah kedaluwarsa. Minta tautan baru.' });
    return res.json({ message: 'Password berhasil diubah. Silakan masuk dengan password baru.' });
  } catch (error) {
    console.error('Password reset failed:', error.code || error.name);
    return res.status(500).json({ message: 'Password belum berhasil diubah. Silakan coba lagi.' });
  }
};
