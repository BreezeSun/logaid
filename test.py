import logaid as log
log.init(filename='123.log',rotating='day')
log.debug('hello world')
log.info('hello world')
log.warning('hello world')
log.success('hello world')
log.error('hello world')
log.critical('hello world',123,{},[],False)