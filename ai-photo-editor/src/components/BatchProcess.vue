<template>
  <div class="space-y-4 sm:space-y-6 md:space-y-8">

    <!-- 上传源图片文件夹 -->
    <div class="rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-6 border border-gray-200">

      <!-- 图标和文字 -->
      <div class="flex items-center gap-2 sm:gap-3 mb-3 sm:mb-4">
        <div class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 bg-blue-500 rounded-lg flex items-center justify-center">
          <Folder class="w-3 h-3 sm:w-4 sm:h-4 md:w-5 md:h-5 text-white" />
        </div>
        <label class="text-sm sm:text-base md:text-lg font-semibold text-gray-800">上传源图片文件夹</label>
      </div>


      <!-- 上传框 -->
      <div class="flex gap-2 sm:gap-3 md:gap-4 overflow-x-auto pb-2">
        <div class="relative flex-shrink-0">
          <div 
            class="border-2 border-dashed border-blue-300 rounded-xl sm:rounded-2xl w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors group"
            @click="sourceInputRef?.click()"
          >
            <input
              ref="sourceInputRef"
              type="file"
              multiple
              webkitdirectory=""
              class="hidden"
              @change="handleSourceFolderUpload"
            />
            <div class="flex flex-col items-center gap-1 sm:gap-2 text-blue-400 group-hover:text-blue-600 transition-colors pointer-events-none">
              <Folder class="w-5 h-5 sm:w-6 sm:h-6 md:w-8 md:h-8" />
              <span class="text-xs sm:text-sm font-medium">上传文件夹</span>
            </div>
          </div>
        </div>

        <!-- 预览源图片 -->
        <div
          v-for="img in sourceImages"
          :key="img.id"
          class="relative group flex-shrink-0"
        >
          <div class="border-2 border-gray-200 rounded-xl sm:rounded-2xl w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 overflow-hidden">
            <img 
              :src="img.preview" 
              alt="source" 
              class="w-full h-full object-contain bg-gray-50" 
            />
          </div>
          <button
            @click="removeSourceImage(img.id)"
            class="absolute inset-0 bg-red-200/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-300/70 rounded-xl sm:rounded-2xl"
          >
            <X class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-red-600" />
          </button>
        </div>
      </div>

      <!-- 已选择图片数量 -->
      <p v-if="sourceImages.length > 0" class="text-xs sm:text-sm text-blue-600 font-medium mt-2 sm:mt-3 flex items-center gap-2">
        <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-blue-500 rounded-full animate-pulse"></span>
        已选择 {{ sourceImages.length }} 张图片
      </p>
      <p class="text-xs text-red-300 mt-1">建议一次性上传图片张数小于10</p>

    </div>

    <!-- 上传模特图片 -->
    <div 
      v-if="processType === 'model'" 
      :class="[
        'rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-6 border transition-all relative',
        processSteps.faceSwap 
          ? 'border-gray-200' 
          : 'border-gray-300 bg-gray-100/50 opacity-60'
      ]"
    >
      <!-- 禁用遮罩层 -->
      <div 
        v-if="!processSteps.faceSwap"
        class="absolute inset-0 bg-gray-200/30 backdrop-blur-[1px] rounded-xl sm:rounded-2xl z-10 cursor-not-allowed"
      ></div>

      <!-- 图标和文字 -->
      <div class="flex items-center gap-2 sm:gap-3 mb-3 sm:mb-4 relative z-0">
        <div 
          :class="[
            'w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 rounded-lg flex items-center justify-center',
            processSteps.faceSwap ? 'bg-purple-500' : 'bg-gray-400'
          ]"
        >
          <User class="w-3 h-3 sm:w-4 sm:h-4 md:w-5 md:h-5 text-white" />
        </div>
        <label 
          :class="[
            'text-sm sm:text-base md:text-lg font-semibold',
            processSteps.faceSwap ? 'text-gray-800' : 'text-gray-500'
          ]"
        >
          上传模特图片（换脸）
        </label>
      </div>


      <!-- 上传框 -->
      <div class="flex gap-2 sm:gap-3 md:gap-4 overflow-x-auto pb-2 relative z-0">
        <div class="relative flex-shrink-0">
          <div 
            :class="[
              'border-2 border-dashed rounded-xl sm:rounded-2xl w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 flex flex-col items-center justify-center transition-colors group',
              processSteps.faceSwap
                ? 'border-purple-300 cursor-pointer hover:border-purple-500 hover:bg-purple-50'
                : 'border-gray-300 cursor-not-allowed bg-gray-100'
            ]"
            @click="processSteps.faceSwap ? modelInputRef?.click() : null"
          >
            <input
              ref="modelInputRef"
              type="file"
              accept="image/*"
              :disabled="!processSteps.faceSwap"
              class="hidden"
              @change="handleModelImageUpload"
            />
            <div 
              :class="[
                'flex flex-col items-center gap-1 sm:gap-2 transition-colors pointer-events-none',
                processSteps.faceSwap
                  ? 'text-purple-400 group-hover:text-purple-600'
                  : 'text-gray-400'
              ]"
            >
              <User class="w-5 h-5 sm:w-6 sm:h-6 md:w-8 md:h-8" />
              <span class="text-xs sm:text-sm font-medium">上传模特</span>
            </div>
          </div>
        </div>

        <!-- 最近5个模特图片 -->
          <div
            v-for="img in recentModels"
            :key="img.id"
            @click="processSteps.faceSwap ? selectModel(img) : null"
            :class="[
              'relative border-2 rounded-xl sm:rounded-2xl flex-shrink-0 transition-colors',
              processSteps.faceSwap
                ? 'cursor-pointer'
                : 'cursor-not-allowed opacity-60',
              modelImage?.id === img.id && processSteps.faceSwap
                ? 'border-purple-500 ring-2 ring-purple-200' 
                : processSteps.faceSwap
                  ? 'border-gray-200 hover:border-purple-300'
                  : 'border-gray-300'
            ]"
          >
          <div class="w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 overflow-hidden rounded-lg sm:rounded-xl">
            <img :src="img.preview" alt="model" class="w-full h-full object-contain bg-gray-50" />
          </div>
          <div v-if="modelImage?.id === img.id && processSteps.faceSwap" class="absolute -top-1 -right-1 sm:-top-2 sm:-right-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full p-1 sm:p-1.5">
            <ImageIcon class="w-3 h-3 sm:w-4 sm:h-4" />
          </div>
        </div>
      </div>

      <!-- 已选择模特图片数量 -->
      <p 
        v-if="recentModels.length > 0" 
        :class="[
          'text-xs sm:text-sm font-medium mt-2 sm:mt-3 flex items-center gap-2 relative z-0',
          processSteps.faceSwap ? 'text-purple-600' : 'text-gray-400'
        ]"
      >
        <span 
          :class="[
            'w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full',
            processSteps.faceSwap ? 'bg-purple-500 animate-pulse' : 'bg-gray-400'
          ]"
        ></span>
        最近使用（点击切换模特）
      </p>

    </div>


    <!-- 处理步骤选择 -->
    <div class="rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-6 border border-gray-200">

      <!-- 图标和文字 -->
      <div class="flex items-center gap-2 mb-3 sm:mb-4">
        <div class="w-5 h-5 sm:w-6 sm:h-6 bg-green-500 rounded flex items-center justify-center">
          <Settings class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
        </div>
        <h3 class="text-sm sm:text-base font-semibold text-gray-800">处理配置</h3>
      </div>
      

      <div class="space-y-3 sm:space-y-4">

        <!-- 处理类型 -->
        <div>
          <label class="block text-xs sm:text-sm font-semibold text-gray-800 mb-2 sm:mb-3">处理类型</label>
          <div class="flex gap-2 sm:gap-3 items-center">
            <button
              @click="handleTypeChange('model')"
              :class="[
                'px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors',
                processType === 'model'
                  ? 'bg-green-500 text-white hover:bg-green-600'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              模特图
            </button>
            <button
              @click="handleTypeChange('real')"
              :class="[
                'px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors',
                processType === 'real'
                  ? 'bg-green-500 text-white hover:bg-green-600'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              实拍图
            </button>
          </div>
        </div>


        <!-- 处理步骤 -->
        <div class="space-y-3 sm:space-y-4">
          <label class="block text-xs sm:text-sm font-semibold text-gray-800 mb-2 sm:mb-3">处理步骤</label>
          
          <!-- 第一组：基础处理步骤 -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border-2 border-blue-100 shadow-sm">
            <div class="flex items-center gap-2 mb-3 sm:mb-4">
              <div class="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
              <h4 class="text-xs sm:text-sm font-semibold text-blue-700">基础处理</h4>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 sm:gap-3">
              <label class="flex items-center gap-1.5 sm:gap-2 cursor-pointer group p-2 sm:p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-blue-100">
                <input
                  type="checkbox"
                  v-model="processSteps.watermark"
                  class="w-3 h-3 sm:w-4 sm:h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <span class="text-xs sm:text-sm font-medium text-gray-700 group-hover:text-blue-600 transition-colors">去水印</span>
              </label>
              <template v-if="processType === 'model'">
                <label class="flex items-center gap-2 cursor-pointer group p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-purple-100">
                  <input
                    type="checkbox"
                    v-model="processSteps.faceSwap"
                    class="w-4 h-4 text-purple-600 rounded focus:ring-purple-500"
                  />
                  <span class="text-sm font-medium text-gray-700 group-hover:text-purple-600 transition-colors">换脸</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer group p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-yellow-100">
                  <input
                    type="checkbox"
                    v-model="processSteps.poseSwap"
                    class="w-4 h-4 text-yellow-600 rounded focus:ring-yellow-500"
                  />
                  <span class="text-sm font-medium text-gray-700 group-hover:text-yellow-600 transition-colors">换姿态</span>
                </label>
              </template>
              <label class="flex items-center gap-2 cursor-pointer group p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-green-100">
                <input
                  type="checkbox"
                  v-model="processSteps.backgroundSwap"
                  class="w-4 h-4 text-green-600 rounded focus:ring-green-500"
                />
                <span class="text-sm font-medium text-gray-700 group-hover:text-green-600 transition-colors">换背景</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer group p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-indigo-100">
                <input
                  type="checkbox"
                  v-model="processSteps.superResolution"
                  class="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
                />
                <span class="text-sm font-medium text-gray-700 group-hover:text-indigo-600 transition-colors">超分</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer group p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-teal-100">
                <input
                  type="checkbox"
                  v-model="processSteps.extractDetail"
                  class="w-4 h-4 text-teal-600 rounded focus:ring-teal-500"
                />
                <span class="text-sm font-medium text-gray-700 group-hover:text-teal-600 transition-colors">提取细节图</span>
              </label>
            </div>
          </div>

          <!-- 第二组：特殊功能 -->
          <div class="bg-gradient-to-br from-pink-50 to-rose-50 rounded-xl p-5 border-2 border-pink-100 shadow-sm">
            <div class="flex items-center gap-2 mb-4">
              <div class="w-1.5 h-1.5 bg-pink-500 rounded-full"></div>
              <h4 class="text-sm font-semibold text-pink-700">特殊功能</h4>
            </div>
            <div class="space-y-3">
              <template v-if="processType === 'model'">
                <!-- 自动裁剪 -->
                <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 p-2 sm:p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-pink-100">
                  <label class="flex items-center gap-1.5 sm:gap-2 cursor-pointer group flex-1">
                    <input
                      type="checkbox"
                      v-model="processSteps.autoCrop"
                      class="w-3 h-3 sm:w-4 sm:h-4 text-pink-600 rounded focus:ring-pink-500"
                    />
                    <span class="text-xs sm:text-sm font-medium text-gray-700 group-hover:text-pink-600 transition-colors">自动裁剪</span>
                  </label>
                  <div v-if="processSteps.autoCrop" class="flex-shrink-0 w-full sm:w-auto">
                    <select
                      v-model="cropRatio"
                      class="px-2 py-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm border-2 border-pink-200 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-400 bg-white shadow-sm transition-all w-full sm:min-w-[120px]"
                    >
                      <option value="16:9">16:9</option>
                      <option value="9:16">9:16</option>
                      <option value="1:1">1:1</option>
                      <option value="4:3">4:3</option>
                      <option value="3:4">3:4</option>
                      <option value="3:2">3:2</option>
                      <option value="2:3">2:3</option>
                    </select>
                  </div>
                </div>
                <!-- 提取实拍图 -->
                <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 p-2 sm:p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-red-100">
                  <label class="flex items-center gap-1.5 sm:gap-2 cursor-pointer group flex-1">
                    <input
                      type="checkbox"
                      v-model="processSteps.extractReal"
                      class="w-3 h-3 sm:w-4 sm:h-4 text-red-600 rounded focus:ring-red-500"
                    />
                    <span class="text-xs sm:text-sm font-medium text-gray-700 group-hover:text-red-600 transition-colors">提取实拍图</span>
                  </label>
                  <div v-if="processSteps.extractReal" class="flex-shrink-0 w-full sm:w-auto">
                    <select
                      v-model="extractRealType"
                      class="px-2 py-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm border-2 border-red-200 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-400 bg-white shadow-sm transition-all w-full sm:min-w-[120px]"
                    >
                      <option value="上装">上装</option>
                      <option value="下装">下装</option>
                      <option value="裙装">裙装</option>
                    </select>
                  </div>
                </div>
              </template>
              <!-- 加水印 -->
              <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 p-2 sm:p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-cyan-100">
                <label class="flex items-center gap-1.5 sm:gap-2 cursor-pointer group flex-1">
                  <input
                    type="checkbox"
                    v-model="processSteps.addWatermark"
                    class="w-3 h-3 sm:w-4 sm:h-4 text-cyan-600 rounded focus:ring-cyan-500"
                  />
                  <span class="text-xs sm:text-sm font-medium text-gray-700 group-hover:text-cyan-600 transition-colors">加水印</span>
                </label>
                <div v-if="processSteps.addWatermark" class="flex-shrink-0 w-full sm:w-auto">
                  <select
                    v-model="watermarkName"
                    class="px-2 py-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm border-2 border-cyan-200 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-400 bg-white shadow-sm transition-all w-full sm:min-w-[160px]"
                  >
                    <option value="@FF studio">@FF studio</option>
                    <option value="7 SEVEN G">7 SEVEN G</option>
                    <option value="百烁BUSSIO">百烁BUSSIO</option>
                    <option value="崛Ascend">崛Ascend</option>
                    <option value="诺华NovaBloom">诺华NovaBloom</option>
                    <option value="七吉 Seven G">七吉 Seven G</option>
                    <option value="甜莓派">甜莓派</option>
                    <option value="希大掌柜·崛">希大掌柜·崛</option>
                    <option value="gotrendy">gotrendy</option>
                    <option value="GTstudio">GTstudio</option>
                    <option value="NOVA">NOVA</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- 一键处理按钮 -->
    <div class="flex justify-center">
      <button
        @click="handleProcess"
        :disabled="!canProcess"
        class="group relative px-6 py-2.5 sm:px-8 sm:py-3 md:px-12 md:py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl sm:rounded-2xl font-semibold text-sm sm:text-base md:text-lg shadow-2xl hover:shadow-indigo-500/25 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 disabled:hover:scale-100 w-full sm:w-auto"
      >
        <div class="flex items-center gap-2 sm:gap-3 justify-center">
          <Play class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 group-hover:animate-pulse" />
          {{ isProcessing ? '处理中...' : '一键处理' }}
        </div>
        <div v-if="isProcessing" class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl sm:rounded-2xl animate-pulse opacity-50"></div>
      </button>
    </div>


    <!-- 处理进度 -->
    <div v-if="isProcessing" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200/50">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center animate-pulse">
          <Play class="w-5 h-5 text-white" />
        </div>
        <h3 class="text-lg font-semibold text-gray-800">处理进度</h3>
      </div>
      <div class="space-y-3">
        <div class="h-3 bg-gray-200 rounded-full overflow-hidden shadow-inner">
          <div
            class="h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500 ease-out rounded-full shadow-lg"
            :style="{ width: `${processingProgress}%` }"
          />
        </div>
        <div class="flex justify-between items-center">
          <p class="text-lg font-semibold text-gray-700">{{ processingProgress }}%</p>
          <p class="text-sm text-gray-500">正在处理图片...</p>
        </div>
      </div>
    </div>


    <!-- 处理结果 -->
    <div v-if="hasResults" class="bg-white rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-6 border border-gray-200">

      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-0 mb-4 sm:mb-6">
        <div class="flex items-center gap-2 sm:gap-3">
          <div class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 bg-green-500 rounded-lg flex items-center justify-center">
            <CheckCircle class="w-4 h-4 sm:w-4.5 sm:h-4.5 md:w-5 md:h-5 text-white" />
          </div>
          <h3 class="text-base sm:text-lg md:text-xl font-semibold text-gray-800">处理结果</h3>
        </div>
        <button
          @click="handleDownload"
          class="flex items-center gap-1.5 sm:gap-2 px-3 py-1.5 sm:px-4 sm:py-2 md:px-6 md:py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg sm:rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-green-500/25 text-xs sm:text-sm md:text-base w-full sm:w-auto justify-center"
        >
          <Download class="w-4 h-4 sm:w-4.5 sm:h-4.5 md:w-5 md:h-5" />
          一键下载
        </button>
      </div>


      <div class="max-h-96 overflow-y-auto">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
          <div
            v-for="(result, idx) in processResults"
            :key="idx"
            :class="[
              'border-2 rounded-xl sm:rounded-2xl p-3 sm:p-4 shadow-lg transition-all duration-300',
              result.is_success 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            ]"
          >
            <p 
              :class="[
                'text-xs sm:text-sm font-semibold mb-3 sm:mb-4 text-center rounded-lg py-1.5 sm:py-2',
                result.is_success 
                  ? 'text-green-700 bg-gradient-to-r from-green-100 to-green-200' 
                  : 'text-red-700 bg-gradient-to-r from-red-100 to-red-200'
              ]"
            >#{{ idx + 1 }}</p>
            <div :class="[
              'grid gap-2 sm:gap-3',
              result.extract_real_url && result.extract_detail_url ? 'grid-cols-2 sm:grid-cols-4' :
              (result.extract_real_url || result.extract_detail_url) ? 'grid-cols-2 sm:grid-cols-3' : 'grid-cols-2'
            ]">
              <div>
                <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">原图</p>
                <div 
                  class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm cursor-pointer sm:cursor-default"
                  @click="openPhotoSwipe([result.original_url], 0)"
                >
                  <img :src="result.original_url" :alt="`input-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                </div>
              </div>
              <div>
                <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">效果图</p>
                <div 
                  class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm cursor-pointer sm:cursor-default"
                  @click="openPhotoSwipe([result.processed_url], 0)"
                >
                  <img :src="result.processed_url" :alt="`output-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                </div>
              </div>
              <div v-if="result.extract_real_url">
                <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">实拍图</p>
                <div 
                  class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm cursor-pointer sm:cursor-default"
                  @click="openPhotoSwipe([result.extract_real_url], 0)"
                >
                  <img :src="result.extract_real_url" :alt="`extract-real-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                </div>
              </div>
              <div v-if="result.extract_detail_url">
                <p class="text-xs font-medium text-gray-500 mb-1 sm:mb-2">细节图</p>
                <div 
                  class="aspect-square overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 shadow-sm cursor-pointer sm:cursor-default"
                  @click="openPhotoSwipe([result.extract_detail_url], 0)"
                >
                  <img :src="result.extract_detail_url" :alt="`extract-detail-${idx}`" class="w-full h-full object-contain bg-gray-50" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 下载成功提示卡片 -->
    <Transition name="fade">
      <div
        v-if="showDownloadSuccess"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        @click.self="closeDownloadSuccess"
      >
        <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4 transform transition-all">
          <div class="flex flex-col items-center gap-4">
            <div 
              :class="[
                'w-16 h-16 rounded-full flex items-center justify-center',
                downloadIsSuccess ? 'bg-green-500' : 'bg-red-500'
              ]"
            >
              <CheckCircle class="w-10 h-10 text-white" />
            </div>
            <h3 
              :class="[
                'text-2xl font-bold',
                downloadIsSuccess ? 'text-gray-800' : 'text-red-600'
              ]"
            >
              {{ downloadIsSuccess ? '下载成功' : '下载失败' }}
            </h3>
            <p class="text-gray-600 text-center whitespace-pre-line">{{ downloadSuccessMessage }}</p>
            <button
              @click="closeDownloadSuccess"
              :class="[
                'mt-4 px-8 py-3 text-white rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg font-semibold',
                downloadIsSuccess 
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 hover:shadow-green-500/25'
                  : 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 hover:shadow-red-500/25'
              ]"
            >
              确定
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- PhotoSwipe 图片查看器 -->
    <PhotoSwipeViewer
      :images="photoSwipeImages"
      :visible="photoSwipeVisible"
      :initial-index="photoSwipeIndex"
      @close="closePhotoSwipe"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Play, Download, X, Image as ImageIcon, Folder, User, Settings, CheckCircle } from 'lucide-vue-next'
