import { createRouter, createWebHistory } from 'vue-router'

import LandingPage from '../pages/LandingPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import PatientsPage from '../pages/PatientsPage.vue'
import AddPatientPage from '../pages/AddPatientPage.vue'
import PatientDetailPage from '../pages/PatientDetailPage.vue'
import EditPatientPage from '../pages/EditPatientPage.vue'
import TriageResultPage from '../pages/TriageResultPage.vue'
import LiveDemoPage from '../pages/LiveDemoPage.vue'

const routes = [
  { path: '/', name: 'landing', component: LandingPage },
  { path: '/team', name: 'team', component: () => import('../pages/TeamPage.vue') },
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/register', name: 'register', component: () => import('../pages/RegisterPage.vue') },
  { path: '/dashboard', name: 'dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/patients', name: 'patients', component: PatientsPage, meta: { requiresAuth: true } },
  { path: '/patients/new', name: 'patient-new', component: AddPatientPage, meta: { requiresAuth: true } },
  { path: '/patients/:id', name: 'patient-detail', component: PatientDetailPage, meta: { requiresAuth: true } },
  { path: '/patients/:id/edit', name: 'patient-edit', component: EditPatientPage, meta: { requiresAuth: true } },
  { path: '/recordings/:id/triage', name: 'triage-result', component: TriageResultPage, meta: { requiresAuth: true } },
  { path: '/live', name: 'live-demo', component: LiveDemoPage, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !localStorage.getItem('ct_token')) {
    return { path: '/login' }
  }
})

export default router
