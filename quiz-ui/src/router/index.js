import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewQuizPage from '@/views/NewQuizPage.vue';
import QuestionsManager from '@/views/QuestionsManager.vue';
import ScorePage from '@/views/ScorePage.vue';
import Admin from '@/views/Admin.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/new-quiz',
      name: 'new-quiz',
      component: NewQuizPage,
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsManager,
    },
    {
      path: '/score',
      name: 'score',
      component: ScorePage,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
  ],
});

export default router;
