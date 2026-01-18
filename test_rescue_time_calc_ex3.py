import unittest

from rescue_time_calc_ex3 import (
    calc_time,
    find_optimal_angle
)

class TestCalcTime(unittest.TestCase):

    def test_calc_time_with_known_results(self):
        expected_result = calc_time(8, 10, 50, 5, 2, 39.413)
        actual_result = 39.9
        self.assertEqual(round(expected_result, 1), actual_result)

    def test_calc_time_with_increasing_n(self):
        """
        Если коэффициент n увеличивается, то время спасения увеличивается
        :return:
        """
        base_result = calc_time(8, 10, 50, 5, 2, 39)
        higher_n_result = calc_time(8, 10, 50, 5, 4, 39)
        self.assertGreater(higher_n_result, base_result)

class TestFindOptimalAngle(unittest.TestCase):

    def test_find_optimal_angle(self):
        d1, d2, h, v_sand, n = 10, 10, 5, 6, 2

        optimal_angle = find_optimal_angle(d1, d2, h, v_sand, n)
        optimal_time = calc_time(d1, d2, h, v_sand, n, optimal_angle)

        for angle in range(0, 90):
            current_time = calc_time(d1, d2, h, v_sand, n, angle)
            self.assertGreaterEqual(current_time, optimal_time)




