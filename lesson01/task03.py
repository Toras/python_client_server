# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

word_list = ['attribute', 'класс', 'функция', 'type']

for word in word_list:
    try:
        print(bytes(word, encoding='ascii'))
    except UnicodeEncodeError:
        print(f'нельзя преобразовать {word} в bytes ascii')
