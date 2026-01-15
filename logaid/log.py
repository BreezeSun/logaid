import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler
import inspect
import os
from time import strftime
import builtins
from logaid.mailer import Mail
import random
import string

email_usable = False
logaid_has_handlers = False

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'fake_lineno'):
            record.fake_lineno = record.lineno
        if not hasattr(record, 'fake_pathname'):
            record.fake_pathname = record.pathname
        if not hasattr(record, 'fake_funcName'):
            record.fake_funcName = record.funcName
        if not hasattr(record, 'fake_levelname'):
            record.fake_levelname = record.levelname
        return super().format(record)


def put_colour(txt, color=None):
    if color == 'red':
        result = f"\033[31m{txt}\033[0m"
    elif color == 'green':
        result = f"\033[32m{txt}\033[0m"
    elif color == 'yellow':
        result = f"\033[33m{txt}\033[0m"
    elif color == 'blue':
        result = f"\033[34m{txt}\033[0m"
    elif color == 'violet':
        result = f"\033[35m{txt}\033[0m"
    elif color == 'cyan':
        result = f"\033[36m{txt}\033[0m"
    elif color == 'gray':
        result = f"\033[37m{txt}\033[0m"
    elif color == 'black':
        result = f"\033[30m{txt}\033[0m"
    elif color == 'default':
        result = f"\033[2m{txt}\033[0m"
    else:
        result = txt
    return result



