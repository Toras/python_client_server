# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

word_list = ['разработка', 'администрирование', 'protocol', 'standard']
word_list_encode = list(map(lambda word: word.encode('utf-8'), word_list))
word_list_decode = list(map(lambda word: word.decode('utf-8'), word_list_encode))
print(word_list)
print(word_list_encode)
print(word_list_decode)
