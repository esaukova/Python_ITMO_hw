import os
import argparse


from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    input_file: str = 'life_input.txt'     # дефолтное имя файла ввода, если не указываем при запуске
    output_file: str = 'output.txt'        # дефолтное имя файла вывода, если не указываем при запуске
    generations: int = 10                 # дефолтное количество шагов, если не указываем при запуске

    cell_size: int = 20
    border_color: tuple = (0, 0, 0)
    background_color: tuple = (255, 255, 255)
    base_color: tuple = (0, 140, 0)

    gen_images_dir: str = 'gen_images'
    gif_name: str = 'life.gif'
    gif_duration: int = 300  # мс между кадрами


Grid = List[List[int]]


def read_input(filename: str) -> Grid:
    grid: Grid = []
    expected_width = None
    expected_height = None

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.rstrip('\n')

                if not line.strip() or line.lstrip().startswith('#'):
                    continue

                tokens = line.split()
                if expected_width is None and len(tokens) == 2 and all(t.isdigit() for t in tokens):
                    expected_width, expected_height = map(int, tokens)
                    continue

                # Преобразуем строку поля в список клеток
                row = []
                for ch in line:
                    if ch in ('X', '1'):
                        row.append(1)
                    elif ch in ('.', '0', ' '):
                        row.append(0)
                    else:
                        raise ValueError(
                            f'Недопустимый символ "{ch}" в строке {line_num}'
                        )

                # Проверяем ширину строки
                if expected_width is not None and len(row) != expected_width:
                    raise ValueError(
                        f'Неверная длина строки {line_num}: '
                        f'ожидалось {expected_width}, получено {len(row)}'
                    )

                grid.append(row)

        if not grid:
            raise ValueError('Входной файл не содержит данных игрового поля')

        # Проверяем высоту поля
        if expected_height is not None and len(grid) != expected_height:
            raise ValueError(
                f'Неверное количество строк поля: '
                f'ожидалось {expected_height}, получено {len(grid)}'
            )

        return grid

    except FileNotFoundError:
        raise FileNotFoundError(f'Файл "{filename}" не найден')



def write_output(grid: Grid, filename: str, step: int) -> None:
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'--- Step {step} ---\n')
            for row in grid:
                f.write(';'.join(map(str, row)) + '\n')
    except OSError as e:
        raise OSError(f'Ошибка записи в файл "{filename}": {e}')


def live_neighbors(grid: Grid, row: int, col: int) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue

            ny, nx = row + dy, col + dx
            if 0 <= ny < rows and 0 <= nx < cols:
                if grid[ny][nx] > 0:
                    count += 1
    return count


def next_generation(grid: Grid) -> Grid:
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            neighbors = live_neighbors(grid, r, c)
            age = grid[r][c]

            if age > 0:
                new_grid[r][c] = age + 1 if neighbors in (2, 3) else 0
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1

    return new_grid


def age_color(age: int, base_color: tuple) -> tuple:
    factor = min(age * 20, 255)
    return tuple(min(c + factor, 255) for c in base_color)


def write_png(grid: Grid, step: int, config: Config) -> None:
    os.makedirs(config.gen_images_dir, exist_ok=True)

    rows, cols = len(grid), len(grid[0])
    width = cols * config.cell_size
    height = rows * config.cell_size

    img = Image.new('RGB', (width, height), config.background_color)
    draw = ImageDraw.Draw(img)

    for r in range(rows):
        for c in range(cols):
            x1 = c * config.cell_size
            y1 = r * config.cell_size
            x2 = x1 + config.cell_size
            y2 = y1 + config.cell_size

            if grid[r][c] > 0:
                draw.rectangle(
                    [x1, y1, x2, y2],
                    fill=age_color(grid[r][c], config.base_color)
                )

            draw.rectangle(
                [x1, y1, x2, y2],
                outline=config.border_color
            )

    filename = os.path.join(
        config.gen_images_dir,
        f'generation_{step:03}.png'
    )
    img.save(filename)


def make_gif(config: Config) -> None:
    try:
        gen_image = sorted(
            os.path.join(config.gen_images_dir, f)
            for f in os.listdir(config.gen_images_dir)
            if f.endswith('.png')
        )

        if not gen_image:
            raise ValueError('Нет PNG файлов для создания GIF')

        images = [Image.open(frame) for frame in gen_image]

        images[0].save(
            config.gif_name,
            save_all=True,
            append_images=images[1:],
            duration=config.gif_duration,
            loop=0
        )

    except Exception as e:
        raise RuntimeError(f'Ошибка создания GIF: {e}')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Игра Жизнь: генерация PNG и GIF'
    )

    parser.add_argument(
        'input_file',
        help='Файл с начальным состоянием поля'
    )

    parser.add_argument(
        'output_file',
        help='CSV файл для записи поколений'
    )

    parser.add_argument(
        'steps',
        type=int,
        help='Количество поколений'
    )

    return parser.parse_args()


def main():
    try:
        args = parse_args()

        config = Config(
            input_file=args.input_file,
            output_file=args.output_file,
            generations=args.steps
        )

        grid = read_input(config.input_file)
        open(config.output_file, 'w').close()

        for step in range(config.generations + 1):
            write_output(grid, config.output_file, step)
            write_png(grid, step, config)
            grid = next_generation(grid)

        make_gif(config)
        print('GIF успешно создан')

    except Exception as e:
        print(f'Ошибка выполнения программы: {e}')


if __name__ == '__main__':
    main()
