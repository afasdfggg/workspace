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
  </nav>
</template>

<script>
export default {
  name: 'AdminSidebar',
  data() {
    return {
      navItems: [
        { name: 'Dashboard', route: 'AdminDashboard', icon: 'dashboard' },
        { name: 'Employees', route: 'AdminEmployees', icon: 'people' },
        { name: 'Projects', route: 'AdminProjects', icon: 'folder' },
        { name: 'Tasks', route: 'AdminTasks', icon: 'assignment' },
        { name: 'Time Tracking', route: 'AdminTimeTracking', icon: 'timer' },
        { name: 'Screenshots', route: 'AdminScreenshots', icon: 'photo_library' },
        { name: 'Settings', route: 'AdminSettings', icon: 'settings' }
      ]
    };
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
</style>