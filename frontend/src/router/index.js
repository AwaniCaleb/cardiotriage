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
  { path: '/',                   name: 'landing',       component: LandingPage,       meta: { title: 'CardioTriage — AI-Powered ECG Triage' } },
  { path: '/team',               name: 'team',          component: () => import('../pages/TeamPage.vue'), meta: { title: 'Meet the Team — CardioTriage' } },
  { path: '/login',              name: 'login',         component: LoginPage,          meta: { title: 'Sign In — CardioTriage' } },
  { path: '/register',           name: 'register',      component: () => import('../pages/RegisterPage.vue'), meta: { title: 'Create Account — CardioTriage' } },
  { path: '/dashboard',          name: 'dashboard',     component: DashboardPage,      meta: { requiresAuth: true, title: 'Dashboard — CardioTriage' } },
  { path: '/patients',           name: 'patients',      component: PatientsPage,       meta: { requiresAuth: true, title: 'Patients — CardioTriage' } },
  { path: '/patients/new',       name: 'patient-new',   component: AddPatientPage,     meta: { requiresAuth: true, title: 'Add Patient — CardioTriage' } },
  { path: '/patients/:id',       name: 'patient-detail', component: PatientDetailPage, meta: { requiresAuth: true, title: 'Patient Detail — CardioTriage' } },
  { path: '/patients/:id/edit',  name: 'patient-edit',  component: EditPatientPage,    meta: { requiresAuth: true, title: 'Edit Patient — CardioTriage' } },
  { path: '/recordings/:id/triage', name: 'triage-result', component: TriageResultPage, meta: { requiresAuth: true, title: 'Triage Result — CardioTriage' } },
  { path: '/live',               name: 'live-demo',     component: LiveDemoPage,       meta: { requiresAuth: true, title: 'Live Demo — CardioTriage' } },
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

router.afterEach((to) => {
  document.title = to.meta.title || 'CardioTriage'
})

export default router
