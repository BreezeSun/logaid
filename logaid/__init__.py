from .log import debug, info, warning, error,fatal,critical
from . import log
from . import log as logger
from . import log as Logger
__all__ = ['debug', 'info', 'warning', 'error','fatal','critical','logger','Logger']


def init(level='INFO',filename=False,save=False,format=False,show=True,print_pro=False,color={}):
    log.init(level=level,filename=filename,save=save,format=format,show=show,print_pro=print_pro,color=color)
    global debug, info, warning, error,fatal,critical
    debug = log.debug
    info = log.info
    warning= log.warning
    error = log.error
    fatal = log.fatal
    critical = log.critical