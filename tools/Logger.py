import logging
from pathlib import Path

from core.tools.BaseConfig import BaseConfig

formatter: logging.Formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s - %(message)s')


class CustomLoggingHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg: str = self.format(record)
            print(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def __init_logger(log_file: Path, name: str, file_level: int = logging.WARN, console: bool = False, cons_level: int = logging.DEBUG) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file, encoding='UTF8')
    fh.setLevel(file_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if console:
        ch: CustomLoggingHandler = CustomLoggingHandler()
        ch.setLevel(cons_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


log_file_main: Path = Path(BaseConfig.get_dir_out(), BaseConfig.get_name() + '_error.log')
name_main: str = BaseConfig.get_name() + '_main'
log_file_success: Path = Path(BaseConfig.get_dir_out(), BaseConfig.get_name() + '_success.log')
name_success: str = BaseConfig.get_name() + '_success'


def init_loggers():
    __init_logger(log_file_main, name_main, file_level=logging.WARN, console=True, cons_level=logging.DEBUG)
    __init_logger(log_file_success, name_success, file_level=logging.INFO, console=True)


def get_logger_main() -> logging.Logger:
    return logging.getLogger(name_main)


def get_logger_success() -> logging.Logger:
    return logging.getLogger(name_success)
