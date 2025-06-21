<template>
  <DashboardLayout title="Admin Dashboard">
    <template #sidebar>
      <AdminSidebar />
    </template>
    
    <div class="dashboard-container">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">people</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ employeeCount }}</div>
            <div class="stat-label">Employees</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">folder</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ projectCount }}</div>
            <div class="stat-label">Projects</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">assignment</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ taskCount }}</div>
            <div class="stat-label">Tasks</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">timer</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatDuration(totalTrackedTime) }}</div>
            <div class="stat-label">Total Tracked Time</div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-8">
          <Card title="Recent Activity">
            <div v-if="loading" class="text-center p-4">
              <div class="spinner"></div>
            </div>
            
            <div v-else-if="recentActivity.length === 0" class="empty-state">
              <div class="empty-state-icon">
                <i class="material-icons">history</i>
              </div>
              <h3 class="empty-state-title">No Recent Activity</h3>
              <p class="empty-state-description">
                There is no recent activity to display.
              </p>
            </div>
            
            <div v-else class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-time">{{ formatDateTime(activity.timestamp) }}</div>
                <div class="activity-description">
                  {{ activity.description }}
                </div>
                <div class="activity-meta">
                  <span class="activity-user">{{ activity.user }}</span>
                  <span v-if="activity.project" class="activity-project">{{ activity.project }}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
        
        <div class="col-md-4">
          <Card title="Quick Actions">
            <div class="quick-actions">
              <Button
                type="primary"
                icon="person_add"
                class="w-100 mb-2"
                @click="goToAddEmployee"
              >
                Add Employee
              </Button>
              
              <Button
                type="primary"
                icon="create_new_folder"
                class="w-100 mb-2"
                @click="goToAddProject"
              >
                Create Project
              </Button>
              
              <Button
                type="primary"
                icon="assignment_add"
                class="w-100 mb-2"
                @click="goToAddTask"
              >
                Create Task
              </Button>
              
              <Button
                type="primary"
                icon="key"
                class="w-100"
                @click="generateApiKey"
              >
                Generate API Key
              </Button>
            </div>
          </Card>
          
          <Card title="Active Employees">
            <div v-if="loading" class="text-center p-4">
              <div class="spinner"></div>
            </div>
            
            <div v-else-if="activeEmployees.length === 0" class="empty-state">
              <div class="empty-state-icon">
                <i class="material-icons">people</i>
              </div>
              <h3 class="empty-state-title">No Active Employees</h3>
              <p class="empty-state-description">
                There are no active employees at the moment.
              </p>
            </div>
            
            <div v-else class="active-employees-list">
              <div v-for="employee in activeEmployees" :key="employee.id" class="active-employee-item">
                <div class="active-employee-avatar">
                  {{ getInitials(employee.name) }}
                </div>
                <div class="active-employee-info">
                  <div class="active-employee-name">{{ employee.name }}</div>
                  <div class="active-employee-status">
                    <span class="status-dot"></span>
                    Active
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
    
    <Modal
      :show="showApiKeyModal"
      title="API Key"
      @close="closeApiKeyModal"
    >
      <div v-if="generatingApiKey" class="text-center p-4">
        <div class="spinner"></div>
        <p class="mt-3">Generating API Key...</p>
      </div>
      
      <div v-else-if="apiKey" class="api-key-container">
        <p class="mb-3">Your API Key has been generated. Please copy it and store it securely. You won't be able to see it again.</p>
        
        <div class="api-key-display">
          <code>{{ apiKey }}</code>
          <button class="copy-btn" @click="copyApiKey">
            <i class="material-icons">content_copy</i>
          </button>
        </div>
        
        <div v-if="apiKeyCopied" class="alert alert-success mt-3">
          API Key copied to clipboard!
        </div>
      </div>
      
      <template #footer>
        <Button type="secondary" @click="closeApiKeyModal">Close</Button>
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
import { formatDateTime, formatDuration } from '@/utils/date';

