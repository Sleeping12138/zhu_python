<template>
  <div class="space-y-4 sm:space-y-6">
    <!-- 页面标题 -->
    <div class="flex justify-between items-center">
      <h2 class="text-lg sm:text-xl md:text-2xl font-bold text-gray-800">虚拟试衣</h2>
    </div>

    <!-- 主要内容区域：左右布局 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
      <!-- 左侧：上传和配置区域 -->
      <div class="space-y-6">
        <!-- 上传模特图 -->
        <div class="rounded-xl p-3 sm:p-4 border border-gray-200 bg-white relative">
          <div class="flex items-center gap-2 mb-2 sm:mb-3">
            <div class="w-5 h-5 sm:w-6 sm:h-6 bg-blue-500 rounded flex items-center justify-center">
              <Folder class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
            </div>
            <label class="text-sm sm:text-base font-semibold text-gray-800">上传模特图文件夹</label>
          </div>
          <!-- 上传框 -->
          <div class="flex gap-2 sm:gap-3 md:gap-4 overflow-x-auto pb-2 mb-3 sm:mb-4">
            <div class="relative flex-shrink-0">
              <div 
                :class="[
                  'border-2 border-dashed border-blue-300 rounded-xl sm:rounded-2xl w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 flex flex-col items-center justify-center transition-colors group',
                  isUploadingModel ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:border-blue-500 hover:bg-blue-50'
                ]"
                @click="!isUploadingModel && modelInputRef?.click()"
              >
                <input
                  ref="modelInputRef"
                  type="file"
                  multiple
                  webkitdirectory=""
                  class="hidden"
                  @change="handleModelFolderUpload"
                />
                <div class="flex flex-col items-center gap-1 sm:gap-2 text-blue-400 group-hover:text-blue-600 transition-colors pointer-events-none">
                  <Folder class="w-5 h-5 sm:w-6 sm:h-6 md:w-8 md:h-8" />
                  <span class="text-xs sm:text-sm font-medium">上传文件夹</span>
                </div>
              </div>
            </div>

            <!-- 预览模特图片 -->
            <div
              v-for="img in modelImages"
              :key="img.id"
              class="relative border-2 border-gray-200 rounded-xl sm:rounded-2xl flex-shrink-0 group"
            >
              <div class="w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 overflow-hidden rounded-lg sm:rounded-xl">
                <img :src="img.preview" alt="model" class="w-full h-full object-contain bg-gray-50" />
              </div>
              <button
                @click="removeModelImage(img.id)"
                class="absolute inset-0 bg-red-200/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-300/70 rounded-xl sm:rounded-2xl"
              >
                <X class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-red-600" />
              </button>
            </div>
          </div>

          <!-- 已选择图片数量 -->
          <p v-if="modelImages.length > 0" class="text-xs sm:text-sm text-blue-600 font-medium mb-2 sm:mb-3 flex items-center gap-2">
            <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-blue-500 rounded-full animate-pulse"></span>
            已选择 {{ modelImages.length }} 张图片
          </p>

          <!-- 加载蒙版 -->
          <div v-if="isUploadingModel" class="absolute inset-0 bg-white bg-opacity-80 rounded-xl flex items-center justify-center z-10">
            <div class="text-center">
              <Settings class="w-6 h-6 sm:w-8 sm:h-8 text-blue-500 mx-auto mb-2 animate-spin" />
              <span class="text-xs sm:text-sm font-medium text-gray-700">上传中...</span>
            </div>
          </div>

          <!-- 模特图衣服类型选择 -->
          <div class="flex items-center gap-2 mb-2">
            <div class="w-4 h-4 sm:w-5 sm:h-5 bg-purple-500 rounded flex items-center justify-center">
              <Settings class="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" />
            </div>
            <label class="text-xs sm:text-sm font-semibold text-gray-700">衣服类型</label>
          </div>
          <select
            v-model="modelClothingType"
            class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 bg-white"
          >
            <option value="">请选择衣服类型</option>
            <option value="上衣">上衣</option>
            <option value="裤子">裤子</option>
            <option value="裙子">裙子</option>
            <option value="连衣裙">连衣裙</option>
          </select>
        </div>

        <!-- 上传实拍图 -->
        <div class="rounded-xl p-3 sm:p-4 border border-gray-200 bg-white">
          <div class="flex items-center gap-2 mb-2 sm:mb-3">
            <div class="w-5 h-5 sm:w-6 sm:h-6 bg-green-500 rounded flex items-center justify-center">
              <ImageIcon class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
            </div>
            <label class="text-sm sm:text-base font-semibold text-gray-800">上传实拍图</label>
          </div>
          <div class="relative mb-3 sm:mb-4">
            <div 
              :class="[
                'border-2 border-dashed border-green-300 rounded-xl w-full h-32 sm:h-40 md:h-48 flex flex-col items-center justify-center transition-colors group',
                isUploadingClothing ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:border-green-500 hover:bg-green-50'
              ]"
              @click="!isUploadingClothing && clothingInputRef?.click()"
            >
              <input
                ref="clothingInputRef"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleClothingImageUpload"
              />
              <div v-if="!clothingImage" class="text-center">
                <Upload class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 text-green-400 mx-auto mb-2 group-hover:text-green-500 transition-colors" />
                <span class="text-xs sm:text-sm font-medium text-gray-600">点击上传实拍图</span>
              </div>
              <div v-else class="relative w-full h-full">
                <img :src="clothingImage" alt="实拍图" class="w-full h-full object-contain rounded-lg" />
                <button
                  @click.stop="removeClothingImage"
                  class="absolute top-1 right-1 sm:top-2 sm:right-2 w-6 h-6 sm:w-8 sm:h-8 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center transition-colors"
                >
                  <X class="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>
              <!-- 加载蒙版 -->
              <div v-if="isUploadingClothing" class="absolute inset-0 bg-white bg-opacity-80 rounded-xl flex items-center justify-center z-10">
                <div class="text-center">
                  <Settings class="w-6 h-6 sm:w-8 sm:h-8 text-green-500 mx-auto mb-2 animate-spin" />
                  <span class="text-xs sm:text-sm font-medium text-gray-700">上传中...</span>
                </div>
              </div>
            </div>
          </div>
          <!-- 实拍图衣服类型选择 -->
          <div class="flex items-center gap-2 mb-2">
            <div class="w-4 h-4 sm:w-5 sm:h-5 bg-purple-500 rounded flex items-center justify-center">
              <Settings class="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" />
            </div>
            <label class="text-xs sm:text-sm font-semibold text-gray-700">衣服类型</label>
          </div>
          <select
            v-model="clothingClothingType"
            class="w-full px-3 py-1.5 sm:px-4 sm:py-2 text-xs sm:text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-800 bg-white"
          >
            <option value="">请选择衣服类型</option>
            <option value="上衣">上衣</option>
            <option value="裤子">裤子</option>
            <option value="裙子">裙子</option>
            <option value="连衣裙">连衣裙</option>
          </select>
        </div>

        <!-- 执行按钮 -->
        <button
          @click="handleGenerate"
          :disabled="!canGenerate || isGenerating"
          :class="[
            'w-full px-4 py-2.5 sm:px-6 sm:py-4 rounded-xl font-semibold text-white transition-all duration-300 flex items-center justify-center gap-2 text-sm sm:text-base',
            canGenerate && !isGenerating
              ? 'bg-blue-500 hover:bg-blue-600 shadow-lg hover:shadow-xl transform hover:scale-105'
              : 'bg-gray-400 cursor-not-allowed'
          ]"
        >
          <Settings v-if="isGenerating" class="w-4 h-4 sm:w-5 sm:h-5 animate-spin" />
          <span>{{ isGenerating ? '生成中...' : `执行（${modelImages.length}张模特图）` }}</span>
        </button>
      </div>

      <!-- 右侧：结果展示区域 -->
      <div class="rounded-xl p-3 sm:p-4 border border-gray-200 bg-white flex flex-col relative">
        <div class="flex items-center gap-2 mb-2 sm:mb-3">
          <div class="w-5 h-5 sm:w-6 sm:h-6 bg-indigo-500 rounded flex items-center justify-center">
            <ImageIcon class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
          </div>
          <label class="text-sm sm:text-base font-semibold text-gray-800">生成结果</label>
        </div>
        <button
          v-if="resultImages.length > 0"
          @click="downloadAllResults"
          class="absolute top-1 right-1 sm:top-2 sm:right-2 px-2 py-1 sm:px-4 sm:py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg flex items-center gap-1 sm:gap-2 transition-colors shadow-lg z-10 text-xs sm:text-sm"
        >
          <Download class="w-3 h-3 sm:w-4 sm:h-4" />
          <span class="hidden sm:inline">一键下载</span>
        </button>
        <div class="border-2 border-dashed border-gray-300 rounded-xl w-full min-h-[300px] sm:min-h-[400px] md:min-h-[500px] lg:min-h-[600px] max-h-[calc(100vh-200px)] overflow-auto">
          <div v-if="resultImages.length === 0" class="flex items-center justify-center h-full min-h-[300px]">
            <div class="text-center text-gray-400">
              <ImageIcon class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-2 sm:mb-4 opacity-50" />
              <p class="text-sm sm:text-base md:text-lg">生成的图片将显示在这里</p>
            </div>
          </div>
          <div v-else class="p-2 sm:p-4 space-y-4 sm:space-y-6">
            <div
              v-for="(result, idx) in resultImages"
              :key="idx"
              class="border-2 rounded-xl sm:rounded-2xl p-3 sm:p-4 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 shadow-sm"
            >
              <p class="text-xs sm:text-sm font-semibold mb-3 sm:mb-4 text-center rounded-lg py-1.5 sm:py-2 text-blue-700 bg-gradient-to-r from-blue-100 to-blue-200">
                #{{ idx + 1 }} - {{ result.modelName || `模特图 ${idx + 1}` }}
              </p>
              <div class="grid grid-cols-2 gap-2 sm:gap-3">
                <div>
                  <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">模特图</p>
                  <div class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm">
                    <img :src="result.modelPreview" alt="model" class="w-full h-full object-contain bg-gray-50" />
                  </div>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">生成结果</p>
                  <div class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm">
                    <img :src="result.resultUrl" alt="result" class="w-full h-full object-contain bg-gray-50" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload, User, ImageIcon, Settings, X, Download, Folder } from 'lucide-vue-next'
