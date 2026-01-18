import math
from utils.float_input_checker import float_data_reader


def yards_to_feet(yards):
    """
    Перевод расстояния из ярдов в футы.
    :param yards: float, расстояние в ярдах
    :return: расстояние в футах
    """
    return yards * 3


def mile_per_hour_to_feet_per_second(mph):
    """
    Перевод скорости из миль в час в футы в секунду.
    :param mph: float, скорость в милях в час
    :return: скорость в футах в секунду
    """
    return mph * 5280 / 3600


def degree_to_radians(degrees):
    """
    Перевод угла из градусов в радианы.
    :param degrees: float, угол в градусах
    :return: значение угла в радианах
    """
    return math.radians(degrees)


def calc_time(d1_yards, d2_feet, h_yards, v_sand_mph, n, theta1_deg):
    """
    Вычисляет время спасения при заданном угле движения.
    :param d1_yards: float, расстояние от спасателя до воды (ярды)
    :param d2_feet: float, расстояние от утопающего до берега (футы)
    :param h_yards: float, боковое смещение между спасателем и утопающим (ярды)
    :param v_sand_mph: float, скорость движения по песку (миль/ч)
    :param n: коэффициент замедления движения в воде
    :param theta1_deg: float, угол движения по песку (градусы)
    :return: float, время спасения в секундах (секунды)
    """
    d1_feet = yards_to_feet(d1_yards)
    h_feet = yards_to_feet(h_yards)
    v_mph = mile_per_hour_to_feet_per_second(v_sand_mph)
    theta1_rad = degree_to_radians(theta1_deg)

    x = d1_feet * math.tan(theta1_rad)
    l1 = math.sqrt(math.pow(x, 2) + math.pow(d1_feet, 2))
    l2 = math.sqrt(math.pow((h_feet - x), 2) + math.pow(d2_feet, 2))

    return (l1 + n * l2) / v_mph


def find_optimal_angle(d1, d2, h, v_sand, n):
    """
    Подбирает оптимальный угол движения спасателя.
    :param d1: float, расстояние от спасателя до воды (ярды)
    :param d2: float, расстояние от утопающего до берега (футы)
    :param h: float, боковое смещение (ярды)
    :param v_sand: float, скорость по песку (миль/ч)
    :param n: float, коэффициент замедления в воде
    :return: оптимальный угол (градусы) и минимальное время (секунды)
    """
    best_time = None
    best_angle = 0

    for angle in range(0, 90):
        t = calc_time(d1, d2, h, v_sand, n, angle)
        if best_time is None or t < best_time:
            best_time = t
            best_angle = angle

    return best_angle


def main():
    """
    Запрашивает данные у пользователя и выводит результат расчёта.
    """
    d1 = float_data_reader("Расстояние до воды (ярды): ")
    d2 = float_data_reader("Расстояние утопающего до берега (футы): ")
    h = float_data_reader("Боковое смещение (ярды): ")
    v_sand = float_data_reader("Скорость по песку (миль/ч): ")
    n = float_data_reader("Коэффициент замедления в воде (>1): ", min_value=1)

    angle, time = find_optimal_angle(d1, d2, h, v_sand, n)

    print(f"Оптимальный угол: {angle} градусов")


if __name__ == "__main__":
    main()
