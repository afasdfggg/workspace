<template>
  <div v-if="show" :class="['alert', `alert-${type}`]">
    <div class="alert-content">
      {{ message }}
    </div>
    <button v-if="dismissible" class="alert-close" @click="dismiss">
      &times;
    </button>
  </div>
</template>

<script>
export default {
  name: 'Alert',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: value => ['info', 'success', 'warning', 'danger', 'primary', 'secondary'].includes(value)
    },
    message: {
      type: String,
      required: true
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    duration: {
      type: Number,
      default: 0 // 0 means it won't auto-dismiss
    }
  },
  data() {
    return {
      show: true,
      timer: null
    };
  },
  mounted() {
    if (this.duration > 0) {
      this.timer = setTimeout(() => {
        this.show = false;
        this.$emit('dismissed');
      }, this.duration);
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
  },
  methods: {
    dismiss() {
      this.show = false;
      this.$emit('dismissed');
    }
  }
};
</script>

<style scoped>
.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.alert-content {
  flex: 1;
}

.alert-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  margin-left: 0.5rem;
  opacity: 0.5;
  transition: opacity 0.3s;
}

.alert-close:hover {
  opacity: 1;
}

.alert-primary {
  color: #004085;
  background-color: #cce5ff;
  border-color: #b8daff;
}

.alert-secondary {
  color: #383d41;
  background-color: #e2e3e5;
  border-color: #d6d8db;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.alert-warning {
  color: #856404;
  background-color: #fff3cd;
  border-color: #ffeeba;
}

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}
</style>