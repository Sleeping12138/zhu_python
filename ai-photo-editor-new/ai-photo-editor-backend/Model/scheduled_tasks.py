from sqlalchemy import Column, String, DateTime, Text, Boolean, Index
from sqlalchemy.sql import func
from database import Base


class ScheduledTasks(Base):
    """定时任务表模型"""
    __tablename__ = 'ai_photo_editor_scheduled_tasks'
    
    # 主键
    task_id = Column(String(36), primary_key=True, comment='任务ID（UUID）')
    
    # 计划执行时间
    scheduled_time = Column(DateTime, nullable=False, comment='计划执行时间')
    
    # 图片URL信息
    source_image_urls = Column(Text, nullable=False, comment='源图片URL列表（JSON格式）')
    model_image_url = Column(String(500), nullable=True, comment='模特图片URL（可选）')
    
    # 处理配置
    process_config = Column(Text, nullable=False, comment='处理配置（JSON格式，包含process_type、process_steps、crop_ratio、extract_real_type等）')
    
    # 任务状态
    status = Column(String(20), nullable=False, default='pending', comment='任务状态：pending-等待中, processing-执行中, completed-已完成, failed-失败')
    
    # 时间字段
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    
    # 删除标记
    deleted = Column(Boolean, nullable=False, default=False, comment='删除标记：0-未删除, 1-已删除')
    
    # 索引
    __table_args__ = (
        Index('idx_scheduled_time', 'scheduled_time'),
        Index('idx_status', 'status'),
        Index('idx_deleted', 'deleted'),
    )

