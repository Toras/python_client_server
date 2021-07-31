# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
# и проверить тип и содержание соответствующих переменных. Затем без помощи онлайн-конвертера
# преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.

word_list = ['разработка', 'сокет', 'декоратор']
word_list_utf_8 = list(map(lambda word: word.encode('unicode_escape').decode(), word_list))
for i in range(len(word_list)):
    print(f'{type(word_list[i])} - {word_list[i]}')
    # new_word = word.encode(encoding='utf-8')
    print(f'{type(word_list_utf_8[i])} - {word_list_utf_8[i]}')
