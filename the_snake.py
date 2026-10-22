from random import randint
import pygame

# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует объект позицией и цветом."""
        if position is None:
            position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Базовый метод отрисовки (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создаёт яблоко и задаёт ему случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию для яблока внутри сетки."""
        x = randint(0, GRID_WIDTH - 1)
        y = randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """
        Инициализирует змейку в центре поля,
        задаёт начальное направление.
        """
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(position=start_pos, body_color=SNAKE_COLOR)
        self.positions = [start_pos]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет направление движения,
        запрещая разворот на 180 градусов.
        """
        if self.next_direction is not None:
            if (
                self.next_direction[0] + self.direction[0] != 0
                or self.next_direction[1] + self.direction[1] != 0
            ):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Вычисляет новую позицию головы, двигает змейку и удаляет хвост."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def check_self_collision(self):
        """Проверяет, не столкнулась ли голова змейки с её телом."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def reset(self):
        """Сбрасывает состояние змейки в начальное положение."""
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [start_pos]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает тело змейки на поверхности."""
        for x, y in self.positions:
            rect = pygame.Rect(
                x * GRID_SIZE, y * GRID_SIZE,
                GRID_SIZE, GRID_SIZE,
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last is not None:
            lx, ly = self.last
            last_rect = pygame.Rect(
                lx * GRID_SIZE, ly * GRID_SIZE,
                GRID_SIZE, GRID_SIZE,
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_events(snake):
    """Обрабатывает события PyGame: выход из игры и нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True


def update_game_state(snake, apple):
    """
    Обновляет логику игры: движение,
    поедание яблока, проверка столкновений.
    """
    snake.update_direction()
    snake.move()
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()
    if snake.check_self_collision():
        snake.reset()
        return False
    return True


def draw_game(screen, snake, apple):
    """Очищает экран и отрисовывает змейку и яблоко."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw(screen)
    apple.draw(screen)
    pygame.display.update()


def main():
    """Запускает игровой цикл, обрабатывает события и управляет отрисовкой."""
    pygame.init()
    screen = pygame.display.set_mode
    (
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        0,
        32,
    )
    pygame.display.set_caption('Змейка — Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_events(snake)
        if not running:
            break

        game_running = update_game_state(snake, apple)
        if not game_running:
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.update()
            continue

        draw_game(screen, snake, apple)
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
