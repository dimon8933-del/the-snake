import pygame

import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Глобальные переменные (изначально None) ---
screen = None
clock = None


class GameObject:
    """Базовый класс игрового объекта."""
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        if isinstance(surface, pygame.Surface):
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)


class Apple(GameObject):
    """Яблоко — еда для змейки."""
    def __init__(self):
        super().__init__(
            position=self.randomize_position(),
            body_color=(255, 0, 0)  # Красный
        )

    @staticmethod
    def randomize_position():
        return (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Змейка — управляемый объект."""
    def __init__(self):
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        self.positions = [(start_x // GRID_SIZE, start_y // GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)  # Зелёный

    @property
    def position(self):
        x, y = self.positions[0]
        return x * GRID_SIZE, y * GRID_SIZE

    def get_head_position(self):
        return self.position

    def update_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.next_direction = direction

    def move(self):
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def reset(self):
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        self.positions = [(start_x // GRID_SIZE, start_y // GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self, surface):
        for x, y in self.positions:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)
    return True


def main():
    global screen, clock

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка — Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_keys(snake)
        if not running:
            break

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.positions[-1])
            apple.position = apple.randomize_position()

            while apple.position in [
                (x * GRID_SIZE, y * GRID_SIZE) for x, y in snake.positions
            ]:
                apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
