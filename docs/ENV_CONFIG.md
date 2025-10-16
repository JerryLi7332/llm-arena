# 环境配置文件说明

## 📁 文件说明

| 文件 | 用途 | 是否提交到 Git |
|------|------|----------------|
| `.env.example` | 配置模板，包含所有可配置项 | ✅ 提交 |
| `.env` | 实际使用的配置文件，包含敏感信息 | ❌ 不提交 |

## 🚀 快速开始

### 1. 创建配置文件

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
