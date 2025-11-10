<template>
  <div class="space-y-4 sm:space-y-6">


    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-0">
      <h2 class="text-lg sm:text-xl md:text-2xl font-bold text-gray-800">定时处理</h2>
      <button
        @click="startCreating"
        class="flex items-center gap-1.5 sm:gap-2 px-3 py-1.5 sm:px-4 sm:py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm sm:text-base w-full sm:w-auto justify-center"
      >
        <Plus class="w-4 h-4 sm:w-5 sm:h-5" />
        新建任务
      </button>
    </div>


    <div v-if="isCreating" class="space-y-4 sm:space-y-6">
      <div class="flex justify-between items-center">
        <h3 class="text-base sm:text-lg font-semibold text-gray-800">创建定时任务</h3>
        <button
          @click="cancelCreate"
          class="w-7 h-7 sm:w-8 sm:h-8 bg-gray-200 hover:bg-gray-300 rounded-lg flex items-center justify-center transition-colors duration-300"
        >
          <X class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-gray-600" />
        </button>
      </div>


      <!-- 上传源图片文件夹 -->
      <div class="rounded-xl p-3 sm:p-4 border border-gray-200">
        <div class="flex items-center gap-2 mb-2 sm:mb-3">
          <div class="w-5 h-5 sm:w-6 sm:h-6 bg-blue-500 rounded flex items-center justify-center">
            <Folder class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
          </div>
          <label class="text-sm sm:text-base font-semibold text-gray-800">上传源图片文件夹</label>
        </div>
        <div class="flex gap-2 sm:gap-3 overflow-x-auto pb-2">
          <!-- 上传框 -->
          <div class="relative flex-shrink-0">
            <div 
              class="border-2 border-dashed border-blue-300 rounded-xl w-20 h-20 sm:w-24 sm:h-24 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors group"
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
              <div class="flex flex-col items-center gap-1 text-blue-400 group-hover:text-blue-600 transition-colors pointer-events-none">
                <Folder class="w-5 h-5 sm:w-6 sm:h-6" />
                <span class="text-xs font-medium">上传文件夹</span>
              </div>
            </div>
          </div>

          <!-- 预览源图片 -->
          <div
            v-for="img in sourceImages"
            :key="img.id"
            class="relative group flex-shrink-0"
          >
            <div class="border-2 border-gray-200 rounded-xl w-20 h-20 sm:w-24 sm:h-24 overflow-hidden">
              <img 
                :src="img.preview" 
                alt="source" 
                class="w-full h-full object-contain bg-gray-50" 
              />
            </div>
            <button
              @click="removeSourceImage(img.id)"
              class="absolute inset-0 bg-red-200/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-300/70 rounded-xl"
            >
              <X class="w-4 h-4 sm:w-5 sm:h-5 text-red-600" />
            </button>
          </div>
        </div>
        <p v-if="sourceImages.length > 0" class="text-xs text-blue-600 font-medium mt-2 flex items-center gap-2">
          <span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
          已选择 {{ sourceImages.length }} 张图片
        </p>
        <p class="text-xs text-red-300 mt-1">建议一次性上传图片张数小于10</p>
      </div>


      <!-- 上传模特图片 -->
      <div 
        v-if="processType === 'model'" 
        :class="[
          'rounded-xl p-4 border transition-all relative',
          processSteps.faceSwap 
            ? 'border-gray-200' 
            : 'border-gray-300 bg-gray-100/50 opacity-60'
        ]"
      >
        <!-- 禁用遮罩层 -->
        <div 
          v-if="!processSteps.faceSwap"
          class="absolute inset-0 bg-gray-200/30 backdrop-blur-[1px] rounded-xl z-10 cursor-not-allowed"
        ></div>

        <div class="flex items-center gap-2 mb-3 relative z-0">
          <div 
            :class="[
              'w-6 h-6 rounded flex items-center justify-center',
              processSteps.faceSwap ? 'bg-purple-500' : 'bg-gray-400'
            ]"
          >
            <User class="w-4 h-4 text-white" />
          </div>
          <label 
            :class="[
              'text-base font-semibold',
              processSteps.faceSwap ? 'text-gray-800' : 'text-gray-500'
            ]"
          >
            上传模特图片（换脸）
          </label>
        </div>
        <div class="flex gap-3 overflow-x-auto pb-2 relative z-0">
          <!-- 上传框 -->
          <div class="relative flex-shrink-0">
            <div 
              :class="[
                'border-2 border-dashed rounded-xl w-24 h-24 flex flex-col items-center justify-center transition-colors group',
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
                  'flex flex-col items-center gap-1 transition-colors pointer-events-none',
                  processSteps.faceSwap
                    ? 'text-purple-400 group-hover:text-purple-600'
                    : 'text-gray-400'
                ]"
              >
                <User class="w-6 h-6" />
                <span class="text-xs font-medium">上传模特</span>
              </div>
            </div>
          </div>

          <!-- 最近5个模特图片 -->
          <div
            v-for="img in recentModels"
            :key="img.id"
            @click="processSteps.faceSwap ? selectModel(img) : null"
            :class="[
              'relative border-2 rounded-xl flex-shrink-0 transition-colors',
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
            <div class="w-24 h-24 overflow-hidden rounded-lg">
              <img :src="img.preview" alt="model" class="w-full h-full object-contain bg-gray-50" />
            </div>
            <div v-if="modelImage?.id === img.id && processSteps.faceSwap" class="absolute -top-1 -right-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full p-1">
              <ImageIcon class="w-3 h-3" />
            </div>
          </div>
        </div>
        <p 
          v-if="recentModels.length > 0" 
          :class="[
            'text-xs font-medium mt-2 flex items-center gap-2 relative z-0',
            processSteps.faceSwap ? 'text-purple-600' : 'text-gray-400'
          ]"
        >
          <span 
            :class="[
              'w-1.5 h-1.5 rounded-full',
              processSteps.faceSwap ? 'bg-purple-500 animate-pulse' : 'bg-gray-400'
            ]"
          ></span>
          最近使用（点击切换模特）
        </p>
      </div>


      <!-- 执行时间设置 -->
      <div class="rounded-xl p-3 sm:p-4 border border-gray-200">
        <div class="flex items-center gap-2 mb-2 sm:mb-3">
          <div class="w-5 h-5 sm:w-6 sm:h-6 bg-orange-500 rounded flex items-center justify-center">
            <Clock class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
          </div>
          <label class="text-sm sm:text-base font-semibold text-gray-800">执行时间</label>
        </div>
        <div class="space-y-2 sm:space-y-3">
          <div class="flex gap-2 sm:gap-3 items-center">
            <button
              @click="executionMode = 'immediate'"
              :class="[
                'px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors',
                executionMode === 'immediate'
                  ? 'bg-orange-600 text-white hover:bg-orange-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              立即执行
            </button>
            <button
              @click="executionMode = 'scheduled'"
              :class="[
                'px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors',
                executionMode === 'scheduled'
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              定时任务
            </button>
          </div>
          <div v-if="executionMode === 'scheduled'" class="flex gap-2 sm:gap-3 items-center">
            <div class="relative flex-shrink-0 w-full sm:w-auto">
              <input
                type="datetime-local"
                v-model="scheduledDateTime"
                :min="getMinDateTime()"
                class="w-full sm:w-48 px-2 py-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
          </div>
          <p v-if="executionMode === 'immediate'" class="text-xs text-orange-600 font-medium">任务将在确认后立即执行</p>
          <p v-else-if="executionMode === 'scheduled'" class="text-xs text-gray-500">选择执行日期和时间</p>
        </div>
      </div>


      <!-- 处理步骤选择 -->
      <div class="rounded-xl p-3 sm:p-4 border border-gray-200">
        <div class="flex items-center gap-2 mb-2 sm:mb-3">
          <div class="w-5 h-5 sm:w-6 sm:h-6 bg-green-500 rounded flex items-center justify-center">
            <Settings class="w-3 h-3 sm:w-4 sm:h-4 text-white" />
          </div>
          <h3 class="text-sm sm:text-base font-semibold text-gray-800">处理配置</h3>
        </div>
        
        <div class="space-y-2 sm:space-y-3">
          <div>
            <label class="block text-xs sm:text-sm font-semibold text-gray-800 mb-2">处理类型</label>
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
                  <div class="flex items-center gap-4 p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-pink-100">
                    <label class="flex items-center gap-2 cursor-pointer group flex-1">
                      <input
                        type="checkbox"
                        v-model="processSteps.autoCrop"
                        class="w-4 h-4 text-pink-600 rounded focus:ring-pink-500"
                      />
                      <span class="text-sm font-medium text-gray-700 group-hover:text-pink-600 transition-colors">自动裁剪</span>
                    </label>
                    <div v-if="processSteps.autoCrop" class="flex-shrink-0">
                      <select
                        v-model="cropRatio"
                        class="px-3 py-2 text-sm border-2 border-pink-200 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-400 bg-white shadow-sm transition-all min-w-[120px]"
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
                  <div class="flex items-center gap-4 p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-red-100">
                    <label class="flex items-center gap-2 cursor-pointer group flex-1">
                      <input
                        type="checkbox"
                        v-model="processSteps.extractReal"
                        class="w-4 h-4 text-red-600 rounded focus:ring-red-500"
                      />
                      <span class="text-sm font-medium text-gray-700 group-hover:text-red-600 transition-colors">提取实拍图</span>
                    </label>
                    <div v-if="processSteps.extractReal" class="flex-shrink-0">
                      <select
                        v-model="extractRealType"
                        class="px-3 py-2 text-sm border-2 border-red-200 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-400 bg-white shadow-sm transition-all min-w-[120px]"
                      >
                        <option value="上装">上装</option>
                        <option value="下装">下装</option>
                        <option value="裙装">裙装</option>
                      </select>
                    </div>
                  </div>
                </template>
                <!-- 加水印 -->
                <div class="flex items-center gap-4 p-3 rounded-lg bg-white/80 hover:bg-white hover:shadow-md transition-all duration-300 border border-cyan-100">
                  <label class="flex items-center gap-2 cursor-pointer group flex-1">
                    <input
                      type="checkbox"
                      v-model="processSteps.addWatermark"
                      class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500"
                    />
                    <span class="text-sm font-medium text-gray-700 group-hover:text-cyan-600 transition-colors">加水印</span>
                  </label>
                  <div v-if="processSteps.addWatermark" class="flex-shrink-0">
                    <select
                      v-model="watermarkName"
                      class="px-3 py-2 text-sm border-2 border-cyan-200 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-400 bg-white shadow-sm transition-all min-w-[160px]"
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


      <div class="flex gap-2 sm:gap-3 md:gap-4">
        <button
          @click="handleCreateTask"
          :disabled="sourceImages.length === 0 || (processType === 'model' && processSteps.faceSwap && !modelImage)"
          class="flex-1 px-4 py-2 sm:px-6 sm:py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm sm:text-base"
        >
          确认
        </button>
        <button
          @click="cancelCreate"
          class="px-4 py-2 sm:px-6 sm:py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm sm:text-base"
        >
          取消
        </button>
      </div>
    </div>


    <!-- 任务列表 -->
    <div class="space-y-4">
      <div v-if="scheduledTasks.length === 0 && !isCreating" class="text-center py-16">
        <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 mb-6">
          <Clock class="w-12 h-12 text-indigo-400" />
        </div>
        <p class="text-lg font-semibold text-gray-600 mb-2">暂无定时任务</p>
        <p class="text-sm text-gray-400">点击上方"新建任务"按钮创建定时处理任务</p>
      </div>
      <div v-else-if="scheduledTasks.length > 0" class="space-y-4">
        <div
          v-for="task in scheduledTasks"
          :key="task.id"
          class="relative bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group"
        >
          <div class="p-3 sm:p-4 md:p-5">
            <!-- 头部信息 -->
            <div class="flex flex-col sm:flex-row justify-between items-start gap-3 sm:gap-0 mb-3 sm:mb-4">
              <div class="flex-1 w-full sm:w-auto">
                <!-- 执行时间 -->
                <div class="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-3">
                  <div class="flex items-center justify-center w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500 flex-shrink-0">
                    <Clock class="w-4 h-4 sm:w-4.5 sm:h-4.5 md:w-5 md:h-5 text-white" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs text-gray-500 font-medium mb-0.5 sm:mb-1">执行时间</p>
                    <p class="text-sm sm:text-base font-semibold text-gray-800 break-words">{{ formatTaskTime(task.scheduledTime) }}</p>
                  </div>
                </div>

                <!-- 任务信息统计 -->
                <div class="flex flex-wrap items-center gap-2 sm:gap-3 md:gap-4 ml-0 sm:ml-[36px] md:ml-[52px]">
                  <div v-if="task.sourceImages && task.sourceImages.length > 0" class="flex items-center gap-1.5 sm:gap-2">
                    <div class="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-blue-400 flex-shrink-0"></div>
                    <span class="text-xs sm:text-sm text-gray-600 whitespace-nowrap">
                      <span class="font-semibold text-gray-800">{{ task.sourceImages.length }}</span> 张源图片
                    </span>
                  </div>
                  <div v-if="task.modelImagePreview" class="flex items-center gap-1.5 sm:gap-2">
                    <div class="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-purple-400 flex-shrink-0"></div>
                    <span class="text-xs sm:text-sm text-gray-600 whitespace-nowrap">模特图片</span>
                  </div>
                  <div v-if="task.processType" class="flex items-center gap-1.5 sm:gap-2">
                    <div class="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-green-400 flex-shrink-0"></div>
                    <span class="text-xs sm:text-sm text-gray-600 whitespace-nowrap">
                      {{ task.processType === 'model' ? '模特图' : '实拍图' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 状态和操作按钮 -->
              <div class="flex items-center gap-2 sm:gap-3 w-full sm:w-auto justify-end sm:justify-start">
                <div :class="[
                  'inline-flex items-center gap-1.5 sm:gap-2 px-2.5 py-1.5 sm:px-3 sm:py-1.5 md:px-4 md:py-2 rounded-lg text-xs sm:text-sm font-medium shadow-sm',
                  getStatusClass(task.status)
                ]">
                  <div :class="[
                    'w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full flex-shrink-0',
                    task.status === 'completed' ? 'bg-green-500' :
                    task.status === 'processing' ? 'bg-blue-500 animate-pulse' :
                    task.status === 'failed' ? 'bg-red-500' :
                    'bg-yellow-500'
                  ]"></div>
                  <span class="whitespace-nowrap">{{ getStatusText(task.status) }}</span>
                </div>
                <button
                  @click="deleteTask(task.id)"
                  class="w-8 h-8 sm:w-9 sm:h-9 bg-gray-100 hover:bg-red-100 text-gray-600 hover:text-red-600 rounded-lg flex items-center justify-center transition-all duration-200 shadow-sm hover:shadow flex-shrink-0"
                  title="删除任务"
                >
                  <X class="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                </button>
              </div>
            </div>

            <div class="border-t border-gray-100 pt-3 sm:pt-4 mt-3 sm:mt-4 space-y-3 sm:space-y-4">
              <!-- 源图片 -->
              <div v-if="task.sourceImages && task.sourceImages.length > 0">
                <div class="flex items-center gap-1.5 sm:gap-2 mb-2 sm:mb-3">
                  <Folder class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-500 flex-shrink-0" />
                  <p class="text-xs sm:text-sm font-semibold text-gray-700">源图片</p>
                  <span class="text-xs text-gray-500 bg-blue-50 px-1.5 sm:px-2 py-0.5 rounded-full">({{ task.sourceImages.length }})</span>
                </div>
                <div class="flex gap-2 sm:gap-3 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
                  <div
                    v-for="img in task.sourceImages"
                    :key="img.id"
                    class="relative flex-shrink-0 group/image"
                  >
                    <div 
                      class="border-2 border-gray-200 rounded-xl w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 overflow-hidden shadow-sm group-hover/image:border-blue-400 transition-all duration-200 cursor-pointer sm:cursor-default"
                      @click="openPhotoSwipe(task.sourceImages.map(i => i.preview), task.sourceImages.findIndex(i => i.id === img.id))"
                    >
                      <img 
                        :src="img.preview" 
                        alt="source" 
                        class="w-full h-full object-cover bg-gray-50 group-hover/image:scale-105 transition-transform duration-200" 
                      />
                    </div>
                  </div>
                </div>
              </div>

              <!-- 模特图片 -->
              <div v-if="task.modelImagePreview">
                <div class="flex items-center gap-1.5 sm:gap-2 mb-2 sm:mb-3">
                  <User class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-purple-500 flex-shrink-0" />
                  <p class="text-xs sm:text-sm font-semibold text-gray-700">模特图片</p>
                </div>
                <div 
                  class="inline-block border-2 border-purple-200 rounded-xl overflow-hidden shadow-sm hover:border-purple-400 transition-all duration-200 cursor-pointer sm:cursor-default"
                  @click="openPhotoSwipe([task.modelImagePreview], 0)"
                >
                  <img 
                    :src="task.modelImagePreview" 
                    alt="model" 
                    class="w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28 object-cover bg-gray-50 hover:scale-105 transition-transform duration-200" 
                  />
                </div>
              </div>

              <!-- 处理步骤 -->
              <div v-if="task.processSteps && Object.values(task.processSteps).some(v => v)">
                <div class="flex items-center gap-1.5 sm:gap-2 mb-2 sm:mb-3">
                  <Settings class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-green-500 flex-shrink-0" />
                  <p class="text-xs sm:text-sm font-semibold text-gray-700">处理步骤</p>
                </div>
                <div class="flex flex-wrap gap-1.5 sm:gap-2">
                  <span v-if="task.processSteps.watermark" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-blue-50 text-blue-700 rounded-lg text-xs font-medium border border-blue-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0"></div>
                    去水印
                  </span>
                  <span v-if="task.processSteps.faceSwap" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-purple-50 text-purple-700 rounded-lg text-xs font-medium border border-purple-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-purple-500 flex-shrink-0"></div>
                    换脸
                  </span>
                  <span v-if="task.processSteps.backgroundSwap" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-green-50 text-green-700 rounded-lg text-xs font-medium border border-green-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-green-500 flex-shrink-0"></div>
                    换背景
                  </span>
                  <span v-if="task.processSteps.poseSwap" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-yellow-50 text-yellow-700 rounded-lg text-xs font-medium border border-yellow-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-yellow-500 flex-shrink-0"></div>
                    换姿态
                  </span>
                  <span v-if="task.processSteps.autoCrop" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-pink-50 text-pink-700 rounded-lg text-xs font-medium border border-pink-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-pink-500 flex-shrink-0"></div>
                    自动裁剪
                    <span v-if="task.cropRatio" class="text-pink-600 font-bold">({{ task.cropRatio }})</span>
                  </span>
                  <span v-if="task.processSteps.extractReal" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-red-50 text-red-700 rounded-lg text-xs font-medium border border-red-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-red-500 flex-shrink-0"></div>
                    提取实拍图
                    <span v-if="task.extractRealType" class="text-red-600 font-bold">({{ task.extractRealType }})</span>
                  </span>
                  <span v-if="task.processSteps.superResolution" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-indigo-50 text-indigo-700 rounded-lg text-xs font-medium border border-indigo-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0"></div>
                    超分
                  </span>
                  <span v-if="task.processSteps.extractDetail" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-teal-50 text-teal-700 rounded-lg text-xs font-medium border border-teal-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-teal-500 flex-shrink-0"></div>
                    提取细节图
                  </span>
                  <span v-if="task.processSteps.addWatermark" class="inline-flex items-center gap-1 sm:gap-1.5 px-2 py-1 sm:px-2.5 sm:py-1.5 bg-cyan-50 text-cyan-700 rounded-lg text-xs font-medium border border-cyan-200 shadow-sm">
                    <div class="w-1.5 h-1.5 rounded-full bg-cyan-500 flex-shrink-0"></div>
                    加水印
                  </span>
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

  <!-- 加载蒙版 -->
  <div 
    v-if="isLoading" 
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-xl p-8 flex flex-col items-center gap-4 shadow-2xl">
      <div class="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-lg font-semibold text-gray-800">加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Upload, Clock, Download, X, Image as ImageIcon, Plus, Folder, User, Settings } from 'lucide-vue-next'