import dayjs from 'dayjs'
import { saveAs } from 'file-saver'
import { executeImmediateTask } from '../api/sqlApi.js'
import { uploadFile } from '../utils/uploadUtils.js'
import PhotoSwipeViewer from './PhotoSwipeViewer.vue'

// 源图片上传输入框
const sourceInputRef = ref()
// 模特图片上传输入框
const modelInputRef = ref()
// 源图片列表
const sourceImages = ref([])
// 当前选中的模特图片
const modelImage = ref(null)
// 最近使用过的模特图片列表
const recentModels = ref([])
// 是否正在处理
const isProcessing = ref(false)
// 处理进度（百分比）
const processingProgress = ref(0)
// 处理结果列表
const processResults = ref([])
// 处理类型（'model' 为模特图, 其它为实拍图）
const processType = ref('model')
// 自动裁剪比例
const cropRatio = ref('3:4')
// 实拍类型（如"上装"、"下装"等）
const extractRealType = ref('上装')
// 水印名称（从下拉框选择）
const watermarkName = ref('')
// 处理步骤配置
const processSteps = ref({
  watermark: true,
  faceSwap: true,
  backgroundSwap: true,
  poseSwap: true,
  autoCrop: true,
  extractReal: false,
  superResolution: false,
  extractDetail: false,
  addWatermark: false
})
// 是否显示下载成功卡片
const showDownloadSuccess = ref(false)
// 下载成功消息
const downloadSuccessMessage = ref('')
// 下载是否成功（用于显示不同的样式）
const downloadIsSuccess = ref(true)

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

