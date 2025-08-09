<template>
  <div class="home">
    <!-- 导航栏 -->
    <AppHeader />

    <!-- 主要内容 -->
    <main class="main-content">
      <!-- 英雄区域 -->
      <section class="hero">
        <div class="hero-content">
          <h1 class="hero-title">大语言模型竞技场</h1>
          <p class="hero-subtitle">体验最先进的人工智能技术，与各种大语言模型进行对话和比较</p>
          <div class="hero-actions">
            <router-link to="/register" class="btn btn-gradient btn-large" v-if="!userStore.isLoggedIn">
              立即开始
            </router-link>
            <router-link to="/arena" class="btn btn-gradient btn-large" v-else>
              开始对战
            </router-link>
          </div>
        </div>
      </section>

      <!-- 特性区域 -->
      <section class="features">
        <div class="container">
          <h2 class="section-title">核心特性</h2>
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><ChatDotRound /></el-icon>
              </div>
              <h3>多模型对话</h3>
              <p>支持多种大语言模型，包括GPT、Claude、Gemini等，让您体验不同AI的对话风格</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><ScaleToOriginal /></el-icon>
              </div>
              <h3>性能对比</h3>
              <p>实时对比不同模型的响应速度、准确性和创造力，帮助您选择最适合的AI助手</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><DataAnalysis /></el-icon>
              </div>
              <h3>数据分析</h3>
              <p>详细的使用统计和分析报告，帮助您了解AI模型的使用情况和效果</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><Setting /></el-icon>
              </div>
              <h3>个性化设置</h3>
              <p>自定义对话参数、模型偏好和界面主题，打造专属的AI体验</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 统计区域 -->
      <section class="stats">
        <div class="container">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">活跃用户</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">AI模型</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">对话次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">0</div>
              <div class="stat-label">可用性</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ChatDotRound, ScaleToOriginal, DataAnalysis, Setting } from '@element-plus/icons-vue'
import AppHeader from '@/components/AppHeader.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
}



.main-content {
  padding-top: 80px;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 120px 0 80px;
  text-align: center;

  .hero-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .hero-title {
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }

  .hero-actions {
    .btn-large {
      padding: 16px 32px;
      font-size: 1.1rem;
    }
  }
}

.features {
  padding: 80px 0;
  background: var(--bg-secondary);

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 3rem;
    color: var(--text-primary);
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
  }

  .feature-card {
    background: var(--bg-primary);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .feature-icon {
      font-size: 3rem;
      color: var(--primary-color);
      margin-bottom: 1rem;
    }

    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 1rem;
      color: var(--text-primary);
    }

    p {
      color: var(--text-secondary);
      line-height: 1.6;
    }
  }
}

.stats {
  padding: 80px 0;
  background: var(--bg-primary);

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    text-align: center;
  }

  .stat-item {
    .stat-number {
      font-size: 3rem;
      font-weight: bold;
      color: var(--primary-color);
      margin-bottom: 0.5rem;
    }

    .stat-label {
      font-size: 1.1rem;
      color: var(--text-secondary);
    }
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .nav-menu {
    display: none;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
