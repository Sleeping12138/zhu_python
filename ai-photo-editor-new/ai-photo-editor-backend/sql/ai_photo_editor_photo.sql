CREATE TABLE ai_photo_editor_photo
(
    id                BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '任务ID',
    -- 批次ID，用于标识同一批处理的任务
    batch_id          VARCHAR(36) NULL COMMENT '批次ID，同一批处理的任务具有相同的batch_id',
    -- 任务状态
    status            ENUM('success', 'failed') NOT NULL COMMENT '任务状态：成功或失败',
    -- 任务来源
    task_source       ENUM('batch', 'scheduled') NOT NULL DEFAULT 'batch' COMMENT '任务来源：batch=批量处理，scheduled=定时任务',
    -- 时间字段
    created_at        DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    completed_at      DATETIME      DEFAULT CURRENT_TIMESTAMP COMMENT '完成时间',
    -- 处理配置
    process_type      ENUM('model', 'real') NOT NULL COMMENT '处理类型：模特图或实拍图',
    process_steps     JSON NOT NULL COMMENT '处理步骤配置，如{"watermark":true,"faceSwap":true}',
    crop_ratio        VARCHAR(10) NULL COMMENT '裁剪比例，如3:4',
    extract_real_type VARCHAR(20) NULL COMMENT '实拍图类型，如上装、下装等',
    -- 图片信息
    source_images     JSON NOT NULL COMMENT '源图片信息数组',
    model_image       VARCHAR(255) NULL COMMENT '模特图片信息',
    processed_results JSON NOT NULL COMMENT '处理结果数组，包含原图、效果图、实拍图URL',
    -- 统计信息
    source_count      INT  NOT NULL DEFAULT 0 COMMENT '源图片数量',
    success_count     INT  NOT NULL DEFAULT 0 COMMENT '成功处理数量',
    failed_count      INT  NOT NULL DEFAULT 0 COMMENT '失败处理数量',
    total_processed   INT  NOT NULL DEFAULT 0 COMMENT '总处理数量（成功+失败）',
    INDEX             idx_status (status),
    INDEX             idx_created_at (created_at),
    INDEX             idx_task_source (task_source),
    INDEX             idx_batch_id (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='批量处理任务表'