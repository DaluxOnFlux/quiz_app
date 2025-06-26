<script setup>
import { ref, watch } from 'vue';
import quizApiService from '@/services/QuizApiService';
import ImageUpload from './ImageUpload.vue';

const props = defineProps({
  questionToEdit: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['back-to-list']);

const question = ref({
  id: null,
  position: 1,
  title: '',
  text: '',
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
  ],
  image: '',
});

watch(
  () => props.questionToEdit,
  (newVal) => {
    if (newVal) {
      // Copie profonde avec sécurité sur les réponses
      question.value = {
        id: newVal.id || null,
        position: newVal.position || 1,
        title: newVal.title || '',
        text: newVal.text || '',
        image: newVal.image || '',
        possibleAnswers: (newVal.possibleAnswers || []).map((ans) => ({
          text: ans.text || '',
          isCorrect: !!ans.isCorrect,
        })),
      };
    }
  },
  { immediate: true }
);

function imageFileChangedHandler(b64String) {
  question.value.image = b64String;
}

async function saveQuestion() {
  const token = localStorage.getItem('token');

  if (question.value.id) {
    await quizApiService.call('put', `questions/${question.value.id}`, question.value, token);
  } else {
    await quizApiService.call('post', 'questions', question.value, token);
  }

  emit('back-to-list');
}

function cancelEdit() {
  emit('back-to-list');
}
</script>

<template>
  <div class="question-edition">
    <h2>{{ question.id ? 'Modifier la question' : 'Créer une nouvelle question' }}</h2>

    <label>
      Titre :
      <input v-model="question.title" type="text" />
    </label>

    <label>
      Position :
      <input v-model.number="question.position" type="number" min="1" />
    </label>

    <label>
      Texte :
      <textarea v-model="question.text"></textarea>
    </label>

    <h3>Réponses possibles</h3>
    <div v-for="(answer, index) in question.possibleAnswers" :key="index" class="answer-item">
      <input v-model="answer.text" type="text" placeholder="Texte de la réponse" />
      <label>
        <input type="checkbox" v-model="answer.isCorrect" />
        Bonne réponse
      </label>
    </div>

    <h3>Image</h3>
    <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="question.image" />

    <div class="edition-actions">
      <button @click="saveQuestion">Enregistrer</button>
      <button @click="cancelEdit">Annuler</button>
    </div>
  </div>
</template>

<style scoped>
.question-edition {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h2,
h3 {
  color: #333;
  text-align: center;
}

label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
  color: #444;
}

input[type='text'],
input[type='number'],
textarea {
  margin-top: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  transition: border-color 0.2s ease;
}

input[type='text']:focus,
input[type='number']:focus,
textarea:focus {
  border-color: #007bff;
  outline: none;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.answer-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.answer-item input[type='text'] {
  flex: 1;
}

.answer-item label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.edition-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.edition-actions button {
  padding: 0.6rem 1.4rem;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.edition-actions button:first-of-type {
  background-color: #28a745;
  color: white;
}

.edition-actions button:first-of-type:hover {
  background-color: #218838;
}

.edition-actions button:last-of-type {
  background-color: #6c757d;
  color: white;
}

.edition-actions button:last-of-type:hover {
  background-color: #5a6268;
}
</style>
