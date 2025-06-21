import axios from 'axios';

const state = {
  tasks: [],
  task: null
};

const getters = {
  getTasks: state => state.tasks,
  getTask: state => state.task,
  getTasksByProject: state => projectId => state.tasks.filter(t => t.projectId === projectId)
};

const mutations = {
  SET_TASKS(state, tasks) {
    state.tasks = tasks;
  },
  SET_TASK(state, task) {
    state.task = task;
  },
  ADD_TASK(state, task) {
    state.tasks.push(task);
  },
  UPDATE_TASK(state, updatedTask) {
    const index = state.tasks.findIndex(t => t.id === updatedTask.id);
    if (index !== -1) {
      state.tasks.splice(index, 1, updatedTask);
    }
    if (state.task && state.task.id === updatedTask.id) {
      state.task = updatedTask;
    }
  },
  REMOVE_TASK(state, taskId) {
    state.tasks = state.tasks.filter(t => t.id !== taskId);
    if (state.task && state.task.id === taskId) {
      state.task = null;
    }
  }
};

const actions = {
  // Get all tasks
  async getTasks({ commit, dispatch }, projectId = null) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const url = projectId ? `/api/v1/task?projectId=${projectId}` : '/api/v1/task';
      const response = await axios.get(url);
      
      commit('SET_TASKS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch tasks', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get task by ID
  async getTask({ commit, dispatch }, taskId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get(`/api/v1/task/${taskId}`);
      
      commit('SET_TASK', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch task', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Create new task
  async createTask({ commit, dispatch }, taskData) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/task', taskData);
      
      commit('ADD_TASK', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Task created successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to create task', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Update task
  async updateTask({ commit, dispatch }, { taskId, taskData }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.put(`/api/v1/task/${taskId}`, taskData);
      
      commit('UPDATE_TASK', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Task updated successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to update task', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Delete task
  async deleteTask({ commit, dispatch }, taskId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.delete(`/api/v1/task/${taskId}`);
      
      commit('REMOVE_TASK', taskId);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Task deleted successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to delete task', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};