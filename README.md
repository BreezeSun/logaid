# LogAid

A log aid for you.
## wait development
```console
1. add jsonlogger
2. add rotation
```
## Installation
```console
pip install logaid
```

## Usage 
### just print
```python
from logaid import log

log.info('hello world')
log.warning('hello world')
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