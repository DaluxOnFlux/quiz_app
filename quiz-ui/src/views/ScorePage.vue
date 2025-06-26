<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from '@/services/ParticipationStorageService';

const playerName = ref('');
const score = ref(0);

onMounted(() => {
  playerName.value = participationStorageService.getPlayerName();
  score.value = participationStorageService.getParticipationScore();
});
</script>

<template>
  <div class="score-page">
    <h1>Félicitations {{ playerName }} !</h1>
    <p>
      Votre score final est : <strong>{{ score }}</strong>
    </p>
  </div>
</template>

<style scoped>
.score-page {
  text-align: center;
  padding: 3rem;
  color: #2c3e50;
}

.score-page h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.score-page p {
  font-size: 1.5rem;
}
</style>
