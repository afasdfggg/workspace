<template>
  <AuthLayout title="Employee Login">
    <Alert
      v-if="error"
      type="danger"
      :message="error"
      @dismissed="clearError"
    />
    
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          placeholder="Enter your email"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          placeholder="Enter your password"
          required
        />
      </div>
      
      <div class="form-group text-right">
        <router-link :to="{ name: 'ForgotPassword' }" class="forgot-password">
          Forgot password?
        </router-link>
      </div>
      
      <div class="form-group">
        <Button
          type="primary"
          :loading="loading"
          class="w-100"
        >
          Log In
        </Button>
      </div>
    </form>
    
    <template #footer>
      <p>
        Are you an admin?
        <router-link :to="{ name: 'AdminLogin' }">
          Admin Login
        </router-link>
      </p>
    </template>
  </AuthLayout>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import AuthLayout from '@/components/layout/AuthLayout.vue';
import Alert from '@/components/common/Alert.vue';
import Button from '@/components/common/Button.vue';

export default {
  name: 'Login',
  components: {
    AuthLayout,
    Alert,
    Button
  },
  data() {
    return {
      email: '',
      password: ''
    };
  },
  computed: {
    ...mapGetters({
      loading: 'isLoading',
      error: 'getError'
    })
  },
  methods: {
    ...mapActions({
      loginAction: 'auth/login',
      clearError: 'clearError'
    }),
    
    async login() {
      try {
        await this.loginAction({
          username: this.email,
          password: this.password
        });
      } catch (error) {
        console.error('Login error:', error);
      }
    }
  }
};
</script>

<style scoped>
.forgot-password {
  font-size: 0.875rem;
}
</style>