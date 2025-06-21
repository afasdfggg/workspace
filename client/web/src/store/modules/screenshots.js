import axios from 'axios';

const state = {
  screenshots: [],
  paginatedScreenshots: {
    data: [],
    next: null
  },
  hasMore: false
};

const getters = {
  getScreenshots: state => state.screenshots,
  getPaginatedScreenshots: state => state.paginatedScreenshots.data,
  hasMoreScreenshots: state => state.hasMore
};

const mutations = {
  SET_SCREENSHOTS(state, screenshots) {
    state.screenshots = screenshots;
  },
  SET_PAGINATED_SCREENSHOTS(state, { data, next }) {
    state.paginatedScreenshots = { data, next };
    state.hasMore = !!next;
  },
  APPEND_SCREENSHOTS(state, { data, next }) {
    state.paginatedScreenshots.data = [...state.paginatedScreenshots.data, ...data];
    state.paginatedScreenshots.next = next;
    state.hasMore = !!next;
  },
  REMOVE_SCREENSHOT(state, screenshotId) {
    state.screenshots = state.screenshots.filter(s => s.id !== screenshotId);
    state.paginatedScreenshots.data = state.paginatedScreenshots.data.filter(s => s.id !== screenshotId);
  }
};

const actions = {
  // Get screenshots
  async getScreenshots({ commit, dispatch }, params) {
    try {
      dispatch('setLoading', true, { root: true });
      
      // Build query string from params
      const queryParams = new URLSearchParams();
      Object.keys(params).forEach(key => {
        if (params[key]) {
          queryParams.append(key, params[key]);
        }
      });
      
      const url = `/api/v1/analytics/screenshot?${queryParams.toString()}`;
      const response = await axios.get(url);
      
      commit('SET_SCREENSHOTS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch screenshots', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get paginated screenshots
  async getPaginatedScreenshots({ commit, dispatch }, params) {
    try {
      dispatch('setLoading', true, { root: true });
      
      // Build query string from params
      const queryParams = new URLSearchParams();
      Object.keys(params).forEach(key => {
        if (params[key]) {
          queryParams.append(key, params[key]);
        }
      });
      
      const url = `/api/v1/analytics/screenshot/paginate?${queryParams.toString()}`;
      const response = await axios.get(url);
      
      commit('SET_PAGINATED_SCREENSHOTS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch paginated screenshots', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Load more screenshots
  async loadMoreScreenshots({ commit, dispatch, state }, params) {
    try {
      if (!state.paginatedScreenshots.next) {
        return;
      }
      
      dispatch('setLoading', true, { root: true });
      
      // Build query string from params
      const queryParams = new URLSearchParams();
      Object.keys(params).forEach(key => {
        if (params[key]) {
          queryParams.append(key, params[key]);
        }
      });
      
      // Add next token
      queryParams.append('next', state.paginatedScreenshots.next);
      
      const url = `/api/v1/analytics/screenshot/paginate?${queryParams.toString()}`;
      const response = await axios.get(url);
      
      commit('APPEND_SCREENSHOTS', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to load more screenshots', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Delete screenshot
  async deleteScreenshot({ commit, dispatch }, screenshotId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      await axios.delete(`/api/v1/analytics/screenshot/${screenshotId}`);
      
      commit('REMOVE_SCREENSHOT', screenshotId);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Screenshot deleted successfully!'
      }, { root: true });
      
      return true;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to delete screenshot', { root: true });
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