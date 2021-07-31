# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о
# заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров —
# товар (item),
# количество (quantity),
# цена (price),
# покупатель (buyer),
# дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
# каждого параметра.

import json


def write_order_to_json(item, quantity, price, buyer, date):
    data = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('orders.json', 'r', encoding='utf-8') as json_file:
        orders = json.load(json_file)
    with open('orders.json', 'w+', encoding='utf-8') as json_file:
        orders['orders'].append(data)
        json.dump(orders, json_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    with open('orders.json', 'w', encoding='utf-8') as file:
        json.dump({"orders": []}, file, indent=4)
    write_order_to_json('phone', '3', '4987.34', 'Jason', '2020-06-01')
    write_order_to_json('printer', '1', '14500', 'Олег', '2021-01-01')
    write_order_to_json('плакат', '1', '700', 'Владимир', '2020-11-08')
