<template>
  <div class="arena">
    <AppHeader />
    <div class="container">
      <h1 class="page-title">对战大厅</h1>
      <p class="page-subtitle">选择您想要对战的AI模型，开始精彩的对话体验</p>
      
      <div class="models-grid">
        <div class="model-card" v-for="model in models" :key="model.id">
          <div class="model-avatar">
            <el-avatar :size="80" :src="model.avatar" />
          </div>
          <h3 class="model-name">{{ model.name }}</h3>
          <p class="model-description">{{ model.description }}</p>
          <div class="model-stats">
            <span class="stat">响应速度: {{ model.speed }}</span>
            <span class="stat">准确度: {{ model.accuracy }}</span>
          </div>
          <el-button type="primary" class="start-chat-btn" @click="startChat(model)">
            开始对话
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/AppHeader.vue'

const models = ref([
  {
    id: 1,
    name: 'GPT-4',
    description: 'OpenAI最新的大语言模型，具有强大的推理和创造能力',
    avatar: 'https://via.placeholder.com/80x80/4F46E5/FFFFFF?text=GPT',
    speed: '快速',
    accuracy: '95%'
  },
  {
    id: 2,
    name: 'Claude-3',
    description: 'Anthropic开发的AI助手，擅长分析和写作任务',
    avatar: 'https://via.placeholder.com/80x80/10B981/FFFFFF?text=Claude',
    speed: '中等',
    accuracy: '92%'
  },
  {
    id: 3,
    name: 'Gemini Pro',
    description: 'Google的多模态AI模型，支持文本和图像理解',
    avatar: 'https://via.placeholder.com/80x80/F59E0B/FFFFFF?text=Gemini',
    speed: '快速',
    accuracy: '90%'
  },
  {
    id: 4,
    name: 'Llama 2',
    description: 'Meta开源的大语言模型，适合各种对话场景',
    avatar: 'https://via.placeholder.com/80x80/EF4444/FFFFFF?text=Llama',
    speed: '中等',
    accuracy: '88%'
  }
])

const startChat = (model) => {
  ElMessage.success(`即将与 ${model.name} 开始对话`)
  // 这里可以跳转到对话页面
}
</script>

<style lang="scss" scoped>
.arena {
  padding: 120px 0 80px;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  text-align: center;
  font-size: 3rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
}

.page-subtitle {
  text-align: center;
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 3rem;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.model-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
  }

  .model-avatar {
    margin-bottom: 1rem;
  }

  .model-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 1rem;
  }

  .model-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .model-stats {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;

    .stat {
      background: var(--bg-secondary);
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      color: var(--text-secondary);
    }
  }

  .start-chat-btn {
    width: 100%;
    padding: 12px 24px;
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .models-grid {
    grid-template-columns: 1fr;
  }
}
</style>
