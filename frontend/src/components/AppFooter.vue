<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 主要内容区域 -->
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">LLM Arena</h3>
          <p class="footer-description">
            大语言模型竞技场
          </p>
          <div class="social-links">
            <a href="#" class="social-link" title="GitHub">
              <el-icon><Platform /></el-icon>
            </a>
            <a href="#" class="social-link" title="Twitter">
              <el-icon><ChatDotRound /></el-icon>
            </a>
            <a href="#" class="social-link" title="Discord">
              <el-icon><Message /></el-icon>
            </a>
          </div>
        </div>

        <div class="footer-section">
          <h4 class="footer-subtitle">产品</h4>
          <ul class="footer-links">
            <li><router-link to="/arena" class="footer-link">对战大厅</router-link></li>
            <li><router-link to="/my-ai" class="footer-link">我的AI</router-link></li>
            <li><router-link to="/collaboration" class="footer-link">共创</router-link></li>
            <li><router-link to="/about" class="footer-link">关于我们</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="footer-subtitle">支持</h4>
          <ul class="footer-links">
            <li><a href="#" class="footer-link">帮助中心</a></li>
            <li><a href="#" class="footer-link">API文档</a></li>
            <li><a href="#" class="footer-link">联系我们</a></li>
            <li><a href="#" class="footer-link">反馈建议</a></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4 class="footer-subtitle">法律</h4>
          <ul class="footer-links">
            <li><a href="#" class="footer-link">隐私政策</a></li>
            <li><a href="#" class="footer-link">服务条款</a></li>
            <li><a href="#" class="footer-link">Cookie政策</a></li>
            <li><a href="#" class="footer-link">免责声明</a></li>
          </ul>
        </div>
      </div>

      <!-- 底部版权信息 -->
      <div class="footer-bottom">
        <div class="footer-bottom-content">
          <p class="copyright">
            © {{ currentYear }} LLM Arena. 保留所有权利。
          </p>
          <div class="footer-bottom-links">
            <a href="#" class="footer-bottom-link">隐私政策</a>
            <span class="separator">|</span>
            <a href="#" class="footer-bottom-link">服务条款</a>
            <span class="separator">|</span>
            <a href="#" class="footer-bottom-link">Cookie设置</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { Platform, ChatDotRound, Message } from '@element-plus/icons-vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style lang="scss" scoped>
.footer {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  color: #ffffff;
  margin-top: auto;
  padding-top: 3rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-section {
  .footer-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .footer-description {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .footer-subtitle {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #ffffff;
  }

  .footer-links {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      margin-bottom: 0.5rem;
    }

    .footer-link {
      color: rgba(255, 255, 255, 0.8);
      text-decoration: none;
      transition: color 0.3s;

      &:hover {
        color: #667eea;
      }
    }
  }

  .social-links {
    display: flex;
    gap: 1rem;

    .social-link {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      color: rgba(255, 255, 255, 0.8);
      text-decoration: none;
      transition: all 0.3s;

      &:hover {
        background: #667eea;
        color: #ffffff;
        transform: translateY(-2px);
      }

      .el-icon {
        font-size: 1.2rem;
      }
    }
  }
}

.footer-bottom {
  padding: 1.5rem 0;

  .footer-bottom-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .copyright {
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
  }

  .footer-bottom-links {
    display: flex;
    align-items: center;
    gap: 1rem;

    .footer-bottom-link {
      color: rgba(255, 255, 255, 0.6);
      text-decoration: none;
      font-size: 0.9rem;
      transition: color 0.3s;

      &:hover {
        color: #667eea;
      }
    }

    .separator {
      color: rgba(255, 255, 255, 0.3);
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer-bottom {
    .footer-bottom-content {
      flex-direction: column;
      text-align: center;
    }
  }
}

@media (max-width: 480px) {
  .footer {
    padding-top: 2rem;
  }

  .footer-container {
    padding: 0 15px;
  }

  .footer-content {
    gap: 1.5rem;
  }
}
</style>
