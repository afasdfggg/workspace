<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="not-found-code">404</div>
      <h1 class="not-found-title">Page Not Found</h1>
      <p class="not-found-message">
        The page you are looking for does not exist or has been moved.
      </p>
      <div class="not-found-actions">
        <Button type="primary" @click="goBack">
          Go Back
        </Button>
        <Button type="outline-primary" @click="goHome">
          Go Home
        </Button>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '@/components/common/Button.vue';

export default {
  name: 'NotFound',
  components: {
    Button
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      const isAdmin = this.$store.getters['auth/isAdmin'];
      const routeName = isAdmin ? 'AdminDashboard' : 'EmployeeDashboard';
      
      this.$router.push({ name: routeName });
    }
  }
};
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--body-bg);
  padding: 1rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.not-found-code {
  font-size: 8rem;
  font-weight: 700;
  color: var(--primary-color);
  line-height: 1;
  margin-bottom: 1rem;
}

.not-found-title {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.not-found-message {
  color: var(--text-muted);
  margin-bottom: 2rem;
}

.not-found-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
</style>