// 是否可以一键处理
const canProcess = computed(() => {
  if (isProcessing.value || sourceImages.value.length === 0) {
    return false
  }
  
  if (processType.value === 'model' && processSteps.value.faceSwap) {
    return modelImage.value !== null && modelImage.value !== undefined
  }
  
  return true
})

const hasResults = computed(() => processResults.value.length > 0)

// 监听加水印选项变化，取消选择时清空水印名称
watch(() => processSteps.value.addWatermark, (newValue) => {
  if (!newValue) {
    watermarkName.value = ''
  }
})

// 根据处理类型自动调整处理步骤
watch(processType, (newType) => {
  if (newType === 'model') {
    // 模特图：去水印、换脸、换背景、换姿态、自动裁剪
    processSteps.value = {
      watermark: true,
      faceSwap: true,
      backgroundSwap: true,
      poseSwap: true,
      autoCrop: true,
      extractReal: false,
      superResolution: false,
      extractDetail: false,
      addWatermark: false
    }
  } else {
    // 实拍图：去水印、换背景
    processSteps.value = {
      watermark: true,
      faceSwap: false,
      backgroundSwap: true,
      poseSwap: false,
      autoCrop: false,
      extractReal: false,
      superResolution: false,
      extractDetail: false,
      addWatermark: false
    }
  }
})


