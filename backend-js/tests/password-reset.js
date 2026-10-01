const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { once } = require('node:events');
const query = require('../src/utils/db');
const pool = require('../src/config/db');
const app = require('../src/app');
const email = `reset-test-${Date.now()}@example.test`;
const oldPassword = 'OldPassword123!';
const newPassword = 'NewPassword456!';
const mailbox = 'http://127.0.0.1:8025';
let server, base, userId, count = 0;
async function api(route, body, status = 200, token) {
  const r = await fetch(base + route, { method: body ? 'POST' : 'GET', headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) }, body: body ? JSON.stringify(body) : undefined });
  const data = await r.json();
  assert.equal(r.status, status, `${route}: ${JSON.stringify(data)}`);
  count++;
  return data;
}
async function messages() {
  const r = await fetch(`${mailbox}/api/v1/messages`);
  const list = await r.json();
  return list.messages.filter(m => m.To.some(to => to.Address === email));
}
async function latestToken() {
  const list = await messages();
  assert.ok(list.length, 'Reset email delivered to Mailpit');
  const mail = await (await fetch(`${mailbox}/api/v1/message/${list[0].ID}`)).json();
  return mail.Text.match(/token=([a-f0-9]{64})/)[1];
}
async function main() {
  server = app.listen(0, '127.0.0.1');
  await once(server, 'listening');
  base = `http://127.0.0.1:${server.address().port}/api/clients/`;
  try {
    const registration = await api('register', { name: 'Reset integration test', email, password: oldPassword }, 201);
    userId = registration.data.userId;
    const login = await api('login', { email, password: oldPassword });
    const unknown = await api('forgot-password', { email: `unknown-${email}` });
    const known = await api('forgot-password', { email });
    assert.deepEqual(known, unknown, 'No account existence disclosure');
    let token = await latestToken();
    const [saved] = await query('SELECT token_hash FROM password_reset_tokens WHERE user_id = ?', [userId]);
    assert.equal(saved.token_hash, crypto.createHash('sha256').update(token).digest('hex'));
    await api('forgot-password', { email });
    assert.equal((await messages()).length, 1, 'Cooldown prevents duplicate emails');
    await api('reset-password', { token, password: 'short', confirmPassword: 'short' }, 400);
    await api('reset-password', { token, password: newPassword, confirmPassword: 'different' }, 400);
    await api('reset-password', { token: 'a'.repeat(64), password: newPassword, confirmPassword: newPassword }, 400);
    await query('UPDATE password_reset_tokens SET expires_at = DATE_SUB(NOW(), INTERVAL 1 MINUTE) WHERE user_id = ?', [userId]);
    await api('reset-password', { token, password: newPassword, confirmPassword: newPassword }, 400);
    await query('UPDATE password_reset_tokens SET requested_at = DATE_SUB(NOW(), INTERVAL 2 MINUTE) WHERE user_id = ?', [userId]);
    await api('forgot-password', { email });
    const expiredToken = token;
    token = await latestToken();
    assert.notEqual(expiredToken, token);
    await api('reset-password', { token: expiredToken, password: newPassword, confirmPassword: newPassword }, 400);
    const responses = await Promise.all([1, 2].map(() => fetch(base + 'reset-password', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token, password: newPassword, confirmPassword: newPassword }) })));
    assert.deepEqual(responses.map(r => r.status).sort(), [200, 400], 'Concurrent token consumption succeeds only once'); count += 2;
    await api('login', { email, password: oldPassword }, 401);
    const updatedLogin = await api('login', { email, password: newPassword });
    await api('profile', undefined, 401, login.token);
    await api('profile', undefined, 200, updatedLogin.token);
    await api('reset-password', { token, password: oldPassword, confirmPassword: oldPassword }, 400);
    // Exhaust rate limit without sending emails.
    let limited = false;
    for (let i = 0; i < 22; i++) {
      const r = await fetch(base + 'forgot-password', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'invalid' }) });
      if (r.status === 429) { limited = true; break; }
    }
    assert.ok(limited, 'Rate limiting is active'); count++;
    console.log(`PASS: ${count} password reset checks, SMTP delivery, expiry, replay, race, password change and session invalidation.`);
  } finally {
    if (userId) await query('DELETE FROM users WHERE ID_user = ?', [userId]);
    const ids = (await messages()).map(m => m.ID);
    if (ids.length) await fetch(`${mailbox}/api/v1/messages`, { method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ IDs: ids }) });
    await new Promise(resolve => server.close(resolve));
    await pool.promise().end();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
