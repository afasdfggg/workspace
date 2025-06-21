<template>
  <DashboardLayout title="Dashboard">
    <template #sidebar>
      <EmployeeSidebar />
    </template>
    
    <div class="dashboard-container">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">access_time</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatDuration(todayTime) }}</div>
            <div class="stat-label">Today</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">date_range</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatDuration(weekTime) }}</div>
            <div class="stat-label">This Week</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">folder</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ assignedProjects.length }}</div>
            <div class="stat-label">Assigned Projects</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="material-icons">assignment</i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ assignedTasks.length }}</div>
            <div class="stat-label">Assigned Tasks</div>
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
                You haven't tracked any time yet. Start tracking time to see your activity here.
              </p>
            </div>
            
            <div v-else class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-time">{{ formatDateTime(activity.timestamp) }}</div>
                <div class="activity-description">
                  {{ activity.description }}
                </div>
                <div class="activity-meta">
                  <span v-if="activity.project" class="activity-project">{{ activity.project }}</span>
                  <span v-if="activity.duration" class="activity-duration">{{ formatDuration(activity.duration) }}</span>
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
                icon="play_arrow"
                class="w-100 mb-2"
                @click="goToTimeTracking"
                :disabled="isTracking"
              >
                Start Tracking
              </Button>
              
              <Button
                type="danger"
                icon="stop"
                class="w-100 mb-2"
                @click="stopTracking"
                :disabled="!isTracking"
              >
                Stop Tracking
              </Button>
              
              <Button
                type="primary"
                icon="download"
                class="w-100"
                @click="downloadDesktopApp"
              >
                Download Desktop App
              </Button>
            </div>
          </Card>
          
          <Card title="Current Tracking">
            <div v-if="loading" class="text-center p-4">
              <div class="spinner"></div>
            </div>
            
            <div v-else-if="!isTracking" class="empty-state">
              <div class="empty-state-icon">
                <i class="material-icons">timer_off</i>
              </div>
              <h3 class="empty-state-title">Not Tracking</h3>
              <p class="empty-state-description">
                You are not currently tracking time.
              </p>
            </div>
            
            <div v-else class="current-tracking">
              <div class="tracking-project">{{ currentTracking.project }}</div>
              <div v-if="currentTracking.task" class="tracking-task">{{ currentTracking.task }}</div>
              <div class="tracking-time">
                Started: {{ formatDateTime(currentTracking.start) }}
              </div>
              <div class="tracking-duration">
                Duration: {{ formatDuration(currentTrackingDuration) }}
              </div>
            </div>
          </Card>
        </div>
      </div>
      
      <div class="row mt-4">
        <div class="col-12">
          <Card title="Assigned Projects">
            <div v-if="loading" class="text-center p-4">
              <div class="spinner"></div>
            </div>
            
            <div v-else-if="assignedProjects.length === 0" class="empty-state">
              <div class="empty-state-icon">
                <i class="material-icons">folder_off</i>
              </div>
              <h3 class="empty-state-title">No Assigned Projects</h3>
              <p class="empty-state-description">
                You are not assigned to any projects yet.
              </p>
            </div>
            
            <div v-else class="projects-grid">
              <div v-for="project in assignedProjects" :key="project.id" class="project-card">
                <div class="project-header">
                  <div class="project-name">{{ project.name }}</div>
                  <div class="project-badge" :class="project.archived ? 'badge-archived' : 'badge-active'">
                    {{ project.archived ? 'Archived' : 'Active' }}
                  </div>
                </div>
                <div class="project-description">{{ project.description }}</div>
                <div class="project-stats">
                  <div class="project-stat">
                    <div class="project-stat-label">Tasks</div>
                    <div class="project-stat-value">{{ project.taskCount }}</div>
                  </div>
                  <div class="project-stat">
                    <div class="project-stat-label">Time Tracked</div>
                    <div class="project-stat-value">{{ formatDuration(project.timeTracked) }}</div>
                  </div>
                </div>
                <div class="project-actions">
                  <Button
                    type="primary"
                    size="small"
                    @click="trackProject(project.id)"
                  >
                    Track Time
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import DashboardLayout from '@/components/layout/DashboardLayout.vue';
import EmployeeSidebar from '@/components/employee/EmployeeSidebar.vue';
import Card from '@/components/common/Card.vue';
import Button from '@/components/common/Button.vue';
import { formatDateTime, formatDuration } from '@/utils/date';

