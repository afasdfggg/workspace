import axios from 'axios';
import router from '../../router';

const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  isAdmin: localStorage.getItem('isAdmin') === 'true' || false
};

const getters = {
  isAuthenticated: state => !!state.token,
  getUser: state => state.user,
  isAdmin: state => state.isAdmin,
  getToken: state => state.token
};

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
  },
  SET_USER(state, user) {
    state.user = user;
  },
  SET_ADMIN(state, isAdmin) {
    state.isAdmin = isAdmin;
  },
  CLEAR_AUTH(state) {
    state.token = null;
    state.user = null;
    state.isAdmin = false;
  }
};

const actions = {
  // Check if user is authenticated
  checkAuth({ commit, state }) {
    if (state.token && state.user) {
      // Set axios default headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${state.token}`;
    }
  },
  
  // Login user
  async login({ commit, dispatch }, credentials) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/auth/login', credentials);
      
      const token = response.data.access_token;
      const user = {
        id: response.data.id,
        name: response.data.name,
        email: response.data.email,
        organizationId: response.data.organizationId
      };
      
      // Save to localStorage
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('isAdmin', 'false');
      
      // Set axios default headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // Update state
      commit('SET_TOKEN', token);
      commit('SET_USER', user);
      commit('SET_ADMIN', false);
      
      // Redirect to dashboard
      router.push({ name: 'EmployeeDashboard' });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'Login successful!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Login failed', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Login admin
  async loginAdmin({ commit, dispatch }, credentials) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/auth/admin/login', credentials);
      
      const token = response.data.access_token;
      const user = {
        id: response.data.id,
        name: response.data.name,
        email: response.data.email,
        organizationId: response.data.organizationId
      };
      
      // Save to localStorage
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('isAdmin', 'true');
      
      // Set axios default headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // Update state
      commit('SET_TOKEN', token);
      commit('SET_USER', user);
      commit('SET_ADMIN', true);
      
      // Redirect to admin dashboard
      router.push({ name: 'AdminDashboard' });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'Admin login successful!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Admin login failed', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Generate API key for admin
  async generateApiKey({ commit, dispatch, state }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/auth/admin/api-key', {
        username: state.user.email,
        password: '' // This would need to be provided by the user
      });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'API key generated successfully!'
      }, { root: true });
      
      return response.data.api_key;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to generate API key', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Set password (for employee email verification)
  async setPassword({ dispatch }, { token, password }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post(`/api/v1/auth/set-password/${token}`, { password });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'Password set successfully! You can now log in.'
      }, { root: true });
      
      // Redirect to login page
      router.push({ name: 'Login' });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to set password', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Forgot password
  async forgotPassword({ dispatch }, email) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/auth/forgot-password', { email });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'Password reset email sent! Check your inbox.'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to send password reset email', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Reset password
  async resetPassword({ dispatch }, { token, password }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post(`/api/v1/auth/reset-password/${token}`, { password });
      
      // Show success notification
      dispatch('setNotification', {
        type: 'success',
        message: 'Password reset successfully! You can now log in.'
      }, { root: true });
      
      // Redirect to login page
      router.push({ name: 'Login' });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to reset password', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Logout
  logout({ commit }) {
    // Clear localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('isAdmin');
    
    // Clear axios default headers
    delete axios.defaults.headers.common['Authorization'];
    
    // Update state
    commit('CLEAR_AUTH');
    
    // Redirect to login page
    router.push({ name: 'Login' });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};