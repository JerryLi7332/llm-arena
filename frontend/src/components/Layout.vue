<template>
  <div class="layout">
    <!-- 导航栏 -->
    <AppHeader />
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <slot />
    </main>
    
    <!-- 页脚 -->
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>

<style lang="scss" scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 80px; // 为固定导航栏留出空间
}
</style>
