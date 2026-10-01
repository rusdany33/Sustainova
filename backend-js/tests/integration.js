// Tests use uniquely named temporary records and remove them in finally.
const assert = require('node:assert/strict');
const mysql = require('mysql2/promise');
const fs = require('node:fs/promises');
const path = require('node:path');
const { db, port } = require('../src/config/env');
const marker = `integration-${Date.now()}`;
let checks = 0;
async function api(route, method = 'GET', body, token, expected = 200) {
  const multipart = body instanceof FormData;
  const response = await fetch(`http://localhost:${port}/api/${route}`, {
    method, signal: AbortSignal.timeout(10000),
    headers: { ...(body && !multipart ? { 'Content-Type': 'application/json' } : {}), ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: body ? (multipart ? body : JSON.stringify(body)) : undefined,
  });
  const text = await response.text();
  assert.equal(response.status, expected, `${method} ${route}: ${text}`);
  checks++;
  return JSON.parse(text);
}
function form(fields, fileField, filename, type) {
  const data = new FormData();
  for (const [key, value] of Object.entries(fields)) data.append(key, value);
  if (fileField) data.append(fileField, new Blob(['integration fixture'], { type }), filename);
  return data;
}
async function main() {
  const connection = await mysql.createConnection({ host: db.host, port: db.port, user: db.user, password: db.password, database: db.name });
  let userId;
  try {
    for (const route of ['health', 'clients/home', 'clients/program', 'clients/berita', 'clients/news', 'clients/jurnal', 'clients/riset', 'clients/publikasi', 'clients/team', 'clients/partners']) await api(route);
    const accounts = {};
    for (const role of ['admin', 'editor', 'author']) {
      accounts[role] = await api('clients/login', 'POST', { email: `${role}@test.com`, password: 'password123' });
      assert.ok(accounts[role].user.id);
      await api('clients/profile', 'GET', undefined, accounts[role].token);
    }
    const { token: admin } = accounts.admin;
    const { token: editor } = accounts.editor;
    const { token: author } = accounts.author;
    for (const route of ['dashboard', 'programs', 'jurnal', 'berita', 'messages']) await api(`admin/${route}`, 'GET', undefined, admin);
    for (const route of ['dashboard/stats', 'journals', 'journals/pending', 'collaborations', 'collaboration-requests']) await api(`editor/${route}`, 'GET', undefined, editor);
    await api('author/journals', 'GET', undefined, author);
    await api('clients/profile', 'GET', undefined, undefined, 401);
    await api('admin/dashboard', 'GET', undefined, author, 403);
    const registration = await api('clients/register', 'POST', { name: marker, email: `${marker}@example.test`, password: 'Temporary123!' }, undefined, 201);
    userId = registration.data.userId;
    const login = await api('clients/login', 'POST', { email: `${marker}@example.test`, password: 'Temporary123!' });
    await api('clients/profile', 'PUT', { name: marker, email: `${marker}@example.test`, telephone: '080000000', username: 'integration', address: 'Local test', bio: 'Test' }, login.token);
    assert.equal((await api('clients/profile', 'GET', undefined, login.token)).data.telephone, '080000000');
    await api('clients/contact', 'POST', { name: marker, email: `${marker}@example.test`, subject: marker, message: marker }, undefined, 201);
    const collab = await api('clients/collaboration-request', 'POST', { organizationName: marker, contactName: marker, contactEmail: `${marker}@example.test`, description: marker, collaborationType: 'research' }, undefined, 201);
    await api(`editor/collaboration-requests/${collab.data.ID_request}/accept`, 'PUT', {}, editor);
    const journalFields = { title: marker, writer: marker, keyword: 'test', abstract: marker, doi: 'test' };
    const journal = await api('author/journals', 'POST', form(journalFields, 'file', `${marker}.pdf`, 'application/pdf'), author, 201);
    const jid = journal.data.ID_jurnal;
    await api(`author/journals/${jid}`, 'PUT', journalFields, author);
    await api(`author/journals/${jid}`, 'GET', undefined, author);
    await api(`author/journals/${jid}/submit-review`, 'POST', {}, author);
    await api(`editor/journals/${jid}/review`, 'POST', { ID_jurnal: jid, FK_ID_author: accounts.author.user.id, status: 'approved', feedback: marker }, editor, 201);
    const published = await api('clients/publikasi');
    assert.ok(published.data.some(row => row.ID_jurnal === jid));
    await api(`admin/jurnal/${jid}`, 'DELETE', undefined, admin);
    const draft = await api('author/journals', 'POST', journalFields, author, 201);
    await api(`author/journals/${draft.data.ID_jurnal}`, 'DELETE', undefined, author);
    const program = await api('uploads/tambah/program', 'POST', form({ name: marker, description: marker, status: 'aktif', peserta: '1', start_date: '2026-10-01', end_date: '2026-10-02' }, 'poster', `${marker}.png`, 'image/png'), admin);
    await api(`clients/programs/${program.data.id}`);
    await api(`admin/programs/${program.data.id}`, 'PUT', { name: marker }, admin);
    await api(`admin/delete/programs/${program.data.id}`, 'DELETE', undefined, admin);
    const news = await api('uploads/tambah/berita', 'POST', form({ title: marker, kategori: 'test', ringkasan: marker, text: marker, date_published: '2026-10-01' }, 'cover_image', `${marker}.png`, 'image/png'), admin);
    await api(`clients/news/${news.data.id}`);
    await api(`admin/berita/${news.data.id}`, 'PUT', { title: marker }, admin);
    await api(`admin/delete/berita/${news.data.id}`, 'DELETE', undefined, admin);
    console.log(`PASS: ${checks} API checks, including registration, profile, contact, collaboration, journal review, program and news CRUD.`);
  } finally {
    await connection.query('DELETE FROM collaboration_requests WHERE contact_email = ?', [`${marker}@example.test`]);
    await connection.query('DELETE FROM contact_messages WHERE email = ?', [`${marker}@example.test`]);
    await connection.query('DELETE FROM jurnal WHERE title = ?', [marker]);
    await connection.query('DELETE FROM programs WHERE name = ?', [marker]);
    await connection.query('DELETE FROM news WHERE title = ?', [marker]);
    if (userId) await connection.query('DELETE FROM users WHERE ID_user = ?', [userId]);
    for (const folder of ['pdf', 'images/program', 'images/berita', 'images/jurnal']) {
      const directory = path.resolve(__dirname, '../src/fileSaved', folder);
      for (const name of await fs.readdir(directory).catch(() => [])) {
        if (name.includes(marker)) await fs.unlink(path.join(directory, name));
      }
    }
    await connection.end();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
