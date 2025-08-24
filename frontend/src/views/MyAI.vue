<template>
  <div class="my-ai">
    <AppHeader />
    <div class="container">
      <h1 class="page-title">我的AI</h1>
      <p class="page-subtitle">管理您创建的AI助手和对话历史</p>
      
      <div class="content-tabs">
        <el-tabs v-model="activeTab" class="custom-tabs">
          
          <el-tab-pane label="游戏AI代码" name="game-ai">
            <div class="game-ai-section">
              <div class="section-header">
                <h3>游戏AI代码管理</h3>
                <el-button type="primary" @click="openUploadDialog">
                  <el-icon><Upload /></el-icon>
                  上传AI代码
                </el-button>
              </div>
              
              <!-- 游戏类型选择 -->
              <div class="game-types">
                <el-radio-group v-model="selectedGame" @change="onGameTypeChange">
                  <el-radio-button label="rock_paper_scissors">石头剪刀布</el-radio-button>
                  <el-radio-button label="avalon">阿瓦隆</el-radio-button>
                </el-radio-group>
              </div>
              
              <!-- AI代码列表 -->
              <div class="ai-codes-grid" v-if="gameAICodes.length > 0">
                <div class="ai-code-card" v-for="aiCode in gameAICodes" :key="aiCode.id" 
                     :class="{ 'active': aiCode.is_active }">
                  <div class="ai-code-header">
                    <div class="ai-code-info">
                      <div class="ai-code-title">
                        <div class="title-left">
                          <el-icon class="file-icon" :class="getFileIconClass(aiCode.file_name)">
                            <Document />
                          </el-icon>
                          <h4>{{ aiCode.name }}</h4>
                        </div>
                        <el-tag :type="aiCode.is_active ? 'success' : 'info'" size="small">
                          {{ aiCode.is_active ? '已激活' : '未激活' }}
                        </el-tag>
                      </div>
                      <p>{{ aiCode.description || '暂无描述' }}</p>
                      <div class="ai-code-meta">
                        <el-tag type="primary" size="small">
                          {{ getGameTypeName(aiCode.game_type) }}
                        </el-tag>
                        <span class="version">版本: {{ aiCode.version }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="ai-code-stats">
                    <span>上传时间: {{ formatDate(aiCode.created_at) }}</span>
                    <span>文件大小: {{ formatFileSize(aiCode.file_size) }}</span>
                    <span v-if="aiCode.last_used">最后使用: {{ formatDate(aiCode.last_used) }}</span>
                  </div>
                  <div class="ai-code-actions">
                    <el-button size="small" @click="activateAICode(aiCode)" 
                               :disabled="aiCode.is_active" 
                               :type="aiCode.is_active ? 'success' : 'primary'">
                      {{ aiCode.is_active ? '已激活' : '激活' }}
                    </el-button>
                    <el-button size="small" @click="downloadAICode(aiCode)">下载</el-button>
                    <el-button size="small" type="warning" @click="editAICode(aiCode)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deleteAICode(aiCode)">删除</el-button>
                  </div>
                  
                  <!-- 上传进度条 -->
                  <div v-if="aiCode.uploading" class="upload-progress">
                    <el-progress :percentage="aiCode.uploadProgress || 0" :show-text="false" />
                    <span class="progress-text">上传中... {{ aiCode.uploadProgress || 0 }}%</span>
                  </div>
                </div>
              </div>
              
              <el-empty v-else description="还没有上传AI代码" />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="对话历史" name="history">
            <div class="history-section">
              <div class="section-header">
                <h3>最近的对话</h3>
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索对话..."
                  prefix-icon="Search"
                  style="width: 300px"
                />
              </div>
              
              <div class="conversations-list" v-if="conversations.length > 0">
                <div class="conversation-item" v-for="conversation in filteredConversations" :key="conversation.id">
                  <div class="conversation-info">
                    <h4>{{ conversation.title }}</h4>
                    <p>{{ conversation.lastMessage }}</p>
                    <span class="conversation-time">{{ conversation.updatedAt }}</span>
                  </div>
                  <div class="conversation-actions">
                    <el-button size="small" @click="continueConversation(conversation)">继续对话</el-button>
                    <el-button size="small" type="danger" @click="deleteConversation(conversation)">删除</el-button>
                  </div>
                </div>
              </div>
              
              <el-empty v-else description="还没有对话记录" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    
    <!-- 上传AI代码对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传AI代码"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef" label-width="100px">
        <el-form-item label="游戏类型" prop="game_type">
          <el-select v-model="uploadForm.game_type" placeholder="选择游戏类型" style="width: 100%">
            <el-option label="石头剪刀布" value="rock_paper_scissors" />
            <el-option label="阿瓦隆" value="avalon" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="AI名称" prop="name">
          <el-input v-model="uploadForm.name" placeholder="请输入AI代码名称" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入AI代码描述（可选）"
          />
        </el-form-item>
        
        <el-form-item label="代码文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".py,.js,.java,.cpp,.c,.zip,.rar"
            :limit="1"
            :before-upload="beforeFileUpload"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持Python、JavaScript、Java、C++、C等代码文件，或ZIP/RAR压缩包
                <br>文件大小限制：10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showUploadDialog = false" :disabled="uploading">取消</el-button>
          <el-button type="primary" @click="uploadAICode" :loading="uploading">
            {{ uploading ? '上传中...' : '上传' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Document } from '@element-plus/icons-vue'
import AppHeader from '@/components/AppHeader.vue'
import { useUserStore } from '@/stores/user'
import { gameAIApi } from '@/api/gameAI'

const userStore = useUserStore()

const activeTab = ref('game-ai')
const searchQuery = ref('')
const selectedGame = ref('rock_paper_scissors')
const showUploadDialog = ref(false)
const uploading = ref(false)
const gameAICodes = ref([])

// 上传表单
const uploadForm = ref({
  game_type: '',
  name: '',
  description: '',
  file: null
})

const uploadRules = {
  game_type: [{ required: true, message: '请选择游戏类型', trigger: 'change' }],
  name: [{ required: true, message: '请输入AI代码名称', trigger: 'blur' }],
  file: [{ required: true, message: '请选择代码文件', trigger: 'change' }]
}

const uploadFormRef = ref()
const uploadRef = ref()
const fileList = ref([])

// 模拟数据
const assistants = ref([
  {
    id: 1,
    name: '智能助手',
    description: '一个智能的AI助手',
    avatar: '',
    conversations: 10,
    createdAt: '2024-01-01'
  }
])

const conversations = ref([
  {
    id: 1,
    title: '关于AI的讨论',
    lastMessage: 'AI技术发展很快...',
    updatedAt: '2024-01-01 10:00'
  }
])

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  return conversations.value.filter(conv => 
    conv.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    conv.lastMessage.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const createAssistant = () => {
  ElMessage.info('创建助手功能开发中...')
}

const editAssistant = (assistant) => {
  ElMessage.info('编辑助手功能开发中...')
}

const chatWithAssistant = (assistant) => {
  ElMessage.info('对话功能开发中...')
}

const deleteAssistant = (assistant) => {
  ElMessage.info('删除助手功能开发中...')
}

const continueConversation = (conversation) => {
  ElMessage.info('继续对话功能开发中...')
}

const deleteConversation = (conversation) => {
  ElMessage.info('删除对话功能开发中...')
}

// 游戏AI代码相关方法
const openUploadDialog = () => {
  uploadForm.value.game_type = selectedGame.value
  showUploadDialog.value = true
}

const onGameTypeChange = () => {
  loadGameAICodes()
}

const loadGameAICodes = async () => {
  try {
    console.log('开始获取AI代码列表...')
    console.log('当前游戏类型:', selectedGame.value)
    console.log('当前用户token:', userStore.token)
    console.log('用户登录状态:', userStore.isLoggedIn)
    
    const response = await gameAIApi.getGameAICodes(selectedGame.value)
    console.log('API响应:', response)
    
    // 直接使用响应数据，因为request拦截器已经处理了response.data
    gameAICodes.value = response || []
    console.log('设置AI代码列表:', gameAICodes.value)
  } catch (error) {
    console.error('获取AI代码列表失败:', error)
    console.error('错误详情:', error.response?.data)
    console.error('错误状态:', error.response?.status)
    gameAICodes.value = []
    // 暂时使用模拟数据，等后端API完善后移除
    gameAICodes.value = [
      {
        id: 1,
        name: '智能石头剪刀布AI',
        description: '基于机器学习的石头剪刀布AI',
        game_type: 'rock_paper_scissors',
        version: 1,
        is_active: true,
        created_at: '2024-01-01T10:00:00Z',
        file_size: 1024 * 1024 // 1MB
      }
    ]
  }
}

const beforeFileUpload = (file) => {
  const maxSize = 10 * 1024 * 1024 // 10MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  return true
}

const handleFileChange = (file) => {
  uploadForm.value.file = file.raw
  fileList.value = [file]
}

const uploadAICode = async () => {
  // 表单验证
  try {
    await uploadFormRef.value.validate()
  } catch (error) {
    return
  }
  
  if (!uploadForm.value.file) {
    ElMessage.error('请选择代码文件')
    return
  }
  
  try {
    uploading.value = true
    
    console.log('开始上传AI代码...')
    console.log('上传数据:', {
      game_type: uploadForm.value.game_type,
      name: uploadForm.value.name,
      description: uploadForm.value.description,
      file: uploadForm.value.file
    })
    console.log('当前用户token:', userStore.token)
    
    // 使用gameAIApi上传AI代码
    const uploadResponse = await gameAIApi.uploadGameAICode(
      uploadForm.value.game_type,
      uploadForm.value
    )
    
    console.log('上传响应:', uploadResponse)
    
    // 直接使用响应数据
    if (uploadResponse) {
      ElMessage.success('AI代码上传成功！')
      showUploadDialog.value = false
      await loadGameAICodes()
      
      // 重置表单
      uploadForm.value = {
        game_type: '',
        name: '',
        description: '',
        file: null
      }
      fileList.value = []
    } else {
      ElMessage.error('上传失败：未知错误')
    }
  } catch (error) {
    console.error('上传失败:', error)
    console.error('错误详情:', error.response?.data)
    console.error('错误状态:', error.response?.status)
    ElMessage.error('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

const activateAICode = async (aiCode) => {
  try {
    const response = await gameAIApi.activateAICode(aiCode.id)
    if (response) {
      ElMessage.success('AI代码激活成功！')
      await loadGameAICodes()
    } else {
      ElMessage.error('激活失败：未知错误')
    }
  } catch (error) {
    console.error('激活失败:', error)
    ElMessage.error('激活失败，请重试')
  }
}

const downloadAICode = async (aiCode) => {
  try {
    const response = await gameAIApi.downloadAICode(aiCode.id)
    
    // 创建下载链接
    const blob = new Blob([response])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = aiCode.name + '.zip'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('下载开始')
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败，请重试')
  }
}

const editAICode = (aiCode) => {
  ElMessage.info('编辑AI代码功能开发中...')
}

const deleteAICode = async (aiCode) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除AI代码"${aiCode.name}"吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const response = await gameAIApi.deleteAICode(aiCode.id)
    if (response) {
      ElMessage.success('删除成功！')
      await loadGameAICodes()
    } else {
      ElMessage.error('删除失败：未知错误')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const getGameTypeName = (gameType) => {
  const gameTypeMap = {
    'rock_paper_scissors': '石头剪刀布',
    'avalon': '阿瓦隆'
  }
  return gameTypeMap[gameType] || gameType
}

const getFileIconClass = (fileName) => {
  if (!fileName) return 'file-default'
  const ext = fileName.split('.').pop()?.toLowerCase()
  const iconMap = {
    'py': 'file-python',
    'js': 'file-javascript',
    'java': 'file-java',
    'cpp': 'file-cpp',
    'c': 'file-c',
    'zip': 'file-zip',
    'rar': 'file-rar'
  }
  return iconMap[ext] || 'file-default'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

onMounted(async () => {
  // 确保用户已登录
  if (!userStore.isLoggedIn) {
    ElMessage.error('请先登录')
    return
  }
  
  // 如果用户信息不完整，尝试获取
  if (!userStore.user && userStore.token) {
    try {
      await userStore.initUser()
    } catch (error) {
      console.error('获取用户信息失败:', error)
      ElMessage.error('获取用户信息失败，请重新登录')
      return
    }
  }
  
  loadGameAICodes()
})
</script>

<style lang="scss" scoped>
.my-ai {
  padding: 120px 0 80px;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  text-align: center;
  font-size: 3rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
}

.page-subtitle {
  text-align: center;
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 3rem;
}

.content-tabs {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.custom-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 2rem;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
  
  :deep(.el-tabs__item) {
    font-size: 1.1rem;
    font-weight: 500;
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  h3 {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-primary);
  }
}

.game-types {
  margin-bottom: 2rem;
  text-align: center;
}

.ai-codes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.ai-code-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  
  &.active {
    border-color: #67c23a;
    box-shadow: 0 0 0 2px rgba(103, 194, 58, 0.2);
  }
  
  .ai-code-header {
    margin-bottom: 1rem;
    
    .ai-code-info {
      .ai-code-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        
        .title-left {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          
          .file-icon {
            font-size: 1.5rem;
            color: var(--text-secondary);
            
            &.file-python { color: #3776ab; }
            &.file-javascript { color: #f7df1e; }
            &.file-java { color: #007396; }
            &.file-cpp { color: #00599c; }
            &.file-c { color: #a8b9cc; }
            &.file-zip { color: #ffd700; }
            &.file-rar { color: #e31b23; }
            &.file-default { color: var(--text-secondary); }
          }
        }
        
        h4 {
          font-size: 1.2rem;
          font-weight: bold;
          color: var(--text-primary);
          margin: 0;
        }
      }
      
      p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
      }
      
      .ai-code-meta {
        display: flex;
        align-items: center;
        gap: 1rem;
        
        .version {
          font-size: 0.8rem;
          color: var(--text-secondary);
        }
      }
    }
  }
  
  .ai-code-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }
  
  .ai-code-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .upload-progress {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
    
    .progress-text {
      display: block;
      text-align: center;
      font-size: 0.8rem;
      color: var(--text-secondary);
      margin-top: 0.5rem;
    }
  }
}

.assistants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.assistant-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  
  .assistant-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    
    .assistant-info {
      flex: 1;
      
      h4 {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
      }
      
      p {
        color: var(--text-secondary);
        font-size: 0.9rem;
      }
    }
  }
  
  .assistant-stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }
  
  .assistant-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.conversations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  
  .conversation-info {
    flex: 1;
    
    h4 {
      font-size: 1.1rem;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 0.5rem;
    }
    
    p {
      color: var(--text-secondary);
      margin-bottom: 0.5rem;
    }
    
    .conversation-time {
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
  }
  
  .conversation-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .assistants-grid,
  .ai-codes-grid {
    grid-template-columns: 1fr;
  }
  
  .conversation-item {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style>
