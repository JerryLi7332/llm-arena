<template>
  <div class="loading-spinner" v-if="loading">
    <div class="spinner">
      <div class="bounce1"></div>
      <div class="bounce2"></div>
      <div class="bounce3"></div>
    </div>
    <p class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style lang="scss" scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;

  > div {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--primary-color);
    animation: bounce 1.4s ease-in-out infinite both;

    &.bounce1 {
      animation-delay: -0.32s;
    }

    &.bounce2 {
      animation-delay: -0.16s;
    }
  }
}

.loading-text {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>
