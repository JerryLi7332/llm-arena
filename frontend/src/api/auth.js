import request from '@/utils/request'

export const authApi = {
  // 用户登录
  login: (credentials) => {
    return request.post('/api/v1/base/auth/access_token', credentials)
  },

  // 用户注册
  register: (userData) => {
    return request.post('/api/v1/base/auth/register', userData)
  },

  // 获取用户资料
  getProfile: () => {
    return request.get('/api/v1/base/userinfo')
  },

  // 更新用户资料
  updateProfile: (profileData) => {
    return request.put('/api/v1/users/profile', profileData)
  },

  // 上传用户头像
  uploadAvatar: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/v1/users/upload_avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 删除用户头像
  deleteAvatar: () => {
    return request.delete('/api/v1/users/avatar')
  },

  // 修改密码
  changePassword: (passwordData) => {
    return request.put('/api/v1/users/password', passwordData)
  },

  // 刷新token
  refreshToken: (refreshToken) => {
    return request.post('/api/v1/base/refresh_token', { refresh_token: refreshToken })
  },

  // 健康检查
  healthCheck: () => {
    return request.get('/api/v1/base/health')
  },

  // 获取版本信息
  getVersion: () => {
    return request.get('/api/v1/base/version')
  }
}
