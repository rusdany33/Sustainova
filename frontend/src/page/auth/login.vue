<template>
  <div class="auth-page login-bg">
    <div class="auth-container">
      <h1 class="auth-title">MASUK</h1>

      <form @submit.prevent="handleLogin" class="auth-form" novalidate>
        <div v-if="errorMessage" class="alert alert-danger mb-0" role="alert">{{ errorMessage }}</div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" autocomplete="email" class="form-control" :class="{ 'is-invalid': errors.email }" :aria-invalid="!!errors.email" aria-describedby="email-error" @input="errors.email = ''; errorMessage = ''">
          <p v-if="errors.email" id="email-error" class="field-error" role="alert">{{ errors.email }}</p>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" autocomplete="current-password" class="form-control" :class="{ 'is-invalid': errors.password }" :aria-invalid="!!errors.password" aria-describedby="password-error" @input="errors.password = ''; errorMessage = ''">
          <p v-if="errors.password" id="password-error" class="field-error" role="alert">{{ errors.password }}</p>
        </div>

        <div class="form-options">
          <div class="remember-me">
            <input type="checkbox" id="remember" v-model="rememberMe">
            <label for="remember">Ingat saya</label>
          </div>
          <router-link to="/forgotPass" class="forgot-password">Lupa password?</router-link>
        </div>

        <button type="submit" class="btn-auth" :disabled="loading"><span v-if="loading" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>{{ loading ? 'Memproses…' : 'Masuk' }}</button>
      </form>

      <div class="auth-footer">
        <p>Belum punya akun? <router-link to="/register">Daftar</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { getRemember, setSession, dashboardPath } from '../../utils/auth';
const router = useRouter();
const saved = getRemember();
const email = ref(saved?.email || '');
const password = ref('');
const rememberMe = ref(!!saved);
const loading = ref(false);
const errors = reactive({ email: '', password: '' });
const errorMessage = ref('');
async function focusError() {
  await nextTick();
  document.getElementById(errors.email ? 'email' : 'password')?.focus();
}
async function handleLogin() {
  if (loading.value) return;
  errors.email = ''; errors.password = ''; errorMessage.value = '';
  email.value = email.value.trim();
  if (!email.value) errors.email = 'Email wajib diisi.';
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) errors.email = 'Masukkan alamat email yang valid.';
  if (!password.value) errors.password = 'Password wajib diisi.';
  if (errors.email || errors.password) { focusError(); return; }
  loading.value = true;
  try {
    const { data } = await axios.post('http://localhost:3000/api/clients/login', { email: email.value, password: password.value });
    setSession(data.token, data.user, rememberMe.value);
    await router.replace(dashboardPath(data.user.role));
  } catch (error) {
    const data = error.response?.data;
    for (const field of ['email', 'password']) if (data?.errors?.[field]) errors[field] = data.errors[field];
    if (['email', 'password'].includes(data?.field) && !errors[data.field]) errors[data.field] = data.message;
    if (!errors.email && !errors.password) errorMessage.value = data?.message || 'Tidak dapat terhubung ke server. Silakan coba lagi.';
    else focusError();
  } finally { loading.value = false; }
}
</script>


<style scoped>
.field-error { color: #b42318; font-size: .875rem; margin: 0; }
.form-control.is-invalid { border-color: #b42318; }
.btn-auth:disabled { opacity: .65; cursor: wait; }
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-size: cover;
  background-position: center;
}

.login-bg {
  background-image: url('../../assets/background/bg-login.png');
}

.auth-container {
  width: 100%;
  max-width: 450px;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(5px);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: #000;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-bottom: 1px solid #333;
  background-color: transparent;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #5a8f00;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.forgot-password {
  color: #333;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.btn-auth {
  background-color: #3b711c;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.btn-auth:hover {
  background-color: #2d5915;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 0.9rem;
}

.auth-footer a {
  color: #5a8f00;
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>