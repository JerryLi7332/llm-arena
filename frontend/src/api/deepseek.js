import request from '@/utils/request'

// DeepSeek API配置
const DEEPSEEK_API_BASE = 'https://api.deepseek.com/v1'
const DEEPSEEK_MODEL = 'deepseek-chat' // 默认模型

// DeepSeek聊天API
export const deepseekApi = {
  // 发送聊天消息
  async chatCompletion(messages, options = {}) {
    try {
      const response = await request({
        url: '/api/v1/deepseek/chat',
        method: 'post',
        data: {
          messages,
          model: options.model || DEEPSEEK_MODEL,
          temperature: options.temperature || 0.7,
          max_tokens: options.max_tokens || 1000,
          stream: options.stream || false
        }
      })
      return response
    } catch (error) {
      console.error('DeepSeek API调用失败:', error)
      throw error
    }
  },

  // 获取可用模型列表
  async getModels() {
    try {
      const response = await request({
        url: '/api/v1/deepseek/models',
        method: 'get'
      })
      return response
    } catch (error) {
      console.error('获取模型列表失败:', error)
      throw error
    }
  },

  // 检查API状态
  async checkStatus() {
    try {
      const response = await request({
        url: '/api/v1/deepseek/status',
        method: 'get'
      })
      return response
    } catch (error) {
      console.error('检查API状态失败:', error)
      throw error
    }
  }
}

// 本地测试用的模拟API（当后端API未就绪时使用）
export const mockDeepseekApi = {
  async chatCompletion(messages, options = {}) {
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
    
    const lastMessage = messages[messages.length - 1]
    const userMessage = lastMessage.content
    
    // 根据用户消息生成更智能的回复
    let response = ''
    
    if (userMessage.includes('你好') || userMessage.includes('hello')) {
      response = '您好！我是您的DeepSeek AI助手，很高兴为您服务。我可以帮助您回答问题、解决问题、进行创意写作等。请告诉我您需要什么帮助？'
    } else if (userMessage.includes('天气') || userMessage.includes('温度')) {
      response = '抱歉，我无法获取实时天气信息。建议您查看天气预报网站或使用天气APP来获取准确的天气信息。'
    } else if (userMessage.includes('时间') || userMessage.includes('几点')) {
      const now = new Date()
      response = `现在是${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}。`
    } else if (userMessage.includes('计算') || userMessage.includes('数学')) {
      response = '我可以帮助您进行基本的数学计算。请告诉我具体的计算问题，我会尽力协助您。'
    } else if (userMessage.includes('编程') || userMessage.includes('代码')) {
      response = '我很乐意帮助您解决编程问题！请详细描述您遇到的问题，我会提供相应的解决方案和代码示例。'
    } else if (userMessage.includes('学习') || userMessage.includes('教育')) {
      response = '学习是一个持续的过程！我建议您：\n\n1. 制定明确的学习目标\n2. 找到适合自己的学习方法\n3. 保持持续的学习习惯\n4. 多实践和应用\n\n有什么具体的学习问题需要帮助吗？'
    } else {
      // 通用回复模板
      const responses = [
        `关于"${userMessage}"，这是一个很好的问题。让我为您详细分析一下...`,
        `我理解您的问题"${userMessage}"。基于我的知识，我建议从以下几个角度来考虑：\n\n1. 首先分析问题的核心\n2. 然后考虑可能的解决方案\n3. 最后评估最佳方案`,
        `您提到的"${userMessage}"确实很重要。这涉及到多个方面，需要综合考虑各种因素。让我为您提供一些见解...`,
        `"${userMessage}"是一个很有趣的话题！我可以从几个角度来为您解答：\n\n• 理论层面\n• 实践应用\n• 注意事项\n• 发展趋势`
      ]
      response = responses[Math.floor(Math.random() * responses.length)]
    }
    
    return {
      id: `chatcmpl-${Date.now()}`,
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: DEEPSEEK_MODEL,
      choices: [
        {
          index: 0,
          message: {
            role: 'assistant',
            content: response
          },
          finish_reason: 'stop'
        }
      ],
      usage: {
        prompt_tokens: userMessage.length,
        completion_tokens: response.length,
        total_tokens: userMessage.length + response.length
      }
    }
  },

  async getModels() {
    return {
      data: [
        {
          id: 'deepseek-chat',
          object: 'model',
          created: 1677610602,
          owned_by: 'deepseek',
          permission: [],
          root: 'deepseek-chat',
          parent: null
        },
        {
          id: 'deepseek-coder',
          object: 'model',
          created: 1687882411,
          owned_by: 'deepseek',
          permission: [],
          root: 'deepseek-coder',
          parent: null
        }
      ]
    }
  },

  async checkStatus() {
    return {
      status: 'available',
      message: '模拟API运行正常'
    }
  }
}
