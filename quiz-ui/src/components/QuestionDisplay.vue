<script setup>
const props = defineProps({
  question: Object,
});
const emit = defineEmits(['click-on-answer']);
</script>

<template>
  <div class="question-display">
    <h2>{{ question.title }}</h2>
    <p>{{ question.text }}</p>

    <img v-if="question.image" :src="question.image" class="question-image" />

    <ul class="answers">
      <li
        v-for="(answer, index) in question.possibleAnswers"
        :key="index"
        @click="emit('click-on-answer', index + 1)"
      >
        {{ answer.text }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.question-display {
  text-align: center;
  padding: 2rem;
}

.question-image {
  max-width: 300px;
  margin: 1rem auto;
  display: block;
}

.answers {
  list-style: none;
  padding: 0;
  margin-top: 2rem;
}

.answers li {
  margin: 0.5rem 0;
  padding: 0.8rem;
  background-color: #007bff;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.answers li:hover {
  background-color: #0056b3;
}
</style>
