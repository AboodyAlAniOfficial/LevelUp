import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import MealView from '../views/MealView.vue'
import ExerciseView from '../views/ExerciseView.vue'
import Login from '../views/LoginView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/meal',
    name: 'meal',
    component: MealView
  },
  {
    path: '/exercise',
    name: 'exercise',
    component: ExerciseView
  },
  {
    path: '/leaderboard',
    name: 'leaderboard',
    component: LeaderboardView
  }
]

const router = createRouter({
  history: createWebHistory(), // Removed process.env.BASE_URL for simplicity
  routes
})

// Navigation guard (optional)
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken') !== null; // Check login status

  if (to.matched.some(record => record.meta.requireLogin) && !isAuthenticated) {
    next({ name: 'login', query: { to: to.path } }); // Redirect to login page
  } else {
    next();
  }
});

export default router;
