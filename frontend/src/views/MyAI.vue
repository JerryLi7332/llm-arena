<template>
  <Layout>
    <div class="my-ai">
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
          
          <el-tab-pane label="AI聊天" name="chat">
            <div class="chat-section">
              <!-- API配置面板 -->
              <div class="api-config-panel">
                <div class="config-header">
                  <h4>DeepSeek API配置</h4>
                  <el-switch
                    v-model="useRealAPI"
                    @change="toggleAPI"
                    active-text="真实API"
                    inactive-text="模拟模式"
                  />
                </div>
                
                <div class="config-options" v-if="useRealAPI">
                  <el-row :gutter="20">
                    <el-col :span="8">
                      <el-form-item label="模型">
                        <el-select v-model="selectedModel" placeholder="选择模型">
                          <el-option
                            v-for="model in availableModels"
                            :key="model.id"
                            :label="model.id"
                            :value="model.id"
                          />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="创造性">
                        <el-slider
                          v-model="temperature"
                          :min="0"
                          :max="2"
                          :step="0.1"
                          show-tooltip
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="最大长度">
                        <el-input-number
                          v-model="maxTokens"
                          :min="100"
                          :max="4000"
                          :step="100"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  
                  <div class="api-status">
                    <el-tag :type="apiStatus === 'available' ? 'success' : apiStatus === 'error' ? 'danger' : 'warning'">
                      API状态: {{ apiStatus === 'available' ? '正常' : apiStatus === 'error' ? '错误' : '未知' }}
                    </el-tag>
                  </div>
                </div>
                
                <div class="config-info" v-else>
                  <el-alert
                    title="模拟模式"
                    description="当前使用模拟AI回复，无需API密钥。切换到真实DeepSeek API模式可获得更智能的回复。"
                    type="info"
                    show-icon
                    :closable="false"
                  />
                </div>
              </div>
              
              <div class="chat-container">
                <!-- 聊天消息列表 -->
                <div class="chat-messages" ref="chatMessagesRef">
                  <div v-if="messages.length === 0" class="welcome-message">
                    <div class="welcome-icon">
                      <el-icon size="48"><ChatDotRound /></el-icon>
                    </div>
                    <h3>欢迎使用AI聊天助手</h3>
                    <p>我是您的智能AI助手，可以回答各种问题、帮助解决问题、进行创意写作等。</p>
                    <p>请开始您的对话吧！</p>
                  </div>
                  
                  <div v-else class="message-list">
                    <div 
                      v-for="message in messages" 
                      :key="message.id" 
                      class="message-item"
                      :class="{ 'user-message': message.role === 'user', 'ai-message': message.role === 'assistant' }"
                    >
                      <div class="message-avatar">
                        <el-avatar 
                          :size="32" 
                          :src="message.role === 'user' ? userStore.user?.avatar : '/ai-avatar.png'"
                          :icon="message.role === 'user' ? 'User' : 'Service'"
                        />
                      </div>
                      <div class="message-content">
                        <div class="message-header">
                          <span class="message-role">{{ message.role === 'user' ? '您' : 'AI助手' }}</span>
                          <span class="message-time">{{ formatMessageTime(message.timestamp) }}</span>
                        </div>
                        <div class="message-text" v-html="formatMessageText(message.content)"></div>
                        <div v-if="message.role === 'assistant'" class="message-actions">
                          <el-button size="small" text @click="copyMessage(message.content)">
                            <el-icon><CopyDocument /></el-icon>
                            复制
                          </el-button>
                          <el-button size="small" text @click="regenerateMessage(message)">
                            <el-icon><Refresh /></el-icon>
                            重新生成
                          </el-button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 加载状态 -->
                    <div v-if="isLoading" class="message-item ai-message">
                      <div class="message-avatar">
                        <el-avatar size="32" icon="Service" />
                      </div>
                      <div class="message-content">
                        <div class="message-header">
                          <span class="message-role">AI助手</span>
                        </div>
                        <div class="message-text">
                          <div class="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 聊天输入区域 -->
                <div class="chat-input-area">
                  <div class="input-container">
                    <el-input
                      v-model="inputMessage"
                      type="textarea"
                      :rows="1"
                      :autosize="{ minRows: 1, maxRows: 4 }"
                      placeholder="输入您的消息... (Shift+Enter换行，Enter发送)"
                      @keydown.enter.prevent="handleEnterKey"
                      @keydown.shift.enter="handleShiftEnter"
                      ref="messageInputRef"
                      class="message-input"
                    />
                    <div class="input-actions">
                      <el-button 
                        type="primary" 
                        :disabled="!inputMessage.trim() || isLoading"
                        @click="sendMessage"
                        :loading="isLoading"
                        class="send-button"
                      >
                        <el-icon v-if="!isLoading"><Promotion /></el-icon>
                        <span v-if="!isLoading">发送</span>
                        <span v-else>生成中...</span>
                      </el-button>
                    </div>
                  </div>
                  
                  <!-- 快捷操作 -->
                  <div class="quick-actions">
                    <el-button size="small" text @click="clearChat">
                      <el-icon><Delete /></el-icon>
                      清空对话
                    </el-button>
                    <el-button size="small" text @click="exportChat">
                      <el-icon><Download /></el-icon>
                      导出对话
                    </el-button>
                  </div>
                </div>
              </div>
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
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Document, ChatDotRound, CopyDocument, Refresh, Promotion, Delete, Download } from '@element-plus/icons-vue'
import Layout from '@/components/Layout.vue'
import { useUserStore } from '@/stores/user'
import { gameAIApi } from '@/api/gameAI'
import { deepseekApi, mockDeepseekApi } from '@/api/deepseek'

