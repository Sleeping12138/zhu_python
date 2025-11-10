import { request } from '../utils/request.js'

/**
 * 保存批量任务到数据库
 * @param {*} tasks 
 * @returns {Promise<Object>} 保存结果
 */
export function saveBatchTasks(tasks) {
    return request.post('/batch_insert_tasks', JSON.stringify(tasks))
}

/**
 * 查询批量任务
 * @returns {Promise<Array>} 批量任务列表
 */
export function getBatchTasks() {
    return request.get('/get_batch_tasks')
}


/**
 * 立即执行处理任务
 * @param {Array<string>} sourceImageUrls - 源图片URL数组
 * @param {string|null} modelImageUrl - 模特图片URL（可选）
 * @param {Object} processConfig - 处理配置
 * @returns {Promise<Object>} 处理结果
 */
export function executeImmediateTask(sourceImageUrls, modelImageUrl, processConfig) {
    const requestData = {
        source_image_urls: sourceImageUrls,
        model_image_url: modelImageUrl || null,
        process_config: processConfig
    }

    return request.post('/execute_immediate_task', JSON.stringify(requestData))
}


/**
 * 创建定时任务
 * @param {Array<string>} sourceImageUrls - 源图片URL数组
 * @param {string|null} modelImageUrl - 模特图片URL（可选）
 * @param {Object} processConfig - 处理配置
 * @param {string} scheduledTime - 执行时间，格式：'YYYY-MM-DD HH:MM:SS'
 * @returns {Promise<Object>} 创建结果
 */
export function createScheduledTask(sourceImageUrls, modelImageUrl, processConfig, scheduledTime) {
    const requestData = {
        source_image_urls: sourceImageUrls,
        model_image_url: modelImageUrl || null,
        process_config: processConfig,
        scheduled_time: scheduledTime
    }

    return request.post('/create_scheduled_task', JSON.stringify(requestData))
}


/**
 * 获取所有定时任务
 * @returns {Promise<Array>} 定时任务列表
 */
export function getScheduledTasks() {
    return request.get('/get_scheduled_tasks')
}


/**
 * 删除定时任务
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>} 删除结果
 */
export function deleteScheduledTask(taskId) {
    return request.delete(`/delete_scheduled_task/${taskId}`)
}


/**
 * 生成虚拟试衣图片
 * @param {string} modelImage - 模特图片URL
 * @param {string} clothingImage - 实拍图片URL
 * @param {string} modelClothingType - 模特图衣服类型
 * @param {string} clothingClothingType - 实拍图衣服类型
 * @returns {Promise<Object>} 生成结果
 */
export function generateVirtualTryon(modelImage, clothingImage, modelClothingType, clothingClothingType) {
    const requestData = {
        image_url_1: modelImage,
        image_url_2: clothingImage,
        clothes_1_type: modelClothingType,
        clothes_2_type: clothingClothingType
    }

    return request.post('/virtual_tryon', JSON.stringify(requestData))
}