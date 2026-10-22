<template>
  <main class="author-dashboard"><div class="container py-5">
    <div class="dashboard-heading"><div><p class="eyebrow">RUANG PENULIS</p><h1>Dashboard Author</h1><p class="text-muted mb-0">Selamat datang, {{ user?.name || user?.username || user?.email }}. Pantau perkembangan jurnal Anda.</p></div><router-link class="btn btn-success" to="/author/journals/create"><i class="bi bi-plus-lg me-2"></i>Buat jurnal</router-link></div>
    <div v-if="error" class="alert alert-danger" role="alert">{{ error }} <button class="btn btn-sm btn-outline-danger ms-2" @click="load">Coba lagi</button></div>
    <div v-if="loading" class="py-5 text-center" role="status"><span class="spinner-border text-success"></span><p class="mt-3">Memuat jurnal Anda…</p></div>
    <template v-else-if="!error">
      <section class="journal-stats" aria-label="Ringkasan jurnal"><div v-for="stat in stats" :key="stat.label"><span>{{ stat.label }}</span><strong>{{ stat.count }}</strong></div></section>
      <section class="journal-panel"><div class="panel-heading"><h2>Jurnal terbaru</h2><router-link to="/author/journals">Lihat semua <i class="bi bi-arrow-right"></i></router-link></div>
        <div v-if="!journals.length" class="journal-empty"><i class="bi bi-journal-richtext"></i><h3>Mulai publikasi pertama Anda</h3><p class="text-muted">Buat draft, kirim untuk ditinjau, dan pantau statusnya di sini.</p><router-link to="/author/journals/create" class="btn btn-outline-success">Tulis jurnal pertama</router-link></div>
        <div v-else class="journal-list"><router-link v-for="journal in recent" :key="journal.ID_jurnal" :to="`/author/journals/${journal.ID_jurnal}`" class="journal-row"><div><h3>{{ journal.title }}</h3><p>{{ (journal.abstract || '').slice(0, 140) }}</p></div><span class="status-pill" :class="journal.status">{{ labels[journal.status] || journal.status }}</span><i class="bi bi-chevron-right"></i></router-link></div>
      </section>
      <router-link to="/author/journals/pending" class="pending-link"><i class="bi bi-clock-history me-2"></i>Lihat jurnal dalam proses review</router-link>
    </template>
  </div></main>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { getUser } from '../../utils/auth';
const user = getUser(), journals = ref([]), loading = ref(true), error = ref('');
const labels = { draft: 'Draft', pending_review: 'Menunggu review', under_revision: 'Dalam revisi', revision_needed: 'Perlu revisi', published: 'Dipublikasikan', rejected: 'Ditolak', approved: 'Disetujui' };
const stats = computed(() => [
 { label: 'Total jurnal', count: journals.value.length },
 { label: 'Draft', count: journals.value.filter(j => j.status === 'draft').length },
 { label: 'Dalam review', count: journals.value.filter(j => j.status === 'pending_review').length },
 { label: 'Perlu revisi', count: journals.value.filter(j => ['under_revision','revision_needed'].includes(j.status)).length },
 { label: 'Dipublikasikan', count: journals.value.filter(j => j.status === 'published').length },
]);
const recent = computed(() => [...journals.value].sort((a,b) => new Date(b.updated_at || b.created_at || 0) - new Date(a.updated_at || a.created_at || 0)).slice(0,5));
async function load() { loading.value = true; error.value = ''; try { const { data } = await axios.get('http://localhost:3000/api/author/journals'); journals.value = data.data || []; } catch { error.value = 'Jurnal belum dapat dimuat. Silakan coba lagi.'; } finally { loading.value = false; } }
onMounted(load);
</script>
<style scoped>
.author-dashboard { min-height:70vh; background:#f4f7f5; }.dashboard-heading { display:flex; justify-content:space-between; align-items:center; gap:24px; margin-bottom:32px; }.dashboard-heading h1 { margin-bottom:10px; font-size:32px; }.dashboard-heading .btn { flex-shrink:0; }.eyebrow { font-size:11px; letter-spacing:.14em; font-weight:700; color:#3b7852; margin-bottom:8px; }
.journal-stats { display:grid; grid-template-columns:repeat(5,1fr); background:white; border:1px solid #e0e8e2; border-radius:12px; margin-bottom:28px; }.journal-stats div { padding:24px; border-right:1px solid #e0e8e2; }.journal-stats div:last-child { border:0; }.journal-stats span { display:block; color:#637568; font-size:13px; }.journal-stats strong { font-size:30px; color:#234e34; }
.journal-panel { background:white; border:1px solid #e0e8e2; border-radius:12px; overflow:hidden; }.panel-heading { padding:22px 24px; border-bottom:1px solid #e0e8e2; display:flex; align-items:center; justify-content:space-between; gap:16px; }.panel-heading h2 { font-size:19px; margin:0; }.panel-heading a,.pending-link { color:#346f49; text-decoration:none; font-size:14px; }.journal-empty { padding:48px 20px; text-align:center; }.journal-empty > i { font-size:36px; color:#508265; }.journal-empty h3 { font-size:20px; margin:16px 0 8px; }.journal-row { display:flex; align-items:center; gap:18px; padding:22px 24px; border-bottom:1px solid #edf0ed; text-decoration:none; color:#2b4433; }.journal-row:hover { background:#f7faf7; }.journal-row > div { flex:1; min-width:0; }.journal-row h3 { font-size:16px; margin-bottom:6px; overflow-wrap:anywhere; }.journal-row p { color:#67786e; font-size:13px; margin:0; }.status-pill { border-radius:6px; padding:5px 9px; background:#eff3f0; font-size:12px; white-space:nowrap; }.status-pill.published { background:#e1f3e6; color:#235f3c; }.status-pill.revision_needed { background:#fff0d6; color:#80540f; }.pending-link { display:inline-block; margin-top:20px; }
@media(max-width:768px) { .dashboard-heading { align-items:flex-start; flex-direction:column; }.journal-stats { grid-template-columns:repeat(2,1fr); }.journal-stats div { padding:18px; border-bottom:1px solid #e0e8e2; }.journal-row { flex-wrap:wrap; }.journal-row > div { flex-basis:100%; } }
</style>
