<template>
  <div class="card">
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 v-if="title" class="card-title">{{ title }}</h3>
      </slot>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
};
</script>

<style scoped>
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: var(--card-bg);
  background-clip: border-box;
  border-radius: 0.5rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
}

.card-header {
  padding: 1rem 1.5rem;
  margin-bottom: 0;
  background-color: rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid var(--border-color);
}

.card-title {
  margin-bottom: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.card-body {
  flex: 1 1 auto;
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  background-color: rgba(0, 0, 0, 0.03);
  border-top: 1px solid var(--border-color);
}
</style>