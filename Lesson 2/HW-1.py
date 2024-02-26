#1 Создайте ряд функций для проведения математических вычислений:

#Функция вычисления факториала числа:
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

#Поиск наибольшего числа из трёх:
def max_of_three(a, b, c):
    return max(a, b, c)
#Расчёт площади прямоугольного треугольника:
def area_of_right_triangle(a, b):
    return 0.5 * a * b

#2 Создайте функцию для генерации текста с адресом суда.rts, respondents
get_ipython().system('pip install requests')
import requests, time
def save_www_file(link):
    filename = link.split('/')[-1]
    req = requests.get(link, allow_redirects = True)
    open(filename, "wb").write(req.content)
    return
link = 'https://raw.githubusercontent.com/sirotinsky/HSE_LegalPy/main/homeworks/lesson2/lesson_2_data.py'
save_www_file(link)
from lesson_2_data import courts, respondents
def generate_header(data):
    # Получаем номер дела и адрес суда из данных
    case_number = data['case_number']
    court_code = case_number[:3]

    # Выбираем суд на основании его кода
    courts = {
        'MO': 'Московский арбитражный суд',
        'SP': 'Санкт-Петербургский арбитражный суд',
        'KE': 'Кемеровский арбитражный суд',
        'KH': 'Ханты-Мансийский арбитражный суд',
        'NO': 'Новосибирский арбитражный суд',
    }
    court = courts[court_code]

    # Получаем данные о суде из файла
    import lesson_2_data
    court_data = next(filter(lambda x: x['code'] == court_code, lesson_2_data.courts))
    court_address = court_data['address']

    # Создаем f-string для форматирования шапки
    my_data = {
        'name': 'Иванов Иван Иванович',
        'inn': '1234567890',
        'ogrnip': '123456789012345',
        'address': '123456, г. Москва, ул. Лесная, 7',
    }
    opponent_data = data['opponent']
    header = f'''
В {court}
Адрес: {court_address}
Истец: {my_data['name']}
ИНН {my_data['inn']} ОГРНИП {my_data['ogrnip']}
Адрес: {my_data['address']}
Ответчик: {opponent_data['name']}
ИНН {opponent_data['inn']} ОГРН {opponent_data['ogrn']}
Адрес: {opponent_data['address']}
Номер дела {case_number}
'''

    return header
def generate_headers(data_list):
    for data in data_list:
        header = generate_header(data)
        print(header)

