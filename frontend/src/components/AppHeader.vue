<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <h1 class="text-gradient">LLM Arena</h1>
        </router-link>
      </div>
      
      <div class="nav-menu">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/arena" class="nav-link" :class="{ active: $route.path === '/arena' }">对战大厅</router-link>
        <router-link to="/my-ai" class="nav-link" :class="{ active: $route.path === '/my-ai' }" v-if="userStore.isLoggedIn">我的AI</router-link>
        <router-link to="/collaboration" class="nav-link" :class="{ active: $route.path === '/collaboration' }">共创</router-link>
        <router-link to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">关于</router-link>
      </div>
      
      <div class="nav-auth">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <span class="user-menu">
              <el-avatar :size="32" :src="userStore.avatar || 'https://via.placeholder.com/32x32/4F46E5/FFFFFF?text=' + userStore.username?.charAt(0)" />
              <span class="username">{{ userStore.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn-primary">登录</router-link>
          <router-link to="/register" class="btn btn-secondary">注册</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()

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
</script>

<style lang="scss" scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  z-index: 1000;
  padding: 1rem 0;

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .nav-brand {
    .brand-link {
      text-decoration: none;
      
      h1 {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
      }
    }
  }

  .nav-menu {
    display: flex;
    gap: 2rem;

    .nav-link {
      color: var(--text-primary);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.3s;
      padding: 0.5rem 0;
      position: relative;

      &:hover {
        color: var(--primary-color);
      }

      &.active {
        color: var(--primary-color);
        
        &::after {
          content: '';
          position: absolute;
          bottom: -1rem;
          left: 0;
          right: 0;
          height: 2px;
          background: var(--primary-color);
        }
      }
    }
  }

  .nav-auth {
    display: flex;
    gap: 1rem;
    align-items: center;

    .btn {
      padding: 8px 16px;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 500;
      transition: all 0.3s;

      &.btn-primary {
        background: var(--primary-color);
        color: white;

        &:hover {
          background: #4f46e5;
        }
      }

      &.btn-secondary {
        background: transparent;
        color: var(--text-primary);
        border: 1px solid var(--border-color);

        &:hover {
          background: var(--bg-secondary);
        }
      }
    }

    .user-menu {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 6px;
      transition: background 0.3s;

      &:hover {
        background: var(--bg-secondary);
      }

      .username {
        font-weight: 500;
        color: var(--text-primary);
      }
    }
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
}
</style>
