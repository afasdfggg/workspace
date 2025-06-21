<template>
  <AuthLayout title="Forgot Password">
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
    
    <form v-if="!success" @submit.prevent="forgotPassword">
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
        <Button
          type="primary"
          :loading="loading"
          class="w-100"
        >
          Reset Password
        </Button>
      </div>
    </form>
    
    <template #footer>
      <p>
        Remember your password?
        <router-link :to="{ name: 'Login' }">
          Back to Login
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
  name: 'ForgotPassword',
  components: {
    AuthLayout,
    Alert,
    Button
  },
  data() {
    return {
      email: '',
      success: ''
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
      forgotPasswordAction: 'auth/forgotPassword',
      clearError: 'clearError'
    }),
    
    async forgotPassword() {
      try {
        await this.forgotPasswordAction(this.email);
        this.success = 'Password reset email sent! Check your inbox.';
      } catch (error) {
        console.error('Forgot password error:', error);
      }
    }
  }
};
</script>