import { uploadFile } from '../utils/uploadUtils.js'
import { generateVirtualTryon } from '../api/sqlApi.js'


// 模特图片输入框的 ref
const modelInputRef = ref(null)
// 实拍图片输入框的 ref
const clothingInputRef = ref(null)
// 模特图片列表（数组）
const modelImages = ref([])
// 实拍图片的 URL
const clothingImage = ref(null)
// 模特图所选的衣服类型
const modelClothingType = ref('')
// 实拍图所选的衣服类型
const clothingClothingType = ref('')
// 生成的结果列表（数组，每个结果包含模特图和生成结果）
const resultImages = ref([])
// 是否正在生成中
const isGenerating = ref(false)
// 是否正在上传模特图
const isUploadingModel = ref(false)
// 是否正在上传实拍图
const isUploadingClothing = ref(false)

// 是否可以生成
const canGenerate = computed(() => {
  return modelImages.value.length > 0 && clothingImage.value && modelClothingType.value && clothingClothingType.value
})


/**
 * 模特图文件夹上传
 * @param e 
 */ 
const handleModelFolderUpload = (e) => {
  const files = Array.from(e.target.files || [])
  const imageFiles = files.filter(file => file.type.startsWith('image/'))
  
  // 先收集所有新图片，然后统一添加到最前面
  const newImages = imageFiles.map(file => {
    const id = Math.random().toString(36).substring(7)
    // 创建本地预览URL
    const preview = URL.createObjectURL(file)
    return {
      id,
      file,
      preview  // 使用本地预览URL
    }
  })
  
  // 将新图片添加到数组最前面
  modelImages.value.unshift(...newImages)
  
  // 重置 input，以便可以重复选择相同的文件
  if (e.target) {
    e.target.value = ''
  }
}

