import axios from 'axios';

const state = {
  employees: [],
  employee: null
};

const getters = {
  getEmployees: state => state.employees,
  getEmployee: state => state.employee
};

const mutations = {
  SET_EMPLOYEES(state, employees) {
    state.employees = employees;
  },
  SET_EMPLOYEE(state, employee) {
    state.employee = employee;
  },
  ADD_EMPLOYEE(state, employee) {
    state.employees.push(employee);
  },
  UPDATE_EMPLOYEE(state, updatedEmployee) {
    const index = state.employees.findIndex(e => e.id === updatedEmployee.id);
    if (index !== -1) {
      state.employees.splice(index, 1, updatedEmployee);
    }
    if (state.employee && state.employee.id === updatedEmployee.id) {
      state.employee = updatedEmployee;
    }
  },
  REMOVE_EMPLOYEE(state, employeeId) {
    state.employees = state.employees.filter(e => e.id !== employeeId);
    if (state.employee && state.employee.id === employeeId) {
      state.employee = null;
    }
  }
};

const actions = {
  // Get all employees
  async getEmployees({ commit, dispatch }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get('/api/v1/employee');
      
      commit('SET_EMPLOYEES', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch employees', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Get employee by ID
  async getEmployee({ commit, dispatch }, employeeId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.get(`/api/v1/employee/${employeeId}`);
      
      commit('SET_EMPLOYEE', response.data);
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to fetch employee', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Create new employee
  async createEmployee({ commit, dispatch }, employeeData) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.post('/api/v1/employee', employeeData);
      
      commit('ADD_EMPLOYEE', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Employee created successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to create employee', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Update employee
  async updateEmployee({ commit, dispatch }, { employeeId, employeeData }) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.put(`/api/v1/employee/${employeeId}`, employeeData);
      
      commit('UPDATE_EMPLOYEE', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Employee updated successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to update employee', { root: true });
      throw error;
    } finally {
      dispatch('setLoading', false, { root: true });
    }
  },
  
  // Deactivate employee
  async deactivateEmployee({ commit, dispatch }, employeeId) {
    try {
      dispatch('setLoading', true, { root: true });
      
      const response = await axios.put(`/api/v1/employee/deactivate/${employeeId}`);
      
      commit('UPDATE_EMPLOYEE', response.data);
      
      dispatch('setNotification', {
        type: 'success',
        message: 'Employee deactivated successfully!'
      }, { root: true });
      
      return response.data;
    } catch (error) {
      dispatch('setError', error.response?.data?.message || 'Failed to deactivate employee', { root: true });
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