import dayjs from 'dayjs'
import { createScheduledTask, getScheduledTasks, deleteScheduledTask } from '../api/sqlApi.js'
import { uploadFile } from '../utils/uploadUtils.js'
import PhotoSwipeViewer from './PhotoSwipeViewer.vue'

/**
 * 获取默认值：明天凌晨1点
 */
const getDefaultDateTime = () => {
  return dayjs().add(1, 'day').hour(1).minute(0).second(0).millisecond(0).format('YYYY-MM-DDTHH:mm')
}

// 获取当前时间的ISO格式，用于限制最小值
const getMinDateTime = () => {
  return dayjs().second(0).millisecond(0).format('YYYY-MM-DDTHH:mm') // 格式: YYYY-MM-DDTHH:mm
}

// 定时任务列表
const scheduledTasks = ref([])
// 是否正在创建任务
const isCreating = ref(false)
// 是否正在加载
const isLoading = ref(false)
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
// 水印名称（从下拉框选择）
const watermarkName = ref('')
// 处理类型（'model' 为模特图, 其它为实拍图）
const processType = ref('model')
// 自动裁剪比例
const cropRatio = ref('3:4')
// 实拍类型（如"上装"、"下装"等）
const extractRealType = ref('上装')
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
// 执行时间（用于表单绑定）
const scheduledDateTime = ref(getDefaultDateTime())
// 执行模式：'immediate' 立即执行，'scheduled' 定时任务
const executionMode = ref('immediate')

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
 * 根据类型重置选项
 */