/**
 * 移除模特图
 * @param id 
 */
const removeModelImage = (id) => {
  // 先找到要删除的图片并释放预览URL
  const imgToRemove = modelImages.value.find(img => img.id === id)
  if (imgToRemove && imgToRemove.preview && imgToRemove.preview.startsWith('blob:')) {
    URL.revokeObjectURL(imgToRemove.preview)
  }
  
  // 删除图片
  modelImages.value = modelImages.value.filter(img => img.id !== id)
  
  // 如果删除后没有图片了，清空衣服类型
  if (modelImages.value.length === 0) {
    modelClothingType.value = ''
  }
}


/**
 * 实拍图上传
 * @param e 
 */ 
const handleClothingImageUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  isUploadingClothing.value = true
  try {
    const fileUrl = await uploadFile(file)
    clothingImage.value = fileUrl
    console.log('clothingImage', clothingImage.value)
  } catch (error) {
    console.error('上传实拍图失败:', error)
    alert('上传实拍图失败，请重试')
  } finally {
    isUploadingClothing.value = false
  }
}




/**
 * 移除实拍图
 */ 
const removeClothingImage = () => {
  clothingImage.value = null
  clothingClothingType.value = ''
  if (clothingInputRef.value) {
    clothingInputRef.value.value = ''
  }
}

