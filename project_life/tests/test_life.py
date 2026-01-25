import unittest

from project_life.life_from_class import (
    read_input,
    age_color,
    Config,
)

class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = Config()

        self.assertEqual(config.generations, 10)
        self.assertEqual(config.cell_size, 20)
        self.assertEqual(config.gen_images_dir, 'gen_images')

class TestReadInput(unittest.TestCase):
    def test_read_valid_input(self):
        grid = read_input('data/test_life_input.txt')

        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0]
        ]

        self.assertEqual(grid, expected)

    def test_read_invalid_input(self):
        grid = read_input('data/test_life_input_invalid.txt')

        expected = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0]
        ]

        self.assertNotEqual(grid, expected)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_input('no_such_file.txt')

class TestAgeColor(unittest.TestCase):
    def test_color_increases_with_age(self): # становится светлее
        base = (0, 140, 0)

        young = age_color(1, base)
        old = age_color(5, base)

        self.assertTrue(old[0] >= young[0])
        self.assertTrue(old[1] >= young[1])
        self.assertTrue(old[2] >= young[2])
