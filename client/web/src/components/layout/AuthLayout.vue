<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-logo">
          <img src="@/assets/images/logo.svg" alt="Insightful Logo" />
        </div>
        <h1 class="auth-title">{{ title }}</h1>
        <slot></slot>
        <div class="auth-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout',
  props: {
    title: {
      type: String,
      default: 'Insightful'
    }
  }
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--body-bg);
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

.auth-card {
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-lg);
  padding: 2rem;
}

.auth-logo {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-logo img {
  height: 60px;
}

.auth-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}
</style>