__author__ = '刘士'
__version__ = '1.4.7'

from .HTMLReport import TestRunner
from .images.SaveImages import AddImage
from .log.Logger import GeneralLogger

# 日志记录器
logger = GeneralLogger().get_logger