const userStore = useUserStore()

const activeTab = ref('chat')
const searchQuery = ref('')
const selectedGame = ref('rock_paper_scissors')
const showUploadDialog = ref(false)
const uploading = ref(false)
const gameAICodes = ref([])

// 聊天相关数据
const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const chatMessagesRef = ref(null)
const messageInputRef = ref(null)

// DeepSeek API配置
const useRealAPI = ref(true) // 是否使用真实DeepSeek API，默认开启
const selectedModel = ref('deepseek-chat')
const temperature = ref(0.7)
const maxTokens = ref(1000)
const availableModels = ref([])
const apiStatus = ref('unknown')

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


// 聊天相关方法
const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return
  
  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputMessage.value.trim(),
    timestamp: new Date()
  }
  
  messages.value.push(userMessage)
  const messageToSend = inputMessage.value.trim()
  inputMessage.value = ''
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
  
  // 调用AI API
  isLoading.value = true
  try {
    if (useRealAPI.value) {
      await callDeepseekAPI(messageToSend)
    } else {
      await callMockAPI(messageToSend)
    }
  } catch (error) {
    console.error('AI回复失败:', error)
    ElMessage.error('AI回复失败，请重试')
    
    // 如果真实API失败，自动切换到模拟API
    if (useRealAPI.value) {
      ElMessage.warning('真实API调用失败，已切换到模拟模式')
      useRealAPI.value = false
      await callMockAPI(messageToSend)
    }
  } finally {
    isLoading.value = false
  }
}

const callDeepseekAPI = async (userMessage) => {
  try {
    // 构建消息历史
    const messageHistory = messages.value.map(msg => ({
      role: msg.role,
      content: msg.content
    }))
    
    // 调用DeepSeek API
    const response = await deepseekApi.chatCompletion(messageHistory, {
      model: selectedModel.value,
      temperature: temperature.value,
      max_tokens: maxTokens.value
    })
    
    // 处理API响应
    if (response && response.choices && response.choices[0]) {
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.choices[0].message.content,
        timestamp: new Date(),
        model: response.model,
        usage: response.usage
      }
      
      messages.value.push(aiMessage)
      
      // 滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
      
      // 显示token使用情况
      if (response.usage) {
        console.log(`Token使用: 输入${response.usage.prompt_tokens}, 输出${response.usage.completion_tokens}, 总计${response.usage.total_tokens}`)
      }
    } else {
      throw new Error('API响应格式错误')
    }
  } catch (error) {
    console.error('DeepSeek API调用失败:', error)
    throw error
  }
}

