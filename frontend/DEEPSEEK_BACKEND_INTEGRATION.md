# DeepSeek API后端集成说明

## 概述

为了使用真实的DeepSeek API，需要在后端实现相应的API端点。DeepSeek是一个优秀的开源AI模型提供商，提供类似GPT的性能。

## 获取API密钥

### 1. 注册DeepSeek账户
访问 [DeepSeek官网](https://platform.deepseek.com/) 注册账户

### 2. 获取API密钥
- 登录后进入API管理页面
- 创建新的API密钥
- 复制并保存API密钥（格式类似：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 3. 查看API文档
- 访问 [DeepSeek API文档](https://platform.deepseek.com/api-docs)
- 了解API使用限制和定价

## 必需的API端点

### 1. 聊天完成接口

**端点**: `POST /api/v1/deepseek/chat`

**请求体**:
```json
{
  "messages": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "您好！我是AI助手"},
    {"role": "user", "content": "请介绍一下自己"}
  ],
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": false
}
```

**响应体**:
```json
{
  "id": "chatcmpl-1234567890",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "我是您的AI助手，很高兴为您服务..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

### 2. 获取模型列表接口

**端点**: `GET /api/v1/deepseek/models`

**响应体**:
```json
{
  "data": [
    {
      "id": "deepseek-chat",
      "object": "model",
      "created": 1677610602,
      "owned_by": "deepseek",
      "permission": [],
      "root": "deepseek-chat",
      "parent": null
    }
  ]
}
```

### 3. API状态检查接口

**端点**: `GET /api/v1/deepseek/status`

**响应体**:
```json
{
  "status": "available",
  "message": "API运行正常"
}
```

## 环境变量配置

后端需要配置以下环境变量：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_DEFAULT_MODEL=deepseek-chat

# 可选配置
DEEPSEEK_MAX_TOKENS=4000
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_REQUEST_TIMEOUT=30000
```

## 安全考虑

1. **API密钥保护**: 确保DeepSeek API密钥不会暴露给前端
2. **请求限制**: 实现速率限制和用户配额管理
3. **内容过滤**: 对用户输入和AI输出进行内容安全检查
4. **用户认证**: 确保只有认证用户才能访问API

## 错误处理

实现以下错误处理：

- API密钥无效
- 配额超限
- 速率限制
- 网络错误
- 模型不可用

## 成本控制

1. **Token计数**: 记录每次请求的token使用量
2. **用户配额**: 为每个用户设置月度/日度使用限制
3. **成本监控**: 实时监控API调用成本
4. **自动降级**: 当配额用完时自动切换到模拟模式

## 实现示例

### Python FastAPI示例

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
import httpx
import os
import json

app = FastAPI()
security = HTTPBearer()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

@app.post("/api/v1/deepseek/chat")
async def chat_completion(request: dict, token: str = Depends(security)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DEEPSEEK_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": request.get("model", "deepseek-chat"),
                    "messages": request["messages"],
                    "temperature": request.get("temperature", 0.7),
                    "max_tokens": request.get("max_tokens", 1000)
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/deepseek/models")
async def get_models(token: str = Depends(security)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DEEPSEEK_API_BASE}/models",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/deepseek/status")
async def check_status(token: str = Depends(security)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DEEPSEEK_API_BASE}/models",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                return {"status": "available", "message": "API运行正常"}
            else:
                return {"status": "error", "message": f"API错误: {response.status_code}"}
                
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### Node.js Express示例

```javascript
const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();

// DeepSeek API配置
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_BASE = process.env.DEEPSEEK_API_BASE || 'https://api.deepseek.com/v1';

app.post('/api/v1/deepseek/chat', async (req, res) => {
  try {
    const response = await axios.post(
      `${DEEPSEEK_API_BASE}/chat/completions`,
      {
        model: req.body.model || 'deepseek-chat',
        messages: req.body.messages,
        temperature: req.body.temperature || 0.7,
        max_tokens: req.body.max_tokens || 1000
      },
      {
        headers: {
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000
      }
    );
    
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/v1/deepseek/models', async (req, res) => {
  try {
    const response = await axios.get(
      `${DEEPSEEK_API_BASE}/models`,
      {
        headers: {
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
        },
        timeout: 10000
      }
    );
    
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/v1/deepseek/status', async (req, res) => {
  try {
    await axios.get(
      `${DEEPSEEK_API_BASE}/models`,
      {
        headers: {
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
        },
        timeout: 10000
      }
    );
    
    res.json({ status: 'available', message: 'API运行正常' });
  } catch (error) {
    res.json({ status: 'error', message: error.message });
  }
});
```

## 测试建议

1. **单元测试**: 测试各个API端点的功能
2. **集成测试**: 测试与DeepSeek API的集成
3. **性能测试**: 测试API响应时间和并发处理能力
4. **安全测试**: 测试认证和授权机制

## 部署注意事项

1. **环境隔离**: 确保开发、测试、生产环境分离
2. **监控告警**: 设置API调用失败和成本超限告警
3. **日志记录**: 记录所有API调用日志用于审计
4. **备份策略**: 定期备份配置和用户数据

## DeepSeek API优势

1. **开源友好**: 提供开源模型，支持本地部署
2. **成本效益**: 相比OpenAI，价格更具竞争力
3. **中文支持**: 对中文有很好的理解和生成能力
4. **代码能力**: 在编程任务上表现优秀
5. **响应速度**: API响应速度快，延迟低
