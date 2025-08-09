<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1>页面未找到</h1>
      <p>抱歉，您访问的页面不存在或已被移除。</p>
      <div class="actions">
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button @click="goBack">返回上页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style lang="scss" scoped>
.not-found {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.not-found-content {
  text-align: center;
  color: white;
  max-width: 500px;

  .error-code {
    font-size: 8rem;
    font-weight: bold;
    margin-bottom: 1rem;
    opacity: 0.8;
  }

  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .not-found-content {
    .error-code {
      font-size: 6rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    p {
      font-size: 1rem;
    }

    .actions {
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>
