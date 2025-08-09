import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api/auth'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000, // 增加超时时间
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // 允许携带cookies
})

// 是否正在刷新token
let isRefreshing = false
// 存储等待token刷新的请求
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  
  failedQueue = []
}

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    // 添加请求时间戳，避免缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  (error) => {
    ElMessage.error('请求配置错误')
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const userStore = useUserStore()
    const originalRequest = error.config
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 如果是刷新token的请求失败，直接登出
          if (originalRequest.url.includes('/refresh_token')) {
            ElMessage.error('登录已过期，请重新登录')
            userStore.logout()
            window.location.href = '/login'
            return Promise.reject(error)
          }
          
          // 如果正在刷新token，将请求加入队列
          if (isRefreshing) {
            return new Promise((resolve, reject) => {
              failedQueue.push({ resolve, reject })
            }).then(token => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              return request(originalRequest)
            }).catch(err => {
              return Promise.reject(err)
            })
          }
          
          // 开始刷新token
          isRefreshing = true
          
          try {
            const refreshToken = userStore.refreshToken
            if (!refreshToken) {
              throw new Error('没有刷新令牌')
            }
            
            const response = await authApi.refreshToken(refreshToken)
            const { access_token, refresh_token } = response.data
            
            // 更新token
            userStore.setTokens(access_token, refresh_token)
            
            // 处理队列中的请求
            processQueue(null, access_token)
            
            // 重试原请求
            originalRequest.headers.Authorization = `Bearer ${access_token}`
            return request(originalRequest)
          } catch (refreshError) {
            processQueue(refreshError, null)
            ElMessage.error('登录已过期，请重新登录')
            userStore.logout()
            window.location.href = '/login'
            return Promise.reject(refreshError)
          } finally {
            isRefreshing = false
          }
          
        case 403:
          ElMessage.error('权限不足，请联系管理员')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          const errorMsg = data?.detail || data?.message || '请求参数错误'
          ElMessage.error(errorMsg)
          break
        case 429:
          ElMessage.error('请求过于频繁，请稍后再试')
          break
        case 500:
          ElMessage.error('服务器内部错误，请联系管理员')
          break
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default request
