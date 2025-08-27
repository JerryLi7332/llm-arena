// DeepSeek API配置文件

export const DEEPSEEK_CONFIG = {
  // API基础URL
  API_BASE_URL: 'https://api.deepseek.com/v1',
  
  // 默认模型
  DEFAULT_MODEL: 'deepseek-chat',
  
  // 可用模型列表
  AVAILABLE_MODELS: [
    {
      id: 'deepseek-chat',
      name: 'DeepSeek Chat',
      description: '通用对话模型，适合大多数任务',
      max_tokens: 4096,
      cost_per_1k_tokens: 0.001
    },
    {
      id: 'deepseek-coder',
      name: 'DeepSeek Coder',
      description: '专业编程助手，代码生成和调试',
      max_tokens: 8192,
      cost_per_1k_tokens: 0.001
    },
    {
      id: 'deepseek-chat-33b',
      name: 'DeepSeek Chat 33B',
      description: '33B参数大模型，更强的理解能力',
      max_tokens: 16384,
      cost_per_1k_tokens: 0.002
    }
  ],
  
  // 默认参数
  DEFAULT_PARAMS: {
    temperature: 0.7,      // 创造性 (0-2)
    max_tokens: 1000,      // 最大输出长度
    top_p: 1,              // 核采样
    frequency_penalty: 0,  // 频率惩罚
    presence_penalty: 0    // 存在惩罚
  },
  
  // 温度值说明
  TEMPERATURE_EXPLANATIONS: {
    0: '非常确定，回答一致性强',
    0.3: '较为确定，适合事实性回答',
    0.7: '平衡，既有创造性又有准确性',
    1.0: '更有创造性，回答多样化',
    1.5: '高度创造性，适合创意写作',
    2.0: '最大创造性，回答非常多样化'
  },
  
  // 错误消息
  ERROR_MESSAGES: {
    API_KEY_MISSING: 'DeepSeek API密钥未配置',
    API_KEY_INVALID: 'DeepSeek API密钥无效',
    RATE_LIMIT: 'API调用频率超限，请稍后重试',
    QUOTA_EXCEEDED: 'API配额已用完',
    MODEL_NOT_FOUND: '指定的模型不存在',
    INVALID_REQUEST: '请求参数无效',
    SERVER_ERROR: 'DeepSeek服务器错误',
    NETWORK_ERROR: '网络连接错误',
    UNKNOWN_ERROR: '未知错误，请重试'
  },
  
  // 提示词模板
  PROMPT_TEMPLATES: {
    GENERAL: '你是一个有用的AI助手，请帮助用户解决问题。',
    PROGRAMMING: '你是一个专业的编程助手，请帮助用户解决编程问题。',
    WRITING: '你是一个创意写作助手，请帮助用户进行创意写作。',
    TRANSLATION: '你是一个翻译助手，请帮助用户进行语言翻译。',
    ANALYSIS: '你是一个分析助手，请帮助用户分析问题。'
  }
}

// 获取模型信息
export const getModelInfo = (modelId) => {
  return DEEPSEEK_CONFIG.AVAILABLE_MODELS.find(model => model.id === modelId)
}

// 计算预估成本
export const estimateCost = (inputTokens, outputTokens, modelId = 'deepseek-chat') => {
  const model = getModelInfo(modelId)
  if (!model) return 0
  
  const inputCost = (inputTokens / 1000) * model.cost_per_1k_tokens
  const outputCost = (outputTokens / 1000) * model.cost_per_1k_tokens
  
  return inputCost + outputCost
}

// 格式化成本显示
export const formatCost = (cost) => {
  if (cost < 0.001) {
    return `$${(cost * 1000).toFixed(3)} (千分之一美元)`
  } else if (cost < 0.01) {
    return `$${cost.toFixed(4)}`
  } else {
    return `$${cost.toFixed(3)}`
  }
}
