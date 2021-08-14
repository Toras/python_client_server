import logging
import sys
import traceback
import gb_messenger_logs.configs.server_log_config
import gb_messenger_logs.configs.client_log_config


if sys.argv[0].split('/')[-1] == 'client.py':
    log = logging.getLogger('client')
else:
    log = logging.getLogger('server')


def deco_log(func):
    def wrapper(*args, **kwargs):
        log.debug(f'Вызвана функция {func.__name__} с аргументами {args}, {kwargs}. '
                  f'Вызвана из модуля {func.__module__}. '
                  f'Вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}',
                  stacklevel=2)
        return func(*args, **kwargs)
    return wrapper


class DecoLogCls:

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            log.debug(f'Вызвана функция {func.__name__} с аргументами {args}, {kwargs}. '
                      f'Вызвана из модуля {func.__module__}. '
                      f'Вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}',
                      stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
