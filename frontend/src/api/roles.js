import request from '@/utils/request'

export const rolesApi = {
  // 获取角色列表
  getRoles: (params) => {
    return request.get('/api/v1/role/list', { params })
  },

  // 获取单个角色
  getRole: (id) => {
    return request.get(`/api/v1/role/${id}`)
  },

  // 创建角色
  createRole: (roleData) => {
    return request.post('/api/v1/role/create', roleData)
  },

  // 更新角色
  updateRole: (id, roleData) => {
    return request.put(`/api/v1/role/${id}`, roleData)
  },

  // 删除角色
  deleteRole: (id) => {
    return request.delete(`/api/v1/role/${id}`)
  },

  // 批量删除角色
  batchDeleteRoles: (ids) => {
    return request.delete('/api/v1/role/batch', { data: { ids } })
  },

  // 获取角色权限
  getRolePermissions: (id) => {
    return request.get(`/api/v1/role/${id}/permissions`)
  },

  // 更新角色权限
  updateRolePermissions: (id, permissions) => {
    return request.put(`/api/v1/role/${id}/permissions`, { permissions })
  }
}