/**
 * 根据类型重置类型
 * @param type 
 */
const handleTypeChange = (type) => {
  processType.value = type
  
  // 清空已选择的图片
  sourceImages.value = []
  modelImage.value = null
  processResults.value = []
  processingProgress.value = 0
  isProcessing.value = false
}


/**
 * 将用户上传的文件夹中的图片转换为图片对象
 * 结果:{
      id: "随机生成的ID字符串",        
      file: File对象,                  
      preview: 本地预览URL       
    }
 */
 const handleSourceFolderUpload = (e) => {
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
  sourceImages.value.unshift(...newImages)
  
  // 重置 input，以便可以重复选择相同的文件
  if (e.target) {
    e.target.value = ''
  }
}



/**
 * 将用户上传的模特图片转换存储到数组中
 * 结果:{
      id: "abc123", 
      file: File对象, 
      preview: 本地预览URL
    }
 */
 const handleModelImageUpload = (e) => {
  const files = Array.from(e.target.files || [])
  files.forEach(file => {
    const id = Math.random().toString(36).substring(7)
    const preview = URL.createObjectURL(file)
    
    // 更新模型图片
    const newModel = {
      id,
      file,
      preview  // 使用本地预览URL
    }

    modelImage.value = newModel
    recentModels.value = [newModel, ...recentModels.value.filter(m => m.id !== newModel.id)].slice(0, 5)
  })
}


