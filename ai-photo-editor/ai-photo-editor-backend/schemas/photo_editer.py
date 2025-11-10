from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Generic, TypeVar

# 定义泛型类型变量
T = TypeVar('T')


# 统一响应模型
class ApiResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    code: int = 200
    success: bool = True
    message: str = "操作成功"
    data: Optional[T] = None


# 存储数据库参数模型
class BatchTaskData(BaseModel):
    status: str  # 'success' 或 'failed'
    task_source: str  # 'batch' 或 'scheduled'
    created_at: str
    process_type: str  # 'model' 或 'real'
    process_steps: str
    crop_ratio: str
    extract_real_type: str
    source_images: str
    model_image: str
    processed_results: str
    source_count: int
    success_count: int
    failed_count: int
    total_processed: int


# 立即执行函数参数模型
class ImmediateTaskRequest(BaseModel):
    source_image_urls: List[str]
    model_image_url: Optional[str] = None
    process_config: Dict[str, Any]


# 定时任务请求模型
class ScheduledTaskRequest(BaseModel):
    source_image_urls: List[str]
    model_image_url: Optional[str] = None
    process_config: Dict[str, Any]
    scheduled_time: str  # 执行时间格式：'YYYY-MM-DD HH:MM:SS'


# 服装替换请求模型
class ClothesSwapRequest(BaseModel):
    image_url_1: str
    image_url_2: str
    clothes_1_type: str
    clothes_2_type: str