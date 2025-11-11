<template>
  <div class="space-y-4 sm:space-y-6 md:space-y-8">

    <!-- 页面标题 -->
    <div class="text-center mb-4 sm:mb-6 md:mb-8">
      <div class="inline-flex items-center gap-2 sm:gap-3 mb-2 sm:mb-3">
        <div class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl sm:rounded-2xl flex items-center justify-center shadow-lg">
          <HistoryIcon class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-white" />
        </div>
        <h2 class="text-xl sm:text-2xl md:text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          历史记录
        </h2>
      </div>
      <p class="text-gray-600 text-sm sm:text-base md:text-lg">查看所有处理任务的历史记录和结果</p>
    </div>


    <!-- 没有历史记录 -->
    <div v-if="!hasHistory" class="text-center py-8 sm:py-12 md:py-16 bg-gradient-to-r from-gray-50 to-gray-100 rounded-2xl sm:rounded-3xl border border-gray-200/50">
      <div class="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6">
        <HistoryIcon class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 text-gray-400" />
      </div>
      <h3 class="text-lg sm:text-xl font-semibold text-gray-600 mb-2">暂无历史记录</h3>
      <p class="text-sm sm:text-base text-gray-500">开始处理图片后，历史记录将显示在这里</p>
    </div>


    <!-- 有历史记录 -->
    <div v-else class="space-y-4 sm:space-y-6">
      <div
        v-for="batch in groupedHistory"
        :key="batch.batchId"
        class="bg-white border border-gray-200 rounded-xl p-3 sm:p-4 md:p-6 shadow-lg"
      >
        <!-- 批次头部信息 -->
        <div class="flex flex-col sm:flex-row justify-between items-start gap-3 sm:gap-0 mb-4 sm:mb-6">
          <div class="flex items-center gap-2 sm:gap-3">
            <div class="w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 rounded-lg sm:rounded-xl flex items-center justify-center" :class="getBatchStatusBgClass(batch.status)">
              <component :is="getStatusIcon(batch.status)" class="w-4 h-4 sm:w-4.5 sm:h-4.5 md:w-5 md:h-5" :class="getStatusIconClass(batch.status)" />
            </div>
            <div>
              <h3 class="text-base sm:text-lg md:text-xl font-bold text-gray-800 mb-1">
                {{ batch.taskSource === 'batch' ? '批量处理' : '定时处理' }}
                <span class="text-xs sm:text-sm font-normal text-gray-500 ml-1 sm:ml-2">({{ batch.tasks.length }} 个任务)</span>
              </h3>
              <div class="space-y-1">
                <p class="text-xs sm:text-sm text-gray-600 flex items-center gap-1 sm:gap-2">
                  <Calendar class="w-3 h-3 sm:w-4 sm:h-4" />
                  <span class="hidden sm:inline">创建时间: </span><span class="font-bold text-gray-800">{{ format(batch.createdAt, 'yyyy-MM-dd HH:mm:ss') }}</span>
                </p>
                <p v-if="batch.completedAt" class="text-xs sm:text-sm text-gray-600 flex items-center gap-1 sm:gap-2">
                  <CheckCircle class="w-3 h-3 sm:w-4 sm:h-4" />
                  <span class="hidden sm:inline">完成时间: </span><span class="font-bold text-gray-800">{{ format(batch.completedAt, 'yyyy-MM-dd HH:mm:ss') }}</span>
                </p>
              </div>
            </div>
          </div>
          <span :class="[
            'px-2 py-1 sm:px-3 sm:py-1.5 md:px-4 md:py-2 rounded-full text-xs sm:text-sm font-semibold',
            getStatusBadgeClass(batch.status)
          ]">
            {{ getStatusText(batch.status) }}
          </span>
        </div>

        <!-- 批次统计信息 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 md:gap-4 mb-4 sm:mb-6">
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-2 sm:p-3 md:p-4 border border-blue-200/50">
            <p class="text-xs sm:text-sm font-semibold text-gray-600 mb-1 sm:mb-2 flex items-center gap-1">
              <Image class="w-3 h-3 sm:w-4 sm:h-4" />
              总源图片
            </p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-blue-600">{{ batch.totalSourceCount }}</p>
          </div>
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-2 sm:p-3 md:p-4 border border-green-200/50">
            <p class="text-xs sm:text-sm font-semibold text-gray-600 mb-1 sm:mb-2 flex items-center gap-1">
              <CheckCircle class="w-3 h-3 sm:w-4 sm:h-4" />
              成功处理
            </p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-green-600">{{ batch.totalSuccessCount }}</p>
          </div>
          <div class="bg-gradient-to-r from-red-50 to-pink-50 rounded-lg p-2 sm:p-3 md:p-4 border border-red-200/50">
            <p class="text-xs sm:text-sm font-semibold text-gray-600 mb-1 sm:mb-2 flex items-center gap-1">
              <XCircle class="w-3 h-3 sm:w-4 sm:h-4" />
              失败处理
            </p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-red-600">{{ batch.totalFailedCount }}</p>
          </div>
          <div class="bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg p-2 sm:p-3 md:p-4 border border-purple-200/50">
            <p class="text-xs sm:text-sm font-semibold text-gray-600 mb-1 sm:mb-2 flex items-center gap-1">
              <Settings class="w-3 h-3 sm:w-4 sm:h-4" />
              处理进度
            </p>
            <p class="text-lg sm:text-xl md:text-2xl font-bold text-purple-600">{{ batch.progressPercentage }}%</p>
          </div>
        </div>

        <!-- 源图片 -->
        <div v-if="batch.sourceImages && batch.sourceImages.length > 0" class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-6 h-6 bg-blue-500 rounded flex items-center justify-center">
              <Image class="w-4 h-4 text-white" />
            </div>
            <p class="text-sm font-semibold text-gray-800">源图片 ({{ batch.sourceImages.length }} 张)</p>
          </div>
          <div class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-1">
            <div
              v-for="(sourceImage, idx) in batch.sourceImages"
              :key="idx"
              class="border border-blue-200 rounded-lg overflow-hidden bg-gray-50 cursor-pointer sm:cursor-default"
              @click="openPhotoSwipe(batch.sourceImages, idx)"
            >
              <div class="aspect-square">
                <img 
                  :src="sourceImage" 
                  :alt="`source-${idx}`" 
                  class="w-full h-full object-contain" 
                />
              </div>
              <div class="p-1 bg-gradient-to-r from-blue-50 to-indigo-50 text-center">
                <p class="text-xs font-semibold text-blue-800">#{{ idx + 1 }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 模特图片 -->
        <div v-if="batch.modelImagePreview" class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-6 h-6 bg-purple-500 rounded flex items-center justify-center">
              <User class="w-4 h-4 text-white" />
            </div>
            <p class="text-sm font-semibold text-gray-800">模特图片</p>
          </div>
          <div 
            class="w-32 h-32 border-2 border-purple-200 rounded-lg overflow-hidden cursor-pointer sm:cursor-default"
            @click="openPhotoSwipe([batch.modelImagePreview], 0)"
          >
            <img :src="batch.modelImagePreview" alt="model" class="w-full h-full object-contain bg-gray-50" />
          </div>
        </div>

        <!-- 处理步骤 -->
        <div v-if="batch.processSteps" class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
              <Settings class="w-4 h-4 text-white" />
            </div>
            <p class="text-sm font-semibold text-gray-800">处理步骤</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <span v-if="batch.processSteps.watermark" class="px-3 py-1 bg-gradient-to-r from-blue-100 to-blue-200 text-blue-800 rounded-full text-xs font-semibold">
              去水印
            </span>
            <span v-if="batch.processSteps.faceSwap" class="px-3 py-1 bg-gradient-to-r from-purple-100 to-purple-200 text-purple-800 rounded-full text-xs font-semibold">
              换脸
            </span>
            <span v-if="batch.processSteps.backgroundSwap" class="px-3 py-1 bg-gradient-to-r from-green-100 to-green-200 text-green-800 rounded-full text-xs font-semibold">
              换背景
            </span>
            <span v-if="batch.processSteps.poseSwap" class="px-3 py-1 bg-gradient-to-r from-yellow-100 to-yellow-200 text-yellow-800 rounded-full text-xs font-semibold">
              换姿态
            </span>
            <span v-if="batch.processSteps.superResolution" class="px-3 py-1 bg-gradient-to-r from-indigo-100 to-indigo-200 text-indigo-800 rounded-full text-xs font-semibold">
              超分
            </span>
            <span v-if="batch.processSteps.extractDetail" class="px-3 py-1 bg-gradient-to-r from-teal-100 to-teal-200 text-teal-800 rounded-full text-xs font-semibold">
              提取细节图
            </span>
            <span v-if="batch.processSteps.autoCrop" class="px-3 py-1 bg-gradient-to-r from-pink-100 to-pink-200 text-pink-800 rounded-full text-xs font-semibold">
              自动裁剪 {{ batch.cropRatio ? `(${batch.cropRatio})` : '' }}
            </span>
            <span v-if="batch.processSteps.extractReal" class="px-3 py-1 bg-gradient-to-r from-red-100 to-red-200 text-red-800 rounded-full text-xs font-semibold">
              提取实拍图 {{ batch.extractRealType ? `(${batch.extractRealType})` : '' }}
            </span>
            <span v-if="batch.processSteps.addWatermark" class="px-3 py-1 bg-gradient-to-r from-cyan-100 to-cyan-200 text-cyan-800 rounded-full text-xs font-semibold">
              加水印
            </span>
          </div>
        </div>

        <!-- 所有任务的预览结果 -->
        <div v-if="batch.allImageComparisons && batch.allImageComparisons.length > 0" class="mb-4">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-6 h-6 bg-indigo-500 rounded flex items-center justify-center">
              <Image class="w-4 h-4 text-white" />
            </div>
            <p class="text-sm font-semibold text-gray-800">预览结果</p>
          </div>
          <div class="max-h-96 overflow-y-auto">
            <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-2 sm:gap-3 md:gap-4">
              <div
                v-for="(comparison, idx) in batch.allImageComparisons"
                :key="idx"
                :class="[
                  'border rounded-lg p-2 sm:p-3',
                  comparison.processed
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200' 
                    : 'bg-gradient-to-r from-red-50 to-pink-50 border-red-200'
                ]"
              >
                <p class="text-xs font-semibold text-gray-600 mb-2 text-center bg-gradient-to-r from-indigo-100 to-purple-100 rounded py-1">#{{ idx + 1 }}</p>
                <div :class="[
                  'grid gap-2',
                  comparison.extractReal && comparison.extractDetail ? 'grid-cols-4' :
                  (comparison.extractReal || comparison.extractDetail) ? 'grid-cols-3' : 'grid-cols-2'
                ]">
                  <div>
                    <p class="text-xs text-gray-500 mb-1">原图</p>
                    <div 
                      class="aspect-square overflow-hidden rounded border border-gray-200 cursor-pointer sm:cursor-default"
                      @click="openPhotoSwipe([comparison.original], 0)"
                    >
                      <img :src="comparison.original" :alt="`original-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                    </div>

                  </div>
                  <div>
                    <p class="text-xs text-gray-500 mb-1">效果图</p>
                    <div 
                      class="aspect-square overflow-hidden rounded border border-gray-200 cursor-pointer sm:cursor-default"
                      @click="openPhotoSwipe([comparison.processed], 0)"
                    >
                      <img :src="comparison.processed" :alt="`processed-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                    </div>

                  </div>
                  <div v-if="comparison.extractReal">
                    <p class="text-xs text-gray-500 mb-1">实拍图</p>
                    <div 
                      class="aspect-square overflow-hidden rounded border border-gray-200 cursor-pointer sm:cursor-default"
                      @click="openPhotoSwipe([comparison.extractReal], 0)"
                    >
                      <img :src="comparison.extractReal" :alt="`extract-real-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                    </div>

                  </div>
                  <div v-if="comparison.extractDetail">
                    <p class="text-xs text-gray-500 mb-1">细节图</p>
                    <div 
                      class="aspect-square overflow-hidden rounded border border-gray-200 cursor-pointer sm:cursor-default"
                      @click="openPhotoSwipe([comparison.extractDetail], 0)"
                    >
                      <img :src="comparison.extractDetail" :alt="`extract-detail-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- PhotoSwipe 图片查看器 -->
  <PhotoSwipeViewer
    :images="photoSwipeImages"
    :visible="photoSwipeVisible"
    :initial-index="photoSwipeIndex"
    @close="closePhotoSwipe"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { History as HistoryIcon, Clock, CheckCircle, XCircle, Calendar, Image, User, Settings } from 'lucide-vue-next'