const selectModel = (image) => {
  modelImage.value = image
}




/**
 * 删除某张图片
 */
const removeSourceImage = (id) => {
  sourceImages.value = sourceImages.value.filter(img => img.id !== id)
}


/**
 * 一键处理图片
 */
const handleProcess = async () => {
  isProcessing.value = true
  processingProgress.value = 0
  processResults.value = []

  try {
    // 源图片获取真实URL
    const total = sourceImages.value.length
    // 存储源图片真实URL列表
    const sourceImageUrls = []
    
    // 上传源图片，模拟进度（上传阶段）
    processingProgress.value = 10
    for (let i = 0; i < total; i++) {      
      // 上传文件获取真实URL
      const imageUrl = await uploadFile(sourceImages.value[i].file)
      console.log("imageUrl", imageUrl)
      // 更新图片对象的真实URL
      sourceImages.value[i].preview = imageUrl
      sourceImageUrls.push(imageUrl)
      // 更新上传进度（10% - 30%）
      processingProgress.value = Math.round(10 + (i + 1) / total * 20)
    }

    // 模特图片获取真实URL
    let modelImageUrl = ''
    if (processSteps.value.faceSwap && modelImage.value) {
      // 上传文件获取真实URL
      modelImageUrl = await uploadFile(modelImage.value.file)
      console.log("modelImageUrl", modelImageUrl)
      // 更新模特图片对象的真实URL
      modelImage.value.preview = modelImageUrl
      // 更新上传进度（30% - 40%）
      processingProgress.value = 40
    } else {
      // 如果没有勾选换脸功能，直接跳到40%
      processingProgress.value = 40
    }

    // 构建处理配置对象
    const processConfig = {
      processType: processType.value,
      processSteps: processSteps.value,
      cropRatio: cropRatio.value,
      extractRealType: extractRealType.value,
      watermark_name: watermarkName.value ? watermarkName.value + '.png' : '',
    }

    console.log("processConfig", processConfig)

    // 调用后端接口处理图片（处理阶段进度：40% - 95%）
    processingProgress.value = 50
    
    // 使用定时器模拟处理进度
    const progressInterval = setInterval(() => {
      if (processingProgress.value < 95) {
        processingProgress.value = Math.min(processingProgress.value + 2, 95)
      }
    }, 500)

    try {
      // 调用后端接口
      const response = await executeImmediateTask(
        sourceImageUrls,
        processSteps.value.faceSwap ? modelImageUrl : null,
        processConfig
      )

      clearInterval(progressInterval)
      processingProgress.value = 100

      console.log("response", response)

      // 处理返回结果
      if (response.data && response.data.success) {
        const responseData = response.data.data
        const { results, success_count, failed_count } = responseData
        
        // 更新处理结果
        processResults.value = results.map(result => ({
          original_url: result.original_url,
          processed_url: result.processed_url,
          extract_real_url: result.extract_real_url,
          extract_detail_url: result.extract_detail_url,
          is_success: result.is_success
        }))

        // 输出最终统计结果
        console.log(`处理完成 - 成功: ${success_count}张, 失败: ${failed_count}张, 总计: ${total}张`)
      } else {
        throw new Error(response.data?.message || '处理失败')
      }
    } catch (apiError) {
      clearInterval(progressInterval)
      throw apiError
    }

  } catch (error) {
    alert(`处理过程中发生错误: ${error.message || '未知错误'}`)
    console.error('处理过程中发生错误:', error)
    processingProgress.value = 0
    processResults.value = []
  } finally {
    isProcessing.value = false
  }
}