/**
 * 生成虚拟试衣图片（对所有模特图生成）
 */ 
const handleGenerate = async () => {
  if (!canGenerate.value || isGenerating.value) return

  isGenerating.value = true
  resultImages.value = []

  try {
    const total = modelImages.value.length
    const results = []

    // 遍历所有模特图进行生成
    for (let i = 0; i < total; i++) {
      const modelImg = modelImages.value[i]
      
      // 上传模特图获取真实URL
      let modelImageUrl = modelImg.preview
      if (modelImageUrl.startsWith('blob:')) {
        modelImageUrl = await uploadFile(modelImg.file)
        // 更新预览URL为真实URL
        modelImg.preview = modelImageUrl
      }

      try {
        const response = await generateVirtualTryon(
          modelImageUrl,
          clothingImage.value,
          modelClothingType.value,
          clothingClothingType.value
        )

        console.log(`模特图 ${i + 1} 生成结果:`, response)

        if (response.data.success) {
          results.push({
            modelPreview: modelImageUrl,
            resultUrl: response.data.data.result_url,
            modelName: `模特图 ${i + 1}`,
            success: true
          })
        } else {
          results.push({
            modelPreview: modelImageUrl,
            resultUrl: null,
            modelName: `模特图 ${i + 1}`,
            success: false,
            error: response.data?.message || '生成失败'
          })
        }
      } catch (error) {
        console.error(`模特图 ${i + 1} 生成失败:`, error)
        results.push({
          modelPreview: modelImageUrl,
          resultUrl: null,
          modelName: `模特图 ${i + 1}`,
          success: false,
          error: error.message || '生成失败'
        })
      }
    }

    resultImages.value = results

    // 统计成功和失败数量
    const successCount = results.filter(r => r.success).length
    const failedCount = results.filter(r => !r.success).length
    
    if (failedCount > 0) {
      alert(`生成完成：成功 ${successCount} 张，失败 ${failedCount} 张`)
    } else {
      alert(`生成完成：成功 ${successCount} 张`)
    }
  } catch (error) {
    console.error('生成虚拟试衣失败:', error)
    alert('生成过程中发生错误，请重试')
  } finally {
    isGenerating.value = false
  }
}


/**
 * 下载所有结果
 */ 
const downloadAllResults = async () => {
  if (resultImages.value.length === 0) return

  try {
    for (let i = 0; i < resultImages.value.length; i++) {
      const result = resultImages.value[i]
      if (result.success && result.resultUrl) {
        try {
          const timestamp = Date.now() + i
          const link = document.createElement('a')
          link.href = result.resultUrl
          link.download = `virtual-tryon-${i + 1}-${timestamp}.jpg`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          
          // 添加延迟，避免浏览器阻止多个下载
          await new Promise(resolve => setTimeout(resolve, 300))
        } catch (error) {
          console.error(`下载结果 ${i + 1} 失败:`, error)
        }
      }
    }
  } catch (error) {
    console.error('下载过程中发生错误:', error)
    alert('下载失败，请重试')
  }
}
</script>

<style scoped>
</style>

