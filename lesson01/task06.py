# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
# Unicode и вывести его содержимое.

import chardet


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
