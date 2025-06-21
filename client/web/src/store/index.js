import { createStore } from 'vuex';
import auth from './modules/auth';
import employees from './modules/employees';
import projects from './modules/projects';
import tasks from './modules/tasks';
import timeTracking from './modules/timeTracking';
import screenshots from './modules/screenshots';

export default createStore({
  state: {
    loading: false,
    error: null,
    notification: null
  },
  getters: {
    isLoading: state => state.loading,
    getError: state => state.error,
    getNotification: state => state.notification
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    CLEAR_ERROR(state) {
      state.error = null;
    },
    SET_NOTIFICATION(state, notification) {
      state.notification = notification;
    },
    CLEAR_NOTIFICATION(state) {
      state.notification = null;
    }
  },
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading);
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error);
    },
    clearError({ commit }) {
      commit('CLEAR_ERROR');
    },
    setNotification({ commit }, notification) {
      commit('SET_NOTIFICATION', notification);
      
      // Auto clear notification after 5 seconds
      setTimeout(() => {
        commit('CLEAR_NOTIFICATION');
      }, 5000);
    },
    clearNotification({ commit }) {
      commit('CLEAR_NOTIFICATION');
    }
  },
  modules: {
    auth,
    employees,
    projects,
    tasks,
    timeTracking,
    screenshots
  }
});