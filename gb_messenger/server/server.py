import logging
import select
import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import actions, get_message, send_message, deco_log
import gb_messenger_logs.configs.server_log_config


log = logging.getLogger('server')


@deco_log
def action_from_client(msg, msgs_list, client_sock, clients_list, names_dict):
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
                if msg['user'] not in names_dict.keys():
                    names_dict[msg['user']] = client_sock
                    send_message(client_sock, result, 'utf-8')
                else:
                    result = {
                        'response': 400,
                        'timestamp': int(time.time()),
                        'error': 'user name already registered'
                    }
                    send_message(client_sock, result, 'utf-8')
                    clients.remove(client_sock)
                    client_sock.close()
                return
            elif msg['action'] == 2:
                msgs_list.append(msg)
                return
            elif msg['action'] == 5 and 'user' in msg:
                print(msg['user'])
                print(clients_list)
                print(names_dict)
                clients_list.remove(client_sock)
                names_dict[msg['user']].close()
                del names_dict[msg['user']]
                print(clients_list)
                print(names_dict)
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


@deco_log
def message_to_client(cur_msg, names, send_msg_list):
    print(cur_msg, names, send_msg_list, sep='\n')
    if cur_msg['destination'] in names and names[cur_msg['destination']] in send_msg_list:
        send_message(names[cur_msg['destination']], cur_msg)
    elif cur_msg['destination'] in names and names[cur_msg['destination']] not in send_msg_list:
        raise ConnectionError
    else:
        log.error(f'user {cur_msg["destination"]} not on server,'
                  f'can\'t send message.')


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
    names_dict = {}
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
                        action_from_client(msg_from_client, messages_list, client, clients_list, names_dict)
                    except Exception:
                        log.info(f'Client {client.getpeername()} logged off')
                        clients_list.remove(client)

            for message in messages_list:
                try:
                    message_to_client(message, names_dict, snd_msg_list)
                except Exception as e:
                    log.info(f'Client {message["destination"].getpeername()} logged off')
                    clients_list.remove(names_dict[message['destination']])
                    del names_dict[message['destination']]
            messages_list.clear()
            # print(names_dict)
    finally:
        SERVER_SOCKET.close()
        log.info(f'stopped msg server at: {server_address} on: {server_port}')
