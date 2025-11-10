from tools.logger import setup_logging
from fastapi import HTTPException, UploadFile
import asyncio
from datetime import datetime
from io import BytesIO
from PIL import Image
from obs import ObsClient
from config import settings

# 初始化日志
logger = setup_logging()


def generate_unique_file_name(current_date):
    """
    生成唯一的图片文件名
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    return f"{current_date}_{timestamp}.png"


def upload_to_oss_sync(image_bytes, category: str = None) -> str:
    """
    同步方法：上传图片到华为云 OBS
    """
    try:
        # 将字节流转换为图像对象
        image = Image.open(image_bytes)

        # 将图像保存到内存流
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        # OBS 上传配置
        bucket_name = "yishou-img"
        current_date = datetime.now().strftime("%Y%m%d") if not category else category
        object_key = f"yishou_tqsx_img/new_goods_monitor/picture/gce/{current_date}/{generate_unique_file_name(current_date)}"

        # 上传文件到华为云
        obsClient = ObsClient(
            access_key_id=settings.OBS_ACCESS_KEY_ID,
            secret_access_key=settings.OBS_SECRET_ACCESS_KEY,
            server=settings.OBS_SERVER
        )

        resp = obsClient.putContent(bucket_name, object_key, buffer)

        if resp.status < 300:
            image_url = f'https://yishou-img.obs.cn-south-1.myhuaweicloud.com/{object_key}'
            logger.info(f"文件上传成功，URL: {image_url}")
            return image_url
        else:
            logger.error(f"上传失败，状态码: {resp.status}")
            raise Exception(f"上传失败，状态码: {resp.status}")
    except Exception as e:
        logger.error(f"上传到华为云 OBS 时出错: {str(e)}")
        raise e  # 重新抛出异常，交给 FastAPI 处理


async def upload_file_to_obs(file: UploadFile) -> str:
    """
    上传文件到OSS并返回URL
    """
    try:
        file_content = await file.read()
        file_bytes = BytesIO(file_content)

        # 在线程池中执行同步上传方法，避免阻塞事件循环
        image_url = await asyncio.to_thread(upload_to_oss_sync, file_bytes)
        return image_url
    except Exception as e:
        logger.error(f"上传文件到OSS失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"上传文件失败: {str(e)}")
