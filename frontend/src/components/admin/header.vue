<template>
  <header class="admin-header"><span class="header-caption">Ruang kerja / <strong>Admin</strong></span><AccountMenu /></header>
</template>
<script setup>
import AccountMenu from '../AccountMenu.vue';
</script>
<style scoped>
.admin-header { position:fixed; top:0; right:0; left:var(--admin-sidebar-width,280px); height:78px; display:flex; justify-content:space-between; align-items:center; padding:12px 24px; background:#fff; border-bottom:1px solid #e4ebe7; z-index:990; transition:left .2s; }
.header-caption { font-size:13px; color:#687a88; }
@media(max-width:768px) { .admin-header { left:0; padding:12px 14px 12px 82px; justify-content:flex-end; }.header-caption { display:none; } }
</style>
