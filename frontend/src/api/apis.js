import request from '@/utils/request'

export const apisApi = {
  // 获取API列表
  getApis: (params) => {
    return request.get('/api/v1/api/list', { params })
  },

  // 获取单个API
  getApi: (id) => {
    return request.get(`/api/v1/api/${id}`)
  },

  // 创建API
  createApi: (apiData) => {
    return request.post('/api/v1/api/create', apiData)
  },

  // 更新API
  updateApi: (id, apiData) => {
    return request.put(`/api/v1/api/${id}`, apiData)
  },

  // 删除API
  deleteApi: (id) => {
    return request.delete(`/api/v1/api/${id}`)
  },

  // 批量删除API
  batchDeleteApis: (ids) => {
    return request.delete('/api/v1/api/batch', { data: { ids } })
  },

  // 刷新API列表
  refreshApis: () => {
    return request.post('/api/v1/api/refresh')
  }
}
