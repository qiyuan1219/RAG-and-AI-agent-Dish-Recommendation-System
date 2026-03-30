import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime
# 日志文件路径
LOG_ROOT=get_abs_path("logs")
os.makedirs(LOG_ROOT,exist_ok=True)

DEFAULT_LOG_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

def get_logger(
        name:str="my_logger",
        console_level:int = logging.INFO,
        file_level:int = logging.DEBUG,
        log_file:str=None,
)->logging.Logger:

    #创建日志器
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 文件Handler
    if not log_file:        # 日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

logger = get_logger()
'''
# 快捷获取日志器
logger = get_logger()
if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")
    
 #D:\Project_Package\PythonProject\AI Agent口味推荐系统\config/config.txt
2026-03-24 23:27:58,459 - my_logger - INFO - logger_handler.py:49 - 信息日志
2026-03-24 23:27:58,459 - my_logger - ERROR - logger_handler.py:50 - 错误日志
2026-03-24 23:27:58,459 - my_logger - WARNING - logger_handler.py:51 - 警告日志
'''