const handleTypeChange = (type) => {
  processType.value = type
  if (type === 'model') {
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
}

// 监听加水印选项变化，取消选择时清空水印名称
watch(() => processSteps.value.addWatermark, (newValue) => {
  if (!newValue) {
    watermarkName.value = ''
  }
})


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
    const preview = URL.createObjectURL(file)
    return {
      id,
      file,
      preview
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
    
    const newModel = {
      id,
      file,
      preview
    }

    modelImage.value = newModel
    recentModels.value = [newModel, ...recentModels.value.filter(m => m.id !== newModel.id)].slice(0, 5)
  })
}


/**
 * 选择模特图片
 * @param {Object} image - 模特图片对象
 */
const selectModel = (image) => {
  modelImage.value = image
}



/**
 * 删除源图片
 * @param {string} id - 源图片ID
 */
const removeSourceImage = (id) => {
  sourceImages.value = sourceImages.value.filter(img => img.id !== id)
}


/**
 * 新建任务
 */
const startCreating = () => {
  isCreating.value = true
}


/**
 * 确认按钮逻辑
 */
 const handleCreateTask = async () => {
  try {
    // 如果选择了立即执行，创建下一分钟整点的定时任务
    if (executionMode.value === 'immediate') {
      const currentTime = dayjs().add(1, 'minute').second(0).millisecond(0).format('YYYY-MM-DD HH:mm:ss')
      await handleScheduledTask(currentTime)
    } else {
      // 定时任务，使用表单选择的时间
      await handleScheduledTask()
    }

    // 重置表单
    resetForm()
    isCreating.value = false
  } catch (error) {
    // 错误已在各自的处理函数中显示，这里不需要额外处理
    console.error('创建任务失败:', error)
  }
}