import { format } from 'date-fns'
import { getBatchTasks } from '../api/sqlApi.js'
import PhotoSwipeViewer from './PhotoSwipeViewer.vue'

// 历史记录列表，保存历史任务的数据
const history = ref([])
// 是否有历史记录
const hasHistory = computed(() => history.value.length > 0)

// PhotoSwipe 相关状态
const photoSwipeVisible = ref(false)
const photoSwipeImages = ref([])
const photoSwipeIndex = ref(0)

/**
 * 打开 PhotoSwipe 图片查看器（仅在手机端）
 */
const openPhotoSwipe = (images, index = 0) => {
  // 只在手机端启用（屏幕宽度小于 640px）
  if (window.innerWidth < 640) {
    photoSwipeImages.value = images
    photoSwipeIndex.value = index
    photoSwipeVisible.value = true
    // 禁止背景滚动
    document.body.style.overflow = 'hidden'
  }
}

/**
 * 关闭 PhotoSwipe 图片查看器
 */
const closePhotoSwipe = () => {
  photoSwipeVisible.value = false
  photoSwipeImages.value = []
  photoSwipeIndex.value = 0
  // 恢复背景滚动
  document.body.style.overflow = ''
}


/**
 * 按批次分组的历史记录
 * 使用数据库中的batch_id字段进行分组，同一批处理的任务具有相同的batch_id
 * @returns {Array} 分组后的历史记录
 */ 
