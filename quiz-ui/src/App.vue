<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <header class="main-header">
      <RouterLink to="/" class="header-link">Accueil</RouterLink>
      <RouterLink to="/admin" class="header-link">Admin</RouterLink>
    </header>

    <RouterView />
  </div>
</template>

<script setup></script>

<style scoped>
.main-header {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-link {
  text-decoration: none;
  color: #007bff;
  font-weight: 600;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.header-link:hover {
  color: #0056b3;
}
</style>
