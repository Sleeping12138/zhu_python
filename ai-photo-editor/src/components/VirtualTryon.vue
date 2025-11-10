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
        <div class="rounded-xl p-3 sm:p-4 border border-gray-200 bg-white">
          <div class="flex items-center gap-2 mb-2 sm:mb-3">
            <div class="w-5 h-5 sm:w-6 sm:h-6 bg-blue-500 rounded flex items-center justify-center">
              <User class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
            </div>
            <label class="text-sm sm:text-base font-semibold text-gray-800">上传模特图</label>
          </div>
          <div class="relative mb-3 sm:mb-4">
            <div 
              :class="[
                'border-2 border-dashed border-blue-300 rounded-xl w-full h-32 sm:h-40 md:h-48 flex flex-col items-center justify-center transition-colors group',
                isUploadingModel ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:border-blue-500 hover:bg-blue-50'
              ]"
              @click="!isUploadingModel && modelInputRef?.click()"
            >
              <input
                ref="modelInputRef"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleModelImageUpload"
              />
              <div v-if="!modelImage" class="text-center">
                <Upload class="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 text-blue-400 mx-auto mb-2 group-hover:text-blue-500 transition-colors" />
                <span class="text-xs sm:text-sm font-medium text-gray-600">点击上传模特图</span>
              </div>
              <div v-else class="relative w-full h-full">
                <img :src="modelImage" alt="模特图" class="w-full h-full object-contain rounded-lg" />
                <button
                  @click.stop="removeModelImage"
                  class="absolute top-1 right-1 sm:top-2 sm:right-2 w-6 h-6 sm:w-8 sm:h-8 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center transition-colors"
                >
                  <X class="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>
              <!-- 加载蒙版 -->
              <div v-if="isUploadingModel" class="absolute inset-0 bg-white bg-opacity-80 rounded-xl flex items-center justify-center z-10">
                <div class="text-center">
                  <Settings class="w-6 h-6 sm:w-8 sm:h-8 text-blue-500 mx-auto mb-2 animate-spin" />
                  <span class="text-xs sm:text-sm font-medium text-gray-700">上传中...</span>
                </div>
              </div>
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
          <span>{{ isGenerating ? '生成中...' : '执行' }}</span>
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
          v-if="resultImage"
          @click="downloadResult"
          class="absolute top-1 right-1 sm:top-2 sm:right-2 px-2 py-1 sm:px-4 sm:py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg flex items-center gap-1 sm:gap-2 transition-colors shadow-lg z-10 text-xs sm:text-sm"
        >
          <Download class="w-3 h-3 sm:w-4 sm:h-4" />
          <span class="hidden sm:inline">下载</span>
        </button>
        <div class="border-2 border-dashed border-gray-300 rounded-xl w-full min-h-[300px] sm:min-h-[400px] md:min-h-[500px] lg:min-h-[600px] max-h-[calc(100vh-200px)] flex items-center justify-center overflow-auto">
          <div v-if="!resultImage" class="text-center text-gray-400">
            <ImageIcon class="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-2 sm:mb-4 opacity-50" />
            <p class="text-sm sm:text-base md:text-lg">生成的图片将显示在这里</p>
          </div>
          <div v-else class="relative w-full h-full p-2 sm:p-4 flex items-center justify-center">
            <img :src="resultImage" alt="生成结果" class="max-w-full max-h-full object-contain rounded-lg" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload, User, ImageIcon, Settings, X, Download } from 'lucide-vue-next'
import { uploadFile } from '../utils/uploadUtils.js'
import { generateVirtualTryon } from '../api/sqlApi.js'


// 模特图片输入框的 ref
const modelInputRef = ref(null)
// 实拍图片输入框的 ref
const clothingInputRef = ref(null)
// 模特图片的 URL
const modelImage = ref(null)
// 实拍图片的 URL
const clothingImage = ref(null)
// 模特图所选的衣服类型
const modelClothingType = ref('')
// 实拍图所选的衣服类型
const clothingClothingType = ref('')
// 生成的结果图片 URL
const resultImage = ref(null)
// 是否正在生成中
const isGenerating = ref(false)
// 是否正在上传模特图
const isUploadingModel = ref(false)
// 是否正在上传实拍图
const isUploadingClothing = ref(false)

// 是否可以生成
const canGenerate = computed(() => {
  return modelImage.value && clothingImage.value && modelClothingType.value && clothingClothingType.value
})


/**
 * 模特图上传
 * @param e 
 */ 
const handleModelImageUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  isUploadingModel.value = true
  try {
    const fileUrl = await uploadFile(file)
    modelImage.value = fileUrl
    console.log('modelImage', modelImage.value)
  } catch (error) {
    console.error('上传模特图失败:', error)
    alert('上传模特图失败，请重试')
  } finally {
    isUploadingModel.value = false
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
 * 移除模特图
 */ 
const removeModelImage = () => {
  modelImage.value = null
  modelClothingType.value = ''
  if (modelInputRef.value) {
    modelInputRef.value.value = ''
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
 * 生成虚拟试衣图片
 */ 
const handleGenerate = async () => {
  if (!canGenerate.value || isGenerating.value) return

  isGenerating.value = true
  resultImage.value = null

  try {
    const response = await generateVirtualTryon(
      modelImage.value,
      clothingImage.value,
      modelClothingType.value,
      clothingClothingType.value
    )

    console.log('response', response)

    if (response.data.success) {
      resultImage.value = response.data.data.result_url
    } else {
      throw new Error('生成失败')
    }
  } catch (error) {
    console.error('生成虚拟试衣失败:', error)
    alert('生成失败，请重试')
  } finally {
    isGenerating.value = false
  }
}


/**
 * 下载结果
 */ 
const downloadResult = () => {
  if (!resultImage.value) return

  const link = document.createElement('a')
  link.href = resultImage.value
  link.download = `virtual-tryon-${Date.now()}.jpg`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<style scoped>
</style>

