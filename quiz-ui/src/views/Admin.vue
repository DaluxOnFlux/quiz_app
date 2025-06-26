<script setup>
import { ref } from 'vue';
import quizApiService from '@/services/QuizApiService';
import QuestionsList from '@/components/admin/QuestionsList.vue';

const password = ref('');
const token = ref(localStorage.getItem('token') || '');
const showPassword = ref(false);

const connect = async () => {
  try {
    const res = await quizApiService.login(password.value);
    if (res.status === 200) {
      token.value = res.data.token;
      localStorage.setItem('token', res.data.token);
    } else {
      alert('Mot de passe incorrect');
    }
  } catch (err) {
    alert('Mot de passe incorrect');
  }
};

const logout = () => {
  token.value = '';
  localStorage.removeItem('token');
};
</script>

<template>
  <div class="admin-container">
    <h1>Administration</h1>

    <div v-if="!token" class="login-form">
      <label>
        Mot de passe :
        <div class="password-wrapper">
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Entrez le mot de passe admin"
          />
          <button class="toggle-password" @click="showPassword = !showPassword" type="button">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </label>
      <button @click="connect" class="btn-primary">Connexion</button>
    </div>

    <div v-else>
      <p class="connected">Connecté à la zone admin ✅</p>
      <button @click="logout" class="btn-secondary">Se déconnecter</button>
      <QuestionsList />
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: sans-serif;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

label {
  display: block;
  font-weight: bold;
  color: #333;
}

.password-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.3rem;
}

.password-wrapper input {
  flex: 1;
  padding: 0.6rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 250px;
}

.toggle-password {
  background: none;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 0.3rem 0.6rem;
}

button {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #dc3545;
  color: white;
}

.btn-secondary:hover {
  background-color: #c82333;
}

.connected {
  margin-bottom: 1rem;
  font-weight: bold;
  color: #28a745;
}
</style>
