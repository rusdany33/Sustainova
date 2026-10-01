import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { getToken } from './utils/auth'
import axios from 'axios'

axios.interceptors.request.use((config) => {
  const token = getToken();
  const url = new URL(config.url, window.location.origin);
  if (token && url.origin === 'http://localhost:3000') {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App)
app.use(router)
app.mount('#app')
