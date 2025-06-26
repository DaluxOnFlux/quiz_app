<template>
  <div class="newquiz">
    <h1>Nouvelle partie</h1>

    <p>Nom du joueur</p>
    <input type="text" v-model="username" />

    <button @click="launchNewQuiz">Démarrer !</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (!username.value.trim()) return;

  console.log('Launch new quiz with', username.value);
  participationStorageService.savePlayerName(username.value.trim());

  router.push('/questions');
}
</script>

<style scoped>
.newquiz {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  padding-top: 4rem;
}

h1 {
  font-size: 2.2rem;
  color: #2c3e50;
}

p {
  font-weight: 500;
  margin: 0;
  color: #007bff;
}

input[type='text'] {
  padding: 0.6rem 1rem;
  border: 2px solid #007bff;
  border-radius: 6px;
  font-size: 1rem;
  width: 100%;
  max-width: 300px;
}

button {
  padding: 0.6rem 1.2rem;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