const callMockAPI = async (userMessage) => {
  try {
    // 构建消息历史
    const messageHistory = messages.value.map(msg => ({
      role: msg.role,
      content: msg.content
    }))
    
    // 调用模拟API
    const response = await mockDeepseekApi.chatCompletion(messageHistory, {
      model: selectedModel.value,
      temperature: temperature.value,
      max_tokens: maxTokens.value
    })
    
    // 处理API响应
    if (response && response.choices && response.choices[0]) {
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.choices[0].message.content,
        timestamp: new Date(),
        model: response.model,
        usage: response.usage
      }
      
      messages.value.push(aiMessage)
      
      // 滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
    } else {
      throw new Error('模拟API响应格式错误')
    }
  } catch (error) {
    console.error('模拟API调用失败:', error)
    throw error
  }
}

const handleEnterKey = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

const handleShiftEnter = () => {
  // 允许换行
}

const scrollToBottom = () => {
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}

const copyMessage = async (content) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}

const regenerateMessage = (message) => {
  // 找到用户消息
  const userMessageIndex = messages.value.findIndex(m => m.id === message.id) - 1
  if (userMessageIndex >= 0) {
    const userMessage = messages.value[userMessageIndex]
    // 删除当前AI回复
    messages.value.splice(userMessageIndex + 1, 1)
    // 重新生成回复
    inputMessage.value = userMessage.content
    sendMessage()
  }
}

const clearChat = () => {
  ElMessageBox.confirm(
    '确定要清空所有对话记录吗？此操作不可恢复。',
    '确认清空',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    messages.value = []
    ElMessage.success('对话已清空')
  }).catch(() => {
    // 用户取消
  })
}

