# Создание переменных
a = 10
b = 20
c = "Hello, World!"

# Вывод на экран
print("a =", a)
print("b =", b)
print("c =", c)

# Запрос у пользователя некоторых чисел и строк
num1 = input("Введите число: ")
num2 = input("Введите еще одно число: ")
str1 = input("Введите строку: ")

# Сохранение в переменные
a = int(num1)
b = int(num2)
c = str1

# Вывод на экран
print("a =", a)
print("b =", b)
print("c =", c)

# Использование функции id()
print("id(a) =", id(a))
print("id(b) =", id(b))
print("id(c) =", id(c))

# Запрос у пользователя времени в секундах
time_str = input("Введите время в секундах: ")

# Проверка наличия только числовых данных
if time_str.isdigit():
    # Преобразование строки в число
    time_sec = int(time_str)

    # Рассчет количества часов, минут и секунд
    hours = time_sec // 3600
    minutes = (time_sec % 3600) // 60
    seconds = time_sec % 60

    # Сохранение времени в отдельных переменных
    time_hours = hours
    time_minutes = minutes
    time_seconds = seconds

    # Вывод рассчитанных часов, минут и секунд по отдельности в консоль
    print("Часы: ", time_hours)
    print("Минуты: ", time_minutes)
    print("Секунды: ", time_seconds)
else:
    print("Введено некорректное значение. Пожалуйста, введите только числовые данные.")

    # Запрос у пользователя числа n
    n_str = input("Введите число n (от 1 до 9): ")

    # Проверка введеного числа на корректность
    while not n_str.isdigit() or int(n_str) < 1 or int(n_str) > 9:
        print("Введено некорректное значение. Пожалуйста, введите число от 1 до 9.")
        n_str = input("Введите число n (от 1 до 9): ")

    # Преобразование строки в число
    n = int(n_str)

    # Расчет суммы чисел n + nn + nnn
    sum_nnn = n + int(str(n) + str(n) + str(n)) + int(str(n) + str(n) + str(n))

    # Вывод суммы в консоль
    print("Сумма чисел n + nn + nnn =", sum_nnn)