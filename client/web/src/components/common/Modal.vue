<template>
  <transition name="modal">
    <div v-if="show" class="modal-backdrop" @click="closeOnBackdrop && close()">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ title }}</h3>
          <button v-if="showClose" class="modal-close" @click="close">&times;</button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div v-if="$slots.footer" class="modal-footer">
          <slot name="footer">
            <Button @click="close">Close</Button>
          </slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import Button from './Button.vue';

export default {
  name: 'Modal',
  components: {
    Button
  },
  props: {
    show: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    showClose: {
      type: Boolean,
      default: true
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  watch: {
    show(value) {
      if (value) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
  },
  beforeUnmount() {
    document.body.style.overflow = '';
  },
  methods: {
    close() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-container {
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  opacity: 0.5;
  transition: opacity 0.3s;
}

.modal-close:hover {
  opacity: 1;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: translateY(20px);
}
</style>