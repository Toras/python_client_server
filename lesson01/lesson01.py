import os
import subprocess
import chardet


# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
# и проверить тип и содержание соответствующих переменных. Затем без помощи онлайн-конвертера
# преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.

word_list = ['разработка', 'сокет', 'декоратор']
word_list_utf_8 = list(map(lambda word: word.encode(encoding='utf-8'), word_list))
for i in range(len(word_list)):
    print(f'{type(word_list[i])} - {word_list[i]}')
    # new_word = word.encode(encoding='utf-8')
    print(f'{type(word_list_utf_8[i])} - {word_list_utf_8[i]}')

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

word_list = [b'class', b'function', b'method']
for word in word_list:
    print(f'{type(word)} - {word} - {len(word)}')

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

word_list = ['attribute', 'класс', 'функция', 'type']

for word in word_list:
    try:
        print(bytes(word, encoding='ascii'))
    except UnicodeEncodeError:
        print(f'нельзя преобразовать {word} в bytes ascii')

# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

word_list = ['разработка', 'администрирование', 'protocol', 'standard']
word_list_encode = list(map(lambda word: word.encode('utf-8'), word_list))
word_list_decode = list(map(lambda word: word.decode('utf-8'), word_list_encode))
print(word_list)
print(word_list_encode)
print(word_list_decode)

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
# в строковый тип на кириллице.


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

# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
# Unicode и вывести его содержимое.


detector = chardet.UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for line in file:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(f'кодировка файла по-умолчанию: {detector.result["encoding"]}')

if detector.result['encoding'] != 'utf-8':
    with open('test_file.txt', 'r', encoding=detector.result['encoding']) as file:
        result = file.read()
    with open('test_file_2.txt', 'w', encoding='utf-8') as file:
        file.write(result)

print('Файл переведенный в utf-8:')
with open('test_file_2.txt', 'r', encoding='utf-8') as file:
    print(file.read())
