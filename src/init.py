import os
import sys
import logging
import conf

def init():
    init_logging()
    init_tmp_dir()
    save_pid()

def init_logging():
    """初始化日志
    """

    format = '[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, format=format, datefmt=datefmt)
    sys.excepthook = exception_hook

def exception_hook(exc_type, exc_value, exc_traceback):
    """全局异常钩子
    """

    if issubclass(exc_type, KeyboardInterrupt):
        # 如果是键盘中断异常，就让它正常处理
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # 记录异常信息到日志
    logging.error("Uncaught exception.", exc_info=(exc_type, exc_value, exc_traceback))

def init_tmp_dir():
    """初始化临时目录
    """

    if not os.path.exists(conf.TMP_DIR):
        os.makedirs(conf.TMP_DIR)

def save_pid():
    """保存进程ID
    """

    with open(conf.PID_FILENAME, 'w') as f:
        pid = os.getpid()
        f.write(str(pid))
