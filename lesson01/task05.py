# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
# в строковый тип на кириллице.

import os
import subprocess
import chardet


def run_command(command):
    ping = subprocess.Popen(command, stdout=subprocess.PIPE)
    for pong in ping.stdout:
        pong_detect = chardet.detect(pong)
        pong_result = pong.decode(encoding=pong_detect['encoding'])
        print(f'{type(pong_result)} - {pong_result}', end='')


ping_keys = {
    'posix': '-c',
    'nt': '-n',
}
run_command(['ping', ping_keys.get(os.name), '3', 'yandex.ru'])
run_command(['ping', ping_keys.get(os.name), '3', 'youtube.com'])
print()
