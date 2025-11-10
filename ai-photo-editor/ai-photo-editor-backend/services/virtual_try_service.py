import requests
from typing import Dict, Any
from tools.logger import setup_logging
from config import settings

# 初始化日志
logger = setup_logging()


async def virtual_tryon_service(
    image_url_1: str,
    image_url_2: str,
    clothes_1_str: str,
    clothes_2_str: str
) -> Dict[str, Any]:
    """
    虚拟试衣服务
    """
    try:
        payload = {
            "image_url_1": image_url_1,
            "image_url_2": image_url_2,
            "clothes_1": f"remove {clothes_1_str}, keep character consistency",
            "clothes_2": f"去掉图2的衣架，图1中女人穿着图2的{clothes_2_str}，保持角色动作、场景以及服装的一致性",
        }
        
        logger.info(f"开始处理虚拟试衣请求: {payload}")
        post_url = f"{settings.BASE_URL}:{settings.VIRTUAL_TRY_SERVICE_PORT}/process"

        response = requests.post(url=post_url, json=payload)

        if response.status_code != 200:
            logger.error(f"请求下游虚拟试衣服务失败: {response.status_code}")
            raise
            
        result = response.json()
        logger.info(f"虚拟试衣请求处理完成: {result}")
        return result

    except Exception as e:
        logger.error(f"虚拟试衣服务处理失败: {str(e)}")
        raise

