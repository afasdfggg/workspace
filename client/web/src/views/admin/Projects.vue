<template>
  <DashboardLayout title="Projects">
    <template #sidebar>
      <AdminSidebar />
    </template>

    <div class="projects-container">
      <!-- Header Actions -->
      <div class="page-header">
        <div class="page-header-left">
          <h2>Projects</h2>
          <p class="text-muted">Manage your organization's projects</p>
        </div>
        <div class="page-header-right">
          <Button
            type="primary"
            icon="create_new_folder"
            @click="showAddModal = true"
          >
            Create Project
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
              placeholder="Search projects..."
            />
          </div>
          
          <div class="filter-group">
            <label class="form-label">Status</label>
            <select v-model="statusFilter" class="form-control">
              <option value="">All</option>
              <option value="active">Active</option>
              <option value="archived">Archived</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="form-label">Billable</label>
            <select v-model="billableFilter" class="form-control">
              <option value="">All</option>
              <option value="true">Billable</option>
              <option value="false">Non-billable</option>
            </select>
          </div>
        </div>
      </Card>

      <!-- Projects Grid -->
      <div v-if="loading" class="text-center p-4">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="filteredProjects.length === 0" class="empty-state">
        <div class="empty-state-icon">
          <i class="material-icons">folder</i>
        </div>
        <h3 class="empty-state-title">No Projects Found</h3>
        <p class="empty-state-description">
          {{ searchQuery ? 'No projects match your search criteria.' : 'Get started by creating your first project.' }}
        </p>
        <Button
          v-if="!searchQuery"
          type="primary"
          icon="create_new_folder"
          @click="showAddModal = true"
        >
          Create Project
        </Button>
      </div>
      
      <div v-else class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card">
          <div class="project-header">
            <div class="project-title">
              <h3>{{ project.name }}</h3>
              <div class="project-badges">
                <span :class="['badge', project.archived ? 'badge-secondary' : 'badge-success']">
                  {{ project.archived ? 'Archived' : 'Active' }}
                </span>
                <span v-if="project.billable" class="badge badge-info">
                  Billable
                </span>
              </div>
            </div>
            <div class="project-actions">
              <Button
                type="outline-primary"
                size="small"
                icon="edit"
                @click="editProject(project)"
              >
                Edit
              </Button>
              
              <Button
                v-if="!project.archived"
                type="outline-warning"
                size="small"
                icon="archive"
                @click="archiveProject(project)"
              >
                Archive
              </Button>
              
              <Button
                v-else
                type="outline-success"
                size="small"
                icon="unarchive"
                @click="unarchiveProject(project)"
              >
                Unarchive
              </Button>
              
              <Button
                type="outline-danger"
                size="small"
                icon="delete"
                @click="deleteProject(project)"
              >
                Delete
              </Button>
            </div>
          </div>
          
          <div class="project-description">
            {{ project.description || 'No description provided.' }}
          </div>
          
          <div class="project-stats">
            <div class="stat">
              <div class="stat-value">{{ project.taskCount || 0 }}</div>
              <div class="stat-label">Tasks</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ project.employees ? project.employees.length : 0 }}</div>
              <div class="stat-label">Members</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ formatDuration(project.totalTime || 0) }}</div>
              <div class="stat-label">Time Tracked</div>
            </div>
          </div>
          
          <div class="project-footer">
            <div class="project-created">
              Created {{ formatDate(project.createdAt) }}
            </div>
            <Button
              type="link"
              size="small"
              @click="viewProject(project)"
            >
              View Details
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Project Modal -->
    <Modal
      :show="showAddModal || showEditModal"
      :title="editingProject ? 'Edit Project' : 'Create Project'"
      @close="closeModal"
    >
      <form @submit.prevent="saveProject">
        <div class="form-group">
          <label class="form-label">Project Name *</label>
          <input
            v-model="projectForm.name"
            type="text"
            class="form-control"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea
            v-model="projectForm.description"
            class="form-control"
            rows="3"
            placeholder="Enter project description..."
          ></textarea>
        </div>
        
        <div class="form-group">
          <label class="form-check">
            <input
              v-model="projectForm.billable"
              type="checkbox"
              class="form-check-input"
            />
            <span class="form-check-label">Billable Project</span>
          </label>
        </div>
        
        <div class="form-group">
          <label class="form-label">Assigned Employees</label>
          <div class="checkbox-group">
            <label v-for="employee in employees" :key="employee.id" class="form-check">
              <input
                v-model="projectForm.employees"
                type="checkbox"
                :value="employee.id"
                class="form-check-input"
              />
              <span class="form-check-label">{{ employee.name }}</span>
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">Teams</label>
          <div class="checkbox-group">
            <label v-for="team in teams" :key="team.id" class="form-check">
              <input
                v-model="projectForm.teams"
                type="checkbox"
                :value="team.id"
                class="form-check-input"
              />
              <span class="form-check-label">{{ team.name }}</span>
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
          @click="saveProject"
        >
          {{ editingProject ? 'Update' : 'Create' }} Project
        </Button>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal
      :show="showDeleteModal"
      title="Delete Project"
      @close="showDeleteModal = false"
    >
      <p>Are you sure you want to delete <strong>{{ projectToDelete?.name }}</strong>?</p>
      <p class="text-danger">
        <strong>Warning:</strong> This action cannot be undone. All tasks and time tracking data associated with this project will be permanently deleted.
      </p>
      
      <template #footer>
        <Button type="secondary" @click="showDeleteModal = false">
          Cancel
        </Button>
        <Button
          type="danger"
          :loading="deleting"
          @click="confirmDelete"
        >
          Delete Project
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
import { formatDate, formatDuration } from '@/utils/date';

