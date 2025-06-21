<template>
  <div class="dashboard-layout">
    <div :class="['dashboard-sidebar', { 'show': sidebarOpen }]">
      <div class="dashboard-sidebar-header">
        <div class="logo">
          <img src="@/assets/images/logo.svg" alt="Insightful Logo" />
          <span>Insightful</span>
        </div>
      </div>
      <div class="dashboard-sidebar-content">
        <slot name="sidebar"></slot>
      </div>
    </div>
    
    <div class="dashboard-main">
      <div class="dashboard-header">
        <div class="header-left">
          <button class="menu-toggle" @click="toggleSidebar">
            <i class="material-icons">menu</i>
          </button>
          <h2 class="page-title">{{ title }}</h2>
        </div>
        <div class="header-right">
          <slot name="header-right"></slot>
          <div class="user-menu">
            <div class="user-menu-toggle" @click="toggleUserMenu">
              <div class="user-avatar">
                {{ userInitials }}
              </div>
              <span class="user-name">{{ userName }}</span>
              <i class="material-icons">arrow_drop_down</i>
            </div>
            <div :class="['user-menu-dropdown', { 'show': userMenuOpen }]">
              <button class="user-menu-item" @click="goToSettings">
                <i class="material-icons">settings</i>
                Settings
              </button>
              <button class="user-menu-item" @click="logout">
                <i class="material-icons">exit_to_app</i>
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-content">
        <slot></slot>
      </div>
      
      <div class="dashboard-footer">
        <div class="footer-left">
          &copy; {{ currentYear }} Insightful. All rights reserved.
        </div>
        <div class="footer-right">
          <slot name="footer-right"></slot>
        </div>
      </div>
    </div>
    
    <div :class="['sidebar-backdrop', { 'show': sidebarOpen }]" @click="closeSidebar"></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'DashboardLayout',
  props: {
    title: {
      type: String,
      default: 'Dashboard'
    }
  },
  data() {
    return {
      sidebarOpen: false,
      userMenuOpen: false,
      currentYear: new Date().getFullYear()
    };
  },
  computed: {
    ...mapGetters('auth', ['getUser']),
    
    userName() {
      return this.getUser?.name || 'User';
    },
    
    userInitials() {
      if (!this.getUser?.name) return 'U';
      
      const nameParts = this.getUser.name.split(' ');
      if (nameParts.length === 1) {
        return nameParts[0].charAt(0).toUpperCase();
      }
      
      return (nameParts[0].charAt(0) + nameParts[nameParts.length - 1].charAt(0)).toUpperCase();
    }
  },
  methods: {
    ...mapActions('auth', ['logout']),
    
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    
    closeSidebar() {
      this.sidebarOpen = false;
    },
    
    toggleUserMenu() {
      this.userMenuOpen = !this.userMenuOpen;
    },
    
    goToSettings() {
      this.userMenuOpen = false;
      
      // Determine which settings route to use based on user role
      const isAdmin = this.$store.getters['auth/isAdmin'];
      const routeName = isAdmin ? 'AdminSettings' : 'EmployeeSettings';
      
      this.$router.push({ name: routeName });
    }
  }
};
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.dashboard-sidebar {
  width: var(--sidebar-width);
  background-color: var(--card-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: var(--transition);
  z-index: 1000;
}

.dashboard-sidebar-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 32px;
  margin-right: 0.75rem;
}

.logo span {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-color);
}

.dashboard-sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 0;
}

.dashboard-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dashboard-header {
  height: var(--header-height);
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  z-index: 999;
}

.header-left {
  display: flex;
  align-items: center;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  margin-right: 1rem;
  color: var(--text-color);
}

.page-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
}

.user-menu-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: var(--transition);
}

.user-menu-toggle:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.user-avatar {
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

.user-name {
  font-weight: 500;
  margin-right: 0.5rem;
}

.user-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  min-width: 10rem;
  padding: 0.5rem 0;
  margin: 0.125rem 0 0;
  background-color: var(--card-bg);
  border-radius: 0.25rem;
  box-shadow: var(--shadow);
  display: none;
}

.user-menu-dropdown.show {
  display: block;
}

.user-menu-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.5rem 1rem;
  clear: both;
  font-weight: 400;
  color: var(--text-color);
  text-align: inherit;
  white-space: nowrap;
  background-color: transparent;
  border: 0;
  cursor: pointer;
  transition: var(--transition);
}

.user-menu-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--primary-color);
}

.user-menu-item i {
  margin-right: 0.5rem;
  font-size: 1.25rem;
}

.dashboard-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.dashboard-footer {
  height: var(--footer-height);
  background-color: var(--card-bg);
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  color: var(--text-muted);
  font-size: 0.875rem;
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 991.98px) {
  .dashboard-sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: -100%;
  }

  .dashboard-sidebar.show {
    left: 0;
  }

  .menu-toggle {
    display: block;
  }

  .sidebar-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: none;
  }

  .sidebar-backdrop.show {
    display: block;
  }
}
</style>