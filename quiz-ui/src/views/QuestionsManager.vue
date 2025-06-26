<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

const router = useRouter();

const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestion = ref(0);

/* charge une question */
async function loadQuestionByPosition(pos) {
  const res = await quizApiService.getQuestion(pos);
  currentQuestion.value = res.data; // ← JSON de la question
}

/* appelé quand on clique sur une réponse */
async function answerClickedHandler(answerIdx) {
  // ← on garde le même nom
  console.log(`Réponse ${answerIdx} cliquée pour la question ${currentQuestionPosition.value}`);

  // ici tu pourras tester si answerIdx est correct et incrémenter un score
  currentQuestionPosition.value++;

  // fin du quiz ?
  if (currentQuestionPosition.value > totalNumberOfQuestion.value) {
    console.log('Fin du quiz');
    participationStorageService.saveParticipationScore(3); // score fictif
    router.push('/score');
    return;
  }

  // sinon, charge la suivante
  await loadQuestionByPosition(currentQuestionPosition.value);
}

/* initialisation */
onMounted(async () => {
  const info = await quizApiService.getQuizInfo();
  totalNumberOfQuestion.value = info.data.size; // nb total
  await loadQuestionByPosition(currentQuestionPosition.value);
});
</script>

<template>
  <div class="quiz-container">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>

    <QuestionDisplay
      v-if="currentQuestion"
      :question="currentQuestion"
      @click-on-answer="answerClickedHandler"
    />
  </div>
</template>

<style scoped>
.quiz-container {
  text-align: center;
  padding: 2rem;
}
</style>
