# LLM Arena 前端

*dmcnczy 25/8/8*

这是 LLM Arena 项目的前端部分，使用 Vue 3 + Vite + Element Plus 构建。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - Vue.js 官方路由管理器
- **Pinia** - Vue 的状态管理库
- **Element Plus** - 基于 Vue 3 的组件库
- **Axios** - HTTP 客户端
- **SCSS** - CSS 预处理器

## 功能特性

- 🎨 现代化的用户界面设计
- 📱 响应式布局，支持移动端
- 🔐 完整的用户认证系统
- 🎯 路由守卫和权限控制
- 🌙 支持浅色/深色主题
- 📊 数据可视化和管理后台
- 🔄 实时数据更新
- 📝 表单验证和错误处理

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API 接口
│   ├── components/        # 公共组件
│   ├── router/           # 路由配置
│   ├── stores/           # 状态管理
│   ├── styles/           # 全局样式
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── index.html             # HTML 模板
├── package.json           # 项目配置
├── vite.config.js         # Vite 配置
└── README.md             # 项目说明
```

## 快速开始

### 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖

```bash
cd frontend
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000 查看应用。

### 构建生产版本

```bash
npm run build
```

构建文件将生成在 `dist` 目录中。

### 预览构建结果

```bash
npm run preview
```

## 开发指南

### 添加新页面

1. 在 `src/views/` 目录下创建新的 Vue 组件
2. 在 `src/router/index.js` 中添加路由配置
3. 根据需要添加相应的 API 接口

### 添加新组件

1. 在 `src/components/` 目录下创建组件
2. 使用 Element Plus 组件库
3. 遵循 Vue 3 Composition API 规范

### 状态管理

使用 Pinia 进行状态管理：

```javascript
import { defineStore } from 'pinia'

export const useExampleStore = defineStore('example', () => {
  // 状态
  const count = ref(0)
  
  // 计算属性
  const doubleCount = computed(() => count.value * 2)
  
  // 方法
  const increment = () => count.value++
  
  return { count, doubleCount, increment }
})
```

### API 调用

使用 Axios 进行 API 调用：

```javascript
import request from '@/utils/request'

// GET 请求
const getData = () => request.get('/api/data')

// POST 请求
const createData = (data) => request.post('/api/data', data)
```

## 环境变量

创建 `.env` 文件配置环境变量：

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=LLM Arena
```

## 代码规范

### ESLint 配置

项目使用 ESLint 进行代码检查：

```bash
npm run lint
```

### Prettier 格式化

使用 Prettier 进行代码格式化：

```bash
npm run format
```

## 部署

### 构建

```bash
npm run build
```

### 部署到服务器

将 `dist` 目录中的文件部署到 Web 服务器。

### Docker 部署

```dockerfile
FROM nginx:alpine
COPY dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

# Vue 3 快速指南

**Vue** 是一个轻量、高效、易上手的前端框架，核心理念是数据驱动视图与组件化开发。它通过响应式系统自动追踪数据变化，并高效地更新视图，减少了手动 DOM 操作的负担。相比其他框架，Vue 的学习曲线更平缓，模板语法直观，同时支持现代的组合式 API，灵活性和可维护性更强。生态上，Vue 拥有丰富的插件、路由（vue-router）、状态管理（Pinia/Vuex）等工具，能快速构建从小型页面到大型单页应用（SPA）的各类项目。

