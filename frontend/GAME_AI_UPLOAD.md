# 游戏AI代码上传功能

## 功能概述

这个功能允许用户为不同的游戏上传和管理AI代码。目前支持的游戏包括：

- 石头剪刀布 (rock_paper_scissors)
- 阿瓦隆 (avalon)

## 主要特性

### 1. 游戏类型选择
- 用户可以通过单选按钮选择要管理的游戏类型
- 切换游戏类型时会自动加载对应的AI代码列表

### 2. AI代码上传
- 支持多种编程语言：Python、JavaScript、Java、C++、C
- 支持压缩包格式：ZIP、RAR
- 文件大小限制：10MB
- 必填信息：游戏类型、AI名称、代码文件
- 可选信息：描述

### 3. AI代码管理
- 查看AI代码列表
- 激活/停用AI代码
- 下载AI代码文件
- 编辑AI代码信息
- 删除AI代码

### 4. 文件类型识别
- 根据文件扩展名显示对应的文件类型图标
- 不同编程语言使用不同的颜色标识

## 使用方法

### 上传AI代码
1. 在"游戏AI代码"标签页中选择游戏类型
2. 点击"上传AI代码"按钮
3. 填写AI代码名称和描述（可选）
4. 选择代码文件
5. 点击"上传"按钮

### 管理AI代码
- **激活**：点击"激活"按钮使AI代码生效
- **下载**：点击"下载"按钮下载AI代码文件
- **编辑**：点击"编辑"按钮修改AI代码信息
- **删除**：点击"删除"按钮删除AI代码

## 技术实现

### 前端组件
- `MyAI.vue`：主要的AI管理页面
- 使用Element Plus组件库构建UI
- 响应式设计，支持移动端

### API接口
- `gameAI.js`：游戏AI相关的API调用
- 支持文件上传、下载、CRUD操作

### 文件上传
- 使用FormData处理文件上传
- 支持进度显示和错误处理
- 文件类型和大小验证

## 后端接口要求

### 文件上传
- 接口：`POST /api/v1/files/upload`
- 参数：`file` (UploadFile)
- 认证：需要用户登录

### 游戏AI代码管理
- 获取列表：`GET /api/v1/games/{game_type}/ai-codes`
- 上传代码：`POST /api/v1/games/{game_type}/ai-codes/upload`
- 激活代码：`POST /api/v1/games/ai-codes/{id}/activate`
- 下载代码：`GET /api/v1/games/ai-codes/{id}/download`
- 删除代码：`DELETE /api/v1/games/ai-codes/{id}`

## 数据结构

### AI代码对象
```javascript
{
  id: 1,
  name: "智能石头剪刀布AI",
  description: "基于机器学习的石头剪刀布AI",
  game_type: "rock_paper_scissors",
  version: 1,
  is_active: true,
  created_at: "2024-01-01T10:00:00Z",
  file_size: 1048576,
  file_name: "ai_code.py",
  last_used: "2024-01-02T15:30:00Z"
}
```

## 注意事项

1. 文件上传需要用户认证
2. 文件大小限制为10MB
3. 支持的文件类型有限制
4. 每个游戏类型可以上传多个AI代码
5. 同一时间只能激活一个AI代码

## 未来扩展

- 支持更多游戏类型
- 添加AI代码版本管理
- 支持AI代码测试功能
- 添加AI代码排行榜
- 支持AI代码分享和协作
