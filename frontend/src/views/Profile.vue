<template>
  <Layout>
    <div class="profile-page">
      <div class="profile-container">
        <div class="profile-header">
        <h1>个人资料</h1>
        <p>管理您的账户信息和设置</p>
      </div>

      <div class="profile-content">
        <!-- 基本信息 -->
        <div class="profile-section">
          <h3>基本信息</h3>
          <el-form
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" />
            </el-form-item>
            
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="profileForm.nickname" />
            </el-form-item>
            
            <el-form-item label="头像">
              <div class="avatar-section">
                <el-upload
                  class="avatar-uploader"
                  :show-file-list="false"
                  :before-upload="beforeAvatarUpload"
                  :http-request="handleAvatarUpload"
                  :disabled="uploading"
                >
                  <UserAvatar
                    v-if="profileForm.avatar"
                    :avatar="profileForm.avatar"
                    :username="profileForm.username"
                    :size="100"
                    class="avatar-preview"
                    ref="avatarRef"
                  />
                  <div v-else class="avatar-placeholder">
                    <el-icon class="avatar-uploader-icon"><Plus /></el-icon>
                    <span class="upload-text">点击上传头像</span>
                  </div>
                </el-upload>
                
                <div v-if="profileForm.avatar" class="avatar-actions">
                  <el-button 
                    size="small" 
                    type="danger" 
                    @click="deleteAvatar"
                    :loading="deleting"
                  >
                    删除头像
                  </el-button>
                </div>
                
                <div class="avatar-tips">
                  <p>支持 JPG、PNG、GIF、WebP 格式</p>
                  <p>文件大小不超过 2MB</p>
                </div>
              </div>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="updateProfile" :loading="userStore.loading">
                保存更改
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 修改密码 -->
        <div class="profile-section">
          <h3>修改密码</h3>
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
          >
            <el-form-item label="当前密码" prop="currentPassword">
              <el-input
                v-model="passwordForm.currentPassword"
                type="password"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                show-password
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="changePassword" :loading="loading">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 偏好设置 -->
        <div class="profile-section">
          <h3>偏好设置</h3>
          <el-form label-width="100px">
            <el-form-item label="主题">
              <el-radio-group v-model="preferences.theme">
                <el-radio label="light">浅色主题</el-radio>
                <el-radio label="dark">深色主题</el-radio>
                <el-radio label="auto">跟随系统</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="语言">
              <el-select v-model="preferences.language">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="通知">
              <el-switch
                v-model="preferences.notifications"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="savePreferences">
                保存设置
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 账户信息 -->
        <div class="profile-section">
          <h3>账户信息</h3>
          <div class="account-info">
            <div class="info-item">
              <span class="label">注册时间：</span>
              <span class="value">{{ userStore.user?.created_at || '未知' }}</span>
            </div>
            <div class="info-item">
              <span class="label">最后登录：</span>
              <span class="value">{{ userStore.user?.last_login || '未知' }}</span>
            </div>
            <div class="info-item">
              <span class="label">用户角色：</span>
              <span class="value">{{ userStore.isAdmin ? '管理员' : '普通用户' }}</span>
            </div>
            <div class="info-item">
              <span class="label">账户状态：</span>
              <span class="value status-active">正常</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </Layout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import Layout from '@/components/Layout.vue'
import UserAvatar from '@/components/UserAvatar.vue'

const userStore = useUserStore()
const profileFormRef = ref()
const passwordFormRef = ref()
const avatarRef = ref()
const loading = ref(false)
const uploading = ref(false)
const deleting = ref(false)

