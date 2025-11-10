import { request } from './request.js'

/**
 * 上传单个文件并获取真实URL
 * @param {File} file - 要上传的文件
 * @returns {Promise<string>} - 返回上传后的真实URL
 */
export const uploadFile = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await request.post('/upload_image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })

    if (!response.data.success) {
        throw new Error(response.data.message || '上传文件失败')
    }

    return response.data.data.fileUrl
}

