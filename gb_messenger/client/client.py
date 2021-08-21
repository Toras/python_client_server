import json
import logging
import sys
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv, exit
from utils import get_message, send_message, DecoLogCls
import gb_messenger_logs.configs.client_log_config


client_log = logging.getLogger('client')


@DecoLogCls()
def action_to_server(action, sock, user='guest'):
    result = {
        'action': action,
        'timestamp': int(time.time()),
        'user': user
    }
    if action == 0:
        return result
    elif action == 2:
        destination = input('Введите получателя: ')
        msg = input('Введите сообщение: ')

        result['message'] = msg
        result['destination'] = destination
        try:
            send_message(sock, result)
            client_log.info(f'message send to user {destination}')
            return
        except Exception as e:
            client_log.error(f'error {e} occurred during sending to {destination}')
            sys.exit(1)
    elif action == 5:
        return result
    return result


@DecoLogCls()
def action_from_server(server_sock, username):
    while True:
        try:
            msg = get_message(server_sock)
            if 'timestamp' in msg and 'response' in msg:
                client_log.info(f'{msg["response"]}')
                if msg["response"] == 400:
                    break
            elif 'action' in msg:
                if msg['action'] == 2 and 'user' in msg and 'destination' in msg \
                        and 'message' in msg and msg['destination'] == username:
                    print(f'\nMessage from user {msg["destination"]}:\n{msg["message"]}')
                    client_log.info(f'Message from user {msg["destination"]}:\n{msg["message"]}')
                else:
                    client_log.info(f'Wrong message from server: {msg}')
        except ValueError as e:
            client_log.error(f'value error {e}')
            break
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError) as e:
            client_log.error(f'error {e}')
            break
        except Exception as e:
            client_log.error(f'unknown error {e}')


@DecoLogCls()
def user_interactive(server_sock, username):
    user_help()
    while True:
        cmd = input('Введите команду: ')
        if cmd == 'message':
            action_to_server(2, server_sock, username)
        elif cmd == 'help':
            user_help()
        elif cmd == 'exit':
            send_message(server_sock, action_to_server(5, server_sock, username), 'utf-8')
            print('Завершение соединения')
            client_log.info('Finishing work on user demands')
            time.sleep(1)
            break
        else:
            print('Неизвестная команда. help - вывести справку.')


@DecoLogCls()
def process_server_answer(msg):
    if 'timestamp' in msg and 'response' in msg:
        client_log.info(f'{msg["response"]}')


def user_help():
    print('Комманды:')
    print('message - отправить сообщение')
    print('help - вывод справки')
    print('exit - выход из программы')


if __name__ == '__main__':
    server_address = '127.0.0.1'
    server_port = 9000
    client_name = False
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
    if argv.count('-n') != 0:
        client_name = argv[argv.index('-n') + 1]

    if not client_name:
        client_name = input('Enter user name: ')

    client_log.info(f'{client_name} connecting to server at: {server_address} on: {server_port}')
    print(f'{client_name} connecting to server at: {server_address} on: {server_port}')

    try:
        SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
        SERVER_SOCKET.connect((server_address, server_port))
        msg_to_server = action_to_server(0, SERVER_SOCKET, user=client_name)
        send_message(SERVER_SOCKET, msg_to_server, 'utf-8')
        msg_from_server = get_message(SERVER_SOCKET, 1024, 'utf-8')
        process_server_answer(msg_from_server)
    except ConnectionRefusedError:
        client_log.error('Connection refused!')
    else:
        receiver = threading.Thread(target=action_from_server, args=(SERVER_SOCKET, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(SERVER_SOCKET, client_name))
        user_interface.daemon = True
        user_interface.start()

        client_log.debug('threads started')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break
        # while True:
        #     if client_mode == 'send':
        #         try:
        #             msg_from_server = action_to_server(2, SERVER_SOCKET)
        #             send_message(SERVER_SOCKET, msg_from_server, 'utf-8')
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             client_log.error(f'Server {server_address}:{server_port} connection was lost!')
        #             sys.exit(1)
        #     elif client_mode == 'listen':
        #         try:
        #             msg_from_server = get_message(SERVER_SOCKET, 1024, 'utf-8')
        #             action_from_server(msg_from_server)
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             client_log.error(f'Server {server_address}:{server_port} connection was lost!')
        #             sys.exit(1)
        #         except Exception as e:
        #             client_log.error(f'Error {e}')
    finally:
        SERVER_SOCKET.close()
