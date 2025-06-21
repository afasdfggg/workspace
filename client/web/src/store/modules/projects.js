import axios from 'axios';

const state = {
  projects: [],
  project: null
};

const getters = {
  getProjects: state => state.projects,
  getProject: state => state.project,
  getActiveProjects: state => state.projects.filter(p => !p.archived)
};

const mutations = {
  SET_PROJECTS(state, projects) {
    state.projects = projects;
  },
  SET_PROJECT(state, project) {
    state.project = project;
  },
  ADD_PROJECT(state, project) {
    state.projects.push(project);
  },
  UPDATE_PROJECT(state, updatedProject) {
    const index = state.projects.findIndex(p => p.id === updatedProject.id);
    if (index !== -1) {
      state.projects.splice(index, 1, updatedProject);
    }
    if (state.project && state.project.id === updatedProject.id) {
      state.project = updatedProject;
    }
  },
  REMOVE_PROJECT(state, projectId) {
    state.projects = state.projects.filter(p => p.id !== projectId);
    if (state.project && state.project.id === projectId) {
      state.project = null;
    }
  }
};

const actions = {
  // Get all projects
  async getProjects({ commit, dispatch }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get('/api/v1/project');
      
      commit('SET_PROJECTS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch projects', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get project by ID
  async getProject({ commit, dispatch }, projectId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get(`/api/v1/project/${projectId}`);
      
      commit('SET_PROJECT', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch project', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Create new project
  async createProject({ commit, dispatch }, projectData) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/project', projectData);
      
      commit('ADD_PROJECT', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Project created successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to create project', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Update project
  async updateProject({ commit, dispatch }, { projectId, projectData }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.put(`/api/v1/project/${projectId}`, projectData);
      
      commit('UPDATE_PROJECT', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Project updated successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to update project', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Delete project
  async deleteProject({ commit, dispatch }, projectId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.delete(`/api/v1/project/${projectId}`);
      
      commit('REMOVE_PROJECT', projectId);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Project deleted successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to delete project', { root: true });
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