/**
 * 定时任务处理逻辑
 * @param {string} customTime - 自定义执行时间，格式：'YYYY-MM-DD HH:mm:ss'
 */
const handleScheduledTask = async (customTime = null) => {
  // 从方法一开始就显示加载蒙版
  isLoading.value = true
  try {
    // 获取执行时间：如果传入了自定义时间则使用自定义时间，否则使用表单中的时间
    const scheduledTime = customTime || dayjs(scheduledDateTime.value).format('YYYY-MM-DD HH:mm:ss')

    // 如果使用表单时间，判断时间是否合法
    if (!customTime && scheduledTime < dayjs().format('YYYY-MM-DD HH:mm:ss')) {
      throw new Error('执行时间不能早于当前时间')
    }
    
    // 上传源图片
    const sourceImageUrls = []
    for (let i = 0; i < sourceImages.value.length; i++) {
      try {
        const imageUrl = await uploadFile(sourceImages.value[i].file)
        console.log(`源图片上传成功:`, imageUrl)
        sourceImageUrls.push(imageUrl)
      } catch (error) {
        console.error(`源图片上传失败:`, error)
        throw new Error(`源图片上传失败: ${error.message}`)
      }
    }

    // 上传模特图片（只有在勾选了换脸功能时才上传）
    let modelImageUrl = null
    if (processSteps.value.faceSwap && modelImage.value) {
      try {
        modelImageUrl = await uploadFile(modelImage.value.file)
        console.log('模特图片上传成功:', modelImageUrl)
      } catch (error) {
        console.error('模特图片上传失败:', error)
        throw new Error(`模特图片上传失败: ${error.message}`)
      }
    }

    // 封装配置
    const processConfig = {
      processType: processType.value,
      processSteps: processSteps.value,
      cropRatio: cropRatio.value,
      extractRealType: extractRealType.value,
      watermark_name: watermarkName.value ? watermarkName.value + '.png' : '',
    }

    // 调用后端接口
    const response = await createScheduledTask(sourceImageUrls, modelImageUrl, processConfig, scheduledTime)
    
    console.log('response', response)

    if (response.data.success) {
      const taskId = response.data.data.task_id

      // 重新加载任务列表
      await loadScheduledTasks()
      console.log('定时任务已创建:', taskId)
    } else {
      throw new Error(response.data.message || '创建定时任务失败')
    }
  } catch (error) {
    alert(`创建定时任务失败: ${error.message}`)
    console.error('创建定时任务失败:', error)
    throw error
  } finally {
    // 确保无论成功还是失败都隐藏加载蒙版
    isLoading.value = false
  }
}


