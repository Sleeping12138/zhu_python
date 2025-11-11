from PIL import Image
from io import BytesIO
import logging
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from datetime import datetime
from obs import ObsClient

app = FastAPI()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('upload_service.log', encoding='utf-8')]
)
logger = logging.getLogger(__name__)

# OBS 配置
OBS_ACCESS_KEY_ID = "EULIXLKJQLUS62GPNIAX"
OBS_SECRET_ACCESS_KEY = "vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK"
OBS_SERVER = "https://obs.cn-south-1.myhuaweicloud.com"

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
            access_key_id=OBS_ACCESS_KEY_ID,
            secret_access_key=OBS_SECRET_ACCESS_KEY,
            server=OBS_SERVER
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

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 读取上传的文件
        image = await file.read()
        image_bytes = BytesIO(image)

        # 上传到华为云 OBS
        file_url = upload_to_oss_sync(image_bytes)

        # 返回成功响应，并传递真实 URL
        return {"success": True, "fileUrl": file_url}
    
    except Exception as e:
        logger.error(f"上传失败，错误信息: {str(e)}")
        raise HTTPException(status_code=500, detail="文件上传失败，请稍后重试")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("图片上传服务启动中...")
    logger.info(f"服务地址: http://0.0.0.0:5090")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=5090)
    except KeyboardInterrupt:
        logger.info("服务被用户中断")
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
    finally:
        logger.info("图片上传服务已停止")
