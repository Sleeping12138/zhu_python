from fastapi import APIRouter, HTTPException, Body
from schemas.photo_editer import ImmediateTaskRequest
from services.photo_editor import (
    execute_task_internal,
    get_batch_tasks_service
)
from tools.logger import setup_logging
from tools.response import success_response, error_response

# 初始化日志
logger = setup_logging()

# 创建路由器
router = APIRouter(tags=["tasks"])


@router.get("/get_batch_tasks")
async def get_batch_tasks():
    """
    按照completed_at字段逆序查询批量处理任务数据
    """
    try:
        result = await get_batch_tasks_service(limit=100)
        return success_response(
            data=result,
            message=f"成功查询到 {result['count']} 条批量处理任务"
        )
    except Exception as e:
        logger.error(f"获取批量处理任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"获取批量处理任务失败: {str(e)}", code=500)
        )


@router.post("/execute_immediate_task")
async def execute_immediate_task(request_data: ImmediateTaskRequest = Body(...)):
    """
    立即执行处理任务
    """
    try:
        result = await execute_task_internal(
            source_image_urls=request_data.source_image_urls,
            model_image_url=request_data.model_image_url or "",
            process_config=request_data.process_config,
            task_source="batch"
        )
        return success_response(
            data=result,
            message=result.get("message", "任务执行成功")
        )
    except Exception as e:
        logger.error(f"执行立即任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"处理过程中发生错误: {str(e)}", code=500)
        )


