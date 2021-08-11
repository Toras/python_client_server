import sys
import os
import logging
import logging.handlers


log_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.dirname(log_path)
log_path = os.path.join(log_path, 'logs\\server.log')

log_formatter = logging.Formatter('%(asctime)-30s %(levelname)-10s %(module)-25s %(message)s')

log_handler_file = logging.handlers.TimedRotatingFileHandler(log_path, 'D', 1, encoding='utf-8')
log_handler_file.setLevel(logging.DEBUG)
log_handler_file.setFormatter(log_formatter)

log_handler_stream = logging.StreamHandler(sys.stderr)
log_handler_stream.setLevel(logging.ERROR)
log_handler_stream.setFormatter(log_formatter)

server_log = logging.getLogger('server')
server_log.addHandler(log_handler_file)
server_log.addHandler(log_handler_stream)
server_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    server_log.error('error test server logging')
    server_log.info('info test server logging')
    server_log.debug('debug test server logging')
