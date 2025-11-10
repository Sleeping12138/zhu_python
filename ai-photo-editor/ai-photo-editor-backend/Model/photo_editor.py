from sqlalchemy import Column, BigInteger, Enum, DateTime, JSON, String, Integer, Index
from sqlalchemy.sql import func
from database import Base


class AIPhotoEditor(Base):
    """
    图片处理表模型
    """
    __tablename__ = 'ai_photo_editor_photo'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='任务ID')
    
    # 批次ID，用于标识同一批处理的任务
    batch_id = Column(String(36), nullable=True, comment='批次ID，同一批处理的任务具有相同的batch_id')
    
    # 任务状态
    status = Column(Enum('success', 'failed', name='status'), nullable=False, comment='任务状态：成功或失败')
    
    # 任务来源
    task_source = Column(Enum('batch', 'scheduled', name='task_source'), nullable=False, default='batch', comment='任务来源：batch=批量处理，scheduled=定时任务')
    
    # 时间字段
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    completed_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='完成时间')
    
    # 处理配置
    process_type = Column(Enum('model', 'real', name='process_type'), nullable=False, comment='处理类型：模特图或实拍图')
    process_steps = Column(JSON, nullable=False, comment='处理步骤配置，如{"watermark":true,"faceSwap":true}')
    crop_ratio = Column(String(10), nullable=True, comment='裁剪比例，如3:4')
    extract_real_type = Column(String(20), nullable=True, comment='实拍图类型，如上装、下装等')
    
    # 图片信息
    source_images = Column(JSON, nullable=False, comment='源图片信息数组')
    model_image = Column(String(255), nullable=True, comment='模特图片信息')
    processed_results = Column(JSON, nullable=False, comment='处理结果数组，包含原图、效果图、实拍图URL')
    
    # 统计信息
    source_count = Column(Integer, nullable=False, default=0, comment='源图片数量')
    success_count = Column(Integer, nullable=False, default=0, comment='成功处理数量')
    failed_count = Column(Integer, nullable=False, default=0, comment='失败处理数量')
    total_processed = Column(Integer, nullable=False, default=0, comment='总处理数量（成功+失败）')
    
    # 索引
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
        Index('idx_task_source', 'task_source'),
        Index('idx_batch_id', 'batch_id'),
    )

