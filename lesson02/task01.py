# 1. Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
#     Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
#       их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью
#       регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС»,
#       «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
#       Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
#       В этой же функции создать главный список для хранения данных отчета — например, main_data — и
#       поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
#       «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и
#       поместить в файл main_data (также для каждого файла);
#     Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
#     получение данных через вызов функции get_data(), а также сохранение подготовленных данных в
#     соответствующий CSV-файл;
#     Проверить работу программы через вызов функции write_to_csv().

import chardet
import re
import csv


def file_encoding(f):
    with open(f, 'rb') as file:
        result = chardet.detect(file.read())['encoding']
    return result


def get_data(file_list: list):
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    control_dict = {
        'Изготовитель ОС': os_prod_list,
        'Название ОС': os_name_list,
        'Код продукта': os_code_list,
        'Тип системы': os_type_list
    }
    main_data = []
    for file_name in file_list:
        f_enc = file_encoding(file_name)
        with open(file_name, 'r', encoding=f_enc) as file:
            file_data = file.read()
        file_data_list = file_data.split('\n')
        temp_dict = {}
        for pattern in control_dict.keys():
            found_str = [line.split(':')[1].strip() for line in file_data_list if re.search(pattern, line)]
            control_dict[pattern].append(','.join(found_str))
            temp_dict[pattern] = ','.join(found_str)
        main_data.append(temp_dict)

    return main_data, control_dict.keys()


def write_to_csv(csv_file):
    found_data, field_names = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=',', fieldnames=field_names)
        writer.writeheader()
        for row in found_data:
            writer.writerow(row)


if __name__ == '__main__':
    csv_path = 'output.csv'
    write_to_csv(csv_path)
