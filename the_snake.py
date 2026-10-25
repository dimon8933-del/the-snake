import sys
import pygame
from random import randint

GRID_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BOARD_BACKGROUND_COLOR = (30, 30, 40)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

SPEED = 10

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)


class GameObject:
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw_rect(self, surface, position, color):
        """Универсальный метод отрисовки прямоугольника по позиции."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):
    def __init__(self, occupied_positions):
        super().__init__(position=(0, 0), body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_cells):
        while True:
            x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            candidate = (x, y)
            if candidate not in occupied_cells:
                self.position = candidate
                return

    def draw(self, surface):
        self.draw_rect(surface, self.position, self.body_color)


class Snake(GameObject):
    def __init__(
        self,
        length=1,
        direction=RIGHT,
        next_direction=None,
        body_color=SNAKE_COLOR
    ):
        start_position = CENTER_OF_SCREEN
        super().__init__(position=start_position, body_color=body_color)

        self.length = length
        self.positions = [self.position]

        self.direction = direction
        self.next_direction = next_direction
        self.last_tail_pos = None

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction is not None:
            if not (
                (self.direction == UP and self.next_direction == DOWN) or
                (self.direction == DOWN and self.next_direction == UP) or
                (self.direction == LEFT and self.next_direction == RIGHT) or
                (self.direction == RIGHT and self.next_direction == LEFT)
            ):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
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
        """Только сброс состояния объекта, без отрисовки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_tail_pos = None

    def draw(self, surface):
        head_pos = self.get_head_position()
        self.draw_rect(surface, head_pos, self.body_color)

        for segment_pos in self.positions[1:]:
            self.draw_rect(surface, segment_pos, self.body_color)


def handle_keys(snake):
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.positions)

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


if __name__ == "__main__":
    main()
