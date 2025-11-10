from fastapi import APIRouter, HTTPException, UploadFile, File
from tools.obs import upload_to_oss_sync
from tools.logger import setup_logging
from tools.response import success_response
from io import BytesIO

# 初始化日志
logger = setup_logging()

# 创建路由器
router = APIRouter(tags=["upload"])


@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        image = await file.read()
        image_bytes = BytesIO(image)

        # 上传到华为云 OBS
        file_url = upload_to_oss_sync(image_bytes)

        # 统一结果返回
        return success_response(data={"fileUrl": file_url}, message="文件上传成功")

    except Exception as e:
        logger.error(f"上传失败，错误信息: {str(e)}")
        raise HTTPException(status_code=500, detail="文件上传失败，请稍后重试")

