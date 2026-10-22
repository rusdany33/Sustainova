import axios from 'axios';
const read = (storage, key) => { try { return JSON.parse(storage.getItem(key) || 'null'); } catch { return null; } };
export function getToken() { return localStorage.getItem('token') || sessionStorage.getItem('token'); }
export function getUser() { return read(localStorage, 'user') || read(sessionStorage, 'user'); }
export function getRemember() {
  const saved = read(localStorage, 'savedUser');
  if (saved) localStorage.setItem('savedUser', JSON.stringify({ email: saved.email || '' }));
  return saved ? { email: saved.email || '' } : null;
}
export function dashboardPath(role = getUser()?.role) { return ({ admin: '/admin/dashboard', editor: '/editor/dashboard', author: '/author/dashboard' })[role] || '/'; }
function changed() { window.dispatchEvent(new Event('auth-changed')); }
export function logout() {
  for (const storage of [localStorage, sessionStorage]) { storage.removeItem('token'); storage.removeItem('user'); }
  delete axios.defaults.headers.common.Authorization;
  getRemember(); changed();
}
export function setSession(token, user, remember = false) {
  logout();
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem('token', token); storage.setItem('user', JSON.stringify(user));
  if (remember) localStorage.setItem('savedUser', JSON.stringify({ email: user.email }));
  else localStorage.removeItem('savedUser');
  changed();
}
export function updateUser(user) {
  const storage = localStorage.getItem('token') ? localStorage : sessionStorage;
  storage.setItem('user', JSON.stringify(user)); changed();
}