def add_context_info(func,name='',level=logging.DEBUG,filename:str='',save_mode='a',format=''
                     ,show=True,only_msg=False,color={},emailer={}
                     ,rotating:str='',backupCount:int=30,maxBytes:int=50 * 1024 * 1024):
    global logaid_has_handlers

    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    logger_name = name or func.__name__ + random_str
    aid_logger = logging.getLogger(logger_name)
    aid_logger.propagate = False
    aid_logger.setLevel(level)
    if aid_logger.hasHandlers() and not logaid_has_handlers:
        logaid_has_handlers = True
        aid_logger.handlers.clear()
        format_txt = '[%(asctime)s] File "%(fake_pathname)s", line %(fake_lineno)d, func %(fake_funcName)s, level %(fake_levelname)s: %(message)s'
        format_txt = put_colour(format_txt, color='default')
        if filename:
            formatter = SafeFormatter(format_txt[5:-4])
            if rotating == 'day':
                file_handler = TimedRotatingFileHandler(
                    filename=filename,
                    when="midnight",
                    interval=1,
                    backupCount=backupCount,
                    encoding="utf-8"
                )
                file_handler.suffix = "%Y-%m-%d.log"
            elif rotating == 'size':
                file_handler = RotatingFileHandler(
                    filename=filename,
                    mode=save_mode,
                    maxBytes=maxBytes,
                    backupCount=backupCount,
                    encoding="utf-8"
                )
            elif rotating == 'day-size':
                file_handler = TimedRotatingFileHandler(
                    filename=filename,
                    when="midnight",
                    interval=1,
                    backupCount=backupCount,
                    encoding="utf-8"
                )
                file_handler.suffix = "%Y-%m-%d.log"
                file_handler.maxBytes = maxBytes
            else:
                file_handler = logging.FileHandler(filename,save_mode, encoding='utf-8')

            file_handler.setFormatter(formatter)
            aid_logger.addHandler(file_handler)
        if show:
            formatter = SafeFormatter(format_txt)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            aid_logger.addHandler(console_handler)

    def wrapper(*args, sep=' ', end='\n', file=None, **kwargs):
        global logaid_has_handlers
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        if func_name == '<module>':
            func_name = 'None'

        co_filename = frame.f_code.co_filename
        if '\\' in co_filename:
            co_filename = co_filename.split('\\')[-1]
        elif '/' in co_filename:
            co_filename = co_filename.split('/')[-1]
        lineno = frame.f_lineno


        if format:
            format_txt = format.replace('%(pathname)s', str(frame.f_code.co_filename)).replace('%(funcName)s', str(func_name)).replace('%(lineno)d', str(lineno))
        else:
            format_txt = f'[%(asctime)s] File "%(fake_pathname)s", line %(fake_lineno)d, func %(fake_funcName)s, level %(fake_levelname)s: %(message)s'
            if only_msg:
                format_txt = f'%(message)s'

        func_dict = {'success':'SUCCESS','warning':'WARNING','error':'ERROR','fatal':'FATAL','critical':'CRITICAL'}
        if name:
            color_txt = 'default'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ == 'debug':
            color_txt = color.get('DEBUG','') or 'gray'
            format_txt = put_colour(format_txt,color=color_txt)
            args = (' '.join([put_colour(str(i),color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ == 'info':
            color_txt = color.get('INFO','') or 'cyan'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ == 'success':
            color_txt = color.get('SUCCESS','') or 'green'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ == 'warning':
            color_txt = color.get('WARNING','') or color.get('WARN','') or 'yellow'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ == 'error':
            color_txt = color.get('ERROR','') or 'red'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        elif func.__name__ in ['fatal','critical']:
            color_txt = color.get('FATAL','') or color.get('CRITICAL','') or 'violet'
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)
        else:
            color_txt = None
            format_txt = put_colour(format_txt, color=color_txt)
            args = (' '.join([put_colour(str(i), color=color_txt) if not filename else str(i) for i in args]),)

        if emailer:
            if func_dict.get(func.__name__,'') in emailer.get('open_level',[]):
                emailer_dict = dict(emailer)
                emailer_dict['subject'] = f'[{func.__name__}] ' + emailer_dict['subject']
                e_mailer = Mail(emailer_dict)
                err_bool, err_txt = e_mailer.send(args[0][5:-4])
                if not err_bool:
                    args = (args[0] + ' [ERROR] Send LogAid mail failed. ' + str(err_txt),)
                else:
                    args = (args[0] + ' [email]',)
        if not aid_logger.hasHandlers() or not logaid_has_handlers:
            logaid_has_handlers = True
            if show:
                formatter = SafeFormatter(format_txt)
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                aid_logger.addHandler(console_handler)
            if filename:
                formatter = SafeFormatter(format_txt[5:-4])
                file_handler = logging.FileHandler(filename,save_mode,encoding='utf-8')
                file_handler.setFormatter(formatter)
                aid_logger.addHandler(file_handler)

            if not any([show,filename]):
                return

        if 'debug' in func.__name__:
            aid_func = aid_logger.debug
        elif 'info' in func.__name__:
            aid_func = aid_logger.info
        elif 'success' in func.__name__:
            aid_func = aid_logger.warning
        elif 'warning' in func.__name__:
            aid_func = aid_logger.warning
        elif 'error' in func.__name__:
            aid_func = aid_logger.error
        elif 'fatal' in func.__name__:
            aid_func = aid_logger.fatal
        elif 'critical' in func.__name__:
            aid_func = aid_logger.critical
        else:
            aid_func = func
        extra = {"fake_lineno": lineno, "fake_funcName": func_name, "fake_pathname": co_filename}
        if 'success' in func.__name__:
            extra.update({'fake_levelname':'SUCCESS'})

        return aid_func(*args,extra=extra, **kwargs)
    return wrapper

def success(*args,**kwargs):pass

debug = add_context_info(logging.debug)
info = add_context_info(logging.info)
warning = add_context_info(logging.warning)
success = add_context_info(success)
error = add_context_info(logging.error)
fatal = add_context_info(logging.fatal)
critical = add_context_info(logging.critical)

def email(*args):
    if not email_usable:
        error(*args, ' [ERROR] mail func not usable,please set init param "email".')


def init(name:str='',level:str='DEBUG',filename:str='',save=False,save_mode:str='a',
         format:str='',show=True,print_pro=False,only_msg=False,color:dict={},mailer:dict={}
         ,rotating:str='',backupCount:int=30,maxBytes:int=50 * 1024 * 1024):
    global success
    """
    
    :param name: log space name (attention:use it color will vanish)
    :param level: log level
    :param filename: filename of save log
    :param save: if save log
    :param save_mode: write log file type. example: a/a+/w/w+
    :param format: custom log print by you
    :param show: if print in console
    :param print_pro: print of python become info
    :param only_msg: only print message
    :param color: custom color print by you
    :param mailer: use mail notify
    :param rotating: `day` or `size` Cut logs by day or by size,Default 0-point cutting or 50MB cutting
    :param backupCount: by default, 30 sets of data are saved
    :param maxBytes: The cutting size in the cutting mode，Default 50MB
    :return:
    """
    global debug,info,warning,error,fatal,critical,email_usable,email
    if level == 'DEBUG':
        log_level = logging.DEBUG
    elif level == 'INFO':
        log_level = logging.INFO
    elif level == 'SUCCESS':
        log_level = 25
    elif level == 'WARN':
        log_level = logging.WARN
    elif level == 'WARNING':
        log_level = logging.WARNING
    elif level == 'ERROR':
        log_level = logging.ERROR
    elif level == 'FATAL':
        log_level = logging.FATAL
    elif level == 'CRITICAL':
        log_level = logging.CRITICAL
    else:
        log_level = logging.INFO
    if save:
        log_dir = os.path.join("logs")
        os.makedirs(log_dir, exist_ok=True)
        filepath = strftime("logaid_%Y_%m_%d_%H_%M_%S.log")
        filename = os.path.join(log_dir, filepath)

    def success(*args,**kwargs):pass

    emailer_copy = dict(mailer)

    debug = add_context_info(logging.debug,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    info = add_context_info(logging.info,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    warning = add_context_info(logging.warning,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    success = add_context_info(success,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    error = add_context_info(logging.error,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    fatal = add_context_info(logging.fatal,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    critical = add_context_info(logging.critical,name, log_level,filename,save_mode,format,show,only_msg,color,emailer_copy,rotating,backupCount,maxBytes)
    if print_pro:
        builtins.print = info

    def email(*args):
        if not email_usable:
            error(*args, ' [ERROR] mail func not usable,please set init param "email".')
            return
        emailer = Mail(emailer_copy)
        err_bool, err_txt = emailer.send(args[0])

        if not err_bool:
            args = args[0]
            error(args)
            return
        info(*args,' [email] send success.')

    if mailer:
        email_usable = True
        email = email

