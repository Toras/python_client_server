import logging
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import get_message, send_message, DecoLogCls
import gb_messenger_logs.configs.client_log_config


client_log = logging.getLogger('client')


@DecoLogCls()
def action_to_server(action, sock, user='guest'):
    if action == 0:
        result = {
            'action': action,
            'timestamp': int(time.time()),
            'user': user
        }
    elif action == 2:
        msg = input('Сообщение (!!! - для завершения): ')

        if msg == '!!!':
            sock.close()
            client_log.info('Closed by user')
            exit(0)
        result = {
            'action': action,
            'message': msg,
            'timestamp': int(time.time()),
            'user': user
        }
    return result


@DecoLogCls()
def action_from_server(msg):
    if 'timestamp' in msg and 'response' in msg:
        client_log.info(f'{msg["response"]}')
    elif 'action' in msg:
        if msg['action'] == 2:
            print(f'Message from user {msg["sender"]}:\n{msg["message"]}')
        else:
            client_log.info(f'Wrong message from server: {msg}')


if __name__ == '__main__':
    server_address = '127.0.0.1'
    server_port = 9000
    client_mode = 'send'
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
    try:
        if argv.count('-m') != 0:
            client_mode = argv[argv.index('-m') + 1]
            if client_mode in ('listen', 'send'):
                pass
            else:
                raise ValueError
    except ValueError:
        client_log.error('Mode must be listen or send!')
        exit(1)
    client_log.info(f'Connecting to server at: {server_address} on: {server_port}')

    try:
        SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
        SERVER_SOCKET.connect((server_address, server_port))
        msg_to_server = action_to_server(0, SERVER_SOCKET)
        send_message(SERVER_SOCKET, msg_to_server, 'utf-8')
        msg_from_server = get_message(SERVER_SOCKET, 1024, 'utf-8')
        action_from_server(msg_from_server)
    except ConnectionRefusedError:
        client_log.error('Connection refused!')
    else:
        while True:
            if client_mode == 'send':
                try:
                    msg_from_server = action_to_server(2, SERVER_SOCKET)
                    send_message(SERVER_SOCKET, msg_from_server, 'utf-8')
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_log.error(f'Server {server_address}:{server_port} connection was lost!')
                    sys.exit(1)
            elif client_mode == 'listen':
                try:
                    msg_from_server = get_message(SERVER_SOCKET, 1024, 'utf-8')
                    action_from_server(msg_from_server)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_log.error(f'Server {server_address}:{server_port} connection was lost!')
                    sys.exit(1)
                except Exception as e:
                    client_log.error(f'Error {e}')
    finally:
        SERVER_SOCKET.close()
