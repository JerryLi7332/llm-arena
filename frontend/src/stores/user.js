import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const loading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_superuser || false)
  const username = computed(() => user.value?.username || '')
  const avatar = computed(() => user.value?.avatar || '')

  // 方法
  const setTokens = (accessToken, refreshTokenValue) => {
    token.value = accessToken
    refreshToken.value = refreshTokenValue
    
    if (accessToken) {
      localStorage.setItem('token', accessToken)
    } else {
      localStorage.removeItem('token')
    }
    
    if (refreshTokenValue) {
      localStorage.setItem('refreshToken', refreshTokenValue)
    } else {
      localStorage.removeItem('refreshToken')
    }
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await authApi.login(credentials)
      const { access_token, refresh_token, username: userName } = response.data
      
      setTokens(access_token, refresh_token)
      
      // 登录后立即获取完整的用户信息
      try {
        const profileResponse = await authApi.getProfile()
        setUser(profileResponse.data)
      } catch (profileError) {
        console.error('获取用户信息失败，使用基本信息:', profileError)
        setUser({ username: userName })
      }
      
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.msg || error.message }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    try {
      const response = await authApi.register(userData)
      const { access_token, refresh_token, username: userName } = response.data
      
      setTokens(access_token, refresh_token)
      
      // 注册后立即获取完整的用户信息
      try {
        const profileResponse = await authApi.getProfile()
        setUser(profileResponse.data)
      } catch (profileError) {
        console.error('获取用户信息失败，使用基本信息:', profileError)
        setUser({ username: userName })
      }
      
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.msg || error.message }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    setTokens('', '')
    setUser(null)
  }

  const initUser = async () => {
    if (token.value && !user.value) {
      try {
        console.log('正在获取用户信息...')
        console.log('当前token:', token.value)
        
        const response = await authApi.getProfile()
        console.log('API响应:', response)
        console.log('获取到的用户信息:', response.data)
        
        setUser(response.data)
        console.log('用户信息设置完成:', user.value)
      } catch (error) {
        console.error('获取用户信息失败:', error)
        console.error('错误详情:', error.response?.data)
        logout()
      }
    } else {
      console.log('跳过initUser调用:', {
        hasToken: !!token.value,
        hasUser: !!user.value
      })
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    try {
      const response = await authApi.updateProfile(profileData)
      setUser(response.data)
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.msg || error.message }
    } finally {
      loading.value = false
    }
  }

  const refreshUserToken = async () => {
    if (!refreshToken.value) {
      throw new Error('没有刷新令牌')
    }
    
    try {
      const response = await authApi.refreshToken(refreshToken.value)
      const { access_token, refresh_token } = response.data
      setTokens(access_token, refresh_token)
      return { success: true }
    } catch (error) {
      logout()
      throw error
    }
  }

  const clearUser = () => {
    user.value = null
  }

  const getUserProfile = async () => {
    try {
      console.log('手动获取用户信息...')
      const response = await authApi.getProfile()
      console.log('手动获取到的用户信息:', response.data)
      setUser(response.data)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('手动获取用户信息失败:', error)
      return { success: false, message: error.message }
    }
  }

  return {
    // 状态
    user,
    token,
    refreshToken,
    loading,
    
    // 计算属性
    isLoggedIn,
    isAdmin,
    username,
    avatar,
    
    // 方法
    login,
    register,
    logout,
    initUser,
    updateProfile,
    setTokens,
    refreshUserToken,
    clearUser,
    getUserProfile
  }
})
