import axios from 'axios';
import store from '../store';
import router from '../router';

// Create axios instance
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      // If token expired, logout user
      store.dispatch('auth/logout');
      router.push({ name: 'Login' });
    }
    
    // Handle 403 Forbidden errors
    if (error.response && error.response.status === 403) {
      store.dispatch('setNotification', {
        type: 'error',
        message: 'You do not have permission to perform this action'
      });
    }
    
    // Handle 404 Not Found errors
    if (error.response && error.response.status === 404) {
      router.push({ name: 'NotFound' });
    }
    
    // Handle 500 Internal Server Error
    if (error.response && error.response.status >= 500) {
      store.dispatch('setNotification', {
        type: 'error',
        message: 'Server error. Please try again later.'
      });
    }
    
    return Promise.reject(error);
  }
);

export default api;