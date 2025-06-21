<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  created() {
    // Check if user is logged in
    this.$store.dispatch('auth/checkAuth');
  }
};
</script>

<style>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>