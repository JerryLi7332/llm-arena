<template>
  <div class="my-ai">
    <AppHeader />
    <div class="container">
      <h1 class="page-title">我的AI</h1>
      <p class="page-subtitle">管理您创建的AI助手和对话历史</p>
      
      <div class="content-tabs">
        <el-tabs v-model="activeTab" class="custom-tabs">
          <el-tab-pane label="我的AI助手" name="assistants">
            <div class="assistants-section">
              <div class="section-header">
                <h3>我创建的AI助手</h3>
                <el-button type="primary" @click="createAssistant">
                  <el-icon><Plus /></el-icon>
                  创建新助手
                </el-button>
              </div>
              
              <div class="assistants-grid" v-if="assistants.length > 0">
                <div class="assistant-card" v-for="assistant in assistants" :key="assistant.id">
                  <div class="assistant-header">
                    <el-avatar :size="60" :src="assistant.avatar" />
                    <div class="assistant-info">
                      <h4>{{ assistant.name }}</h4>
                      <p>{{ assistant.description }}</p>
                    </div>
                  </div>
                  <div class="assistant-stats">
                    <span>对话次数: {{ assistant.conversations }}</span>
                    <span>创建时间: {{ assistant.createdAt }}</span>
                  </div>
                  <div class="assistant-actions">
                    <el-button size="small" @click="editAssistant(assistant)">编辑</el-button>
                    <el-button size="small" type="primary" @click="chatWithAssistant(assistant)">对话</el-button>
                    <el-button size="small" type="danger" @click="deleteAssistant(assistant)">删除</el-button>
                  </div>
                </div>
              </div>
              
              <el-empty v-else description="还没有创建AI助手" />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="对话历史" name="history">
            <div class="history-section">
              <div class="section-header">
                <h3>最近的对话</h3>
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索对话..."
                  prefix-icon="Search"
                  style="width: 300px"
                />
              </div>
              
              <div class="conversations-list" v-if="conversations.length > 0">
                <div class="conversation-item" v-for="conversation in filteredConversations" :key="conversation.id">
                  <div class="conversation-info">
                    <h4>{{ conversation.title }}</h4>
                    <p>{{ conversation.lastMessage }}</p>
                    <span class="conversation-time">{{ conversation.updatedAt }}</span>
                  </div>
                  <div class="conversation-actions">
                    <el-button size="small" @click="continueConversation(conversation)">继续对话</el-button>
                    <el-button size="small" type="danger" @click="deleteConversation(conversation)">删除</el-button>
                  </div>
                </div>
              </div>
              
              <el-empty v-else description="还没有对话记录" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import AppHeader from '@/components/AppHeader.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const activeTab = ref('assistants')
const searchQuery = ref('')

const assistants = ref([
  {
    id: 1,
    name: '编程助手',
    description: '专门帮助解决编程问题的AI助手',
    avatar: 'https://via.placeholder.com/60x60/4F46E5/FFFFFF?text=编程',
    conversations: 15,
    createdAt: '2024-01-15'
  },
  {
    id: 2,
    name: '写作助手',
    description: '帮助创作文章和内容的AI助手',
    avatar: 'https://via.placeholder.com/60x60/10B981/FFFFFF?text=写作',
    conversations: 8,
    createdAt: '2024-01-20'
  }
])

const conversations = ref([
  {
    id: 1,
    title: '关于Vue.js的问题',
    lastMessage: 'Vue.js的响应式系统是如何工作的？',
    updatedAt: '2024-01-25 14:30'
  },
  {
    id: 2,
    title: 'Python数据分析',
    lastMessage: '如何使用pandas处理大型数据集？',
    updatedAt: '2024-01-24 09:15'
  }
])

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  return conversations.value.filter(conv => 
    conv.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    conv.lastMessage.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const createAssistant = () => {
  ElMessage.info('创建AI助手功能开发中...')
}

const editAssistant = (assistant) => {
  ElMessage.info(`编辑助手: ${assistant.name}`)
}

const chatWithAssistant = (assistant) => {
  ElMessage.info(`与 ${assistant.name} 开始对话`)
}

const deleteAssistant = async (assistant) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除AI助手 "${assistant.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    assistants.value = assistants.value.filter(a => a.id !== assistant.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消删除
  }
}

const continueConversation = (conversation) => {
  ElMessage.info(`继续对话: ${conversation.title}`)
}

const deleteConversation = async (conversation) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除对话 "${conversation.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    conversations.value = conversations.value.filter(c => c.id !== conversation.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消删除
  }
}
</script>

<style lang="scss" scoped>
.my-ai {
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

.content-tabs {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.custom-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 2rem;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
  
  :deep(.el-tabs__item) {
    font-size: 1.1rem;
    font-weight: 500;
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  h3 {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-primary);
  }
}

.assistants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.assistant-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  
  .assistant-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    
    .assistant-info {
      flex: 1;
      
      h4 {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
      }
      
      p {
        color: var(--text-secondary);
        font-size: 0.9rem;
      }
    }
  }
  
  .assistant-stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }
  
  .assistant-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.conversations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  
  .conversation-info {
    flex: 1;
    
    h4 {
      font-size: 1.1rem;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 0.5rem;
    }
    
    p {
      color: var(--text-secondary);
      margin-bottom: 0.5rem;
    }
    
    .conversation-time {
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
  }
  
  .conversation-actions {
    display: flex;
    gap: 0.5rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .assistants-grid {
    grid-template-columns: 1fr;
  }
  
  .conversation-item {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style>
