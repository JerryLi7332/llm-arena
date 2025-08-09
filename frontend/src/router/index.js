import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册', requiresGuest: true }
  },
  {
    path: '/arena',
    name: 'Arena',
    component: () => import('@/views/Arena.vue'),
    meta: { title: '对战大厅' }
  },
  {
    path: '/my-ai',
    name: 'MyAI',
    component: () => import('@/views/MyAI.vue'),
    meta: { title: '我的AI', requiresAuth: true }
  },
  {
    path: '/collaboration',
    name: 'Collaboration',
    component: () => import('@/views/Collaboration.vue'),
    meta: { title: '共创' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: { title: '关于' }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/Admin.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人资料', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - LLM Arena` : 'LLM Arena'
  
  // 初始化用户信息
  if (userStore.token && !userStore.user) {
    try {
      await userStore.initUser()
    } catch (error) {
      console.error('初始化用户信息失败:', error)
      userStore.logout()
    }
  }
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
    return
  }
  
  // 已登录用户不能访问登录/注册页面
  if (to.meta.requiresGuest && userStore.isLoggedIn) {
    next('/')
    return
  }
  
  next()
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  // 可以在这里添加错误处理逻辑，比如跳转到错误页面
})

export default router
