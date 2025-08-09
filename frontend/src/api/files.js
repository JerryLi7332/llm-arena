import request from '@/utils/request'

export const filesApi = {
  // 上传文件
  uploadFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/v1/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取文件列表
  getFiles: (params) => {
    return request.get('/api/v1/files/list', { params })
  },

  // 下载文件
  downloadFile: (fileId) => {
    return request.get(`/api/v1/files/download/${fileId}`, {
      responseType: 'blob'
    })
  },

  // 删除文件
  deleteFile: (fileId) => {
    return request.delete(`/api/v1/files/${fileId}`)
  },

  // 批量删除文件
  batchDeleteFiles: (fileIds) => {
    return request.delete('/api/v1/files/batch', { data: { file_ids: fileIds } })
  },

  // 获取文件信息
  getFileInfo: (fileId) => {
    return request.get(`/api/v1/files/${fileId}`)
  }
}
