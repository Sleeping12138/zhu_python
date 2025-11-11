-- 定时任务表建表语句
CREATE TABLE IF NOT EXISTS `ai_photo_editor_scheduled_tasks` (
  `task_id` VARCHAR(36) NOT NULL COMMENT '任务ID（UUID）',
  `scheduled_time` DATETIME NOT NULL COMMENT '计划执行时间',
  `source_image_urls` TEXT NOT NULL COMMENT '源图片URL列表（JSON格式）',
  `model_image_url` VARCHAR(500) DEFAULT NULL COMMENT '模特图片URL（可选）',
  `process_config` TEXT NOT NULL COMMENT '处理配置（JSON格式，包含process_type、process_steps、crop_ratio、extract_real_type等）',
  `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending-等待中, processing-执行中, completed-已完成, failed-失败',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '删除标记：0-未删除, 1-已删除',
  PRIMARY KEY (`task_id`),
  KEY `idx_scheduled_time` (`scheduled_time`),
  KEY `idx_status` (`status`),
  KEY `idx_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='定时任务表';

