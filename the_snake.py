from random import randint

import time

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                raise SystemExit


class GameObject:
    """Родительский класс объектов"""

    def __init__(self):
        """Инициализация атрибутов"""
        self.position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE)

        self.body_color = None

    def draw(self):
        """Метод-заглушка"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        """Инициализация атрибутов"""
        super().__init__()

        self.body_color = APPLE_COLOR
        self.position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE)

    def randomize_position(self, game_object):
        """Меняет позицию яблока на рандомную."""
        # В цикле перебираются координаты, чтобы
        #  яблоко не появлялось внутри змейки.
        while True:
            RANDOM_POSITION = (
                randint(0, GRID_WIDTH - 1) * (GRID_SIZE),
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if RANDOM_POSITION not in game_object.positions:
                break
        self.position = RANDOM_POSITION

        return True

    def get_apple_position(self):
        """Получение позиции головы змейки."""
        return self.position

    def draw(self):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        """Инициализация атрибутов"""
        super().__init__()

        # Длина змейки
        self.length = 1

        # Хранение позиций элементов змейки
        self.positions = [(
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE)]

        # Направление змейки по умолчанию
        self.direction = RIGHT

        # Изменение направления змейки
        self.next_direction = None

        # Цвет змейки
        self.body_color = SNAKE_COLOR

        # Хранение последней позиции
        self.last = None

    def draw(self):
        """Рисует змейку."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            self.delete_part()

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def delete_part(self):
        """Удаление лишних частей змейки."""
        if len(self.positions) > self.length:
            self.positions.pop()

        # Затирание последнего сегмента
        if self.last:

            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Получение координаты головы змейки."""
        return self.positions[0]

    def reset(self, apple):
        """Сбрасывает змейку."""
        self.positions = [(
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE)]
        self.length = 1
        apple.position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE)
        del self.positions[1:]

    def move(self):
        """Движение змейки."""
        head_x, head_y = self.get_head_position()

        # Получение новой позиции.
        new_pos = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE,
        )

        self.positions.insert(0, new_pos)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))

        # Получение прямоугольника экрана.
        screen_rect = screen.get_rect()

        # Проверка выхода змейки за правую часть экрана.
        if head_rect.right > screen_rect.right:

            self.positions.insert(0, (0, head_y))
            self.delete_part()

        # Проверка выхода змейки за левую часть экрана.
        if head_rect.left < screen_rect.left:

            self.positions.insert(0, (screen_rect.right, head_y))
            self.delete_part()

        # Проверка выхода змейки за нижнюю часть экрана.
        if head_rect.bottom > screen_rect.bottom:

            self.positions.insert(0, (head_x, screen_rect.top))
            self.delete_part()

        # Проверка выхода змейки за верхнюю границу экрана.
        if head_rect.top < screen_rect.top:

            self.positions.insert(0, (head_x, screen_rect.bottom))
            self.delete_part()

    def eat(self, apple):
        """Если змейка съела яблоко."""
        if self.get_head_position() == apple.get_apple_position():
            self.length += 1
            return True

    def self_eat(self):
        """Если змейка кусает себя, игра начинается заново."""
        for position in self.positions[1:]:
            if position == self.get_head_position():
                time.sleep(1)
                return True


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    # Основной цикл игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        snake.move()
        if snake.eat(apple):
            apple.randomize_position(snake)
        if snake.self_eat():
            snake.reset(apple)
        pygame.display.update()
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == "__main__":
    main()
