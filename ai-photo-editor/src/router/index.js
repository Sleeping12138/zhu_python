import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import BatchProcess from '../components/BatchProcess.vue'
import ScheduledProcess from '../components/ScheduledProcess.vue'
import VirtualTryon from '../components/VirtualTryon.vue'
import History from '../components/History.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
            title: '用户登录',
            isLoginPage: true
        }
    },
    {
        path: '/batch',
        name: 'BatchProcess',
        component: BatchProcess,
        meta: {
            title: '批量处理'
        }
    },
    {
        path: '/scheduled',
        name: 'ScheduledProcess',
        component: ScheduledProcess,
        meta: {
            title: '定时处理'
        }
    },
    {
        path: '/virtual-tryon',
        name: 'VirtualTryon',
        component: VirtualTryon,
        meta: {
            title: '虚拟试衣'
        }
    },
    {
        path: '/history',
        name: 'History',
        component: History,
        meta: {
            title: '历史记录'
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫：登录检查和设置页面标题
router.beforeEach((to, from, next) => {
    // 设置页面标题
    if (to.meta.title) {
        document.title = `${to.meta.title} - AI修图平台`
    }

    // 检查登录状态
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    const isLoginPage = to.meta.isLoginPage === true

    // 如果已登录，检查登录时间是否过期（一天 = 24小时 = 86400000毫秒）
    if (isLoggedIn) {
        const loginTime = localStorage.getItem('loginTime')
        if (loginTime) {
            const now = Date.now()
            const oneDay = 24 * 60 * 60 * 1000 // 一天的毫秒数
            const timeDiff = now - parseInt(loginTime)

            // 如果超过一天，清除登录状态
            if (timeDiff > oneDay) {
                localStorage.removeItem('isLoggedIn')
                localStorage.removeItem('username')
                localStorage.removeItem('loginTime')

                // 如果访问的不是登录页面，重定向到登录页
                if (!isLoginPage) {
                    next('/login')
                    return
                }
            }
        } else {
            // 如果没有登录时间，清除登录状态
            localStorage.removeItem('isLoggedIn')
            localStorage.removeItem('username')
            localStorage.removeItem('loginTime')
        }
    }

    // 重新获取登录状态（可能已被清除）
    const currentIsLoggedIn = localStorage.getItem('isLoggedIn') === 'true'

    // 如果未登录且不是访问登录页面，重定向到登录页
    if (!currentIsLoggedIn && !isLoginPage) {
        next('/login')
        return
    }

    // 如果已登录且访问登录页面，重定向到批量处理页面
    if (currentIsLoggedIn && isLoginPage) {
        next('/batch')
        return
    }

    next()
})

export default router
