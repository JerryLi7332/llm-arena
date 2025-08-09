<template>
  <div class="dashboard">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="text-gradient">LLM Arena</h2>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item active">
          <el-icon><Monitor /></el-icon>
          <span>仪表板</span>
        </router-link>
        <router-link to="/chat" class="nav-item">
          <el-icon><ChatDotRound /></el-icon>
          <span>AI对话</span>
        </router-link>
        <router-link to="/models" class="nav-item">
          <el-icon><Connection /></el-icon>
          <span>模型管理</span>
        </router-link>
        <router-link to="/history" class="nav-item">
          <el-icon><Clock /></el-icon>
          <span>对话历史</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-avatar :size="32" :src="userStore.user?.avatar">
              {{ userStore.username.charAt(0).toUpperCase() }}
            </el-avatar>
            <span>{{ userStore.username }}</span>
            <el-icon><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="main-header">
        <h1>仪表板</h1>
        <p>欢迎回来，{{ userStore.username }}！</p>
      </header>

      <div class="dashboard-content">
        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">1,234</div>
              <div class="stat-label">总对话数</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">15</div>
              <div class="stat-label">可用模型</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">89</div>
              <div class="stat-label">本月对话</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">4.8</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions">
          <h3>快速操作</h3>
          <div class="actions-grid">
            <div class="action-card" @click="startNewChat">
              <el-icon><Plus /></el-icon>
              <span>开始新对话</span>
            </div>
            <div class="action-card" @click="viewHistory">
              <el-icon><Document /></el-icon>
              <span>查看历史</span>
            </div>
            <div class="action-card" @click="manageModels">
              <el-icon><Setting /></el-icon>
              <span>模型设置</span>
            </div>
            <div class="action-card" @click="viewAnalytics">
              <el-icon><DataAnalysis /></el-icon>
              <span>数据分析</span>
            </div>
          </div>
        </div>

        <!-- 最近对话 -->
        <div class="recent-chats">
          <h3>最近对话</h3>
          <div class="chat-list">
            <div v-for="chat in recentChats" :key="chat.id" class="chat-item">
              <div class="chat-info">
                <div class="chat-title">{{ chat.title }}</div>
                <div class="chat-meta">
                  <span>{{ chat.model }}</span>
                  <span>{{ chat.time }}</span>
                </div>
              </div>
              <el-button size="small" @click="continueChat(chat.id)">
                继续
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  Monitor,
  ChatDotRound,
  Connection,
  Clock,
  Setting,
  ArrowDown,
  Plus,
  Document,
  DataAnalysis,
  Star
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const recentChats = ref([
  {
    id: 1,
    title: '关于人工智能的讨论',
    model: 'GPT-4',
    time: '2小时前'
  },
  {
    id: 2,
    title: '代码优化建议',
    model: 'Claude-3',
    time: '1天前'
  },
  {
    id: 3,
    title: '创意写作帮助',
    model: 'Gemini Pro',
    time: '3天前'
  }
])

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
      break
  }
}

const startNewChat = () => {
  router.push('/chat')
}

const viewHistory = () => {
  router.push('/history')
}

const manageModels = () => {
  router.push('/models')
}

const viewAnalytics = () => {
  router.push('/analytics')
}

const continueChat = (chatId) => {
  router.push(`/chat/${chatId}`)
}
</script>

<style lang="scss" scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;

  .sidebar-header {
    padding: 20px;
    border-bottom: 1px solid var(--border-color);

    h2 {
      font-size: 1.5rem;
      font-weight: bold;
    }
  }

  .sidebar-nav {
    flex: 1;
    padding: 20px 0;

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 20px;
      color: var(--text-secondary);
      text-decoration: none;
      transition: all 0.3s;

      &:hover,
      &.active {
        background: var(--bg-secondary);
        color: var(--primary-color);
      }

      .el-icon {
        font-size: 1.2rem;
      }
    }
  }

  .sidebar-footer {
    padding: 20px;
    border-top: 1px solid var(--border-color);

    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      padding: 8px;
      border-radius: 8px;
      transition: background 0.3s;

      &:hover {
        background: var(--bg-secondary);
      }
    }
  }
}

.main-content {
  flex: 1;
  background: var(--bg-secondary);
  overflow-y: auto;
}

.main-header {
  background: var(--bg-primary);
  padding: 24px 32px;
  border-bottom: 1px solid var(--border-color);

  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 8px;
    color: var(--text-primary);
  }

  p {
    color: var(--text-secondary);
  }
}

.dashboard-content {
  padding: 32px;

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
  }

  .stat-card {
    background: var(--bg-primary);
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 16px;

    .stat-icon {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, var(--primary-color), #8b5cf6);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 1.5rem;
    }

    .stat-info {
      .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 4px;
      }

      .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
      }
    }
  }

  .quick-actions {
    margin-bottom: 32px;

    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 16px;
      color: var(--text-primary);
    }

    .actions-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .action-card {
      background: var(--bg-primary);
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
      }

      .el-icon {
        font-size: 2rem;
        color: var(--primary-color);
      }

      span {
        font-weight: 500;
        color: var(--text-primary);
      }
    }
  }

  .recent-chats {
    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 16px;
      color: var(--text-primary);
    }

    .chat-list {
      background: var(--bg-primary);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .chat-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 24px;
      border-bottom: 1px solid var(--border-color);

      &:last-child {
        border-bottom: none;
      }

      .chat-info {
        .chat-title {
          font-weight: 500;
          color: var(--text-primary);
          margin-bottom: 4px;
        }

        .chat-meta {
          display: flex;
          gap: 16px;
          font-size: 0.9rem;
          color: var(--text-secondary);
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .dashboard {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
  }

  .dashboard-content {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
