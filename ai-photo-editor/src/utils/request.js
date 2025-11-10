import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
    baseURL: 'http://14.103.147.199:5015',
    // baseURL: 'http://127.0.0.1:8000',
    // timeout: 30000,
    headers: {
        'Content-Type': 'application/json;charset=UTF-8'
    }
})

export { request }
