#1 Создайте ряд функций для проведения математических вычислений:

#Функция вычисления факториала числа:
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

#Поиск наибольшего числа из трёх:
def func_2_max_number(*args) -> int | float:
    max_ = 0
    for i in args:
        if i > max_:
            max_ = i
    return max_

#Расчёт площади прямоугольного треугольника:
def func_3_triangle_square(leg_1: int, leg_2: int) -> int | float:
    return (leg_1 * leg_2) / 2
def task_1():
    a, b, c = 15, randint(1, 99), randint(1, 99)
    print(f"Факториал числа a({a}) - {func_1_factorial(a)}")
    print(f"Из чисел a = {a}, b = {b}, c = {c} самое большое - {func_2_max_number(a, b, c)}")
    print(f"Из чисел a = {a}, b = {b}, c = {c} самое большое - {max((a, b, c))}")
    print(f"Катет a = {a} см, катет b = {b} см, площадь треугольника равна - {func_3_triangle_square(a, b)}")

#2 Создайте функцию для генерации текста с адресом суда.rts, respondents

def generate_header(data):
    # Получаем номер дела и адрес суда из данных
    case_number = data['case_number']
    court_name = data['court_name']

    # Выбираем суд на основании его названия
    courts = {
        '123': 'Московский арбитражный суд',
        '456': 'Санкт-Петербургский арбитражный суд',
        '789': 'Кемеровский арбитражный суд',
        '012': 'Ханты-Мансийский арбитражный суд',
        '345': 'Новосибирский арбитражный суд',
    }
def generate_header(data):
        # Получаем номер дела и адрес суда из данных
        case_number = data['case_number']
        court_name = courts[case_number[:3]]

        # Получаем данные о суде из файла
        import lesson_2_data
        court_data = next(filter(lambda x: x['name'] == court_name, lesson_2_data.courts))
        court_address = court_data['address']

        # Получаем данные об истце из данных
        plaintiff = data['plaintiff']

        # Получаем данные об ответчике из данных
        opponent_data = data['respondent']

        # Создаем f-string для форматирования шапки
        my_data = {
            'name': plaintiff['name'],
            'inn': plaintiff['inn'],
            'ogrnip': plaintiff['ogrnip'],
            'address': plaintiff['address'],
        }
        header = f'''
    В {court_name}
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

def task_2():
    plaintiff = {
        "name": "Бендера Сергей Николаевич",
        "inn": "1236182357",
        "ogrnip": "218431927812733",
        "address": "123534, г. Москва, Кремль, 1"
    }
    cleaned_respondents = [i for i in respondents if i.get("case_number")]
    for respondent in cleaned_respondents:
        court_code = respondent["case_number"].split("-")[0]
        court = courts[court_code]
        result = make_a_header(court, plaintiff, respondent)
        print(result)
