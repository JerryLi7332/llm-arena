<template>
  <div class="about">
    <AppHeader />
    <div class="container">
      <h1 class="page-title">关于我们</h1>
      <p class="page-subtitle">了解LLM Arena的使命和愿景</p>
      
      <div class="content-sections">
        <!-- 项目介绍 -->
        <section class="intro-section">
          <div class="section-header">
            <h3>项目介绍</h3>
          </div>
          
          <div class="intro-content">
            <div class="intro-text">
              <h4>什么是LLM Arena？</h4>
              <p>LLM Arena是一个开放的大语言模型竞技场平台，旨在为用户提供多种AI模型的对话体验和性能对比。我们相信，通过让用户直接体验不同AI模型的能力，可以帮助大家更好地理解AI技术的发展现状，并选择最适合自己需求的AI助手。</p>
              
              <h4>我们的使命</h4>
              <p>让AI技术更加透明和可访问，通过开放的平台促进AI技术的普及和发展。我们致力于为用户提供公平、客观的AI模型对比体验，同时为开发者提供展示和测试AI模型的平台。</p>
              
              <h4>核心价值</h4>
              <ul>
                <li><strong>开放透明：</strong>所有模型的表现数据都是公开的，用户可以自由查看和比较</li>
                <li><strong>公平竞争：</strong>为所有AI模型提供平等的展示机会</li>
                <li><strong>用户至上：</strong>始终以用户体验为核心，不断优化产品功能</li>
                <li><strong>社区驱动：</strong>重视用户反馈，与社区共同成长</li>
              </ul>
            </div>
            
            <div class="intro-image">
              <img src="https://via.placeholder.com/400x300/4F46E5/FFFFFF?text=LLM+Arena" alt="LLM Arena" />
            </div>
          </div>
        </section>
        
        <!-- 技术栈 -->
        <section class="tech-section">
          <div class="section-header">
            <h3>技术栈</h3>
          </div>
          
          <div class="tech-grid">
            <div class="tech-card">
              <div class="tech-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <h4>前端技术</h4>
              <ul>
                <li>Vue.js 3 - 现代化的前端框架</li>
                <li>Element Plus - 企业级UI组件库</li>
                <li>Vite - 快速的构建工具</li>
                <li>SCSS - 强大的CSS预处理器</li>
              </ul>
            </div>
            
            <div class="tech-card">
              <div class="tech-icon">
                <el-icon><Platform /></el-icon>
              </div>
              <h4>后端技术</h4>
              <ul>
                <li>FastAPI - 高性能的Python Web框架</li>
                <li>SQLAlchemy - 强大的ORM框架</li>
                <li>PostgreSQL - 可靠的关系型数据库</li>
                <li>Redis - 高性能的缓存数据库</li>
              </ul>
            </div>
            
            <div class="tech-card">
              <div class="tech-icon">
                <el-icon><DataAnalysis /></el-icon>
              </div>
              <h4>AI集成</h4>
              <ul>
                <li>OpenAI API - GPT系列模型</li>
                <li>Anthropic API - Claude系列模型</li>
                <li>Google AI - Gemini系列模型</li>
                <li>开源模型 - Llama、Mistral等</li>
              </ul>
            </div>
          </div>
        </section>
        
        <!-- 团队介绍 -->
        <section class="team-section">
          <div class="section-header">
            <h3>核心团队</h3>
          </div>
          
          <div class="team-grid">
            <div class="team-member">
              <el-avatar :size="80" src="https://via.placeholder.com/80x80/4F46E5/FFFFFF?text=张" />
              <h4>？</h4>
              <p class="role">项目负责人</p>
              <p class="description">description</p>
            </div>
            
            <div class="team-member">
              <el-avatar :size="80" src="https://via.placeholder.com/80x80/10B981/FFFFFF?text=李" />
              <h4>？</h4>
              <p class="role">前端工程师</p>
              <p class="description">description</p>
            </div>
            
            <div class="team-member">
              <el-avatar :size="80" src="https://via.placeholder.com/80x80/F59E0B/FFFFFF?text=王" />
              <h4>？</h4>
              <p class="role">后端工程师</p>
              <p class="description">description</p>
            </div>
            
            <div class="team-member">
              <el-avatar :size="80" src="https://via.placeholder.com/80x80/EF4444/FFFFFF?text=陈" />
              <h4>？</h4>
              <p class="role">AI工程师</p>
              <p class="description">description</p>
            </div>
          </div>
        </section>
        
        <!-- 联系我们 -->
        <section class="contact-section">
          <div class="section-header">
            <h3>联系我们</h3>
          </div>
          
          <div class="contact-content">
            <div class="contact-info">
              <div class="contact-item">
                <el-icon><Message /></el-icon>
                <div>
                  <h4>邮箱</h4>
                  <p>？</p>
                </div>
              </div>
              
              <div class="contact-item">
                <el-icon><Link /></el-icon>
                <div>
                  <h4>GitHub</h4>
                  <p>github.com/pkulab409/llm-arena</p>
                </div>
              </div>
              
              <div class="contact-item">
                <el-icon><ChatDotRound /></el-icon>
                <div>
                  <h4>Discord</h4>
                  <p>？</p>
                </div>
              </div>
              
              <div class="contact-item">
                <el-icon><Document /></el-icon>
                <div>
                  <h4>文档</h4>
                  <p>？</p>
                </div>
              </div>
            </div>
            
            <div class="contact-form">
              <h4>发送消息</h4>
              <el-form :model="contactForm" label-width="80px">
                <el-form-item label="姓名">
                  <el-input v-model="contactForm.name" placeholder="请输入您的姓名" />
                </el-form-item>
                <el-form-item label="邮箱">
                  <el-input v-model="contactForm.email" placeholder="请输入您的邮箱" />
                </el-form-item>
                <el-form-item label="主题">
                  <el-input v-model="contactForm.subject" placeholder="请输入消息主题" />
                </el-form-item>
                <el-form-item label="消息">
                  <el-input
                    v-model="contactForm.message"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入您的消息内容"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="sendMessage">发送消息</el-button>
                </el-form-item>
              </el-form>
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
import { Monitor, Platform, DataAnalysis, Message, Link, ChatDotRound, Document } from '@element-plus/icons-vue'
import AppHeader from '@/components/AppHeader.vue'

