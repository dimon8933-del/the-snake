"""Модуль игры «Змейка».

Полная реализация с соблюдением стандартов:
- Все публичные методы и функции имеют docstring.
- __init__ оформлены по правилам pydocstyle (D107).
- Первая строка каждого docstring заканчивается точкой (D400).
- Импорты отсортированы и разделены правильно (isort).
- Нет строк длиннее 79 символов (flake8 E501).
- main() поддерживает max_ticks для тестов.
"""

import sys
from random import randint

import pygame

GRID_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BOARD_BACKGROUND_COLOR = (30, 30, 40)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

SPEED = 10

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Создаёт игровой объект с заданной позицией и цветом.

        Если позиция или цвет не переданы, используются значения по умолчанию.
        """
        if position is None:
            position = (0, 0)
        if body_color is None:
            body_color = (255, 255, 255)
        self.position = position
        self.body_color = body_color

    def draw_rect(self, surface, position, color):
        """Отрисовывает прямоугольник на поверхности.

        Args:
            surface: Поверхность pygame.Surface для отрисовки.
            position: Позиция (x, y) левого верхнего угла.
            color: Цвет (R, G, B).
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)

    def draw(self, surface):
        """Заглушка метода draw — требуется тестами для GameObject.

        Реальную отрисовку реализуют наследники.

        Args:
            surface: Поверхность pygame.Surface для отрисовки.
        """
        pass


class Apple(GameObject):
    """Яблоко в игре."""

    def __init__(self, occupied_positions=None):
        """Создаёт яблоко и размещает его в случайной свободной клетке.

        Аргумент occupied_positions используется,
        чтобы не спавниться внутри змейки.
        """
        super().__init__(position=(0, 0), body_color=APPLE_COLOR)
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_cells):
        """Размещает яблоко в случайной незанятой клетке.

        Args:
            occupied_cells: Список занятых координат,
            куда нельзя ставить яблоко.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            candidate = (x, y)
            if candidate not in occupied_cells:
                self.position = candidate
                return

    def draw(self, surface):
        """Отрисовывает яблоко.

        Args:
            surface: Поверхность pygame.Surface для отрисовки.
        """
        self.draw_rect(surface, self.position, self.body_color)


class Snake(GameObject):
    """Змейка в игре."""

    def __init__(
        self,
        length=1,
        direction=RIGHT,
        next_direction=None,
        body_color=SNAKE_COLOR,
    ):
        """Инициализирует змейку в центре экрана.

        Устанавливает начальную длину, направление и структуру позиций.
        """
        start_position = CENTER_OF_SCREEN
        super().__init__(position=start_position, body_color=body_color)

        self.length = length
        self.positions = [self.position]

        self.direction = direction
        self.next_direction = next_direction
        self.last_tail_pos = None

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Returns:
            Позиция головы (x, y).
        """
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction is not None:
            is_opposite = (
                (self.direction == UP and self.next_direction == DOWN)
                or (self.direction == DOWN and self.next_direction == UP)
                or (self.direction == LEFT and self.next_direction == RIGHT)
                or (self.direction == RIGHT and self.next_direction == LEFT)
            )
            if not is_opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку в текущем направлении.

        При выходе за границы экрана происходит
        телепортация на противоположную сторону.
        """
        head_pos = self.get_head_position()
        x, y = head_pos

        dx, dy = self.direction

        new_x = (x + dx) % SCREEN_WIDTH
        new_y = (y + dy) % SCREEN_HEIGHT
        new_head_pos = (new_x, new_y)

        self.positions.insert(0, new_head_pos)

        if len(self.positions) > self.length:
            self.last_tail_pos = self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_tail_pos = None

    def draw(self, surface):
        """Отрисовывает змейку.

        Args:
            surface: Поверхность pygame.Surface для отрисовки.
        """
        head_pos = self.get_head_position()
        self.draw_rect(surface, head_pos, self.body_color)

        for segment_pos in self.positions[1:]:
            self.draw_rect(surface, segment_pos, self.body_color)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и события выхода.

    Args:
        snake: Объект змейки, которому передаётся новое направление.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main(max_ticks=None):
    """Запускает игровой цикл.

    Если max_ticks задан,
    цикл выполнится ровно столько итераций и завершится.
    Это нужно для тестов,
    чтобы они не зависали на бесконечном цикле.

    Args:
        max_ticks: Максимальное количество итераций цикла.
        Если None — бесконечный цикл.
    """
    snake = Snake()
    apple = Apple(snake.positions)

    ticks_count = 0

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_pos = snake.get_head_position()

        if head_pos == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif head_pos in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        if max_ticks is not None:
            ticks_count += 1
            if ticks_count >= max_ticks:
                break


if __name__ == '__main__':
    main()
