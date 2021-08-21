import logging
import select
import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import actions, get_message, send_message, deco_log
import gb_messenger_logs.configs.server_log_config


log = logging.getLogger('server')


@deco_log
def action_from_client(msg, msgs_list, client_sock):
    log.debug(f'msg from {client_sock}: {msg}')
    result = {}
    if 'timestamp' in msg and 'action' in msg:
        if msg['action'] in actions.keys():
            if msg['action'] == 0:
                result = {
                    'response': 200,
                    'timestamp': int(time.time()),
                    'alert': 'OK'
                }
                send_message(client_sock, result, 'utf-8')
                return
            elif msg['action'] == 2:
                msgs_list.append((msg['user'], msg['message']))
                return
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
    send_message(client_sock, result, 'utf-8')


def main_loop():
    pass


if __name__ == '__main__':
    server_address = '127.0.0.1'
    server_port = 9000
    try:
        if argv.count('-a') != 0:
            server_address = argv[argv.index('-a') + 1]
    except IndexError:
        log.error('Need address after -a')
        exit(1)
    try:
        if argv.count('-p') != 0:
            server_port = int(argv[argv.index('-p') + 1])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
    except IndexError:
        log.error('Need port number after -p')
        exit(1)
    except ValueError:
        log.error('Port must be between 1025 and 65535')
        exit(1)

    SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
    SERVER_SOCKET.bind((server_address, server_port))
    SERVER_SOCKET.settimeout(0.5)
    clients_list = []
    messages_list = []
    log.info(f'starting msg server at: {server_address} on: {server_port}')
    SERVER_SOCKET.listen(5)

    try:
        while True:
            try:
                CLIENT_SOCKET, client_address = SERVER_SOCKET.accept()
            except OSError:
                pass
            else:
                log.info(f'Connected with client {client_address}')
                clients_list.append(CLIENT_SOCKET)
            rcv_msg_list = []
            snd_msg_list = []
            err_list = []
            try:
                if clients_list:
                    rcv_msg_list, snd_msg_list, err_list = select.select(clients_list, clients_list, [], 0)
            except OSError:
                pass

            if rcv_msg_list:
                for client in rcv_msg_list:
                    try:
                        msg_from_client = get_message(client, 1024, 'utf-8')
                        action_from_client(msg_from_client, messages_list, client)
                    except:
                        log.info(f'Client {client.getpeername()} logged off')
                        clients_list.remove(client)

            if snd_msg_list and messages_list:
                msg_to_client = {
                    'action': 2,
                    'sender': messages_list[0][0],
                    'timestamp': int(time.time()),
                    'message': messages_list[0][1]
                }
                del messages_list[0]
                for client in snd_msg_list:
                    try:
                        send_message(client, msg_to_client, 'utf-8')
                    except Exception as e:
                        log.info(f'Client {client.getpeername()} logged off')
                        clients_list.remove(client)
    finally:
        SERVER_SOCKET.close()
        log.info(f'stopped msg server at: {server_address} on: {server_port}')