const groupedHistory = computed(() => {
  if (!history.value.length) return []
  
  // 按batch_id分组
  const groups = new Map()
  
  history.value.forEach(task => {
    // 只使用batch_id作为分组键，如果没有batch_id则跳过该任务
    if (!task.batchId) {
      return
    }
    
    const batchKey = task.batchId
    
    if (!groups.has(batchKey)) {
      groups.set(batchKey, {
        batchId: batchKey,
        taskSource: task.taskSource || 'batch',
        createdAt: task.createdAt,
        completedAt: task.completedAt,
        status: task.status,
        processSteps: task.processSteps,
        cropRatio: task.cropRatio,
        extractRealType: task.extractRealType,
        modelImagePreview: task.modelImagePreview,
        sourceImages: task.sourceImages,
        tasks: [],
        allImageComparisons: []
      })
    }
    
    const group = groups.get(batchKey)
    group.tasks.push(task)
    
    // 合并所有图片比较结果
    if (task.imageComparisons && task.imageComparisons.length > 0) {
      group.allImageComparisons.push(...task.imageComparisons)
    }
    
    // 更新状态（如果有任务失败，整个批次标记为失败）
    if (task.status === 'failed') {
      group.status = 'failed'
    }
    
    // 更新完成时间（取最新的完成时间）
    if (task.completedAt && (!group.completedAt || new Date(task.completedAt) > new Date(group.completedAt))) {
      group.completedAt = task.completedAt
    }
  })
  
  // 计算批次统计信息
  return Array.from(groups.values()).map(batch => {
    // 源图片数量：取第一个任务的源图片数量（因为同一次处理的所有任务源图片相同）
    const totalSourceCount = batch.tasks[0]?.sourceImages?.length || batch.tasks[0]?.sourceCount || 0
    
    // 基于实际的图片处理结果计算成功和失败数量
    // 因为同一批处理的所有任务记录都保存了相同的统计总数，不能累加
    let totalSuccessCount = 0
    let totalFailedCount = 0
    
    // 优先使用 allImageComparisons 来统计（更准确）
    if (batch.allImageComparisons && batch.allImageComparisons.length > 0) {
      batch.allImageComparisons.forEach(comparison => {
        // 如果 processed 字段存在且不为空，说明处理成功
        if (comparison.processed) {
          totalSuccessCount++
        } else {
          totalFailedCount++
        }
      })
    } else {
      // 如果没有图片比较结果，使用第一个任务的统计信息
      // 因为同一批次的所有任务记录的统计信息相同
      totalSuccessCount = batch.tasks[0]?.successCount || 0
      totalFailedCount = batch.tasks[0]?.failedCount || 0
    }
    
    const totalProcessed = totalSuccessCount + totalFailedCount
    const progressPercentage = totalSourceCount > 0 ? Math.round((totalProcessed / totalSourceCount) * 100) : 0
    
    return {
      ...batch,
      totalSourceCount,
      totalSuccessCount,
      totalFailedCount,
      totalProcessed,
      progressPercentage
    }
  }).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)) // 按创建时间倒序排列
})


