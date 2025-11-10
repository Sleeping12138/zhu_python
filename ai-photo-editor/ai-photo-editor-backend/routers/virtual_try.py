from fastapi import APIRouter, HTTPException, Body
from schemas.photo_editer import ClothesSwapRequest
from services.virtual_try_service import virtual_tryon_service
from tools.logger import setup_logging
from tools.response import success_response, error_response

# 初始化日志
logger = setup_logging()

# 创建路由器
router = APIRouter(tags=["virtual_tryon"])


@router.post("/virtual_tryon")
async def virtual_tryon(request_data: ClothesSwapRequest = Body(...)):
    """
    虚拟试衣接口
    """
    try:
        result = await virtual_tryon_service(
            image_url_1=request_data.image_url_1,
            image_url_2=request_data.image_url_2,
            clothes_1_str=request_data.clothes_1_type,
            clothes_2_str=request_data.clothes_2_type
        )

        return success_response(
            data=result,
            message="虚拟试衣请求成功"
        )
    except Exception as e:
        logger.error(f"虚拟试衣处理失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"虚拟试衣处理失败: {str(e)}", code=500)
        )