export default {
  name: 'AdminDashboard',
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
      employeeCount: 0,
      projectCount: 0,
      taskCount: 0,
      totalTrackedTime: 0,
      recentActivity: [],
      activeEmployees: [],
      showApiKeyModal: false,
      generatingApiKey: false,
      apiKey: '',
      apiKeyCopied: false
    };
  },
  computed: {
    ...mapGetters({
      user: 'auth/getUser'
    })
  },
  async created() {
    await this.fetchDashboardData();
  },
  methods: {
    ...mapActions({
      generateApiKeyAction: 'auth/generateApiKey'
    }),
    
    formatDateTime,
    formatDuration,
    
    async fetchDashboardData() {
      this.loading = true;
      
      try {
        // In a real application, these would be API calls
        // For now, we'll use mock data
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.employeeCount = 12;
        this.projectCount = 8;
        this.taskCount = 24;
        this.totalTrackedTime = 120 * 60 * 60 * 1000; // 120 hours in milliseconds
        
        this.recentActivity = [
          {
            id: 1,
            timestamp: Date.now() - 30 * 60 * 1000, // 30 minutes ago
            description: 'Started tracking time',
            user: 'John Doe',
            project: 'Website Redesign'
          },
          {
            id: 2,
            timestamp: Date.now() - 2 * 60 * 60 * 1000, // 2 hours ago
            description: 'Completed task "Design Homepage"',
            user: 'Jane Smith',
            project: 'Website Redesign'
          },
          {
            id: 3,
            timestamp: Date.now() - 3 * 60 * 60 * 1000, // 3 hours ago
            description: 'Created new project',
            user: 'Admin',
            project: 'Mobile App Development'
          }
        ];
        
        this.activeEmployees = [
          {
            id: 1,
            name: 'John Doe',
            email: 'john.doe@example.com'
          },
          {
            id: 2,
            name: 'Jane Smith',
            email: 'jane.smith@example.com'
          },
          {
            id: 3,
            name: 'Bob Johnson',
            email: 'bob.johnson@example.com'
          }
        ];
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    getInitials(name) {
      if (!name) return '';
      
      const nameParts = name.split(' ');
      if (nameParts.length === 1) {
        return nameParts[0].charAt(0).toUpperCase();
      }
      
      return (nameParts[0].charAt(0) + nameParts[nameParts.length - 1].charAt(0)).toUpperCase();
    },
    
    goToAddEmployee() {
      this.$router.push({ name: 'AdminEmployees', query: { action: 'add' } });
    },
    
    goToAddProject() {
      this.$router.push({ name: 'AdminProjects', query: { action: 'add' } });
    },
    
    goToAddTask() {
      this.$router.push({ name: 'AdminTasks', query: { action: 'add' } });
    },
    
    async generateApiKey() {
      this.showApiKeyModal = true;
      this.generatingApiKey = true;
      this.apiKey = '';
      this.apiKeyCopied = false;
      
      try {
        const apiKey = await this.generateApiKeyAction();
        this.apiKey = apiKey;
      } catch (error) {
        console.error('Error generating API key:', error);
      } finally {
        this.generatingApiKey = false;
      }
    },
    
    copyApiKey() {
      if (!this.apiKey) return;
      
      navigator.clipboard.writeText(this.apiKey)
        .then(() => {
          this.apiKeyCopied = true;
          
          // Reset after 3 seconds
          setTimeout(() => {
            this.apiKeyCopied = false;
          }, 3000);
        })
        .catch(err => {
          console.error('Failed to copy API key:', err);
        });
    },
    
    closeApiKeyModal() {
      this.showApiKeyModal = false;
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.activity-description {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.activity-meta {
  font-size: 0.75rem;
  display: flex;
  gap: 1rem;
}

.activity-user {
  color: var(--text-color);
}

.activity-project {
  color: var(--primary-color);
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.active-employees-list {
  max-height: 300px;
  overflow-y: auto;
}

.active-employee-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.active-employee-item:last-child {
  border-bottom: none;
}

.active-employee-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 0.75rem;
}

.active-employee-info {
  flex: 1;
}

.active-employee-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.active-employee-status {
  font-size: 0.75rem;
  color: var(--success-color);
  display: flex;
  align-items: center;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success-color);
  margin-right: 0.25rem;
}

.api-key-container {
  text-align: center;
}

.api-key-display {
  position: relative;
  background-color: var(--light-color);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
  word-break: break-all;
  text-align: left;
}

.copy-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  transition: var(--transition);
}

.copy-btn:hover {
  color: var(--primary-color);
}
</style>