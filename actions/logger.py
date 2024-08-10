import logging

# 日志工具
def setup_logger(name, log_file, level=logging.INFO):
    """创建并配置日志工具"""
    handler = logging.FileHandler(log_file)        
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# 创建一个全局日志器实例
logger = setup_logger('project_logger', 'project.log')