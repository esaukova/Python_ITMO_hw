import math

def yards_to_feet(yards):
    return yards * 3

def mile_per_hour_to_feet_per_second(mph):
    return mph * 5280 / 3600

def degree_to_radians(degrees):
    return math.radians(degrees)

def calc_time(d1_yards, d2_feet, h_yards, v_sand_mph, n, theta1_deg):
    d1_feet = yards_to_feet(d1_yards)
    h_feet = yards_to_feet(h_yards)
    v_sand_mph = mile_per_hour_to_feet_per_second(v_sand_mph)
    theta1_rad = degree_to_radians(theta1_deg)

    x = d1_feet * math.tan(theta1_rad)
    l1 = math.sqrt(math.pow(x, 2) + math.pow(d1_feet, 2))
    l2 = math.sqrt(math.pow((h_feet - x), 2) + math.pow(d2_feet, 2))

    return (l1 + n * l2) / v_sand_mph

def main():
    d1 = float(input("Введите кратчайшее расстояние от спасателя до кромки воды, в ярдах: "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, в футах: "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, в ярдах: "))
    v_sand = float(input("Введите скорость движения спасателя по песку, в милях в час: "))
    n = float(input("Введите коэффициент замедления спасателя при движении по воде: "))
    theta = float(input("Введите направление движения спасителя по песку, в градусах: "))

    t = calc_time(d1, d2, h, v_sand, n, theta)
    print(f"Если спасатель начнёт движение под углом, равным {int(theta)} градусам, он достигнет утопающего через {t:.1f} секунды")

main()

