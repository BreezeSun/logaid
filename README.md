# LogAid
<p align="left">
    <a href="https://pypi.python.org/pypi/logaid"><img alt="Pypi version" src="https://img.shields.io/pypi/v/logaid.svg"></a>
    <a href="https://pypi.python.org/pypi/logaid"><img alt="Python versions" src="https://img.shields.io/badge/python-3.0%2B%20%7C%20PyPy-blue.svg"></a>
    <a href="https://github.com/BreezeSun/logaid/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/BreezeSun/logaid.svg"></a>
</p>

**LogAid** is a Python library designed to make logging enjoyable.

Have you ever felt too lazy to configure a proper logger and just defaulted to using print()? I know I have. But logging is crucial for any application and really simplifies debugging. With **LogAid**, you’ve got no excuse not to log from the start—it’s as easy as from logaid import logger.

This library aims to ease the pain of Python logging by offering a range of helpful features that address the common pitfalls of standard loggers. Logging in your app should be second nature, and **LogAid** strives to make that process both easy and powerful.
______________________________________________________________________
## wait development
```console
1. add jsonlogger
```
## Installation
```console
pip install logaid
```

## Usage 
### just print
```python
import logaid as log

log.debug('hello world')
log.info('hello world')
log.warning('hello world')
log.success('hello world')
log.error('hello world')
log.fatal('hello world',123,{},[],False)
```
#### or
```python
import logaid

logaid.info('hello world')
logaid.warning('hello world')
logaid.error('hello world')
logaid.fatal('hello world',123,{},[],False)
```
![image](static/0ca51db101c3a32bf3ec3613866347ca.png)
### click jump into code line
![image](static/605d39ba4fa031f56f2bc011fa48129b.png)
### open super print
```python
from logaid import log
log.init(print_pro=True)

print("Hello World")
```
![image](static/screenshot-20240929-103230.png)
### auto_save
```python
from logaid import log
log.init(level='DEBUG',save=True)

log.info('hello world')
```
### save as filename and not print
```python
from logaid import log
log.init(level='DEBUG',filename='test.log',show=False)

log.info('hello world')
```
### define format
```python
from logaid import log
log.init(level='INFO',format='%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s')

log.info('hello world')

```
![image](static/screenshot-20240929-152333.png)
### Split the log files by day
```python
from logaid import log
log.init(filename='test.log',rotating='day')
log.info('hello world')
```
### define color
```python
from logaid import log
color = {
    'DEBUG':'gray',
    'INFO':'green',
    'WARNING':'yellow',
    'ERROR':'red',
    'FATAL':'violet',
}
log.init(level='DEBUG',color=color)

log.debug('hello world')
log.info('hello world')
log.warning('hello world')
log.error('hello world')
log.fatal('hello world',123,{},[],False)
```
![image](static/screenshot-20240929-153019.png)
### send email
```python
from logaid import log
mailer = {
        'host': 'smtp.qq.com',      
        'token': 'xxxxxxxxxxxx',    # IMAP/SMTP code
        'nickname':'LogAid',    
        'sender': 'xxxxxx@qq.com',
        'receivers': ['xxxxxx@qq.com'],
        'subject': 'A log aid for you.',
        'open_level': ['ERROR','FATAL']   # More than WARNING valid.
    }
log.init(level='ERROR',mailer=mailer)

log.error('Exec appear error.')
log.email('Send email tip.')
```