/**
 * 加载定时任务列表
 */
const loadScheduledTasks = async () => {
  try {
    const response = await getScheduledTasks()
    console.log('response', response)
    if (response.data.success) {
      // 将后端返回的任务列表转换为前端需要的格式
      const tasks = response.data.data.tasks.map(task => {
        const taskId = task.task_id
        
        // 转换 scheduled_time 格式用于显示
        let scheduledTime = task.scheduled_time
        if (scheduledTime) {
          // 将数据库格式转换为 datetime-local 需要的格式
          scheduledTime = dayjs(scheduledTime).format('YYYY-MM-DDTHH:mm')
        }
        
        // 从后端数据构建 sourceImages
        const sourceImages = (task.source_image_urls || []).map((url, index) => ({
          id: `source_${taskId}_${index}`,
          preview: url
        }))
        
        // 从 process_config 获取配置信息
        const processConfig = task.process_config || {}
        
        return {
          id: taskId,
          task_id: taskId,
          scheduledTime: scheduledTime,
          next_run_time: task.next_run_time,
          status: task.status || 'pending',
          sourceImages: sourceImages,
          modelImage: task.model_image_url ? {
            id: `model_${taskId}`,
            preview: task.model_image_url
          } : null,
          modelImagePreview: task.model_image_url || null,
          processSteps: processConfig.processSteps || {},
          cropRatio: processConfig.cropRatio,
          extractRealType: processConfig.extractRealType,
          processType: processConfig.processType || 'model'
        }
      })
      
      scheduledTasks.value = tasks
      console.log('scheduledTasks', scheduledTasks.value)
    } else {
      console.error('获取定时任务失败:', response.data.message)
    }
  } catch (error) {
    console.error('获取定时任务失败:', error)
  }
}

