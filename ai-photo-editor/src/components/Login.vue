<template>
  <div class="login-page">
    <div class="svg-top">
      <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="1337"
        width="1337">
        <defs>
          <path id="path-1" opacity="1" fill-rule="evenodd"
            d="M1337,668.5 C1337,1037.455193874239 1037.455193874239,1337 668.5,1337 C523.6725684305388,1337 337,1236 370.50000000000006,1094 C434.03835568300906,824.6732385973953 6.906089672974592e-14,892.6277623047779 0,668.5000000000001 C0,299.5448061257611 299.5448061257609,1.1368683772161603e-13 668.4999999999999,0 C1037.455193874239,0 1337,299.544806125761 1337,668.5Z" />
          <linearGradient id="linearGradient-2" x1="0.79" y1="0.62" x2="0.21" y2="0.86">
            <stop offset="0" stop-color="rgb(255,107,157)" stop-opacity="1" />
            <stop offset="1" stop-color="rgb(255,182,193)" stop-opacity="1" />
          </linearGradient>
        </defs>
        <g opacity="1">
          <use xlink:href="#path-1" fill="url(#linearGradient-2)" fill-opacity="1" />
        </g>
      </svg>
    </div>
    <div class="svg-bottom">
      <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="896"
        width="967.8852157128662">
        <defs>
          <path id="path-2" opacity="1" fill-rule="evenodd"
            d="M896,448 C1142.6325445712241,465.5747656464056 695.2579309733121,896 448,896 C200.74206902668806,896 5.684341886080802e-14,695.2579309733121 0,448.0000000000001 C0,200.74206902668806 200.74206902668791,5.684341886080802e-14 447.99999999999994,0 C695.2579309733121,0 475,418 896,448Z" />
          <linearGradient id="linearGradient-3" x1="0.5" y1="0" x2="0.5" y2="1">
            <stop offset="0" stop-color="rgb(255,182,193)" stop-opacity="1" />
            <stop offset="1" stop-color="rgb(219,112,147)" stop-opacity="1" />
          </linearGradient>
        </defs>
        <g opacity="1">
          <use xlink:href="#path-2" fill="url(#linearGradient-3)" fill-opacity="1" />
        </g>
      </svg>
    </div>

    <section class="container">
      <section class="wrapper">
        <header>
          <div class="logo">
            <img src="/static/yishou.jpg" alt="Logo" />
          </div>
          <h1>Welcome to YiShou</h1>
          <p>User Login</p>
        </header>
        <section class="main-content">
          <form @submit.prevent="handleLogin">
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20.59 22C20.59 18.13 16.74 15 12 15C7.26 15 3.41 18.13 3.41 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input v-model="username" type="text" placeholder="用户名" required class="input-field">
              <div class="input-line"></div>
            </div>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 11V7C7 4.23858 9.23858 2 12 2C14.7614 2 17 4.23858 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input v-model="password" type="password" placeholder="密码" required class="input-field">
              <div class="input-line"></div>
            </div>
            <button type="submit" :disabled="isLoading" class="login-button">
              <span v-if="!isLoading">登录</span>
              <span v-else class="loading-spinner"></span>
            </button>
          </form>
          <transition name="fade">
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>
          </transition>
        </section>
        <footer>
          <p><a href="#" @click.prevent="handleForgotPassword" title="Forgot Password">忘记密码?</a></p>
          <p><a href="#" @click.prevent="handleRegister" title="Register">注册账号</a></p>
        </footer>
      </section>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// 账号密码映射表
const userAccounts = {
  '娜乌': 'k9L@m#2',
  '阿凡达': 'pQ3$hB1',
  '程勇': '8nG*fT7',
  '沐宸': 'dR7v9E2',
  '莫尔': '5tY%kP4',
  '阿葵': 'wZ2@qR9',
  '玄同': 'bM8!vN3',
  '温图尔': 'jH6#pL0',
  '观澜': '3mL$eK8',
  '时生': '9fK@rD5',
  '卷柏': 'B7r$yT2',
  'user1': 'Q9d%Jp6',
  'user2': '5tM@eR3',
  'user3': 'K2n#Wq8',
  'user4': '8hV^mC1',
  'user5': 'F4u&Pk7',
  'user6': 'z6N*Ta5',
  'user7': 'R1x$Gv9',
  'user8': 'L3d@Kb8',
  'user9': 'Y7j^Pn4'
}

/**
 * 显示错误信息
 */
const showError = (message) => {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 3000)
}


/**
 * 登录逻辑
 */
const handleLogin = async () => {
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const user = username.value.trim()
    const pwd = password.value.trim()
    
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 验证账号和密码
    if (!user || !pwd) {
      showError('请输入账号和密码')
      isLoading.value = false
      return
    }
    
    // 检查账号是否存在
    if (!userAccounts.hasOwnProperty(user)) {
      showError('账号或密码错误')
      isLoading.value = false
      return
    }
    
    // 验证密码
    if (userAccounts[user] !== pwd) {
      showError('账号或密码错误')
      isLoading.value = false
      return
    }
    
    // 登录成功，保存登录状态和登录时间
    const loginTime = Date.now()
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('username', user)
    localStorage.setItem('loginTime', loginTime.toString())
    
    // 跳转到批量操作页面
    router.push('/batch')
  } catch (error) {
    console.error('登录错误:', error)
    showError('登录失败，请重试')
    isLoading.value = false
  }
}


/**
 * 忘记密码逻辑
 */
