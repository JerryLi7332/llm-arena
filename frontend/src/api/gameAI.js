import request from '@/utils/request'

export const gameAIApi = {
  // 获取游戏AI代码列表
  getGameAICodes: (gameType) => {
    return request.get(`/api/v1/games/ai-codes/${gameType}`)
  },

  // 上传游戏AI代码
  uploadGameAICode: (gameType, data) => {
    const formData = new FormData()
    formData.append('file', data.file)
    formData.append('name', data.name)
    formData.append('description', data.description || '')
    formData.append('game_type', gameType)
    
    return request.post(`/api/v1/games/ai-codes/${gameType}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 激活AI代码
  activateAICode: (aiCodeId) => {
    return request.post(`/api/v1/games/ai-codes/${aiCodeId}/activate`)
  },

  // 下载AI代码
  downloadAICode: (aiCodeId) => {
    return request.get(`/api/v1/games/ai-codes/${aiCodeId}/download`, {
      responseType: 'blob'
    })
  },

  // 删除AI代码
  deleteAICode: (aiCodeId) => {
    return request.delete(`/api/v1/games/ai-codes/${aiCodeId}`)
  },

  // 获取AI代码详情
  getAICodeDetail: (aiCodeId) => {
    return request.get(`/api/v1/games/ai-codes/${aiCodeId}`)
  },

  // 更新AI代码信息
  updateAICode: (aiCodeId, data) => {
    return request.put(`/api/v1/games/ai-codes/${aiCodeId}`, data)
  }
}
