<template>
  <el-avatar
    :size="size"
    :src="avatarUrl"
    :style="avatarStyle"
    @error="handleError"
  >
    <el-icon v-if="!avatarUrl || imageError" :size="iconSize">
      <User />
    </el-icon>
  </el-avatar>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { User } from '@element-plus/icons-vue'

const props = defineProps({
  // 头像URL
  avatar: {
    type: String,
    default: ''
  },
  // 用户名（用于生成默认头像）
  username: {
    type: String,
    default: ''
  },
  // 头像大小
  size: {
    type: [Number, String],
    default: 40
  },
  // 自定义样式
  customStyle: {
    type: Object,
    default: () => ({})
  }
})

const imageError = ref(false)

// 计算头像URL
const avatarUrl = computed(() => {
  if (props.avatar && !imageError.value) {
    // 如果是相对路径，添加基础URL
    if (props.avatar.startsWith('/') || props.avatar.startsWith('./')) {
      return props.avatar
    }
    // 如果是完整URL，直接返回
    if (props.avatar.startsWith('http://') || props.avatar.startsWith('https://')) {
      return props.avatar
    }
    // 如果是文件路径，添加uploads前缀
    if (props.avatar.includes('uploads/')) {
      return `/${props.avatar}`
    }
    return props.avatar
  }
  return null
})

// 计算图标大小
const iconSize = computed(() => {
  const size = typeof props.size === 'number' ? props.size : parseInt(props.size)
  return Math.max(size * 0.6, 16)
})

// 计算头像样式
const avatarStyle = computed(() => {
  const baseStyle = {
    backgroundColor: '#f0f0f0',
    color: '#999',
    ...props.customStyle
  }
  
  // 如果没有头像，使用用户名首字母作为背景色
  if (!props.avatar || imageError.value) {
    const colors = [
      '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57',
      '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'
    ]
    const colorIndex = props.username.charCodeAt(0) % colors.length
    baseStyle.backgroundColor = colors[colorIndex]
    baseStyle.color = '#fff'
  }
  
  return baseStyle
})

// 处理图片加载错误
const handleError = () => {
  imageError.value = true
}

// 重置错误状态
const resetError = () => {
  imageError.value = false
}

// 监听avatar变化，重置错误状态
watch(() => props.avatar, () => {
  if (props.avatar) {
    resetError()
  }
})

// 暴露方法给父组件
defineExpose({
  resetError
})
</script>

<style scoped>
.el-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.el-avatar:hover {
  transform: scale(1.05);
}
</style>