/**
 * 下载处理结果 - 使用 FileSaver.js 下载图片
 */
const handleDownload = async () => {
  if (processResults.value.length === 0) return

  try {
    let successCount = 0
    let totalCount = 0

    // 下载所有图片
    for (let i = 0; i < processResults.value.length; i++) {
      const result = processResults.value[i]
      
      if (result.is_success) {
        // 下载效果图
        if (result.processed_url) {
          try {
            // 生成时间戳（包含毫秒，确保唯一性）
            const timestamp = dayjs().format('YYYYMMDDHHmmssSSS')
            const response = await fetch(result.processed_url)
            if (response.ok) {
              const blob = await response.blob()
              saveAs(blob, `效果图${timestamp}.jpg`)
              successCount++
              totalCount++
              
              // 添加延迟，避免浏览器阻止多个下载
              await new Promise(resolve => setTimeout(resolve, 300))
            }
          } catch (error) {
            console.error(`下载效果图 ${i + 1} 失败:`, error)
          }
        }

        // 下载实拍图（如果存在）
        if (result.extract_real_url) {
          try {
            // 生成时间戳（包含毫秒，确保唯一性）
            const timestamp = dayjs().format('YYYYMMDDHHmmssSSS')
            const response = await fetch(result.extract_real_url)
            if (response.ok) {
              const blob = await response.blob()
              saveAs(blob, `平铺图${timestamp}.jpg`)
              successCount++
              totalCount++
              
              // 添加延迟，避免浏览器阻止多个下载
              await new Promise(resolve => setTimeout(resolve, 300))
            }
          } catch (error) {
            console.error(`下载平铺图 ${i + 1} 失败:`, error)
          }
        }

        // 下载细节图（如果存在）
        if (result.extract_detail_url) {
          try {
            // 生成时间戳（包含毫秒，确保唯一性）
            const timestamp = dayjs().format('YYYYMMDDHHmmssSSS')
            const response = await fetch(result.extract_detail_url)
            if (response.ok) {
              const blob = await response.blob()
              saveAs(blob, `细节图${timestamp}.jpg`)
              successCount++
              totalCount++
              
              // 添加延迟，避免浏览器阻止多个下载
              await new Promise(resolve => setTimeout(resolve, 300))
            }
          } catch (error) {
            console.error(`下载细节图 ${i + 1} 失败:`, error)
          }
        }
      }
    }

    // 显示下载结果
    if (successCount > 0) {
      downloadIsSuccess.value = true
      downloadSuccessMessage.value = `成功下载 ${successCount} 个文件\n文件已保存到您的下载文件夹`
      showDownloadSuccess.value = true
    } else {
      downloadIsSuccess.value = false
      downloadSuccessMessage.value = '下载失败，请检查网络连接或重试'
      showDownloadSuccess.value = true
    }

  } catch (error) {
    console.error('下载过程中发生错误:', error)
    downloadIsSuccess.value = false
    downloadSuccessMessage.value = '下载失败，请重试'
    showDownloadSuccess.value = true
  }
}

/**
 * 关闭下载成功卡片
 */
const closeDownloadSuccess = () => {
  showDownloadSuccess.value = false
  downloadSuccessMessage.value = ''
}

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
