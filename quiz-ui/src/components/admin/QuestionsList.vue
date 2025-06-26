<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import QuestionEdition from '@/components/admin/QuestionEdition.vue';

const questions = ref([]);
const editingQuestion = ref(null); // soit une question existante, soit null pour création

onMounted(async () => {
  const token = localStorage.getItem('token');
  const res = await quizApiService.call('get', 'questions/all', null, token);
  if (res && res.data) {
    questions.value = res.data;
  }
});

function editQuestion(question) {
  editingQuestion.value = { ...question }; // on clone pour éviter de modifier directement
}

function createNewQuestion() {
  editingQuestion.value = {
    title: '',
    text: '',
    possibleAnswers: [{ text: '' }, { text: '' }, { text: '' }, { text: '' }],
    answerIndex: 1,
    image: '',
  };
}

async function deleteQuestion(id) {
  const token = localStorage.getItem('token');
  const confirmDelete = confirm('Es-tu sûr de vouloir supprimer cette question ?');
  if (!confirmDelete) return;

  const res = await quizApiService.deleteQuestion(id, token);
  if (res && res.status === 204) {
    questions.value = questions.value.filter((q) => q.id !== id);
  } else {
    alert('Erreur lors de la suppression.');
  }
}
</script>

<template>
  <div class="questions-list">
    <h2>Liste des questions</h2>

    <button @click="createNewQuestion">➕ Créer une nouvelle question</button>

    <ul>
      <li v-for="q in questions" :key="q.id">
        {{ q.title }}
        <button @click="editQuestion(q)">✏️ Modifier</button>
        <button @click="deleteQuestion(q.id)">🗑️ Supprimer</button>
      </li>
    </ul>
    <QuestionEdition
      v-if="editingQuestion"
      :question-to-edit="editingQuestion"
      @back-to-list="editingQuestion = null"
    />
  </div>
</template>

<style scoped>
.questions-list {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  font-family: sans-serif;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li > div {
  display: flex;
  gap: 0.5rem;
}

button {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  opacity: 0.9;
}

button:nth-child(1) {
  background-color: #ffc107;
  color: #000;
}

button:nth-child(2) {
  background-color: #dc3545;
  color: white;
}

button:first-of-type {
  background-color: #007bff;
  color: white;
  margin-bottom: 1rem;
}
</style>
