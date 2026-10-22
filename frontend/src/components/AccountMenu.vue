<template>
  <div class="account-menu" ref="root" @focusout="onFocusOut">
    <button ref="trigger" type="button" class="account-trigger" :aria-expanded="open" aria-label="Menu akun" @click="open = !open" @keydown.down.prevent="openAndFocus">
      <span v-if="user" class="account-label"><strong>{{ user.email }}</strong><small>{{ user.role }}</small></span>
      <span class="account-avatar"><i class="bi bi-person-circle" aria-hidden="true"></i></span>
      <i class="bi bi-chevron-down account-chevron" :class="{ rotated: open }" aria-hidden="true"></i>
    </button>
    <div v-if="open" class="account-card" @keydown.esc.stop.prevent="close(true)">
      <template v-if="user">
        <div class="account-summary"><small>AKUN ANDA</small><strong>{{ user.name || user.username || user.email }}</strong><span>{{ user.email }}</span><span class="account-role">{{ user.role }}</span></div>
        <nav aria-label="Navigasi akun" @click="close()">
          <router-link v-if="dashboard !== '/'" :to="dashboard"><i class="bi bi-grid" aria-hidden="true"></i>Dashboard</router-link>
          <router-link to="/profile"><i class="bi bi-person" aria-hidden="true"></i>Profil saya</router-link>
          <router-link v-if="['user','author'].includes(user.role)" to="/author/journals"><i class="bi bi-journal-text" aria-hidden="true"></i>Jurnal saya</router-link>
          <router-link to="/"><i class="bi bi-house" aria-hidden="true"></i>Kembali ke website</router-link>
        </nav>
        <button type="button" class="account-logout" @click="signOut"><i class="bi bi-box-arrow-right" aria-hidden="true"></i>Logout</button>
      </template>
      <nav v-else aria-label="Navigasi akun" @click="close()"><router-link to="/login">Masuk</router-link><router-link to="/register">Daftar akun</router-link></nav>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getUser, getToken, getRemember, dashboardPath, logout } from '../utils/auth';
const root = ref(null), trigger = ref(null), open = ref(false), user = ref(null);
const route = useRoute(), router = useRouter();
const dashboard = computed(() => dashboardPath(user.value?.role));
function sync() { getRemember(); user.value = getToken() ? getUser() : null; }
function close(focus = false) { open.value = false; if (focus) trigger.value?.focus(); }
function outside(event) { if (!root.value?.contains(event.target)) close(); }
function onFocusOut(event) { if (event.relatedTarget && !root.value?.contains(event.relatedTarget)) close(); }
async function openAndFocus() { open.value = true; await nextTick(); root.value?.querySelector('.account-card a')?.focus(); }
function escape(event) { if (event.key === 'Escape' && open.value) close(true); }
async function signOut() { logout(); close(); await router.replace('/login'); }
watch(() => route.fullPath, () => { close(); sync(); });
onMounted(() => { sync(); document.addEventListener('pointerdown', outside); document.addEventListener('keydown', escape); window.addEventListener('auth-changed', sync); window.addEventListener('storage', sync); });
onUnmounted(() => { document.removeEventListener('pointerdown', outside); document.removeEventListener('keydown', escape); window.removeEventListener('auth-changed', sync); window.removeEventListener('storage', sync); });
</script>
<style scoped>
.account-menu { position: relative; text-align: left; }
.account-trigger { display:flex; align-items:center; gap:12px; border:1px solid #dce5eb; background:#f8fafc; padding:6px 12px; border-radius:12px; color:#243748; max-width:100%; }
.account-trigger:hover { background:#edf4ef; border-color:#82a68e; }
.account-trigger:focus-visible, .account-card a:focus-visible, .account-card button:focus-visible { outline:3px solid #85b89a; outline-offset:3px; }
.account-label { text-align:right; display:flex; flex-direction:column; min-width:0; }
.account-label strong { font-size:.875rem; max-width:230px; overflow:hidden; text-overflow:ellipsis; }
.account-label small { font-size:.7rem; color:#607383; text-transform:uppercase; letter-spacing:.08em; }
.account-avatar { display:grid; place-items:center; width:36px; height:36px; border-radius:50%; background:#397153; color:white; font-size:23px; flex-shrink:0; }
.account-chevron { font-size:12px; transition:transform .15s; }.rotated { transform:rotate(180deg); }
.account-card { position:absolute; right:0; top:calc(100% + 10px); width:290px; max-width:calc(100vw - 32px); padding:8px; border:1px solid #e0e7e4; border-radius:14px; background:white; box-shadow:0 14px 40px #18322724; z-index:1100; }
.account-summary { padding:12px 12px 16px; border-bottom:1px solid #e9eeeb; display:flex; flex-direction:column; gap:4px; overflow-wrap:anywhere; }
.account-summary small { color:#607383; font-size:10px; letter-spacing:.12em; }.account-summary strong { font-size:15px; }.account-summary > span { font-size:12px; color:#607383; }.account-summary .account-role { color:#326044; text-transform:capitalize; }
.account-card nav { padding:7px 0; }.account-card a,.account-logout { display:flex; align-items:center; gap:10px; width:100%; padding:10px 12px; border-radius:7px; font-size:14px; text-decoration:none; color:#344c5b; border:0; background:white; text-align:left; }
.account-card a:hover { background:#f0f6f2; color:#28613d; }.account-logout { color:#b42318; border-top:1px solid #e9eeeb; border-radius:0 0 7px 7px; }.account-logout:hover { background:#fff1f0; }
@media(max-width:480px) { .account-label strong { max-width:165px; } .account-trigger { gap:8px; padding:6px 8px; } }
</style>
