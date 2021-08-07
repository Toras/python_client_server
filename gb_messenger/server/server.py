import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import actions, get_message, send_message


def action_from_client(msg):
    result = {}
    if 'timestamp' in msg and 'action' in msg:
        if msg['action'] in actions.keys():
            if msg['action'] == 0:
                result = {
                    'response': 200,
                    'timestamp': int(time.time()),
                    'alert': 'OK'
                }
        else:
            result = {
                'response': 400,
                'timestamp': int(time.time()),
                'error': 'wrong action'
            }
    else:
        result = {
            'response': 400,
            'timestamp': int(time.time()),
            'error': 'wrong msg format'
        }
    return result


if __name__ == '__main__':
    SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
    server_address = '127.0.0.1'
    server_port = 9000
    try:
        if argv.count('-a') != 0:
            server_address = argv[argv.index('-a') + 1]
    except IndexError:
        print('Need address after -a')
        exit(1)
    try:
        if argv.count('-p') != 0:
            server_port = int(argv[argv.index('-p') + 1])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
    except IndexError:
        print('Need port number after -p')
        exit(1)
    except ValueError:
        print('Port must be between 1025 and 65535')
        exit(1)
    SERVER_SOCKET.bind((server_address, server_port))
    print(f'starting msg server at: {server_address} on: {server_port}')
    SERVER_SOCKET.listen(5)

    try:
        while True:
            CLIENT_SOCKET, client_address = SERVER_SOCKET.accept()
            msg_from_client = get_message(CLIENT_SOCKET, 1024, 'utf-8')
            msg_to_client = action_from_client(msg_from_client)
            print(f'incoming inquiry from {client_address}, '
                  f'action: {actions[msg_from_client["action"]]}')
            send_message(CLIENT_SOCKET, msg_to_client, 'utf-8')
            CLIENT_SOCKET.close()
    finally:
        SERVER_SOCKET.close()
        print(f'stopped msg server at: {server_address} on: {server_port}')
