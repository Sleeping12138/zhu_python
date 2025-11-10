import logging
import sys
from datetime import datetime
from pathlib import Path


# 配置日志
def setup_logging():
    """配置日志系统"""
    log_dir = Path(__file__).parent.parent / 'Log'

    log_dir.mkdir(exist_ok=True)

    # 使用日期作为文件名
    log_filename = f"ai_photo_editor_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_filepath = log_dir / log_filename

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # 配置根日志器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_filepath, encoding='utf-8')
        ]
    )

    logger = logging.getLogger('ai_photo_editor')
    logger.setLevel(logging.INFO)

    return logger
