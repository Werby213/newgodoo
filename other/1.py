import pygame
import pymunk
from random import *
# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Создание физического мира
space = pymunk.Space()
space.gravity = 0, 1000

# Создание статического пола
static_body = space.static_body
floor = pymunk.Segment(static_body, (0, 500), (800, 500), 0)
floor.friction = 1.0
space.add(floor)

# Список для хранения физических объектов
objects = []

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка событий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Клавиша F
                # Создание нового физического объекта
                body = pymunk.Body(1, 1)
                body.position = pygame.mouse.get_pos()
                shape = pymunk.Circle(body, randrange(5, 30))
                shape.friction = 0.7
                space.add(body, shape)
                objects.append((body, shape))

    # Обновление физического мира
    dt = 1.0 / 60.0
    space.step(dt)

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка статического пола
    pygame.draw.line(screen, (255, 255, 255), floor.a, floor.b)

    # Отрисовка динамических объектов
    for body, shape in objects:
        pygame.draw.circle(screen, (255, 0, 0), body.position, int(shape.radius))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение Pygame
pygame.quit()