// 生命周期
onMounted(async () => {
  await loadHistoryFromDatabase()
})


// 从数据库加载历史记录
const loadHistoryFromDatabase = async () => {
  try {
    const response = await getBatchTasks()
    console.log('response', response)

    if (response.data && response.data.success) {
      history.value = response.data.data.tasks.map(task => {
      // 解析JSON字符串字段
      let processSteps = JSON.parse(task.process_steps)
      let processedResults = []
      let sourceImages = JSON.parse(task.source_images)
      
      try {
        processedResults = task.processed_results ? JSON.parse(task.processed_results) : []
        // 如果processed_results不是数组，而是单个对象，转换为数组
        if (!Array.isArray(processedResults)) {
          processedResults = [processedResults]
        }
      } catch (e) {
        console.warn('解析processed_results失败:', e)
      }
      

      return {
        id: task.id.toString(),
        batchId: task.batch_id,
        type: task.task_type,
        taskSource: task.task_source,
        status: task.status,
        createdAt: new Date(task.created_at),
        completedAt: task.completed_at ? new Date(task.completed_at) : undefined,
        scheduledTime: task.scheduled_time ? new Date(task.scheduled_time) : undefined,
        processType: task.process_type,
        processSteps: processSteps,
        cropRatio: task.crop_ratio,
        extractRealType: task.extract_real_type,
        sourceImages: sourceImages,
        modelImagePreview: task.model_image?.file_url || task.model_image,
        processedImages: processedResults.map(r => r.processed_url).filter(Boolean),
        imageComparisons: processedResults.map(r => ({
          original: r.original_url,
          processed: r.processed_url,
          extractReal: r.extract_real_url,
          extractDetail: r.extract_detail_url
        })),
        sourceCount: task.source_count,
        successCount: task.success_count,
        failedCount: task.failed_count,
        totalProcessed: task.total_processed
      }
      })
      
      console.log('从数据库加载历史记录成功，共', history.value.length, '条记录')
    } else {
      throw new Error(response.data?.message || '获取历史记录失败')
    }
  } catch (error) {
    console.error('从数据库加载历史记录失败，回退到本地存储:', error)
    // 回退到本地存储
    history.value = getHistoryFromStorage()
  }
}


// 方法
const getStatusIcon = (status) => {
  switch (status) {
    case 'success':
      return CheckCircle
    case 'failed':
      return XCircle
    default:
      return Clock
  }
}


const getStatusIconClass = (status) => {
  switch (status) {
    case 'success':
      return 'text-white'
    case 'failed':
      return 'text-white'
    default:
      return 'text-white'
  }
}


const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'success':
      return 'bg-gradient-to-r from-green-100 to-emerald-200 text-green-800'
    case 'failed':
      return 'bg-gradient-to-r from-red-100 to-pink-200 text-red-800'
    default:
      return 'bg-gradient-to-r from-yellow-100 to-orange-200 text-yellow-800'
  }
}


const getStatusText = (status) => {
  switch (status) {
    case 'success':
      return '成功'
    case 'failed':
      return '失败'
    default:
      return '未知'
  }
}

const getBatchStatusBgClass = (status) => {
  switch (status) {
    case 'success':
      return 'bg-gradient-to-r from-green-500 to-emerald-600'
    case 'failed':
      return 'bg-gradient-to-r from-red-500 to-pink-600'
    default:
      return 'bg-gradient-to-r from-yellow-500 to-orange-600'
  }
}

</script>
