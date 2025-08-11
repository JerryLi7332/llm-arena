![LLM Arena](docs/images/LLMArena.jpg)

> 🚧 仍在开发中……

# LLM Arena

这是一个**以大语言模型为算法基础的策略游戏对战平台**。

先前，[PKULAB409](https://github.com/pkulab409) 已开发了面向校园网的 LLM 对战平台，实现了用户通过 Python 编程使用大语言模型制作 AI，玩《阿瓦隆》游戏（[pkudsa.avalon](https://github.com/pkulab409/pkudsa.avalon)，简化版 [python.avalon](https://github.com/pkulab409/python.avalon)）。我们计划将该平台重构并推广，建立**更完善更丰富**的以大语言模型为算法基础的策略游戏对战平台——LLM Arena。

在 LLM Arena，用户可以编程调用大语言模型实现策略游戏对战，也能参与社区共创，设计出不一样的策略对战游戏上传至平台。

我们希望通过此种方式普及人工智能知识，加速人工智能应用，同时探索人工智能的未来可能。

---

<div align="center">

**简体中文** | [English](README.en.md)

<!-- 点赞区域 -->
<div align="center">
  <a href="https://github.com/pkulab409/llm-arena" target="_blank">
    <img src="https://img.shields.io/badge/⭐_给个Star-支持项目-FFD700?style=for-the-badge&logo=github&logoColor=white&labelColor=FF6B6B&color=FFD700" alt="给个Star">
  </a>
</div><br>

[📖 快速开始](#-快速开始) • [🏗️ 架构说明](#-基础架构) • [🌐 FastAPI文档](http://fastapi.infyai.cn/) • [🤝 贡献指南](CONTRIBUTING.md) • [🌟 给个Star!](https://github.com/pkulab409/llm-arena)

</div>

---

## 基础架构

### 后端

我们基于 [FastAPI Template](https://github.com/JiayuXu0/FastAPI-Template) 进行后端开发。[该项目采用 MIT 证书](docs/MIT_LICENSE_FastAPI_Backend_Template/LICENSE)。

<div align="center">

#### ✨ FastAPI Template的核心特性
<img src="docs/images/features-overview.svg" alt="核心特性" width="700">

</div>

### 前端

我们基于 **Vue 3 + Vite + Element Plus** 进行前端构建。功能特性如下：

- 🎨 现代化的用户界面设计
- 📱 响应式布局，支持移动端
- 🔐 完整的用户认证系统
- 🎯 路由守卫和权限控制
- 🌙 支持浅色/深色主题
- 📊 数据可视化和管理后台
- 🔄 实时数据更新
- 📝 表单验证和错误处理

### 游戏实现逻辑

目前仍待确认的内容有：

[ ] 游戏中，算力资源的分配方式（我们计划将一定算力需求转移到用户浏览器中）
[ ] 游戏可视化具体方式（平台提供 Python 接口 / 直接使用静态 HTML / 融合前端 Vue）
[ ] 游戏实现逻辑模块化与分工（初步分为游戏开发、游戏运行、可视化实现、数据库对接四个模块）

#### 🎮 游戏开发模块
游戏开发模块是平台的核心创意引擎，负责游戏规则的设计和AI策略的实现。开发者可以：
- 使用Python编写游戏逻辑，定义游戏规则、胜利条件和玩家交互方式
- 集成大语言模型API，实现智能AI决策算法
- 设计游戏状态管理，包括回合制、实时对战等不同模式
- 创建游戏配置文件，定义游戏参数、平衡性设置和难度等级

#### 🚀 游戏运行模块
游戏运行模块负责执行游戏逻辑和协调AI对战过程，主要功能包括：
- 游戏引擎核心，负责游戏状态的计算和更新
- AI对战调度器，管理多个AI玩家的并发执行
- 回合制或实时对战的时间控制机制
- 游戏结果的验证和判定，确保公平性

#### 🎨 可视化实现模块
可视化模块为用户提供直观的游戏体验，支持多种实现方式：
- **Python接口方式**：为游戏开发者提供标准化的可视化接口，支持自定义UI组件
- **静态HTML方式**：轻量级实现，适合简单的游戏展示
- **Vue前端融合**：与平台主界面深度集成，提供统一的用户体验
- 实时游戏状态展示，包括游戏进度、玩家操作、结果反馈等

#### 💾 数据库对接模块
数据库模块负责游戏数据的持久化存储和查询：
- 游戏配置数据的存储和管理
- 对战记录和统计数据的保存
- 用户游戏历史和成就系统
- 排行榜和社区数据的实时更新

#### 🔧 算力资源分配策略
为了优化平台性能和用户体验，我们采用分布式算力分配策略：
- **服务端算力**：负责核心游戏逻辑计算和AI模型推理
- **客户端算力**：将部分计算任务转移到用户浏览器，减轻服务器压力
- **智能负载均衡**：根据游戏复杂度和用户设备性能动态调整算力分配
- **缓存机制**：对重复计算进行缓存，提高响应速度

---

## 许可证

本项目基于 GPL-3.0 开源协议。

---

## 贡献和获取帮助

- 请查阅 [🤝 贡献指南](CONTRIBUTING.md) 对本项目贡献。谢谢！

* 如果您在使用过程中遇到问题，可以：

  - 🔍 查看 Issues 查找类似问题
  - 💬 创建新的 Issue 描述问题
  - 📧 联系维护者