const contactForm = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const sendMessage = () => {
  if (!contactForm.value.name || !contactForm.value.email || !contactForm.value.message) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  ElMessage.success('消息发送成功！我们会尽快回复您。')
  contactForm.value = {
    name: '',
    email: '',
    subject: '',
    message: ''
  }
}
</script>

<style lang="scss" scoped>
.about {
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

.intro-section,
.tech-section,
.team-section,
.contact-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.section-header {
  margin-bottom: 2rem;
  
  h3 {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-primary);
  }
}

.intro-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: start;
  
  .intro-text {
    h4 {
      font-size: 1.3rem;
      font-weight: bold;
      color: var(--text-primary);
      margin-bottom: 1rem;
      margin-top: 2rem;
      
      &:first-child {
        margin-top: 0;
      }
    }
    
    p {
      color: var(--text-secondary);
      line-height: 1.8;
      margin-bottom: 1.5rem;
    }
    
    ul {
      color: var(--text-secondary);
      line-height: 1.8;
      
      li {
        margin-bottom: 0.5rem;
      }
    }
  }
  
  .intro-image {
    img {
      width: 100%;
      border-radius: 12px;
    }
  }
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.tech-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  
  .tech-icon {
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 1rem;
  }
  
  h4 {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 1rem;
  }
  
  ul {
    color: var(--text-secondary);
    line-height: 1.8;
    
    li {
      margin-bottom: 0.5rem;
    }
  }
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.team-member {
  text-align: center;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  
  h4 {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--text-primary);
    margin: 1rem 0 0.5rem;
  }
  
  .role {
    color: var(--primary-color);
    font-weight: 500;
    margin-bottom: 1rem;
  }
  
  .description {
    color: var(--text-secondary);
    line-height: 1.6;
  }
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  
  .el-icon {
    font-size: 1.5rem;
    color: var(--primary-color);
  }
  
  h4 {
    font-size: 1rem;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 0.9rem;
  }
}

.contact-form {
  h4 {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .intro-content {
    grid-template-columns: 1fr;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
  }
  
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .contact-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style>