const exportChat = () => {
  if (messages.value.length === 0) {
    ElMessage.warning('没有对话记录可导出')
    return
  }
  
  const chatContent = messages.value.map(msg => {
    const role = msg.role === 'user' ? '用户' : 'AI助手'
    const time = formatMessageTime(msg.timestamp)
    return `[${time}] ${role}: ${msg.content}`
  }).join('\n\n')
  
  const blob = new Blob([chatContent], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `AI对话记录_${new Date().toISOString().split('T')[0]}.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  
  ElMessage.success('对话记录已导出')
}

const formatMessageTime = (timestamp) => {
  const now = new Date()
  const messageTime = new Date(timestamp)
  const diffInMinutes = Math.floor((now - messageTime) / (1000 * 60))
  
  if (diffInMinutes < 1) return '刚刚'
  if (diffInMinutes < 60) return `${diffInMinutes}分钟前`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}小时前`
  
  return messageTime.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatMessageText = (text) => {
  // 简单的文本格式化，支持换行
  return text.replace(/\n/g, '<br>')
}

// DeepSeek API管理相关方法
const checkAPIStatus = async () => {
  try {
    if (useRealAPI.value) {
      const status = await deepseekApi.checkStatus()
      apiStatus.value = status.status || 'unknown'
    } else {
      const status = await mockDeepseekApi.checkStatus()
      apiStatus.value = status.status || 'available'
    }
  } catch (error) {
    console.error('检查API状态失败:', error)
    apiStatus.value = 'error'
  }
}

const loadAvailableModels = async () => {
  try {
    if (useRealAPI.value) {
      const models = await deepseekApi.getModels()
      availableModels.value = models.data || []
    } else {
      const models = await mockDeepseekApi.getModels()
      availableModels.value = models.data || []
    }
  } catch (error) {
    console.error('获取模型列表失败:', error)
    availableModels.value = []
  }
}

const toggleAPI = () => {
  useRealAPI.value = !useRealAPI.value
  ElMessage.success(`已切换到${useRealAPI.value ? '真实DeepSeek API' : '模拟API'}模式`)
  
  // 重新检查状态和加载模型
  checkAPIStatus()
  loadAvailableModels()
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
  
  // 初始化聊天界面和API状态
  nextTick(() => {
    scrollToBottom()
  })
  
  // 初始化API状态
  checkAPIStatus()
  loadAvailableModels()
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

// 聊天界面样式
.chat-section {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.api-config-panel {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid var(--border-color);
  
  .config-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    
    h4 {
      font-size: 1.1rem;
      font-weight: bold;
      color: var(--text-primary);
      margin: 0;
    }
  }
  
  .config-options {
    .el-form-item {
      margin-bottom: 1rem;
    }
    
    .api-status {
      margin-top: 1rem;
      text-align: center;
    }
  }
  
  .config-info {
    margin-top: 1rem;
  }
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: var(--bg-primary);
  
  .welcome-message {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-secondary);
    
    .welcome-icon {
      margin-bottom: 1rem;
      color: var(--primary-color);
    }
    
    h3 {
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 1rem;
    }
    
    p {
      font-size: 1rem;
      line-height: 1.6;
      margin-bottom: 0.5rem;
    }
  }
  
  .message-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .message-item {
    display: flex;
    gap: 1rem;
    animation: fadeIn 0.3s ease-in;
    
    &.user-message {
      flex-direction: row-reverse;
      
      .message-content {
        align-items: flex-end;
        
        .message-text {
          background: var(--primary-color);
          color: white;
          border-radius: 18px 18px 4px 18px;
        }
      }
    }
    
    &.ai-message {
      .message-content {
        align-items: flex-start;
        
        .message-text {
          background: var(--bg-secondary);
          color: var(--text-primary);
          border-radius: 18px 18px 18px 4px;
        }
      }
    }
    
    .message-avatar {
      flex-shrink: 0;
    }
    
    .message-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      max-width: 70%;
      
      .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        color: var(--text-secondary);
      }
      
      .message-text {
        padding: 0.75rem 1rem;
        line-height: 1.5;
        word-wrap: break-word;
        white-space: pre-wrap;
      }
      
      .message-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
        opacity: 0;
        transition: opacity 0.2s ease;
      }
    }
    
    &:hover .message-actions {
      opacity: 1;
    }
  }
  
  .typing-indicator {
    display: flex;
    gap: 0.25rem;
    padding: 0.75rem 1rem;
    
    span {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-secondary);
      animation: typing 1.4s infinite ease-in-out;
      
      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
    }
  }
}

.chat-input-area {
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
  padding: 1rem;
  
  .input-container {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    
    .message-input {
      flex: 1;
      
      :deep(.el-textarea__inner) {
        border-radius: 20px;
        resize: none;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        line-height: 1.4;
        border: 1px solid var(--border-color);
        transition: all 0.2s ease;
        
        &:focus {
          border-color: var(--primary-color);
          box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
        }
      }
    }
    
    .input-actions {
      .send-button {
        border-radius: 20px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        min-width: 80px;
      }
    }
  }
  
  .quick-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
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
  
  .chat-section {
    height: 60vh;
  }
  
  .api-config-panel {
    padding: 1rem;
    
    .config-header {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    
    .config-options {
      .el-row {
        .el-col {
          margin-bottom: 1rem;
        }
      }
    }
  }
  
  .chat-messages {
    padding: 0.5rem;
    
    .message-item {
      gap: 0.5rem;
      
      .message-content {
        max-width: 85%;
      }
    }
  }
  
  .chat-input-area {
    padding: 0.5rem;
    
    .input-container {
      gap: 0.5rem;
      
      .send-button {
        padding: 0.5rem 1rem;
        min-width: 60px;
      }
    }
    
    .quick-actions {
      gap: 0.5rem;
    }
  }
}
</style>
