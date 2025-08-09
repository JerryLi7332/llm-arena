import request from '@/utils/request'

export const usersApi = {
  // 获取用户列表
  getUsers: (params) => {
    return request.get('/api/v1/users/list', { params })
  },

  // 获取单个用户
  getUser: (id) => {
    return request.get(`/api/v1/users/${id}`)
  },

  // 创建用户
  createUser: (userData) => {
    return request.post('/api/v1/users/create', userData)
  },

  // 更新用户
  updateUser: (id, userData) => {
    return request.put(`/api/v1/users/${id}`, userData)
  },

  // 删除用户
  deleteUser: (id) => {
    return request.delete(`/api/v1/users/${id}`)
  },

  // 批量删除用户
  batchDeleteUsers: (ids) => {
    return request.delete('/api/v1/users/batch', { data: { ids } })
  },

  // 更新用户状态
  updateUserStatus: (id, status) => {
    return request.put(`/api/v1/users/${id}/status`, { is_active: status })
  },

  // 重置用户密码
  resetPassword: (id) => {
    return request.put(`/api/v1/users/${id}/reset-password`)
  }
}
