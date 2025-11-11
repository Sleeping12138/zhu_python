from fastapi import HTTPException
from typing import List, Dict, Any
import json
import requests
import asyncio
import uuid
from datetime import datetime
from tools.logger import setup_logging
from config import settings
from repositories.photo_editor_repository import PhotoEditorRepository
from repositories.scheduled_tasks_repository import ScheduledTasksRepository

logger = setup_logging()


async def get_batch_tasks_service(limit: int = 100) -> Dict[str, Any]:
    """
    获取批量处理任务列表
    """
    try:
        tasks = await PhotoEditorRepository.get_batch_tasks(limit=limit)
        logger.info(f"成功获取 {len(tasks)} 条批量处理任务")
        return {
            "tasks": tasks,
            "count": len(tasks)
        }

    except Exception as e:
        logger.error(f"获取批量处理任务失败: {str(e)}")
        raise


# 图片处理服务地址
PROCESS_SERVICE_URL = settings.BASE_URL + ":" + settings.PROCESS_SERVICE_PORT


def process_image(request_data: dict) -> dict:
    """
    调用图片处理接口
    """
    try:
        logger.debug(f"调用图片处理接口: {PROCESS_SERVICE_URL}/process, 请求参数: {request_data}")

        response = requests.post(
            f"{PROCESS_SERVICE_URL}/process",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=500
        )

        if response.status_code != 200:
            error_detail = f"处理失败: HTTP {response.status_code}"
            try:
                error_body = response.text
                logger.error(f"图片处理接口返回错误: {error_detail}, 响应内容: {error_body}")
            except:
                pass
            raise HTTPException(status_code=500, detail=error_detail)

        result = response.json()
        logger.debug(f"图片处理接口返回结果: {result}")

        # 检查返回结果中是否有final_url
        if not result.get("final_url"):
            logger.warning(f"图片处理接口返回成功，但final_url为空. 完整响应: {result}")

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"调用处理接口失败: {str(e)}")
        raise


