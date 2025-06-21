<template>
  <nav class="sidebar-nav">
    <ul>
      <li class="sidebar-nav-item" v-for="item in navItems" :key="item.name">
        <router-link :to="{ name: item.route }" class="sidebar-nav-link" active-class="active">
          <i class="material-icons sidebar-nav-icon">{{ item.icon }}</i>
          {{ item.name }}
        </router-link>
      </li>
    </ul>
    
    <div class="sidebar-section">
      <h4 class="sidebar-section-title">Download</h4>
      <div class="sidebar-section-content">
        <button class="download-btn" @click="downloadDesktopApp">
          <i class="material-icons">download</i>
          Desktop App
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'EmployeeSidebar',
  data() {
    return {
      navItems: [
        { name: 'Dashboard', route: 'EmployeeDashboard', icon: 'dashboard' },
        { name: 'Projects', route: 'EmployeeProjects', icon: 'folder' },
        { name: 'Time Tracking', route: 'EmployeeTimeTracking', icon: 'timer' },
        { name: 'Screenshots', route: 'EmployeeScreenshots', icon: 'photo_library' },
        { name: 'Settings', route: 'EmployeeSettings', icon: 'settings' }
      ]
    };
  },
  methods: {
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
    }
  }
};
</script>

<style scoped>
.sidebar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav-item {
  margin-bottom: 0.25rem;
}

.sidebar-nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: var(--text-color);
  transition: var(--transition);
}

.sidebar-nav-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--primary-color);
  text-decoration: none;
}

.sidebar-nav-link.active {
  background-color: rgba(74, 108, 247, 0.1);
  color: var(--primary-color);
  font-weight: 500;
}

.sidebar-nav-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
  width: 1.25rem;
  text-align: center;
}

.sidebar-section {
  margin-top: 2rem;
  padding: 0 1.5rem;
}

.sidebar-section-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.sidebar-section-content {
  margin-bottom: 1rem;
}

.download-btn {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 500;
  transition: var(--transition);
}

.download-btn:hover {
  background-color: var(--primary-dark);
}

.download-btn i {
  margin-right: 0.5rem;
}
</style>