<template>
  <div class="auth-page forgot-password-bg">
    <div class="auth-container">
      <div class="auth-header">
        <h1 class="auth-title">Password Baru</h1>
        <p class="auth-subtitle">Buat password baru untuk akun Sustainova Anda.</p>
      </div>
      <div v-if="success" class="alert alert-success" role="status">
        {{ success }}
        <router-link to="/login" class="btn-auth mt-3">Masuk</router-link>
      </div>
      <template v-else>
        <p v-if="error" class="alert alert-danger" role="alert">{{ error }}</p>
        <form v-if="token" class="auth-form" @submit.prevent="resetPassword">
          <div class="form-group">
            <label for="password">Password baru</label>
            <input id="password" v-model="password" type="password" autocomplete="new-password" minlength="8" maxlength="72" required class="form-control" placeholder="Minimal 8 karakter">
          </div>
          <div class="form-group">
            <label for="confirmPassword">Konfirmasi password</label>
            <input id="confirmPassword" v-model="confirmPassword" type="password" autocomplete="new-password" minlength="8" maxlength="72" required class="form-control" placeholder="Ulangi password baru">
          </div>
          <button type="submit" class="btn-auth" :disabled="loading">{{ loading ? 'Menyimpan...' : 'Simpan Password' }}</button>
        </form>
        <div class="auth-footer"><router-link to="/forgotPass">Minta tautan reset baru</router-link></div>
      </template>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { logout } from '@/utils/auth';
const route = useRoute();
const router = useRouter();
const token = new URLSearchParams(route.hash.slice(1)).get('token') || '';
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const success = ref('');
const error = ref(/^[a-f0-9]{64}$/.test(token) ? '' : 'Tautan reset tidak valid. Silakan minta tautan baru.');
onMounted(() => router.replace({ path: '/reset-password' }));
async function resetPassword() {
  if (loading.value) return;
  error.value = '';
  if (password.value !== confirmPassword.value) { error.value = 'Konfirmasi password tidak cocok.'; return; }
  loading.value = true;
  try {
    const response = await axios.post('http://localhost:3000/api/clients/reset-password', { token, password: password.value, confirmPassword: confirmPassword.value });
    logout();
    localStorage.removeItem('savedUser');
    delete axios.defaults.headers.common.Authorization;
    success.value = response.data.message;
    password.value = ''; confirmPassword.value = '';
  } catch (err) { error.value = err.response?.data?.message || 'Tidak dapat terhubung ke server. Silakan coba lagi.'; }
  finally { loading.value = false; }
}
</script>
<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.forgot-password-bg {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('../../assets/background/bg-forgot.jpg');
}

.auth-container {
  width: 100%;
  max-width: 450px;
  background-color: rgba(255, 255, 255, 0.288);
  backdrop-filter: blur(10px);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 10px;
}

.auth-subtitle {
  color: #ffffff;
  font-size: 1rem;
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

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.form-control {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f8f8;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
}

.form-control:focus {
  border-color: #5a8f00;
  box-shadow: 0 0 0 3px rgba(90, 143, 0, 0.1);
}

.has-error .form-control {
  border-color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 5px;
}

.btn-auth {
  background-color: #5a8f00;
  color: rgb(0, 0, 0);
  border: none;
  border-radius: 8px;
  padding: 14px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-auth:hover:not(:disabled) {
  background-color: #4a7800;
}

.btn-auth:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 30px;
  text-align: center;
  font-size: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.auth-footer a {
  color: #5a8f00;
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  text-decoration: underline;
}

/* Success message styles */
.success-message {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  font-size: 4rem;
  color: #5a8f00;
  margin-bottom: 20px;
}

.success-message h2 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #333;
}

.success-message p {
  color: #555;
  margin-bottom: 15px;
}

.small-text {
  font-size: 0.85rem;
  color: #777;
}

.text-button {
  background: none;
  border: none;
  color: #5a8f00;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
}

.text-button:hover {
  text-decoration: underline;
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>