先前的 [Tuvalon](https://github.com/pkulab409/pkudsa.avalon) 使用的前端**仍是传统的 HTML + CSS**，适用于入门级开发。如果沿用则离开重构 Tuvalon 平台建立 LLM Arena 的初衷，平台仍然无法适应更大规模的访问需求。


## 0. 从 HTML+CSS 转到 Vue

为避免一下子就被`src/`、`components/`这些陌生目录吓到，此处介绍一个“从 HTML+CSS 转到 Vue”的过渡指南。

### 从“平铺文件”到“模块化工程”

#### 传统 HTML+CSS 的开发方式

* 一个 `.html` 文件里，可能会同时写：

  * HTML 结构（`<div>...`）
  * 内联或链接的 CSS 样式
  * `<script>` 里的 JS 脚本
* 项目可能是：

  ```
  index.html
  about.html
  style.css
  script.js
  images/
  ```

#### Vue 工程的核心变化

* **单页应用（SPA）**：用户只加载一次 `index.html`，后续页面切换靠 JavaScript 控制，不会刷新整个页面。
* **组件化**：一个页面被拆成很多**小部件（组件）**，每个组件里同时包含它的结构、样式、逻辑，互不干扰。
* **模块化文件夹结构**：文件不再“平铺”，而是按职责分目录（UI、数据、路由等）。

### Vue 工程文件的“翻译表”

| 传统 HTML+CSS   | Vue 工程里的位置                    | 说明                        |
| ------------- | ----------------------------- | ------------------------- |
| `index.html`  | `public/index.html`           | 入口 HTML 文件（只写最外层骨架）       |
| 多个 `.html` 页面 | `src/pages/` 下的 `.vue` 文件     | 每个 `.vue` 是一个“页面组件”       |
| `style.css`   | `src/styles/` 或组件内 `<style>`  | 样式可以按组件内写，也可放全局           |
| `script.js`   | 组件内 `<script>` 或 `src/utils/` | 功能代码拆分成多个模块               |
| 图片等资源         | `src/assets/` 或 `public/`     | assets 会打包优化，public 会原样保留 |

### 认识 `.vue` 文件：结构不再分散

传统 HTML 里：

```html
<!-- index.html -->
<h1>Hello</h1>
<script>
  alert('Hi')
</script>
<style>
  h1 { color: red; }
</style>
```

Vue 里同一个组件用 `.vue` 文件包起来：

```vue
<template>
  <h1>{{ message }}</h1>
</template>

<script setup>
import { ref } from 'vue'
const message = ref('Hello Vue!')
</script>

<style scoped>
h1 { color: red; }
</style>
```

特点：

* **模板（HTML）**、**逻辑（JS）**、\*\*样式（CSS）\*\*集中在一个文件，方便维护。
* `scoped` 让样式只作用于当前组件，不会污染全局。

---

### 为什么要有那么多目录？

假设做一个网站：主页、用户中心、商品页……

* 在 HTML 时代，可能是：

  ```
  index.html
  user.html
  product.html
  style.css
  script.js
  ```
- 在 Vue 里，我们会：

  * 把不同页面拆到 `pages/` 里，每个页面是一个 `.vue`
  * 把可复用的小按钮、弹窗放到 `components/`
  * 用 `router/` 管理页面切换
  * 用 `store/` 管理全局数据（比如用户信息、购物车）
  * 用 `assets/` 放图片、字体，打包时会自动优化
  * 用 `utils/` 放通用的功能（比如日期格式化）

这样：

1. 文件更有归属感，不怕“script.js 越写越长”。
2. 新人进项目能快速知道“这东西在哪找”。


### 常见的 Vue 概念对照表

| 新名词                | 类比                          | 作用                      |
| ------------------ | --------------------------- | ----------------------- |
| **组件**             | HTML 的一个独立小块（按钮、导航栏）        | 独立封装，可复用                |
| **props**          | HTML 的属性（`<img src="...">`） | 父组件传数据给子组件              |
| **emit**           | HTML 里自定义事件                 | 子组件通知父组件                |
| **ref / reactive** | JS 变量                       | 特殊变量，能让 Vue 监听变化并自动更新界面 |
| **router**         | 多个 HTML 页面之间的链接             | 控制 SPA 中不同页面的切换         |
| **store**          | 全局变量对象                      | 多个组件之间共享数据              |
| **v-model**        | 双向绑定表单                      | 输入框内容 ↔ 变量同步            |
| **生命周期**           | 网页加载/卸载时触发事件                | 在特定时机执行代码               |


## 1. Vue 核心概念

Vue 3 是一个渐进式 JavaScript 框架，用于构建用户界面。几个关键点：

* **响应式**：数据改变，视图自动更新。
* **组件化**：页面由多个可复用组件组成。
* **组合式 API (Composition API)**：Vue 3 推荐的新写法，更灵活。
* **虚拟 DOM**：提升渲染性能。

## 2. Vue 文件结构

Vue 3 组件通常是 `.vue` 文件，分成三部分：

```vue
<template>
  <h1>{{ message }}</h1>
</template>

<script setup>
import { ref } from 'vue'
const message = ref('Hello Vue 3!')
</script>

<style scoped>
h1 { color: blue; }
</style>
```

* **`<template>`**：HTML 模板。
* **`<script setup>`**：逻辑（推荐新语法）。
* **`<style scoped>`**：样式仅作用于当前组件。

## 3. 响应式数据

```vue
<script setup>
import { ref, reactive } from 'vue'

// 基础类型用 ref
const count = ref(0)

// 对象用 reactive
const user = reactive({ name: 'Alice', age: 20 })

function increment() {
  count.value++
}
</script>

<template>
  <p>{{ count }}</p>
  <button @click="increment">+1</button>
  <p>{{ user.name }} - {{ user.age }}</p>
</template>
```

> 注意：`ref` 取值要用 `.value`（模板里可直接用）。

## 4. 事件与绑定

```vue
<template>
  <!-- v-bind 简写 : -->
  <input :value="name" @input="name = $event.target.value">

  <!-- 双向绑定 v-model -->
  <input v-model="name">

  <button @click="sayHi">点击</button>
</template>

<script setup>
import { ref } from 'vue'
const name = ref('')
function sayHi() {
  alert(`Hello, ${name.value}!`)
}
</script>
```

## 5. 条件与循环

```vue
<template>
  <p v-if="loggedIn">欢迎回来</p>
  <p v-else>请先登录</p>

  <ul>
    <li v-for="(item, index) in list" :key="index">
      {{ index }} - {{ item }}
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'
const loggedIn = ref(true)
const list = ref(['苹果', '香蕉', '橘子'])
</script>
```

## 6. 计算属性 & 侦听器

```vue
<script setup>
import { ref, computed, watch } from 'vue'

const first = ref('Vue')
const last = ref('3')
const fullName = computed(() => first.value + ' ' + last.value)

watch(fullName, (newVal, oldVal) => {
  console.log(`名字从 ${oldVal} 改为 ${newVal}`)
})
</script>

<template>
  <p>{{ fullName }}</p>
</template>
```

## 7. 父子组件通信

**父传子（props）**

```vue
<!-- Parent.vue -->
<Child :msg="parentMsg" />

<script setup>
import Child from './Child.vue'
const parentMsg = '来自父组件的问候'
</script>
```

```vue
<!-- Child.vue -->
<script setup>
defineProps({ msg: String })
</script>
<template>
  <p>{{ msg }}</p>
</template>
```

**子传父（emit）**

```vue
<!-- Child.vue -->
<script setup>
const emit = defineEmits(['customEvent'])
function send() {
  emit('customEvent', 'Hello 父组件')
}
</script>
<template>
  <button @click="send">发消息</button>
</template>
```

```vue
<!-- Parent.vue -->
<Child @customEvent="handleMsg" />
<script setup>
function handleMsg(val) {
  console.log(val)
}
</script>
```

## 8. 生命周期钩子

```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  console.log('组件已挂载')
})

onUnmounted(() => {
  console.log('组件已卸载')
})
</script>
```

## 9. 路由与状态管理

* **路由**（vue-router）

```bash
npm install vue-router
```

```js
// router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import About from './pages/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

```js
// main.js
import router from './router'
createApp(App).use(router).mount('#app')
```

```vue
<router-link to="/">首页</router-link>
<router-link to="/about">关于</router-link>
<router-view></router-view>
```

* **状态管理**（Pinia 推荐）

```bash
npm install pinia
```

```js
// store.js
import { defineStore } from 'pinia'
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: { increment() { this.count++ } }
})
```

## 10. 常用指令

| 指令                              | 作用          |
| ------------------------------- | ----------- |
| `v-bind:` / `:`                 | 绑定属性        |
| `v-on:` / `@`                   | 绑定事件        |
| `v-model`                       | 双向绑定        |
| `v-if` / `v-else-if` / `v-else` | 条件渲染        |
| `v-for`                         | 列表渲染        |
| `v-show`                        | 显隐（仅切换 CSS） |


## 11. 官方资源

* [Vue 3 官方文档](https://vuejs.org/)
* [Vue 3 中文文档](https://cn.vuejs.org/)
