<template>
  <div class="admin">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="text-gradient">管理后台</h2>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-item active">
          <el-icon><Monitor /></el-icon>
          <span>概览</span>
        </router-link>
        <router-link to="/admin/users" class="nav-item">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </router-link>
        <router-link to="/admin/models" class="nav-item">
          <el-icon><Connection /></el-icon>
          <span>模型管理</span>
        </router-link>
        <router-link to="/admin/logs" class="nav-item">
          <el-icon><Document /></el-icon>
          <span>系统日志</span>
        </router-link>
        <router-link to="/admin/settings" class="nav-item">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
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
        <h1>管理后台</h1>
        <p>系统管理和监控</p>
      </header>

      <div class="admin-content">
        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">1,234</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">5,678</div>
              <div class="stat-label">总对话数</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">15</div>
              <div class="stat-label">活跃模型</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">99.9%</div>
              <div class="stat-label">系统可用性</div>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="quick-actions">
          <h3>快速操作</h3>
          <div class="actions-grid">
            <div class="action-card" @click="manageUsers">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </div>
            <div class="action-card" @click="manageModels">
              <el-icon><Connection /></el-icon>
              <span>模型管理</span>
            </div>
            <div class="action-card" @click="viewLogs">
              <el-icon><Document /></el-icon>
              <span>系统日志</span>
            </div>
            <div class="action-card" @click="systemSettings">
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </div>
          </div>
        </div>

        <!-- 最近活动 -->
        <div class="recent-activity">
          <h3>最近活动</h3>
          <div class="activity-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon">
                <el-icon><component :is="activity.icon" /></el-icon>
              </div>
              <div class="activity-info">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-meta">
                  <span>{{ activity.user }}</span>
                  <span>{{ activity.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统状态 -->
        <div class="system-status">
          <h3>系统状态</h3>
          <div class="status-grid">
            <div class="status-item">
              <div class="status-label">CPU使用率</div>
              <el-progress :percentage="65" :color="getStatusColor(65)" />
            </div>
            <div class="status-item">
              <div class="status-label">内存使用率</div>
              <el-progress :percentage="45" :color="getStatusColor(45)" />
            </div>
            <div class="status-item">
              <div class="status-label">磁盘使用率</div>
              <el-progress :percentage="78" :color="getStatusColor(78)" />
            </div>
            <div class="status-item">
              <div class="status-label">网络状态</div>
              <div class="status-indicator online">正常</div>
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
  User,
  Connection,
  Document,
  Setting,
  ArrowDown,
  ChatDotRound,
  TrendCharts
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const recentActivities = ref([
  {
    id: 1,
    title: '新用户注册',
    user: 'user123',
    time: '2分钟前',
    icon: 'User'
  },
  {
    id: 2,
    title: '模型配置更新',
    user: 'admin',
    time: '5分钟前',
    icon: 'Connection'
  },
  {
    id: 3,
    title: '系统备份完成',
    user: 'system',
    time: '1小时前',
    icon: 'Document'
  },
  {
    id: 4,
    title: '新对话开始',
    user: 'user456',
    time: '2小时前',
    icon: 'ChatDotRound'
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

const manageUsers = () => {
  router.push('/admin/users')
}

const manageModels = () => {
  router.push('/admin/models')
}

const viewLogs = () => {
  router.push('/admin/logs')
}

const systemSettings = () => {
  router.push('/admin/settings')
}

const getStatusColor = (percentage) => {
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}
</script>

<style lang="scss" scoped>
.admin {
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

.admin-content {
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

  .recent-activity {
    margin-bottom: 32px;

    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 16px;
      color: var(--text-primary);
    }

    .activity-list {
      background: var(--bg-primary);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .activity-item {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px 24px;
      border-bottom: 1px solid var(--border-color);

      &:last-child {
        border-bottom: none;
      }

      .activity-icon {
        width: 40px;
        height: 40px;
        background: var(--bg-secondary);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary-color);
      }

      .activity-info {
        flex: 1;

        .activity-title {
          font-weight: 500;
          color: var(--text-primary);
          margin-bottom: 4px;
        }

        .activity-meta {
          display: flex;
          gap: 16px;
          font-size: 0.9rem;
          color: var(--text-secondary);
        }
      }
    }
  }

  .system-status {
    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      margin-bottom: 16px;
      color: var(--text-primary);
    }

    .status-grid {
      background: var(--bg-primary);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 24px;
    }

    .status-item {
      .status-label {
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 8px;
      }

      .status-indicator {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 500;
        text-align: center;

        &.online {
          background: #f0f9ff;
          color: #0369a1;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .admin {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: auto;
  }

  .admin-content {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .status-grid {
    grid-template-columns: 1fr;
  }
}
</style>
