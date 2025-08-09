<template>
  <div class="collaboration">
    <AppHeader />
    <div class="container">
      <h1 class="page-title">共创</h1>
      <p class="page-subtitle">与社区一起创造更好的AI体验</p>
      
      <div class="content-sections">
        <!-- 项目展示区域 -->
        <section class="projects-section">
          <div class="section-header">
            <h3>热门项目</h3>
            <el-button type="primary" @click="createProject">
              <el-icon><Plus /></el-icon>
              创建项目
            </el-button>
          </div>
          
          <div class="projects-grid">
            <div class="project-card" v-for="project in projects" :key="project.id">
              <div class="project-header">
                <div class="project-avatar">
                  <el-avatar :size="50" :src="project.avatar" />
                </div>
                <div class="project-info">
                  <h4>{{ project.name }}</h4>
                  <p>{{ project.description }}</p>
                  <div class="project-tags">
                    <el-tag v-for="tag in project.tags" :key="tag" size="small">{{ tag }}</el-tag>
                  </div>
                </div>
              </div>
              <div class="project-stats">
                <span>贡献者: {{ project.contributors }}</span>
                <span>星标: {{ project.stars }}</span>
                <span>更新: {{ project.lastUpdate }}</span>
              </div>
              <div class="project-actions">
                <el-button size="small" @click="viewProject(project)">查看详情</el-button>
                <el-button size="small" type="primary" @click="contributeProject(project)">参与贡献</el-button>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 讨论区域 -->
        <section class="discussions-section">
          <div class="section-header">
            <h3>社区讨论</h3>
            <el-button type="primary" @click="createDiscussion">
              <el-icon><ChatDotRound /></el-icon>
              发起讨论
            </el-button>
          </div>
          
          <div class="discussions-list">
            <div class="discussion-item" v-for="discussion in discussions" :key="discussion.id">
              <div class="discussion-avatar">
                <el-avatar :size="40" :src="discussion.author.avatar" />
              </div>
              <div class="discussion-content">
                <div class="discussion-header">
                  <h4>{{ discussion.title }}</h4>
                  <span class="discussion-author">{{ discussion.author.name }}</span>
                </div>
                <p>{{ discussion.excerpt }}</p>
                <div class="discussion-meta">
                  <span>{{ discussion.replies }} 回复</span>
                  <span>{{ discussion.views }} 浏览</span>
                  <span>{{ discussion.createdAt }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 贡献指南 -->
        <section class="contribution-guide">
          <div class="section-header">
            <h3>贡献指南</h3>
          </div>
          
          <div class="guide-content">
            <div class="guide-item">
              <div class="guide-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="guide-text">
                <h4>代码贡献</h4>
                <p>通过GitHub提交Pull Request来贡献代码，我们欢迎任何形式的改进建议。</p>
              </div>
            </div>
            
            <div class="guide-item">
              <div class="guide-icon">
                <el-icon><ChatDotRound /></el-icon>
              </div>
              <div class="guide-text">
                <h4>问题反馈</h4>
                <p>在GitHub Issues中报告bug或提出新功能建议，帮助我们改进产品。</p>
              </div>
            </div>
            
            <div class="guide-item">
              <div class="guide-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="guide-text">
                <h4>文档贡献</h4>
                <p>帮助完善文档，包括API文档、使用教程和最佳实践指南。</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, ChatDotRound, Document } from '@element-plus/icons-vue'
import AppHeader from '@/components/AppHeader.vue'

const projects = ref([
  {
    id: 1,
    name: 'AI对话增强插件',
    description: '为LLM Arena添加更多对话功能和自定义选项',
    avatar: 'https://via.placeholder.com/50x50/4F46E5/FFFFFF?text=AI',
    tags: ['Vue.js', 'AI', '插件'],
    contributors: 12,
    stars: 45,
    lastUpdate: '2天前'
  },
  {
    id: 2,
    name: '多语言支持',
    description: '为平台添加多语言支持，让更多用户能够使用',
    avatar: 'https://via.placeholder.com/50x50/10B981/FFFFFF?text=多语言',
    tags: ['国际化', '翻译'],
    contributors: 8,
    stars: 32,
    lastUpdate: '1周前'
  },
  {
    id: 3,
    name: '移动端适配',
    description: '优化移动端体验，让用户随时随地使用AI对话',
    avatar: 'https://via.placeholder.com/50x50/F59E0B/FFFFFF?text=移动端',
    tags: ['响应式', '移动端'],
    contributors: 15,
    stars: 67,
    lastUpdate: '3天前'
  }
])

const discussions = ref([
  {
    id: 1,
    title: '如何优化AI对话的响应速度？',
    excerpt: '最近在使用过程中发现某些模型的响应比较慢，大家有什么优化建议吗？',
    author: {
      name: '开发者小王',
      avatar: 'https://via.placeholder.com/40x40/4F46E5/FFFFFF?text=王'
    },
    replies: 8,
    views: 156,
    createdAt: '2小时前'
  },
  {
    id: 2,
    title: '建议添加更多AI模型支持',
    excerpt: '目前支持的模型种类还比较少，建议增加更多开源和商业模型的选择。',
    author: {
      name: 'AI爱好者',
      avatar: 'https://via.placeholder.com/40x40/10B981/FFFFFF?text=AI'
    },
    replies: 12,
    views: 234,
    createdAt: '1天前'
  },
  {
    id: 3,
    title: '关于用户界面的改进建议',
    excerpt: '当前的界面设计还可以进一步优化，提供更好的用户体验。',
    author: {
      name: 'UI设计师',
      avatar: 'https://via.placeholder.com/40x40/F59E0B/FFFFFF?text=UI'
    },
    replies: 5,
    views: 89,
    createdAt: '3天前'
  }
])

const createProject = () => {
  ElMessage.info('创建项目功能开发中...')
}

const viewProject = (project) => {
  ElMessage.info(`查看项目: ${project.name}`)
}

const contributeProject = (project) => {
  ElMessage.info(`参与贡献: ${project.name}`)
}

const createDiscussion = () => {
  ElMessage.info('发起讨论功能开发中...')
}
</script>

<style lang="scss" scoped>
.collaboration {
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

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.projects-section,
.discussions-section,
.contribution-guide {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  
  .project-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    
    .project-info {
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
        margin-bottom: 0.5rem;
      }
      
      .project-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
      }
    }
  }
  
  .project-stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }
  
  .project-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.discussions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.discussion-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  
  .discussion-content {
    flex: 1;
    
    .discussion-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
      
      h4 {
        font-size: 1.1rem;
        font-weight: bold;
        color: var(--text-primary);
      }
      
      .discussion-author {
        font-size: 0.9rem;
        color: var(--text-secondary);
      }
    }
    
    p {
      color: var(--text-secondary);
      margin-bottom: 0.5rem;
    }
    
    .discussion-meta {
      display: flex;
      gap: 1rem;
      font-size: 0.8rem;
      color: var(--text-secondary);
    }
  }
}

.guide-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.guide-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  
  .guide-icon {
    font-size: 2rem;
    color: var(--primary-color);
  }
  
  .guide-text {
    flex: 1;
    
    h4 {
      font-size: 1.2rem;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 0.5rem;
    }
    
    p {
      color: var(--text-secondary);
      line-height: 1.6;
    }
  }
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
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .guide-content {
    grid-template-columns: 1fr;
  }
}
</style>
