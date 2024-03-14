import logging
import os
import sys
import traceback
from functools import wraps



class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.funcName = record.funcName
        record.pathname = record.pathname
        record.lineno = record.lineno
        return super().format(record)


def setup_logger(log_path='log/app.log'):
    """生成logger对象

    Args:
        log_path (str, optional): 日志文件保存的地址. Defaults to 'log/app.log'.

    Returns:
        logger对象: _description_
    """    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = CustomFormatter('%(asctime)s [%(levelname)s] %(funcName)s - %(message)s')

    # 设置控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 设置文件输出
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def log_exceptions_and_info(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info('方法 "%s" 执行成功', func.__name__)
                log_parameters(logger, func, *args, **kwargs)
                log_return(logger, func, result)
                return result
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback_details = {
                    'filename': os.path.abspath(func.__code__.co_filename),
                    'lineno': exc_traceback.tb_lineno,
                    'name': func.__name__,
                    'type': exc_type.__name__,
                    'message': str(e),
                    'traceback': traceback.format_exc()
                }
                logger.error('%(name)s - %(lineno)s - %(type)s: %(message)s\n%(traceback)s', traceback_details)
        return wrapper
    return decorator


def log_parameters(logger, func, *args, **kwargs):
    args_names = func.__code__.co_varnames[:func.__code__.co_argcount]
    params = {name: arg for name, arg in zip(args_names, args)}
    params.update(kwargs)
    logger.info('Function "%s" 入参: %s', func.__name__, params)


def log_return(logger, func, result):
    logger.info('Function "%s" 出参: %s', func.__name__, result)
