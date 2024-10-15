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