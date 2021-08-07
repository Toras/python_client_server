from subprocess import Popen, CREATE_NEW_CONSOLE


if __name__ == '__main__':
    processes = []
    while True:
        action = input('q - exit, s - start server and clients, x - close all: ')
        if action == 'q':
            break
        elif action == 's':
            processes.append(Popen('python server\\server.py', creationflags=CREATE_NEW_CONSOLE))
            for i in range(5):
                processes.append(Popen('python client\\client.py', creationflags=CREATE_NEW_CONSOLE))
        elif action == 'x':
            while processes:
                process = processes.pop()
                process.kill()
