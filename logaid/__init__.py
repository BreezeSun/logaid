from .log import debug, info,success, warning, error,fatal,critical
from . import log
from . import log as logger
from . import log as Logger
__all__ = ['debug', 'info','success', 'warning', 'error','fatal','critical','logger','Logger']


def init(name='',level='DEBUG',filename=False,save=False,save_mode='a',format=False,show=True,print_pro=False,color={},rotating=None):
    log.init(name=name,level=level,filename=filename,save=save,save_mode=save_mode,format=format,show=show,print_pro=print_pro,color=color,rotating=rotating)
    global debug, info,success, warning, error,fatal,critical
    debug = log.debug
    info = log.info
    success = log.success
    warning= log.warning
    error = log.error
    fatal = log.fatal
    critical = log.critical