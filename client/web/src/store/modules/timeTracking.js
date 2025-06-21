import axios from 'axios';

const state = {
  shifts: [],
  currentShift: null,
  projectTime: []
};

const getters = {
  getShifts: state => state.shifts,
  getCurrentShift: state => state.currentShift,
  getProjectTime: state => state.projectTime,
  isTracking: state => !!state.currentShift
};

const mutations = {
  SET_SHIFTS(state, shifts) {
    state.shifts = shifts;
  },
  SET_CURRENT_SHIFT(state, shift) {
    state.currentShift = shift;
  },
  ADD_SHIFT(state, shift) {
    state.shifts.push(shift);
  },
  UPDATE_SHIFT(state, updatedShift) {
    const index = state.shifts.findIndex(s => s.id === updatedShift.id);
    if (index !== -1) {
      state.shifts.splice(index, 1, updatedShift);
    }
    if (state.currentShift && state.currentShift.id === updatedShift.id) {
      state.currentShift = updatedShift;
    }
  },
  CLEAR_CURRENT_SHIFT(state) {
    state.currentShift = null;
  },
  SET_PROJECT_TIME(state, projectTime) {
    state.projectTime = projectTime;
  }
};

const actions = {
  // Get all shifts
  async getShifts({ commit, dispatch }, params = {}) {
    try {
      dispatch('setLoading', true, { root: true });
      
      // Build query string from params
      const queryParams = new URLSearchParams();
      Object.keys(params).forEach(key => {
        if (params[key]) {
          queryParams.append(key, params[key]);
        }
      });
      
      const url = `/api/v1/time-tracking/shift?${queryParams.toString()}`;
      const response = await axios.get(url);
      
      commit('SET_SHIFTS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch shifts', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get shift by ID
  async getShift({ commit, dispatch }, shiftId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get(`/api/v1/time-tracking/shift/${shiftId}`);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch shift', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Start time tracking
  async startTracking({ commit, dispatch, rootGetters }, { projectId, taskId }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const user = rootGetters['auth/getUser'];
      
      const shiftData = {
        type: 'manual',
        start: Date.now(),
        timezoneOffset: new Date().getTimezoneOffset() * 60 * 1000,
        employeeId: user.id,
        organizationId: user.organizationId,
        projectId,
        taskId
      };
      
      const response = await axios.post('/api/v1/time-tracking/shift', shiftData);
      
      commit('SET_CURRENT_SHIFT', response.data);
      commit('ADD_SHIFT', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Time tracking started!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to start time tracking', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Stop time tracking
  async stopTracking({ commit, dispatch, state }) {
    try {
      if (!state.currentShift) {
        throw new Error('No active tracking session');
      }
      
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.put(`/api/v1/time-tracking/shift/${state.currentShift.id}`, {
        end: Date.now()
      });
      
      commit('UPDATE_SHIFT', response.data);
      commit('CLEAR_CURRENT_SHIFT');
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Time tracking stopped!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to stop time tracking', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get project time analytics
  async getProjectTime({ commit, dispatch }, params) {
    try {
      dispatch('setLoading', true, { root: true });
      
      // Build query string from params
      const queryParams = new URLSearchParams();
      Object.keys(params).forEach(key => {
        if (params[key]) {
          queryParams.append(key, params[key]);
        }
      });
      
      const url = `/api/v1/time-tracking/analytics/project-time?${queryParams.toString()}`;
      const response = await axios.get(url);
      
      commit('SET_PROJECT_TIME', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch project time analytics', { root: true });
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