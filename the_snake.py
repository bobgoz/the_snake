from random import randint, choice
import time

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTRAL_POSITION = (
    GRID_WIDTH // 2 * GRID_SIZE,
    GRID_HEIGHT // 2 * GRID_SIZE)

RANDOM_POSITION = (
    randint(0, GRID_WIDTH - 1) * GRID_SIZE,
    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption("Змейка")
clock = pg.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                raise SystemExit
            elif event.key == pg.K_SPACE:
                time.sleep(5)


class GameObject:
    """Родительский класс объектов"""

    def __init__(self, body_color=APPLE_COLOR, position=CENTRAL_POSITION):
        """Инициализация атрибутов"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод отрисовки для производных классов.
        Необходимо переопределить.
        """
        raise NotImplementedError(
            'Необходимо переопределить метод'
            f'в классe {self.__class__.__name__}.'
        )

    def draw_cell(self, position, body_color):
        """Отрисовывает ячейки в произвольных классах"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        """Инициализация атрибутов"""
        super().__init__(body_color)

    def draw(self):
        """Метод отрисовки для яблока"""
        self.draw_cell(self.position, self.body_color)

    def randomize_position(self, positions=[]):
        """
        Меняет позицию яблока на рандомную,
        в аргументах указываются ссылки на
        позиции объектов, можно несколько.
        """
        # В цикле перебираются координаты, чтобы
        #  яблоко не появлялось внутри объектов.
        while True:
            random_position = (
                randint(0, GRID_WIDTH - 1) * (GRID_SIZE),
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if random_position not in positions:
                break
        self.position = random_position


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация атрибутов"""
        super().__init__(body_color)
        # Инициализирует атрибуты, которые
        #  имеют значение по умолчанию.
        self.reset(is_initial=False)

    def reset(self, is_initial=True):
        """Сбрасывает змейку."""
        if is_initial is False:
            self.direction = RIGHT
        else:
            self.direction = choice([UP, RIGHT, DOWN, LEFT])
        self.length = 1
        self.next_direction = None
        self.positions = [self.position]

    def draw(self):
        """Рисует змейку."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def delete_part(self):
        """Удаление лишних частей змейки."""
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Получение координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()

        # Получение новой позиции.
        new_pos = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)
        # Лишние части списка удаляются
        self.delete_part()

    def eat(self, apple):
        """Если змейка съела яблоко."""
        if self.get_head_position() == apple.position:
            self.length += 1
            return True

    def check_bite(self):
        """Если змейка кусает себя, игра начинается заново."""
        if self.get_head_position() in self.positions[4:]:
            # Игра дает передышку в секунду, перед новым началом.
            time.sleep(1)
            return True

    def update_direction(self):
        """Метод обновления направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():
    """Основной цикл игры."""
    pg.init()

    snake = Snake()
    apple = Apple()

    apple.randomize_position()

    # Основной цикл игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.eat(apple):
            apple.randomize_position(snake.position)
        if snake.check_bite():
            snake.reset()
            apple.randomize_position(snake.position)
        apple.draw()
        snake.draw()
        pg.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == "__main__":
    main()
