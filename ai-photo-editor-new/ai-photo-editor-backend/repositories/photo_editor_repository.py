from typing import List, Dict, Any
from sqlalchemy import select, desc
from database import AsyncSessionLocal
from Model.photo_editor import AIPhotoEditor
from tools.logger import setup_logging
import json
from datetime import datetime

logger = setup_logging()


class PhotoEditorRepository:
    @staticmethod
    async def get_batch_tasks(limit: int = 100) -> List[Dict[str, Any]]:
        """
        从数据库查询批量处理任务数据
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"开始查询批量处理任务数据，限制数量: {limit}")

                # 使用SQLAlchemy ORM查询
                query = select(AIPhotoEditor).order_by(desc(AIPhotoEditor.completed_at)).limit(limit)
                result = await session.execute(query)
                tasks = result.scalars().all()

                # 转换类型
                tasks_list = []
                for task in tasks:
                    task_dict = {
                        'id': task.id,
                        'batch_id': task.batch_id,
                        'status': task.status,
                        'task_source': task.task_source,
                        'task_type': task.task_source,
                        'created_at': task.created_at.isoformat() if task.created_at else None,
                        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                        'process_type': task.process_type,
                        'process_steps': json.dumps(task.process_steps, ensure_ascii=False),
                        'crop_ratio': task.crop_ratio,
                        'extract_real_type': task.extract_real_type,
                        'source_images': json.dumps(task.source_images, ensure_ascii=False),
                        'model_image': task.model_image,
                        'processed_results': json.dumps(task.processed_results, ensure_ascii=False) if task.processed_results else "[]",
                        'source_count': task.source_count,
                        'success_count': task.success_count,
                        'failed_count': task.failed_count,
                        'total_processed': task.total_processed
                    }
                    tasks_list.append(task_dict)

                logger.info(f"查询完成，共找到 {len(tasks_list)} 条记录")
                return tasks_list

            except Exception as e:
                logger.error(f"查询批量处理任务失败，失败原因: {str(e)}")
                raise Exception(f"查询数据失败，失败原因: {str(e)}")

    @staticmethod
    async def save_batch_tasks(tasks: List[Dict[str, Any]]) -> None:
        """
        保存批量处理任务数据到数据库
        """
        async with AsyncSessionLocal() as session:
            try:
                logger.info(f"开始批量插入任务数据，共 {len(tasks)} 条")

                task_objects = []
                for i, task_data in enumerate(tasks):
                    logger.info(
                        f"正在准备第 {i + 1}/{len(tasks)} 个任务: process_type={task_data.get('process_type')}, status={task_data.get('status')}")

                    # 解析JSON字段
                    try:
                        process_steps = json.loads(task_data['process_steps']) if isinstance(task_data['process_steps'],
                                                                                             str) else task_data[
                            'process_steps']
                        source_images = json.loads(task_data['source_images']) if isinstance(task_data['source_images'],
                                                                                             str) else task_data[
                            'source_images']
                        processed_results = json.loads(task_data['processed_results']) if isinstance(
                            task_data['processed_results'], str) else task_data['processed_results']
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"解析JSON字段失败: {str(e)}")
                        continue

                    # 解析created_at
                    created_at = None
                    if task_data.get('created_at'):
                        if isinstance(task_data['created_at'], str):
                            created_at = datetime.strptime(task_data['created_at'], "%Y-%m-%d %H:%M:%S")
                        else:
                            created_at = task_data['created_at']

                    # 创建任务对象
                    task_obj = AIPhotoEditor(
                        batch_id=task_data.get('batch_id'),
                        status=task_data['status'],
                        task_source=task_data['task_source'],
                        created_at=created_at,
                        process_type=task_data['process_type'],
                        process_steps=process_steps,
                        crop_ratio=task_data.get('crop_ratio'),
                        extract_real_type=task_data.get('extract_real_type'),
                        source_images=source_images,
                        model_image=task_data.get('model_image'),
                        processed_results=processed_results,
                        source_count=task_data.get('source_count', 0),
                        success_count=task_data.get('success_count', 0),
                        failed_count=task_data.get('failed_count', 0),
                        total_processed=task_data.get('total_processed', 0)
                    )
                    task_objects.append(task_obj)

                # 批量添加
                session.add_all(task_objects)
                await session.commit()

                logger.info(f"批量插入完成，成功保存 {len(task_objects)} 个任务")

            except Exception as e:
                await session.rollback()
                logger.error(f"保存批量处理任务失败: {str(e)}")
                raise Exception(f"保存数据失败，失败原因: {str(e)}")
