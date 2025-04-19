import { createRouter, createWebHistory } from 'vue-router'
import Recognition from '../views/Recognition.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'recognition',
      component: Recognition,
    },
    {
      path: '/counter',
      name: 'counter',
      component: () => import('../views/Counter.vue'),
    },
  ],
})

export default router