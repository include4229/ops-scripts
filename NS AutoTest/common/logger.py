# 日志模块
import logging
import sys
import os
from datetime import datetime
from config.settings import config

def setup_logger(name: str = "nsi_test", level=logging.INFO):
    """配置日志系统"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    try:
        os.makedirs(config.LOG_DIR, exist_ok=True)
        log_file = os.path.join(
            config.LOG_DIR, 
            f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass
    
    return logger

def get_logger(name: str = "nsi_test"):
    return logging.getLogger(name)