export default {
  name: 'EmployeeDashboard',
  components: {
    DashboardLayout,
    EmployeeSidebar,
    Card,
    Button
  },
  data() {
    return {
      loading: true,
      todayTime: 0,
      weekTime: 0,
      assignedProjects: [],
      assignedTasks: [],
      recentActivity: [],
      currentTracking: null,
      trackingTimer: null
    };
  },
  computed: {
    ...mapGetters({
      user: 'auth/getUser',
      isTracking: 'timeTracking/isTracking',
      currentShift: 'timeTracking/getCurrentShift'
    }),
    
    currentTrackingDuration() {
      if (!this.currentTracking) return 0;
      
      return Date.now() - this.currentTracking.start;
    }
  },
  async created() {
    await this.fetchDashboardData();
    
    // Start timer if tracking
    if (this.isTracking && this.currentShift) {
      this.startTrackingTimer();
    }
  },
  beforeUnmount() {
    this.stopTrackingTimer();
  },
  methods: {
    ...mapActions({
      stopTrackingAction: 'timeTracking/stopTracking'
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
        
        this.todayTime = 3 * 60 * 60 * 1000; // 3 hours in milliseconds
        this.weekTime = 15 * 60 * 60 * 1000; // 15 hours in milliseconds
        
        this.assignedProjects = [
          {
            id: 1,
            name: 'Website Redesign',
            description: 'Redesign the company website with a modern look and feel',
            archived: false,
            taskCount: 5,
            timeTracked: 8 * 60 * 60 * 1000 // 8 hours in milliseconds
          },
          {
            id: 2,
            name: 'Mobile App Development',
            description: 'Develop a mobile app for iOS and Android',
            archived: false,
            taskCount: 8,
            timeTracked: 12 * 60 * 60 * 1000 // 12 hours in milliseconds
          }
        ];
        
        this.assignedTasks = [
          {
            id: 1,
            name: 'Design Homepage',
            projectId: 1,
            projectName: 'Website Redesign',
            status: 'In Progress'
          },
          {
            id: 2,
            name: 'Implement User Authentication',
            projectId: 2,
            projectName: 'Mobile App Development',
            status: 'To Do'
          }
        ];
        
        this.recentActivity = [
          {
            id: 1,
            timestamp: Date.now() - 30 * 60 * 1000, // 30 minutes ago
            description: 'Stopped tracking time',
            project: 'Website Redesign',
            duration: 2 * 60 * 60 * 1000 // 2 hours in milliseconds
          },
          {
            id: 2,
            timestamp: Date.now() - 24 * 60 * 60 * 1000, // 1 day ago
            description: 'Completed task "Design Homepage"',
            project: 'Website Redesign'
          }
        ];
        
        // Check if currently tracking
        if (this.isTracking && this.currentShift) {
          const project = this.assignedProjects.find(p => p.id === this.currentShift.projectId);
          const task = this.assignedTasks.find(t => t.id === this.currentShift.taskId);
          
          this.currentTracking = {
            project: project ? project.name : 'Unknown Project',
            task: task ? task.name : null,
            start: this.currentShift.start
          };
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    goToTimeTracking() {
      this.$router.push({ name: 'EmployeeTimeTracking' });
    },
    
    async stopTracking() {
      try {
        await this.stopTrackingAction();
        this.currentTracking = null;
        this.stopTrackingTimer();
        await this.fetchDashboardData();
      } catch (error) {
        console.error('Error stopping tracking:', error);
      }
    },
    
    trackProject(projectId) {
      this.$router.push({
        name: 'EmployeeTimeTracking',
        query: { projectId }
      });
    },
    
    downloadDesktopApp() {
      // Determine OS and provide appropriate download link
      const userAgent = navigator.userAgent;
      let downloadUrl = '';
      
      if (userAgent.indexOf('Win') !== -1) {
        downloadUrl = '/downloads/insightful-time-tracker-win.exe';
      } else if (userAgent.indexOf('Mac') !== -1) {
        downloadUrl = '/downloads/insightful-time-tracker-mac.dmg';
      } else if (userAgent.indexOf('Linux') !== -1) {
        downloadUrl = '/downloads/insightful-time-tracker-linux.AppImage';
      } else {
        // Default to Windows if OS can't be determined
        downloadUrl = '/downloads/insightful-time-tracker-win.exe';
      }
      
      // Create a temporary link and trigger download
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = downloadUrl.split('/').pop();
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    startTrackingTimer() {
      this.trackingTimer = setInterval(() => {
        this.$forceUpdate(); // Force update to recalculate currentTrackingDuration
      }, 1000);
    },
    
    stopTrackingTimer() {
      if (this.trackingTimer) {
        clearInterval(this.trackingTimer);
        this.trackingTimer = null;
      }
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

.activity-project {
  color: var(--primary-color);
}

.activity-duration {
  color: var(--text-muted);
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.current-tracking {
  padding: 1rem;
  background-color: rgba(74, 108, 247, 0.1);
  border-radius: 0.25rem;
}

.tracking-project {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.tracking-task {
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.tracking-time,
.tracking-duration {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.project-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.project-name {
  font-size: 1.25rem;
  font-weight: 600;
}

.project-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-active {
  background-color: rgba(40, 167, 69, 0.1);
  color: var(--success-color);
}

.badge-archived {
  background-color: rgba(108, 117, 125, 0.1);
  color: var(--secondary-color);
}

.project-description {
  color: var(--text-muted);
  margin-bottom: 1rem;
  max-height: 60px;
  overflow: hidden;
}

.project-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.project-stat {
  flex: 1;
}

.project-stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.project-stat-value {
  font-weight: 500;
}

.project-actions {
  display: flex;
  justify-content: flex-end;
}
</style>