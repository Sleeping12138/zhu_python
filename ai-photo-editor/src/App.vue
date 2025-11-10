<template>
  <!-- 登录页面：独立显示，不显示导航栏 -->
  <router-view v-if="$route.meta.isLoginPage" />
  
  <!-- 主应用页面：显示完整布局和导航栏 -->
  <div v-else class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 -left-20 w-96 h-96 bg-gradient-to-br from-indigo-200/20 to-purple-200/20 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 -right-20 w-96 h-96 bg-gradient-to-br from-purple-200/20 to-pink-200/20 rounded-full blur-3xl"></div>
    </div>

    <!-- 头部导航 -->
    <header class="relative bg-white/90 backdrop-blur-xl shadow-xl border-b border-gray-200/60 sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 sm:py-4 md:py-5">
        <div class="flex items-center gap-2 sm:gap-3 md:gap-4">
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl sm:rounded-2xl blur opacity-30 group-hover:opacity-50 transition-opacity"></div>
            <img src="/static/yishou.jpg" alt="一手AI修图平台" class="relative w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 rounded-xl sm:rounded-2xl shadow-lg ring-2 ring-indigo-100/50 transform group-hover:scale-105 transition-transform duration-300" />
            <div class="absolute -top-1 -right-1 w-3 h-3 sm:w-4 sm:h-4 md:w-5 md:h-5 bg-gradient-to-r from-green-400 to-blue-500 rounded-full animate-pulse shadow-lg ring-2 ring-white"></div>
          </div>
          <div>
            <h1 class="text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-gradient">
              一手AI修图平台
            </h1>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="relative container mx-auto px-2 sm:px-4 py-4 sm:py-6 md:py-8 max-w-7xl">
      <!-- 标签页导航 -->
      <nav class="flex gap-1 sm:gap-2 md:gap-3 mb-4 sm:mb-6 md:mb-8 bg-white/60 backdrop-blur-sm rounded-xl sm:rounded-2xl p-1 sm:p-1.5 md:p-2 shadow-lg border border-gray-200/50 overflow-x-auto">
        <router-link
          v-for="tab in tabs"
          :key="tab.key"
          :to="tab.path"
          :class="[
            'relative px-3 py-2 sm:px-4 sm:py-2.5 md:px-6 md:py-3 text-xs sm:text-sm md:text-base font-semibold transition-all duration-300 rounded-lg sm:rounded-xl whitespace-nowrap flex-shrink-0',
            $route.path === tab.path
              ? 'text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg shadow-indigo-500/30 transform scale-105'
              : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
          ]"
        >
          <span class="relative z-10">{{ tab.label }}</span>
          <div v-if="$route.path === tab.path" class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg sm:rounded-xl animate-pulse opacity-75"></div>
        </router-link>
      </nav>

      <!-- 路由内容 -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl sm:rounded-3xl shadow-2xl border border-gray-200/50 p-4 sm:p-6 md:p-8 transform transition-all duration-300 hover:shadow-3xl">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
// 标签页配置
const tabs = [
  { key: 'batch', label: '批量处理', path: '/batch' },
  { key: 'scheduled', label: '定时处理', path: '/scheduled' },
  { key: 'virtual-tryon', label: '虚拟试衣', path: '/virtual-tryon' },
  { key: 'history', label: '历史记录', path: '/history' }
]
</script>

<style scoped>
@keyframes gradient {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}
</style>
