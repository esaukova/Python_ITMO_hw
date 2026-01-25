import math
import utils.zip_util

zip_data = utils.zip_util.read_zip_all()


def find_by_zip(zip_code):
    """
    Находит информацию о почтовом индексе в наборе данных.

    :param zip_code: str, почтовый индекс для поиска
    :return: если запись найдена, то
             [zip, latitude, longitude, city, state, county]
             или None, если индекс не найден
    """

    for code in zip_data:
        if code[0] == zip_code:
            return code
    return None


def find_by_city(city, state):
    """
    Находит все почтовые индексы для указанного города и штата.

    :param city: str, название города
    :param state: str, аббревиатура штата
    :return: list[str], список найденных почтовых индексов
    """

    result = []
    for data in zip_data:
        if data[3].lower() == city.lower() and data[4].lower() == state.lower():
            result.append(data[0])
    return result


def distance_haversine_formula(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние между двумя точками по формуле Хаверсина.

    :param lat1: float, широта первой точки в десятичных градусах
    :param lon1: float, долгота первой точки в десятичных градусах
    :param lat2: float, широта второй точки в десятичных градусах
    :param lon2: float, долгота второй точки в десятичных градусах
    :return: float, расстояние между точками в милях
    """
    EARTH_RADIUS = 3959  # константа, радиус Земли в милях

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    theta = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS * theta

def decimal_to_dms(value, is_lat=True):
    """
    Преобразует координату из десятичных градусов
    в формат градусы–минуты–секунды (DMS).

    :param value: float, значение координаты в десятичных градусах
    :param is_lat: bool, True — широта, False — долгота
    :return: str, координата в формате DMS с указанием направления
    """

    direction = ''
    if is_lat:
        direction = 'N' if value >= 0 else 'S'
    else:
        direction = 'E' if value >= 0 else 'W'

    value = abs(value)
    degrees = int(value)
    minutes_full = (value - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60

    return f'{degrees:03d}°{minutes:02d} {seconds:05.2f}"{direction}'

def print_coordinates(lat, lon):
    """
    Выводит географические координаты в формате
    градусы–минуты–секунды (DMS).

    :param lat: float, широта в десятичных градусах
    :param lon: float, долгота в десятичных градусах
    :return: None
    """

    print(
        f"coordinates: "
        f"({decimal_to_dms(lat, True)}, {decimal_to_dms(lon, False)})"
    )

def repl():
    """
    Поддерживаемые команды:
    - loc — поиск местоположения по почтовому индексу
    - zip — поиск почтовых индексов по городу и штату
    - dist — вычисление расстояния между двумя почтовыми индексами
    - end — завершение работы программы

    :return: None
    """

    print("Command ('loc', 'zip', 'dist', 'end') => ", end='')

    while True:
        cmd = input().strip().lower()

        if cmd == 'end':
            print('Done')
            break

        elif cmd == 'loc':
            zip_code = input('Enter a ZIP Code to lookup => ').strip()
            rec = find_by_zip(zip_code)
            if rec:
                print(f'ZIP Code {rec[0]} is in {rec[3]}, {rec[4]}, {rec[5]} county,')
                print_coordinates(rec[1], rec[2])
            else:
                print('Invalid ZIP code')

        elif cmd == 'zip':
            city = input('Enter a city name to lookup => ')
            state = input('Enter the state name to lookup => ')
            zips = find_by_city(city, state)
            if zips:
                print(f'The following ZIP Code(s) found for {city}, {state}: {", ".join(zips)}')
            else:
                print('No ZIP codes found')

        elif cmd == 'dist':
            z1 = input('Enter the first ZIP Code => ')
            z2 = input('Enter the second ZIP Code => ')
            r1 = find_by_zip(z1)
            r2 = find_by_zip(z2)
            if r1 and r2:
                d = distance_haversine_formula(r1[1], r1[2], r2[1], r2[2])
                print(f'The distance between {z1} and {z2} is {d:.2f} miles')
            else:
                print('Invalid ZIP code(s)')

        else:
            print('Invalid command, ignoring')

        print("\nCommand ('loc', 'zip', 'dist', 'end') => ", end='')


if __name__ == '__main__':
    repl()