const handleForgotPassword = () => {
  alert('还在开发中...')
}

/**
 * 注册逻辑
 */
const handleRegister = () => {
  alert('还在开发中...')
}
</script>

<style scoped>
.login-page {
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: linear-gradient(135deg, #F9DBE0 0%, #FFE5E9 50%, #F9DBE0 100%);
  font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: backgroundShift 15s ease infinite;
}

@keyframes backgroundShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.svg-top {
  position: absolute;
  top: -900px;
  right: -300px;
  z-index: 0;
  animation: float 20s ease-in-out infinite;
  opacity: 0.8;
}

.svg-bottom {
  position: absolute;
  bottom: -500px;
  left: -200px;
  z-index: 0;
  animation: float 25s ease-in-out infinite reverse;
  opacity: 0.8;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(2deg); }
  66% { transform: translate(-20px, 20px) rotate(-2deg); }
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.container .wrapper {
  padding: 50px 45px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 30px;
  width: 450px;
  max-width: 90%;
  margin-right: 80px;
  z-index: 1;
  box-shadow: 0 20px 60px rgba(255, 107, 157, 0.2),
              0 0 0 1px rgba(255, 255, 255, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.container .wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 70px rgba(255, 107, 157, 0.3),
              0 0 0 1px rgba(255, 255, 255, 0.5);
}

.container .wrapper header {
  margin-bottom: 45px;
  text-align: center;
  animation: fadeIn 1s ease-out 0.2s both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.container .wrapper header .logo {
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  margin: 0 auto;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(255, 107, 157, 0.3);
}

.container .wrapper header .logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 20px;
}

.container .wrapper header h1 {
  color: #FF6B9D;
  font-size: 38px;
  font-weight: 600;
  margin-bottom: 0;
  margin-top: 30px;
  background: linear-gradient(135deg, #FF6B9D 0%, #FFB3D9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.container .wrapper header p {
  color: #FF6B9D;
  font-size: 16px;
  font-weight: 400;
  margin: 8px 0 0 0;
  opacity: 0.8;
}

.container .wrapper .main-content {
  animation: fadeIn 1s ease-out 0.4s both;
}

.container .wrapper .main-content form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-icon {
  width: 22px;
  height: 22px;
  color: #FF6B9D;
  opacity: 0.6;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.input-wrapper:focus-within .input-icon {
  opacity: 1;
  transform: scale(1.1);
  color: #FF6B9D;
}

.container .wrapper .main-content .input-field {
  border: none;
  display: block;
  width: 100%;
  height: 50px;
  font-size: 16px;
  color: #333;
  box-sizing: border-box;
  background: transparent;
  padding: 0;
  transition: all 0.3s ease;
}

.container .wrapper .main-content .input-field::placeholder {
  color: #999;
  font-size: 16px;
  font-weight: 400;
  transition: all 0.3s ease;
}

.container .wrapper .main-content .input-field:focus {
  outline: none;
}

.container .wrapper .main-content .input-field:focus::placeholder {
  opacity: 0.5;
  transform: translateX(5px);
}

.input-line {
  position: absolute;
  bottom: 0;
  left: 34px;
  width: calc(100% - 34px);
  height: 2px;
  background: linear-gradient(to right, rgba(255, 107, 157, 0.3), rgba(255, 107, 157, 0.1));
  transition: all 0.3s ease;
}

.input-wrapper:focus-within .input-line {
  height: 2.5px;
  background: linear-gradient(to right, #FF6B9D, #FFB3D9);
  box-shadow: 0 2px 8px rgba(255, 107, 157, 0.4);
}

.container .wrapper .main-content .login-button {
  background: linear-gradient(135deg, #FF6B9D 0%, #FFB3D9 100%);
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 500;
  color: #fff;
  display: block;
  width: 100%;
  height: 50px;
  margin: 20px auto 0;
  outline: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4);
  position: relative;
  overflow: hidden;
}

.container .wrapper .main-content .login-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.container .wrapper .main-content .login-button:hover::before {
  width: 400px;
  height: 400px;
}

.container .wrapper .main-content .login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 157, 0.5);
}

.container .wrapper .main-content .login-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(255, 107, 157, 0.4);
}

.container .wrapper .main-content .login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  margin-top: 15px;
  padding: 12px 20px;
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.1), rgba(255, 182, 193, 0.1));
  border-radius: 8px;
  color: #FF6B9D;
  font-size: 14px;
  text-align: center;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.container .wrapper footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 107, 157, 0.1);
  animation: fadeIn 1s ease-out 0.6s both;
}

.container .wrapper footer p {
  margin: 0;
  font-weight: 400;
  font-size: 14px;
}

.container .wrapper footer p a {
  color: #FF6B9D;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  padding-bottom: 2px;
}

.container .wrapper footer p a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(to right, #FF6B9D, #FFB3D9);
  transition: width 0.3s ease;
}

.container .wrapper footer p a:hover::after {
  width: 100%;
}

.container .wrapper footer p a:hover {
  opacity: 1;
  transform: translateY(-2px);
}

@media (min-width: 320px) and (max-width: 768px) {
  .container .wrapper {
    width: 90%;
    max-width: 450px;
    padding: 35px 30px;
    margin-right: 0;
  }

  .container .wrapper header h1 {
    font-size: 32px;
  }

  .container .wrapper header .logo {
    width: 70px;
    height: 70px;
  }

  .svg-top, .svg-bottom {
    opacity: 0.5;
  }
}
</style>

