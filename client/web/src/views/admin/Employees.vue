<template>
  <DashboardLayout title="Employees">
    <template #sidebar>
      <AdminSidebar />
    </template>

    <div class="employees-container">
      <!-- Header Actions -->
      <div class="page-header">
        <div class="page-header-left">
          <h2>Employees</h2>
          <p class="text-muted">Manage your organization's employees</p>
        </div>
        <div class="page-header-right">
          <Button
            type="primary"
            icon="person_add"
            @click="showAddModal = true"
          >
            Add Employee
          </Button>
        </div>
      </div>

      <!-- Filters -->
      <Card>
        <div class="filters">
          <div class="filter-group">
            <label class="form-label">Search</label>
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search employees..."
            />
          </div>
          
          <div class="filter-group">
            <label class="form-label">Status</label>
            <select v-model="statusFilter" class="form-control">
              <option value="">All</option>
              <option value="active">Active</option>
              <option value="deactivated">Deactivated</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="form-label">Team</label>
            <select v-model="teamFilter" class="form-control">
              <option value="">All Teams</option>
              <option v-for="team in teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
        </div>
      </Card>

      <!-- Employees Table -->
      <Card>
        <div v-if="loading" class="text-center p-4">
          <div class="spinner"></div>
        </div>
        
        <div v-else-if="filteredEmployees.length === 0" class="empty-state">
          <div class="empty-state-icon">
            <i class="material-icons">people</i>
          </div>
          <h3 class="empty-state-title">No Employees Found</h3>
          <p class="empty-state-description">
            {{ searchQuery ? 'No employees match your search criteria.' : 'Get started by adding your first employee.' }}
          </p>
          <Button
            v-if="!searchQuery"
            type="primary"
            icon="person_add"
            @click="showAddModal = true"
          >
            Add Employee
          </Button>
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Employee</th>
                <th>Email</th>
                <th>Title</th>
                <th>Team</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="employee in filteredEmployees" :key="employee.id">
                <td>
                  <div class="employee-info">
                    <div class="employee-avatar">
                      {{ getInitials(employee.name) }}
                    </div>
                    <div>
                      <div class="employee-name">{{ employee.name }}</div>
                      <div class="employee-id">ID: {{ employee.identifier || employee.id }}</div>
                    </div>
                  </div>
                </td>
                <td>{{ employee.email }}</td>
                <td>{{ employee.title || '-' }}</td>
                <td>{{ getTeamName(employee.teamId) }}</td>
                <td>
                  <span :class="['badge', employee.deactivated ? 'badge-danger' : 'badge-success']">
                    {{ employee.deactivated ? 'Deactivated' : 'Active' }}
                  </span>
                </td>
                <td>{{ formatDate(employee.createdAt) }}</td>
                <td>
                  <div class="action-buttons">
                    <Button
                      type="outline-primary"
                      size="small"
                      icon="edit"
                      @click="editEmployee(employee)"
                    >
                      Edit
                    </Button>
                    
                    <Button
                      v-if="!employee.deactivated"
                      type="outline-danger"
                      size="small"
                      icon="block"
                      @click="deactivateEmployee(employee)"
                    >
                      Deactivate
                    </Button>
                    
                    <Button
                      v-else
                      type="outline-success"
                      size="small"
                      icon="check_circle"
                      @click="activateEmployee(employee)"
                    >
                      Activate
                    </Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- Add/Edit Employee Modal -->
    <Modal
      :show="showAddModal || showEditModal"
      :title="editingEmployee ? 'Edit Employee' : 'Add Employee'"
      @close="closeModal"
    >
      <form @submit.prevent="saveEmployee">
        <div class="form-group">
          <label class="form-label">Name *</label>
          <input
            v-model="employeeForm.name"
            type="text"
            class="form-control"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Email *</label>
          <input
            v-model="employeeForm.email"
            type="email"
            class="form-control"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Job Title</label>
          <input
            v-model="employeeForm.title"
            type="text"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Team</label>
          <select v-model="employeeForm.teamId" class="form-control">
            <option value="">No Team</option>
            <option v-for="team in teams" :key="team.id" :value="team.id">
              {{ team.name }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Projects</label>
          <div class="checkbox-group">
            <label v-for="project in projects" :key="project.id" class="form-check">
              <input
                v-model="employeeForm.projects"
                type="checkbox"
                :value="project.id"
                class="form-check-input"
              />
              <span class="form-check-label">{{ project.name }}</span>
            </label>
          </div>
        </div>
      </form>
      
      <template #footer>
        <Button type="secondary" @click="closeModal">
          Cancel
        </Button>
        <Button
          type="primary"
          :loading="saving"
          @click="saveEmployee"
        >
          {{ editingEmployee ? 'Update' : 'Add' }} Employee
        </Button>
      </template>
    </Modal>

    <!-- Deactivate Confirmation Modal -->
    <Modal
      :show="showDeactivateModal"
      title="Deactivate Employee"
      @close="showDeactivateModal = false"
    >
      <p>Are you sure you want to deactivate <strong>{{ employeeToDeactivate?.name }}</strong>?</p>
      <p class="text-muted">
        This will prevent them from logging in and tracking time. You can reactivate them later.
      </p>
      
      <template #footer>
        <Button type="secondary" @click="showDeactivateModal = false">
          Cancel
        </Button>
        <Button
          type="danger"
          :loading="deactivating"
          @click="confirmDeactivate"
        >
          Deactivate
        </Button>
      </template>
    </Modal>
  </DashboardLayout>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import DashboardLayout from '@/components/layout/DashboardLayout.vue';
import AdminSidebar from '@/components/admin/AdminSidebar.vue';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import Modal from '@/components/common/Modal.vue';
import { formatDate } from '@/utils/date';

export default {
  name: 'AdminEmployees',
  components: {
    DashboardLayout,
    AdminSidebar,
    Card,
    Button,
    Modal
  },
  data() {
    return {
      loading: true,
      saving: false,
      deactivating: false,
      searchQuery: '',
      statusFilter: '',
      teamFilter: '',
      showAddModal: false,
      showEditModal: false,
      showDeactivateModal: false,
      editingEmployee: null,
      employeeToDeactivate: null,
      employeeForm: {
        name: '',
        email: '',
        title: '',
        teamId: '',
        projects: []
      },
      teams: [],
      projects: []
    };
  },
  computed: {
    ...mapGetters({
      employees: 'employees/getEmployees'
    }),
    
    filteredEmployees() {
      let filtered = this.employees;
      
      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(employee =>
          employee.name.toLowerCase().includes(query) ||
          employee.email.toLowerCase().includes(query) ||
          (employee.title && employee.title.toLowerCase().includes(query))
        );
      }
      
      // Status filter
      if (this.statusFilter) {
        if (this.statusFilter === 'active') {
          filtered = filtered.filter(employee => !employee.deactivated);
        } else if (this.statusFilter === 'deactivated') {
          filtered = filtered.filter(employee => employee.deactivated);
        }
      }
      
      // Team filter
      if (this.teamFilter) {
        filtered = filtered.filter(employee => employee.teamId === this.teamFilter);
      }
      
      return filtered;
    }
  },
  async created() {
    await this.loadData();
    
    // Check if we should show add modal from query params
    if (this.$route.query.action === 'add') {
      this.showAddModal = true;
    }
  },
  methods: {
    ...mapActions({
      getEmployees: 'employees/getEmployees',
      createEmployee: 'employees/createEmployee',
      updateEmployee: 'employees/updateEmployee',
      deactivateEmployeeAction: 'employees/deactivateEmployee',
      getProjects: 'projects/getProjects'
    }),
    
    formatDate,
    
    async loadData() {
      this.loading = true;
      
      try {
        await Promise.all([
          this.getEmployees(),
          this.getProjects(),
          this.loadTeams()
        ]);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    async loadTeams() {
      // Mock teams data - in real app, this would come from API
      this.teams = [
        { id: 'team1', name: 'Development' },
        { id: 'team2', name: 'Design' },
        { id: 'team3', name: 'Marketing' },
        { id: 'team4', name: 'Sales' }
      ];
    },
    
    getInitials(name) {
      if (!name) return '';
      
      const nameParts = name.split(' ');
      if (nameParts.length === 1) {
        return nameParts[0].charAt(0).toUpperCase();
      }
      
      return (nameParts[0].charAt(0) + nameParts[nameParts.length - 1].charAt(0)).toUpperCase();
    },
    
    getTeamName(teamId) {
      if (!teamId) return '-';
      
      const team = this.teams.find(t => t.id === teamId);
      return team ? team.name : '-';
    },
    
    editEmployee(employee) {
      this.editingEmployee = employee;
      this.employeeForm = {
        name: employee.name,
        email: employee.email,
        title: employee.title || '',
        teamId: employee.teamId || '',
        projects: employee.projects || []
      };
      this.showEditModal = true;
    },
    
    deactivateEmployee(employee) {
      this.employeeToDeactivate = employee;
      this.showDeactivateModal = true;
    },
    
    async activateEmployee(employee) {
      try {
        // In a real app, you would have an activate endpoint
        await this.updateEmployee({
          employeeId: employee.id,
          employeeData: { deactivated: null }
        });
      } catch (error) {
        console.error('Error activating employee:', error);
      }
    },
    
    async confirmDeactivate() {
      if (!this.employeeToDeactivate) return;
      
      this.deactivating = true;
      
      try {
        await this.deactivateEmployeeAction(this.employeeToDeactivate.id);
        this.showDeactivateModal = false;
        this.employeeToDeactivate = null;
      } catch (error) {
        console.error('Error deactivating employee:', error);
      } finally {
        this.deactivating = false;
      }
    },
    
    async saveEmployee() {
      this.saving = true;
      
      try {
        if (this.editingEmployee) {
          await this.updateEmployee({
            employeeId: this.editingEmployee.id,
            employeeData: this.employeeForm
          });
        } else {
          await this.createEmployee(this.employeeForm);
        }
        
        this.closeModal();
      } catch (error) {
        console.error('Error saving employee:', error);
      } finally {
        this.saving = false;
      }
    },
    
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.editingEmployee = null;
      this.employeeForm = {
        name: '',
        email: '',
        title: '',
        teamId: '',
        projects: []
      };
    }
  }
};
</script>

<style scoped>
.employees-container {
  max-width: 1200px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.page-header-left h2 {
  margin-bottom: 0.25rem;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 0;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.employee-info {
  display: flex;
  align-items: center;
}

.employee-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.employee-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.employee-id {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.checkbox-group {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: 0.25rem;
  padding: 0.5rem;
}

.form-check {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.form-check:last-child {
  margin-bottom: 0;
}

.form-check-input {
  margin-right: 0.5rem;
}

.form-check-label {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .page-header-right {
    width: 100%;
  }
  
  .filters {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>