const profileForm = reactive({
  username: '',
  email: '',
  nickname: '',
  avatar: ''
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const preferences = reactive({
  theme: 'light',
  language: 'zh-CN',
  notifications: true
})

const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于 8 个字符', trigger: 'blur' },
    { 
      pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, 
      message: '密码必须包含字母和数字', 
      trigger: 'blur' 
    }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

onMounted(() => {
  // 初始化表单数据
  if (userStore.user) {
    profileForm.username = userStore.user.username || ''
    profileForm.email = userStore.user.email || ''
    profileForm.nickname = userStore.user.nickname || ''
    profileForm.avatar = userStore.user.avatar || ''
  }
})

const updateProfile = async () => {
  if (!profileFormRef.value) return

  try {
    await profileFormRef.value.validate()
    
    const result = await userStore.updateProfile({
      username: profileForm.username,
      email: profileForm.email,
      nickname: profileForm.nickname,
      avatar: profileForm.avatar
    })

    if (result.success) {
      ElMessage.success('个人资料更新成功')
    } else {
      ElMessage.error(result.message || '更新失败')
    }
  } catch (error) {
    console.error('更新个人资料错误:', error)
  }
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    loading.value = true
    
    // 调用修改密码的API
    const passwordData = {
      old_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    }
    
    const response = await authApi.changePassword(passwordData)
    
    if (response.data && response.data.success) {
      ElMessage.success('密码修改成功')
      
      // 清空表单
      passwordForm.currentPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      
      // 重置表单验证状态
      passwordFormRef.value.resetFields()
    } else {
      ElMessage.error(response.data?.msg || '密码修改失败')
    }
  } catch (error) {
    console.error('修改密码错误:', error)
    
    // 处理API错误
    if (error.response && error.response.data) {
      const errorMsg = error.response.data.detail || error.response.data.msg || '密码修改失败'
      ElMessage.error(errorMsg)
    } else {
      ElMessage.error('密码修改失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const savePreferences = () => {
  // 保存偏好设置
  localStorage.setItem('theme', preferences.theme)
  localStorage.setItem('language', preferences.language)
  localStorage.setItem('notifications', preferences.notifications)
  
  ElMessage.success('设置保存成功')
}

const beforeAvatarUpload = (file) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  const isAllowedType = allowedTypes.includes(file.type)
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isAllowedType) {
    ElMessage.error('头像只能是 JPG、PNG、GIF、WebP 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

const handleAvatarUpload = async (options) => {
  const file = options.file
  uploading.value = true
  
  try {
    const result = await userStore.uploadAvatar(file)
    if (result.success) {
      // 更新表单中的头像URL
      profileForm.avatar = result.data.avatar_url
      
      // 重置头像组件的错误状态
      if (avatarRef.value) {
        avatarRef.value.resetError()
      }
      
      ElMessage.success('头像上传成功')
    } else {
      ElMessage.error(result.message || '头像上传失败')
    }
  } catch (error) {
    console.error('头像上传错误:', error)
    ElMessage.error('头像上传失败，请稍后重试')
  } finally {
    uploading.value = false
  }
}

const deleteAvatar = async () => {
  try {
    await ElMessageBox.confirm('确定要删除当前头像吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    deleting.value = true
    const result = await userStore.deleteAvatar()
    
    if (result.success) {
      profileForm.avatar = ''
      ElMessage.success('头像删除成功')
    } else {
      ElMessage.error(result.message || '头像删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('头像删除错误:', error)
      ElMessage.error('头像删除失败')
    }
  } finally {
    deleting.value = false
  }
}
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  padding: 20px;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  text-align: center;
  margin-bottom: 32px;

  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 8px;
    color: var(--text-primary);
  }

  p {
    color: var(--text-secondary);
  }
}

.profile-content {
  .profile-section {
    background: var(--bg-primary);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    h3 {
      font-size: 1.25rem;
      font-weight: bold;
      margin-bottom: 20px;
      color: var(--text-primary);
    }

    .avatar-section {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;

      .avatar-uploader {
        .avatar-preview {
          cursor: pointer;
          transition: all 0.3s ease;
          
          &:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          }
        }

        .avatar-placeholder {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          width: 100px;
          height: 100px;
          border: 2px dashed #d9d9d9;
          border-radius: 50%;
          cursor: pointer;
          transition: all 0.3s ease;
          background-color: #fafafa;

          &:hover {
            border-color: var(--primary-color);
            background-color: #f0f9ff;
          }

          .avatar-uploader-icon {
            font-size: 28px;
            color: #8c939d;
            margin-bottom: 4px;
          }

          .upload-text {
            font-size: 12px;
            color: #8c939d;
          }
        }
      }

      .avatar-actions {
        display: flex;
        gap: 8px;
      }

      .avatar-tips {
        p {
          margin: 0;
          font-size: 12px;
          color: #8c939d;
          line-height: 1.4;
        }
      }
    }

    .account-info {
      .info-item {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid var(--border-color);

        &:last-child {
          border-bottom: none;
        }

        .label {
          font-weight: 500;
          color: var(--text-primary);
        }

        .value {
          color: var(--text-secondary);

          &.status-active {
            color: var(--success-color);
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .profile-page {
    padding: 10px;
  }

  .profile-header h1 {
    font-size: 1.5rem;
  }

  .profile-content .profile-section {
    padding: 16px;
  }
}
</style>
