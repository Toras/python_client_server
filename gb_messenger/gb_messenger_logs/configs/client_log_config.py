import sys
import os
import logging


log_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.dirname(log_path)
log_path = os.path.join(log_path, 'logs\\client.log')

log_formatter = logging.Formatter('%(asctime)-30s %(levelname)-10s %(module)-25s %(message)s')

log_handler_file = logging.FileHandler(log_path, encoding='utf-8')
log_handler_file.setLevel(logging.DEBUG)
log_handler_file.setFormatter(log_formatter)

log_handler_stream = logging.StreamHandler(sys.stderr)
log_handler_stream.setLevel(logging.ERROR)
log_handler_stream.setFormatter(log_formatter)

client_log = logging.getLogger('client')
client_log.addHandler(log_handler_file)
client_log.addHandler(log_handler_stream)
client_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    client_log.error('error test client logging')
    client_log.info('info test client logging')
    client_log.debug('debug test client logging')
