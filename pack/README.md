# LogAid

A log aid for you.

## Installation
```
pip install logaid
```

## Usage 
### just print
```
from logaid import log

log.info('hello world')
log.warning('hello world')
log.error('hello world')
log.fatal('hello world',123,{},[],False)
```
### open super print
```
from logaid import log
log.init(print_pro=True)

print("Hello World")
```
### auto_save
```
from logaid import log
log.init(level='DEBUG',save=True)

log.info('hello world')
```
### save as filename and not print
```
from logaid import log
log.init(level='DEBUG',filename='cs.log',show=False)

log.info('hello world')
```
### define format
```
from logaid import log
log.init(level='INFO',format='%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s')

log.info('hello world')

```