export default {
  name: 'AdminProjects',
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
      deleting: false,
      searchQuery: '',
      statusFilter: '',
      billableFilter: '',
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      editingProject: null,
      projectToDelete: null,
      projectForm: {
        name: '',
        description: '',
        billable: true,
        employees: [],
        teams: []
      },
      employees: [],
      teams: []
    };
  },
  computed: {
    ...mapGetters({
      projects: 'projects/getProjects'
    }),
    
    filteredProjects() {
      let filtered = this.projects;
      
      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(project =>
          project.name.toLowerCase().includes(query) ||
          (project.description && project.description.toLowerCase().includes(query))
        );
      }
      
      // Status filter
      if (this.statusFilter) {
        if (this.statusFilter === 'active') {
          filtered = filtered.filter(project => !project.archived);
        } else if (this.statusFilter === 'archived') {
          filtered = filtered.filter(project => project.archived);
        }
      }
      
      // Billable filter
      if (this.billableFilter) {
        const isBillable = this.billableFilter === 'true';
        filtered = filtered.filter(project => project.billable === isBillable);
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
      getProjects: 'projects/getProjects',
      createProject: 'projects/createProject',
      updateProject: 'projects/updateProject',
      deleteProjectAction: 'projects/deleteProject',
      getEmployees: 'employees/getEmployees'
    }),
    
    formatDate,
    formatDuration,
    
    async loadData() {
      this.loading = true;
      
      try {
        await Promise.all([
          this.getProjects(),
          this.getEmployees(),
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
    
    editProject(project) {
      this.editingProject = project;
      this.projectForm = {
        name: project.name,
        description: project.description || '',
        billable: project.billable,
        employees: project.employees || [],
        teams: project.teams || []
      };
      this.showEditModal = true;
    },
    
    async archiveProject(project) {
      try {
        await this.updateProject({
          projectId: project.id,
          projectData: { archived: true }
        });
      } catch (error) {
        console.error('Error archiving project:', error);
      }
    },
    
    async unarchiveProject(project) {
      try {
        await this.updateProject({
          projectId: project.id,
          projectData: { archived: false }
        });
      } catch (error) {
        console.error('Error unarchiving project:', error);
      }
    },
    
    deleteProject(project) {
      this.projectToDelete = project;
      this.showDeleteModal = true;
    },
    
    async confirmDelete() {
      if (!this.projectToDelete) return;
      
      this.deleting = true;
      
      try {
        await this.deleteProjectAction(this.projectToDelete.id);
        this.showDeleteModal = false;
        this.projectToDelete = null;
      } catch (error) {
        console.error('Error deleting project:', error);
      } finally {
        this.deleting = false;
      }
    },
    
    viewProject(project) {
      // Navigate to project details page
      this.$router.push({ name: 'AdminTasks', query: { projectId: project.id } });
    },
    
    async saveProject() {
      this.saving = true;
      
      try {
        if (this.editingProject) {
          await this.updateProject({
            projectId: this.editingProject.id,
            projectData: this.projectForm
          });
        } else {
          await this.createProject(this.projectForm);
        }
        
        this.closeModal();
      } catch (error) {
        console.error('Error saving project:', error);
      } finally {
        this.saving = false;
      }
    },
    
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.editingProject = null;
      this.projectForm = {
        name: '',
        description: '',
        billable: true,
        employees: [],
        teams: []
      };
    }
  }
};
</script>

<style scoped>
.projects-container {
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  box-shadow: var(--shadow);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.project-title h3 {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}

.project-badges {
  display: flex;
  gap: 0.5rem;
}

.project-actions {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.project-description {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  flex: 1;
  line-height: 1.5;
}

.project-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 0.25rem;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.project-created {
  font-size: 0.875rem;
  color: var(--text-muted);
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
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .project-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .project-actions {
    justify-content: flex-start;
  }
  
  .project-stats {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>