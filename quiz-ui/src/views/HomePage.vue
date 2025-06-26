<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

const registeredScores = ref([]);

onMounted(async () => {
  const res = await quizApiService.getQuizInfo();
  registeredScores.value = res?.data?.scores || [];
});
</script>

<template>
  <section class="home">
    <h1 class="home__title">Bienvenue sur le Quiz</h1>

    <router-link to="/new-quiz" class="home__btn"> Démarrer le quiz ! </router-link>
  </section>
</template>
