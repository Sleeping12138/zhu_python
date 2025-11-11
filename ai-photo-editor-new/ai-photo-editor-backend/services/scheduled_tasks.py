from fastapi import HTTPException
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tools.logger import setup_logging
from repositories.scheduled_tasks_repository import ScheduledTasksRepository
from services.photo_editor import execute_task_internal

logger = setup_logging()

# 调度器实例
scheduler: Optional[AsyncIOScheduler] = None


def set_service_scheduler(sched: AsyncIOScheduler):
    """设置调度器实例"""
    global scheduler
    scheduler = sched


async def create_scheduled_task_service(
    scheduled_time: str,
    source_image_urls: List[str],
    model_image_url: str,
    process_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    创建定时任务服务
    """
    if scheduler is None:
        raise HTTPException(
            status_code=500,
            detail="调度器未初始化"
        )

    # 生成唯一ID
    task_id = str(uuid.uuid4())

    # 解析执行时间
    scheduled_datetime = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")

    # 检查时间是否在将来
    if scheduled_datetime < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="执行时间必须在将来"
        )

    # 保存到数据库
    await ScheduledTasksRepository.save_scheduled_task(
        task_id=task_id,
        scheduled_time=scheduled_time,
        source_image_urls=source_image_urls,
        model_image_url=model_image_url or "",
        process_config=process_config
    )
    logger.info(f"定时任务已保存到数据库: task_id={task_id}")

    # 创建触发器
    trigger = DateTrigger(run_date=scheduled_datetime)
    logger.info(f"创建定时任务 {task_id}，将在 {scheduled_datetime} 执行")

    # 创建任务执行函数
    async def scheduled_task_job():
        try:
            logger.info(f"开始执行定时任务 {task_id}")
            await execute_task_internal(
                source_image_urls=source_image_urls,
                model_image_url=model_image_url or "",
                process_config=process_config,
                task_source="scheduled",
                task_id=task_id
            )
            logger.info(f"定时任务 {task_id} 执行完成")
        except Exception as e:
            logger.error(f"定时任务 {task_id} 执行失败: {str(e)}")

    # 添加任务到调度器
    scheduler.add_job(
        scheduled_task_job,
        trigger=trigger,
        id=task_id,
        replace_existing=True
    )

    return {
        "task_id": task_id,
        "scheduled_time": scheduled_time
    }


async def get_scheduled_tasks_service() -> Dict[str, Any]:
    """
    获取所有定时任务服务
    """
    # 从数据库获取任务列表
    tasks = await ScheduledTasksRepository.get_scheduled_tasks()

    # 转换为前端需要的格式
    result_tasks = []
    for task in tasks:
        scheduled_datetime = datetime.strptime(task['scheduled_time'], "%Y-%m-%d %H:%M:%S")

        result_tasks.append({
            "task_id": task['task_id'],
            "next_run_time": scheduled_datetime.isoformat() if scheduled_datetime > datetime.now() else None,
            "scheduled_time": task['scheduled_time'],
            "source_image_urls": task['source_image_urls'],
            "model_image_url": task['model_image_url'],
            "process_config": task['process_config'],
            "status": task['status'],
            "created_at": task['created_at']
        })

    return {
        "tasks": result_tasks,
        "count": len(result_tasks)
    }


async def delete_scheduled_task_service(task_id: str) -> Dict[str, Any]:
    """
    删除定时任务服务
    """
    # 从数据库删除
    await ScheduledTasksRepository.delete_scheduled_task(task_id)
    logger.info(f"定时任务已从数据库删除: task_id={task_id}")

    # 如果任务还在调度器中，则从调度器中移除
    if scheduler is not None:
        try:
            scheduler.remove_job(task_id)
            logger.info(f"定时任务已从调度器移除: task_id={task_id}")
        except Exception as e:
            logger.warning(f"从调度器移除任务失败（任务可能已执行）: task_id={task_id}, error={str(e)}")

    return {
        "task_id": task_id
    }

