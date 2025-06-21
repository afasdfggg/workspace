<template>
  <AuthLayout title="Reset Password">
    <Alert
      v-if="error"
      type="danger"
      :message="error"
      @dismissed="clearError"
    />
    
    <Alert
      v-if="success"
      type="success"
      :message="success"
    />
    
    <form v-if="!success" @submit.prevent="resetPassword">
      <div class="form-group">
        <label for="password" class="form-label">New Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          placeholder="Enter your new password"
          required
          minlength="8"
        />
        <small class="form-text">Password must be at least 8 characters long</small>
      </div>
      
      <div class="form-group">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          class="form-control"
          placeholder="Confirm your new password"
          required
        />
      </div>
      
      <div v-if="passwordMismatch" class="alert alert-danger">
        Passwords do not match
      </div>
      
      <div class="form-group">
        <Button
          type="primary"
          :loading="loading"
          :disabled="!isValid"
          class="w-100"
        >
          Reset Password
        </Button>
      </div>
    </form>
    
    <div v-if="success" class="text-center mt-4">
      <Button type="primary" @click="goToLogin">
        Go to Login
      </Button>
    </div>
  </AuthLayout>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import AuthLayout from '@/components/layout/AuthLayout.vue';
import Alert from '@/components/common/Alert.vue';
import Button from '@/components/common/Button.vue';

export default {
  name: 'ResetPassword',
  components: {
    AuthLayout,
    Alert,
    Button
  },
  data() {
    return {
      password: '',
      confirmPassword: '',
      success: '',
      token: ''
    };
  },
  computed: {
    ...mapGetters({
      loading: 'isLoading',
      error: 'getError'
    }),
    
    passwordMismatch() {
      return this.password && this.confirmPassword && this.password !== this.confirmPassword;
    },
    
    isValid() {
      return this.password && this.confirmPassword && this.password === this.confirmPassword && this.password.length >= 8;
    }
  },
  created() {
    this.token = this.$route.params.token;
    
    if (!this.token) {
      this.$router.push({ name: 'Login' });
    }
  },
  methods: {
    ...mapActions({
      resetPasswordAction: 'auth/resetPassword',
      clearError: 'clearError'
    }),
    
    async resetPassword() {
      if (!this.isValid) return;
      
      try {
        await this.resetPasswordAction({
          token: this.token,
          password: this.password
        });
        
        this.success = 'Password reset successfully! You can now log in.';
      } catch (error) {
        console.error('Reset password error:', error);
      }
    },
    
    goToLogin() {
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>