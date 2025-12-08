import logging
import os
from datetime import datetime


class LevelFilter(logging.Filter):
    """
    日志级别过滤器
    """

    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class LoggerUtil:
    """
    日志工具类
    """

    def __init__(self, name='logger', log_dir='logs', level=logging.DEBUG):
        # 设置名称和级别（设置为DEBUG以记录所有日志）
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加handler
        if self.logger.handlers:
            return

        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件输出
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 全部日志文件
        all_log_file = os.path.join(log_dir, f'{name}_all_{datetime.now().strftime("%Y%m%d")}.log')
        all_handler = logging.FileHandler(all_log_file, encoding='utf-8')
        all_handler.setLevel(logging.DEBUG)
        all_handler.setFormatter(formatter)
        self.logger.addHandler(all_handler)

        # INFO日志文件
        info_log_file = os.path.join(log_dir, f'{name}_info_{datetime.now().strftime("%Y%m%d")}.log')
        info_handler = logging.FileHandler(info_log_file, encoding='utf-8')
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(LevelFilter(logging.INFO))
        info_handler.setFormatter(formatter)
        self.logger.addHandler(info_handler)

        # ERROR日志文件
        error_log_file = os.path.join(log_dir, f'{name}_error_{datetime.now().strftime("%Y%m%d")}.log')
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.addFilter(LevelFilter(logging.ERROR))
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)
