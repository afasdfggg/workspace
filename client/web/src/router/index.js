import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';

// Auth Views
import Login from '../views/auth/Login.vue';
import AdminLogin from '../views/auth/AdminLogin.vue';
import SetPassword from '../views/auth/SetPassword.vue';
import ForgotPassword from '../views/auth/ForgotPassword.vue';
import ResetPassword from '../views/auth/ResetPassword.vue';

// Admin Views
import AdminDashboard from '../views/admin/Dashboard.vue';
import AdminEmployees from '../views/admin/Employees.vue';
import AdminProjects from '../views/admin/Projects.vue';
import AdminTasks from '../views/admin/Tasks.vue';
import AdminTimeTracking from '../views/admin/TimeTracking.vue';
import AdminScreenshots from '../views/admin/Screenshots.vue';
import AdminSettings from '../views/admin/Settings.vue';

// Employee Views
import EmployeeDashboard from '../views/employee/Dashboard.vue';
import EmployeeProjects from '../views/employee/Projects.vue';
import EmployeeTimeTracking from '../views/employee/TimeTracking.vue';
import EmployeeScreenshots from '../views/employee/Screenshots.vue';
import EmployeeSettings from '../views/employee/Settings.vue';

// Error Views
import NotFound from '../views/errors/NotFound.vue';

const routes = [
  // Auth Routes
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin,
    meta: { requiresAuth: false }
  },
  {
    path: '/set-password/:token',
    name: 'SetPassword',
    component: SetPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/reset-password/:token',
    name: 'ResetPassword',
    component: ResetPassword,
    meta: { requiresAuth: false }
  },
  
  // Admin Routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/employees',
    name: 'AdminEmployees',
    component: AdminEmployees,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/projects',
    name: 'AdminProjects',
    component: AdminProjects,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/tasks',
    name: 'AdminTasks',
    component: AdminTasks,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/time-tracking',
    name: 'AdminTimeTracking',
    component: AdminTimeTracking,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/screenshots',
    name: 'AdminScreenshots',
    component: AdminScreenshots,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: AdminSettings,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  
  // Employee Routes
  {
    path: '/',
    name: 'EmployeeDashboard',
    component: EmployeeDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects',
    name: 'EmployeeProjects',
    component: EmployeeProjects,
    meta: { requiresAuth: true }
  },
  {
    path: '/time-tracking',
    name: 'EmployeeTimeTracking',
    component: EmployeeTimeTracking,
    meta: { requiresAuth: true }
  },
  {
    path: '/screenshots',
    name: 'EmployeeScreenshots',
    component: EmployeeScreenshots,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'EmployeeSettings',
    component: EmployeeSettings,
    meta: { requiresAuth: true }
  },
  
  // Error Routes
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated'];
  const isAdmin = store.getters['auth/isAdmin'];
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      // Redirect to login page
      next({ name: 'Login' });
    } else if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
      // Redirect to employee dashboard if trying to access admin routes without admin privileges
      next({ name: 'EmployeeDashboard' });
    } else {
      next();
    }
  } else {
    // If route doesn't require authentication
    if (isAuthenticated && (to.name === 'Login' || to.name === 'AdminLogin')) {
      // Redirect to dashboard if already authenticated
      if (isAdmin) {
        next({ name: 'AdminDashboard' });
      } else {
        next({ name: 'EmployeeDashboard' });
      }
    } else {
      next();
    }
  }
});

export default router;