import logging
import logging.handlers
import inspect
import os
from time import strftime
import builtins
from logaid.mailer import Mail


email_usable = False

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
    else:
        result = txt
    return result



def add_context_info(func,level=logging.INFO,filename=False,format='',show=True,color={},emailer={}):
    def wrapper(*args, **kwargs):
        [logging.root.removeHandler(handler) or handler.close() for handler in logging.root.handlers[:]]
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
        handler_list =[]
        if filename:
            handler_list.append(logging.FileHandler(filename,encoding='utf-8'))
        if show:
            handler_list.append(logging.StreamHandler())
        if not any([filename,show]):
            logging.disable(logging.CRITICAL)

        if format:
            format_txt = format.replace('%(pathname)s', str(frame.f_code.co_filename)).replace('%(funcName)s', str(func_name)).replace('%(lineno)d', str(lineno))
        else:
            if filename:
                format_txt = f'File "{co_filename}", line {lineno}, time %(asctime)s, func {func_name}, level %(levelname)s: %(message)s'
            else:
                format_txt = f'File "{co_filename}", line {lineno}, func {func_name}, level %(levelname)s: %(message)s'

        func_dict = {'warning':'WARNING','error':'ERROR','fatal':'FATAL','critical':'CRITICAL'}
        if func.__name__ == 'debug':
            color_txt = color.get('DEBUG','') or 'gray'
            format_txt = put_colour(format_txt,color=color_txt)
            args = (' '.join([put_colour(str(i),color=color_txt) if not filename else str(i) for i in args ]),)
        elif func.__name__ == 'info':
            color_txt = color.get('INFO','') or 'cyan'
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

        logging.basicConfig(level=level,
                                    format=format_txt,
                                    handlers=handler_list)
        aid_logger = logging.getLogger(__name__)
        if func.__name__ == 'debug':
            aid_func = aid_logger.debug
        elif func.__name__ == 'info':
            aid_func = aid_logger.info
        elif func.__name__ == 'warning':
            aid_func = aid_logger.warning
        elif func.__name__ == 'error':
            aid_func = aid_logger.error
        elif func.__name__ == 'fatal':
            aid_func = aid_logger.fatal
        elif func.__name__ == 'critical':
            aid_func = aid_logger.critical
        else:
            aid_func = func
        return aid_func(*args, **kwargs)
    return wrapper

debug = add_context_info(logging.debug)
info = add_context_info(logging.info)
warning = add_context_info(logging.warning)
error = add_context_info(logging.error)
fatal = add_context_info(logging.fatal)
critical = add_context_info(logging.critical)

def email(*args):
    if not email_usable:
        error(*args, ' [ERROR] mail func not usable,please set init param "email".')


def init(level='INFO',filename=False,save=False,format='',show=True,print_pro=False,color={},mailer={}):
    global debug,info,warning,error,fatal,critical,email_usable,email
    if level == 'DEBUG':
        log_level = logging.DEBUG
    elif level == 'INFO':
        log_level = logging.INFO
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
        path = os.path.dirname(os.getcwd() + '\\logs\\')  # 判断日志目录
        if not os.path.exists(path):
            os.makedirs(path)
        filename = strftime("logs\my_log_%Y_%m_%d_%H.log")

    emailer_copy = dict(mailer)

    debug = add_context_info(logging.debug, log_level,filename,format,show,color,emailer_copy)
    info = add_context_info(logging.info, log_level,filename,format,show,color,emailer_copy)
    warning = add_context_info(logging.warning, log_level,filename,format,show,color,emailer_copy)
    error = add_context_info(logging.error, log_level,filename,format,show,color,emailer_copy)
    fatal = add_context_info(logging.fatal, log_level,filename,format,show,color,emailer_copy)
    critical = add_context_info(logging.critical, log_level,filename,format,show,color,emailer_copy)
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

