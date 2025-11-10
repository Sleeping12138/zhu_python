from typing import List, Dict, Any, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from database import AsyncSessionLocal
from Model.scheduled_tasks import ScheduledTasks
from tools.logger import setup_logging
import json
from datetime import datetime

logger = setup_logging()


class ScheduledTasksRepository:
    @staticmethod
    async def save_scheduled_task(
            task_id: str,
            scheduled_time: str,
            source_image_urls: List[str],
            model_image_url: str,
            process_config: Dict[str, Any]
    ) -> None:
        """
        保存定时任务到数据库
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"保存定时任务到数据库: task_id={task_id}")

                # 解析 scheduled_time
                scheduled_datetime = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")

                # 创建定时任务对象
                scheduled_task = ScheduledTasks(
                    task_id=task_id,
                    scheduled_time=scheduled_datetime,
                    source_image_urls=json.dumps(source_image_urls, ensure_ascii=False),
                    model_image_url=model_image_url or None,
                    process_config=json.dumps(process_config, ensure_ascii=False),
                    status='pending'
                )

                session.add(scheduled_task)
                await session.commit()
                logger.info(f"定时任务保存成功: task_id={task_id}")

            except Exception as e:
                await session.rollback()
                logger.error(f"保存定时任务失败: {str(e)}")
                raise Exception(f"保存定时任务失败，失败原因: {str(e)}")

    @staticmethod
    async def get_scheduled_tasks(limit: int = 100) -> List[Dict[str, Any]]:
        """
        从数据库获取所有未删除的定时任务
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"开始查询定时任务，限制数量: {limit}")

                # 使用SQLAlchemy ORM查询
                stmt = (
                    select(ScheduledTasks)
                    .where(ScheduledTasks.deleted == False)
                    .order_by(ScheduledTasks.scheduled_time.desc())
                    .limit(limit)
                )
                result = await session.execute(stmt)
                tasks = result.scalars().all()

                # 转换为字典格式
                tasks_list = []
                for task in tasks:
                    try:
                        source_image_urls = json.loads(task.source_image_urls)
                        process_config = json.loads(task.process_config)
                    except json.JSONDecodeError as e:
                        logger.error(f"解析JSON失败: {e}, task_id={task.task_id}")
                        continue

                    tasks_list.append({
                        "task_id": task.task_id,
                        "scheduled_time": task.scheduled_time.strftime("%Y-%m-%d %H:%M:%S") if isinstance(
                            task.scheduled_time, datetime) else str(task.scheduled_time),
                        "source_image_urls": source_image_urls,
                        "model_image_url": task.model_image_url,
                        "process_config": process_config,
                        "status": task.status,
                        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if isinstance(
                            task.created_at, datetime) else str(task.created_at)
                    })

                logger.info(f"查询完成，共找到 {len(tasks_list)} 条定时任务")
                return tasks_list

            except Exception as e:
                logger.error(f"查询定时任务失败: {str(e)}")
                raise Exception(f"查询定时任务失败，失败原因: {str(e)}")

    @staticmethod
    async def update_scheduled_task_status(task_id: str, status: str) -> None:
        """
        更新定时任务状态
        status: 'pending', 'processing', 'completed', 'failed'
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"更新定时任务状态: task_id={task_id}, status={status}")

                # 使用SQLAlchemy ORM更新
                query = (
                    update(ScheduledTasks)
                    .where(ScheduledTasks.task_id == task_id)
                    .values(status=status)
                )
                result = await session.execute(query)
                await session.commit()

                if result.rowcount == 0:
                    logger.warning(f"未找到要更新的任务: task_id={task_id}")
                else:
                    logger.info(f"定时任务状态更新成功: task_id={task_id}, status={status}")

            except Exception as e:
                await session.rollback()
                logger.error(f"更新定时任务状态失败: {str(e)}")
                raise Exception(f"更新定时任务状态失败，失败原因: {str(e)}")

    @staticmethod
    async def delete_scheduled_task(task_id: str) -> None:
        """
        软删除定时任务
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"删除定时任务: task_id={task_id}")

                # 使用SQLAlchemy ORM软删除
                stmt = (
                    update(ScheduledTasks)
                    .where(ScheduledTasks.task_id == task_id, ScheduledTasks.deleted == False)
                    .values(deleted=True)
                )
                result = await session.execute(stmt)
                await session.commit()

                if result.rowcount == 0:
                    raise Exception(f"未找到要删除的任务: {task_id}")

                logger.info(f"定时任务删除成功: task_id={task_id}")

            except Exception as e:
                await session.rollback()
                logger.error(f"删除定时任务失败: {str(e)}")
                raise Exception(f"删除定时任务失败，失败原因: {str(e)}")
