from fastapi import APIRouter, HTTPException, Body
from schemas.photo_editer import ScheduledTaskRequest
from services.scheduled_tasks import (
    create_scheduled_task_service,
    get_scheduled_tasks_service,
    delete_scheduled_task_service,
    set_service_scheduler
)
from tools.logger import setup_logging
from tools.response import success_response, error_response
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 初始化日志
logger = setup_logging()

# 创建路由器
router = APIRouter(tags=["scheduled_tasks"])


def set_scheduler(sched: AsyncIOScheduler):
    """设置调度器实例"""
    set_service_scheduler(sched)


@router.post("/create_scheduled_task")
async def create_scheduled_task(request_data: ScheduledTaskRequest = Body(...)):
    """
    创建定时任务
    """
    try:
        result = await create_scheduled_task_service(
            scheduled_time=request_data.scheduled_time,
            source_image_urls=request_data.source_image_urls,
            model_image_url=request_data.model_image_url or "",
            process_config=request_data.process_config
        )
        return success_response(
            data=result,
            message="定时任务创建成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建定时任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"创建定时任务失败: {str(e)}", code=500)
        )


@router.get("/get_scheduled_tasks")
async def get_scheduled_tasks():
    """
    获取所有定时任务
    """
    try:
        result = await get_scheduled_tasks_service()
        return success_response(
            data=result,
            message=f"成功获取 {result['count']} 个定时任务"
        )
    except Exception as e:
        logger.error(f"获取定时任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"获取定时任务失败: {str(e)}", code=500)
        )


@router.delete("/delete_scheduled_task/{task_id}")
async def delete_scheduled_task(task_id: str):
    """
    删除定时任务
    """
    try:
        result = await delete_scheduled_task_service(task_id)
        return success_response(
            data=result,
            message=f"定时任务 {task_id} 删除成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除定时任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(message=f"删除定时任务失败: {str(e)}", code=500)
        )

