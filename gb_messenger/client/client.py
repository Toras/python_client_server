import logging
import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import get_message, send_message, DecoLogCls
import gb_messenger_logs.configs.client_log_config


client_log = logging.getLogger('client')


@DecoLogCls()
def action_to_server(action):
    result = {
        'action': action,
        'timestamp': int(time.time())
    }
    return result


@DecoLogCls()
def action_from_server(msg):
    if 'timestamp' in msg and 'response' in msg:
        client_log.info(f'{msg["response"]}')


if __name__ == '__main__':
    SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
    server_address = '127.0.0.1'
    server_port = 9000
    try:
        if argv.count('-a') != 0:
            server_address = argv[argv.index('-a') + 1]
    except IndexError:
        client_log.error('Need address after -a')
        exit(1)
    try:
        if argv.count('-p') != 0:
            server_port = int(argv[argv.index('-p') + 1])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
    except IndexError:
        client_log.error('Need port number after -p')
        exit(1)
    except ValueError:
        client_log.error('Port must be between 1025 and 65535')
        exit(1)
    client_log.info(f'Connecting to server at: {server_address} on: {server_port}')
    try:
        SERVER_SOCKET.connect((server_address, server_port))
        msg_to_server = action_to_server(0)
        send_message(SERVER_SOCKET, msg_to_server, 'utf-8')
        msg_from_server = get_message(SERVER_SOCKET, 1024, 'utf-8')
        action_from_server(msg_from_server)
    except ConnectionRefusedError:
        client_log.error('Connection refused!')
    finally:
        SERVER_SOCKET.close()
