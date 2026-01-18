def float_data_reader(message, min_value=None, max_value=None):
    """
    Функция, которая запрашивает данные у пользователя и проверяет, что они соответствуют типу float
    Можно так же задать определенный интервал по необходимости
    :param message: текст сообщения для ввода
    :param min_value: минимально допустимое значение (если задано)
    :param max_value: максимально допустимое значение (если задано)
    :return: число типа float
    """
    while True:
        try:
            value = float(input(message))
            if min_value is not None and value < min_value: # Проверка минимального значение
                print(f"Значение должно быть не меньше {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Значение должно быть не больше {max_value}") # Проверка максимального значения
                continue
            return value
        except ValueError:
            print("Ошибка! Введите число.")