/**
 * 格式化任务时间
 * @param {string} timeStr - 时间字符串
 * @returns {string} 格式化后的时间
 */
const formatTaskTime = (timeStr) => {
  if (!timeStr) return '未知'
  try {
    const date = dayjs(timeStr)
    return date.format('YYYY年M月D日 HH:mm')
  } catch (error) {
    return timeStr
  }
}

/**
 * 获取状态文本
 * @param {string} status - 任务状态
 * @returns {string} 状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    'pending': '等待中',
    'processing': '执行中',
    'completed': '已完成',
    'failed': '失败'
  }
  return statusMap[status] || '未知'
}

/**
 * 获取状态样式类
 * @param {string} status - 任务状态
 * @returns {string} 样式类
 */
const getStatusClass = (status) => {
  const classMap = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'processing': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'failed': 'bg-red-100 text-red-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

/**
 * 删除任务
 * @param {string} taskId - 任务ID
 */
const deleteTask = async (taskId) => {
  try {
    const response = await deleteScheduledTask(taskId)
    
    if (response.data.success) {
      // 从组件状态中删除
      scheduledTasks.value = scheduledTasks.value.filter(t => t.id !== taskId)
      
      console.log('已删除任务:', taskId)
    } else {
      throw new Error(response.data.message || '删除任务失败')
    }
  } catch (error) {
    alert(`删除任务失败: ${error.message}`)
    console.error('删除任务失败:', error)
  }
}

// 组件挂载时加载定时任务列表
onMounted(() => {
  loadScheduledTasks()
})


/**
 * 取消创建任务
 */
const cancelCreate = () => {
  resetForm()
  isCreating.value = false
}


/**
 * 重置表单
 */
const resetForm = () => {
  sourceImages.value = []
  modelImage.value = null
  recentModels.value = []
  watermarkName.value = ''
  scheduledDateTime.value = getDefaultDateTime()
  executionMode.value = 'immediate'
  processType.value = 'model'
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
  cropRatio.value = '3:4'
  extractRealType.value = '上装'
}
</script>
