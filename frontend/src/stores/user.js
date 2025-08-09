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
      setUser({ username: userName })
      
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
      setUser({ username: userName })
      
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
        const response = await authApi.getProfile()
        setUser(response.data)
      } catch (error) {
        logout()
      }
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
    refreshUserToken
  }
})
