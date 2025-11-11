<template>
  <div></div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, nextTick } from 'vue'
import PhotoSwipe from 'photoswipe'
import 'photoswipe/dist/photoswipe.css'

const props = defineProps({
  images: {
    type: Array,
    required: true,
    default: () => []
  },
  visible: {
    type: Boolean,
    default: false
  },
  initialIndex: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['close'])

let pswpInstance = null

/**
 * 获取图片的真实尺寸
 */
const getImageDimensions = (src) => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => {
      resolve({
        width: img.naturalWidth,
        height: img.naturalHeight
      })
    }
    img.onerror = () => {
      // 如果加载失败，使用默认尺寸
      resolve({
        width: 1920,
        height: 1080
      })
    }
    img.src = src
  })
}

const openPhotoSwipe = async () => {
  if (!props.images || props.images.length === 0 || pswpInstance) return

  // 获取所有图片的真实尺寸
  const itemsPromises = props.images.map(async (img) => {
    const src = typeof img === 'string' ? img : (img.src || img.preview || img.url)
    
    // 如果已经提供了宽高，直接使用
    if (img.width && img.height) {
      return {
        src,
        width: img.width,
        height: img.height,
        alt: img.alt || '图片'
      }
    }
    
    // 否则获取真实尺寸
    const dimensions = await getImageDimensions(src)
    return {
      src,
      width: dimensions.width,
      height: dimensions.height,
      alt: img.alt || '图片'
    }
  })

  const items = await Promise.all(itemsPromises)

  const options = {
    dataSource: items,
    index: props.initialIndex,
    showHideAnimationType: 'fade',
    bgOpacity: 0.9,
    spacing: 0.1,
    allowPanToNext: true,
    loop: false,
    pinchToClose: true,
    closeOnVerticalDrag: true,
    escKey: true,
    arrowKeys: true,
    returnFocus: false,
    clickToCloseNonZoomable: true,
    imageClickAction: 'close',
    tapAction: 'toggle-controls',
    doubleTapAction: 'zoom',
    maxSpreadZoom: 3,
    showAnimationDuration: 300,
    hideAnimationDuration: 300,
    zoomAnimationDuration: 300
  }

  pswpInstance = new PhotoSwipe(options)

  pswpInstance.on('close', () => {
    pswpInstance = null
    emit('close')
  })

  pswpInstance.init()
}

const closePhotoSwipe = () => {
  if (pswpInstance) {
    pswpInstance.close()
    pswpInstance = null
  }
}

watch(() => props.visible, async (newVal) => {
  if (newVal) {
    await nextTick()
    // 延迟打开以确保 DOM 已更新
    setTimeout(() => {
      openPhotoSwipe()
    }, 100)
  } else {
    closePhotoSwipe()
  }
})

onMounted(() => {
  if (props.visible) {
    nextTick(() => {
      setTimeout(() => {
        openPhotoSwipe()
      }, 100)
    })
  }
})

onUnmounted(() => {
  closePhotoSwipe()
})
</script>

<style>
/* PhotoSwipe 样式已通过 import 引入 */
</style>

