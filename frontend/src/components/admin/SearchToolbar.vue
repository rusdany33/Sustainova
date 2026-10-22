<template>
  <div class="search-toolbar"><div class="search-field"><label :for="id" class="visually-hidden">{{ label }}</label><i class="bi bi-search" aria-hidden="true"></i><input :id="id" type="search" :value="modelValue" :placeholder="placeholder" @input="$emit('update:modelValue', $event.target.value)" @keydown.esc="$emit('update:modelValue', '')"><button v-if="modelValue" type="button" @click="$emit('update:modelValue', '')" :aria-label="`Hapus pencarian ${label.toLowerCase()}`"><i class="bi bi-x-lg" aria-hidden="true"></i></button></div><span class="search-count" role="status">{{ count }} dari {{ total }} {{ label.toLowerCase() }}</span></div>
</template>
<script setup>
defineProps({ modelValue: String, id: String, label: String, placeholder: String, count: Number, total: Number });
defineEmits(['update:modelValue']);
</script>
<style scoped>
.search-toolbar { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 0 20px; }.search-field { display:flex; align-items:center; border:1px solid #d6e0dd; border-radius:9px; background:#fbfcfb; width:min(100%,520px); padding:0 13px; gap:10px; }.search-field:focus-within { border-color:#4d8864; box-shadow:0 0 0 3px #4d886418; }.search-field > i { color:#65776c; }.search-field input { border:0; outline:0; background:transparent; padding:11px 0; font-size:14px; width:100%; min-width:0; }.search-field input::-webkit-search-cancel-button { display:none; }.search-field button { background:transparent; border:0; color:#5a6f62; padding:4px; }.search-count { color:#65776c; font-size:13px; white-space:nowrap; }
@media(max-width:576px) { .search-toolbar { align-items:flex-start; flex-direction:column; gap:8px; }.search-field { width:100%; } }
</style>
