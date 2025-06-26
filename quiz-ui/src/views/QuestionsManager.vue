<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';

const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestion = ref(0);

async function loadQuestionByPosition(pos) {
  const res = await quizApiService.getQuestion(pos);
  currentQuestion.value = res.data;
}

async function answerClickedHandler(answerIdx) {
  console.log(`Réponse ${answerIdx} cliquée`);
  currentQuestionPosition.value++;

  if (currentQuestionPosition.value > totalNumberOfQuestion.value) {
    console.log('Fin du quiz');
    return;
  }
  await loadQuestionByPosition(currentQuestionPosition.value);
}

onMounted(async () => {
  const info = await quizApiService.getQuizInfo();
  totalNumberOfQuestion.value = info.data.size;
  await loadQuestionByPosition(currentQuestionPosition.value);
});
</script>

<template>
  <div class="quiz-container">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>

    <QuestionDisplay
      v-if="currentQuestion"
      :question="currentQuestion"
      @answer-clicked="answerClickedHandler"
    />
  </div>
</template>

<style scoped>
.quiz-container {
  text-align: center;
  padding: 2rem;
}
</style>
