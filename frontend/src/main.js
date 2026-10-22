import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { getToken, logout } from './utils/auth'
import axios from 'axios'

axios.interceptors.request.use((config) => {
  const token = getToken();
  const url = new URL(config.url, window.location.origin);
  if (token && url.origin === 'http://localhost:3000') {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axios.interceptors.response.use(response => response, error => {
  const url = new URL(error.config?.url || '/', window.location.origin);
  if (error.response?.status === 401 && url.origin === 'http://localhost:3000' && !url.pathname.includes('/clients/login')) {
    logout();
    if (router.currentRoute.value.path !== '/login') router.replace('/login');
  }
  return Promise.reject(error);
});

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App)
app.use(router)
app.mount('#app')