async def execute_task_internal(
        source_image_urls: List[str],
        model_image_url: str,
        process_config: Dict[str, Any],
        task_source: str = "scheduled",
        task_id: str = None
):
    """
    执行任务函数
    """
    try:
        if task_id:
            try:
                await ScheduledTasksRepository.update_scheduled_task_status(task_id, 'processing')
                logger.info(f"定时任务状态已更新为processing: task_id={task_id}")
            except Exception as e:
                logger.error(f"更新任务状态为processing失败: task_id={task_id}, error={str(e)}")

        # 获取配置参数
        process_type = process_config.get("processType", "model")
        process_steps = process_config.get("processSteps", {})
        crop_ratio = process_config.get("cropRatio", "3:4")
        extract_real_type = process_config.get("extractRealType", "上装")
        watermark_name = process_config.get("watermark_name", "")

        logger.info(f"开始执行任务，任务来源: {task_source}, task_id: {task_id}")

        # 存放所有处理结果
        results = []
        success_count = 0
        failed_count = 0
        total = len(source_image_urls)

        # 单张图片的异步函数
        async def process_single_image(source_url: str, index: int):
            """
            处理单张图片的异步函数
            """
            try:
                logger.info(f"正在处理第 {index + 1}/{total} 张源图片: {source_url}")

                # 构建请求参数
                process_request_data = {
                    "image_url_1": source_url,
                    "image_url_2": model_image_url,
                    "image_category": "模特图" if process_type == "model" else "实拍图",
                    "services": [],
                    "garment_part": process_steps.get("extractReal", False) and extract_real_type or ""
                }

                # 根据选中的处理步骤添加服务
                if process_steps.get("watermark", False):
                    process_request_data["services"].append("去水印")
                if process_steps.get("poseSwap", False):
                    process_request_data["services"].append("换姿态")
                if process_steps.get("backgroundSwap", False):
                    process_request_data["services"].append("换背景")
                if process_steps.get("faceSwap", False):
                    process_request_data["services"].append("换脸")
                if process_steps.get("extractReal", False):
                    process_request_data["services"].append("提取实拍图")
                if process_steps.get("superResolution", False):
                    process_request_data["services"].append("超分")
                if process_steps.get("extractDetail", False):
                    process_request_data["services"].append("提取细节图")
                if process_steps.get("addWatermark", False):
                    process_request_data["services"].append("加水印")
                if process_steps.get("autoCrop", False):
                    process_request_data["services"].append("自动裁剪")

                # 如果选择了加水印
                if process_steps.get("addWatermark", False) and watermark_name:
                    process_request_data["watermark_name"] = watermark_name

                # 如果选择了自动裁剪
                if process_steps.get("autoCrop", False) and crop_ratio:
                    process_request_data["crop_ratio"] = crop_ratio

                logger.info("process_request_data", process_request_data)
                print("process_request_data", process_request_data)

                # 在线程池中调用处理接口
                result = await asyncio.to_thread(process_image, process_request_data)

                # 构建成功结果对象
                process_result = {
                    "original_url": source_url,
                    "processed_url": result.get("final_url", ""),
                    "extract_real_url": process_steps.get("extractReal", False) and result.get(
                        "extract_realshot_url") or None,
                    "extract_detail_url": process_steps.get("extractDetail", False) and result.get(
                        "extract_detail_url") or None,
                    "is_success": bool(result.get("final_url") and result.get("final_url", "").strip() != "")
                }

                logger.info(f"第 {index + 1} 张源图片处理成功")
                return process_result

            except Exception as error:
                logger.error(f"源图片 {source_url} 处理失败: {str(error)}")

                # 构建失败结果对象
                process_result = {
                    "original_url": source_url,
                    "processed_url": None,
                    "extract_real_url": None,
                    "extract_detail_url": None,
                    "is_success": False
                }

                return process_result

        # 直接并发处理
        tasks = []
        for i, url in enumerate(source_image_urls):
            tasks.append(process_single_image(url, i))
        task_results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(task_results):
            if isinstance(result, Exception):
                logger.error(f"处理图片时发生异常: {str(result)}")
                results.append({
                    "original_url": source_image_urls[i],
                    "processed_url": None,
                    "extract_real_url": None,
                    "extract_detail_url": None,
                    "is_success": False
                })
                failed_count += 1
            else:
                results.append(result)
                if result["is_success"]:
                    success_count += 1
                else:
                    failed_count += 1

        # 生成批次ID，同一批处理的所有任务使用相同的batch_id
        batch_id = str(uuid.uuid4())

        # 保存到数据库
        sql_data = []
        for i, result_data in enumerate(results):
            task_data = {
                "batch_id": batch_id,
                "status": "success" if result_data["is_success"] else "failed",
                "task_source": task_source,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "process_type": process_type,
                "process_steps": json.dumps(process_steps, ensure_ascii=False),
                "crop_ratio": crop_ratio,
                "extract_real_type": process_steps.get("extractReal", False) and extract_real_type or "",
                "source_images": json.dumps(source_image_urls, ensure_ascii=False),
                "model_image": model_image_url or "",
                "processed_results": json.dumps(result_data, ensure_ascii=False),
                "source_count": total,
                "success_count": success_count,
                "failed_count": failed_count,
                "total_processed": success_count + failed_count
            }
            sql_data.append(task_data)

        if sql_data:
            await PhotoEditorRepository.save_batch_tasks(sql_data)
            logger.info(f"任务完成，成功保存 {len(sql_data)} 条记录到数据库")

        if task_id:
            try:
                await ScheduledTasksRepository.update_scheduled_task_status(task_id, 'completed')
                logger.info(f"定时任务状态已强制更新为completed: task_id={task_id}")
            except Exception as e:
                logger.error(f"更新任务状态失败: task_id={task_id}, error={str(e)}")

        return {
            "success": True,
            "message": f"处理完成，成功: {success_count}, 失败: {failed_count}",
            "results": results,
            "success_count": success_count,
            "failed_count": failed_count,
            "total": total
        }

    except Exception as e:
        logger.error(f"执行任务失败: {str(e)}")
        if task_id:
            try:
                await ScheduledTasksRepository.update_scheduled_task_status(task_id, 'failed')
                logger.info(f"定时任务状态已更新为failed（执行异常）: task_id={task_id}")
            except Exception as update_error:
                logger.error(f"更新任务状态为failed失败: task_id={task_id}, error={str(update_error)}")

        raise
