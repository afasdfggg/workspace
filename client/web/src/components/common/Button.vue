<template>
  <button
    :class="[
      'btn',
      `btn-${type}`,
      { 'btn-lg': size === 'large', 'btn-sm': size === 'small' },
      { 'btn-icon': icon }
    ]"
    :disabled="loading || disabled"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner"></span>
    <i v-else-if="icon" class="material-icons">{{ icon }}</i>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: value => [
        'primary',
        'secondary',
        'success',
        'danger',
        'warning',
        'info',
        'outline-primary',
        'link'
      ].includes(value)
    },
    size: {
      type: String,
      default: 'default',
      validator: value => ['small', 'default', 'large'].includes(value)
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    }
  },
  emits: ['click']
};
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  border: 1px solid transparent;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-icon i {
  margin-right: 0.5rem;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
}

.btn-secondary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
  border-color: #545b62;
}

.btn-success {
  background-color: var(--success-color);
  border-color: var(--success-color);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
  border-color: #1e7e34;
}

.btn-danger {
  background-color: var(--danger-color);
  border-color: var(--danger-color);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #c82333;
  border-color: #bd2130;
}

.btn-warning {
  background-color: var(--warning-color);
  border-color: var(--warning-color);
  color: #212529;
}

.btn-warning:hover:not(:disabled) {
  background-color: #e0a800;
  border-color: #d39e00;
}

.btn-info {
  background-color: var(--info-color);
  border-color: var(--info-color);
  color: white;
}

.btn-info:hover:not(:disabled) {
  background-color: #138496;
  border-color: #117a8b;
}

.btn-outline-primary {
  background-color: transparent;
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-outline-primary:hover:not(:disabled) {
  background-color: var(--primary-color);
  color: white;
}

.btn-link {
  background-color: transparent;
  border-color: transparent;
  color: var(--primary-color);
  padding: 0;
  font-weight: 400;
}

.btn-link:hover:not(:disabled) {
  color: var(--primary-dark);
  text-decoration: underline;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 0.15rem solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>