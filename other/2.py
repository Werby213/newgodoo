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

# Переменные для управления камерой
camera_offset = [0, 0]
camera_dragging = False
camera_drag_start = (0, 0)

# Переменные для создания статических полей
static_field_start = None
static_field_end = None
creating_static_field = False
f1 = pygame.font.Font(None, 35)
f2 = pygame.font.Font(None, 25)
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
                #shape.elasticity = 0
                shape.friction = 0.7
                #shape.mass = 10
                space.add(body, shape)
                objects.append((body, shape))

            elif event.key == pygame.K_b:  # Клавиша B
                if creating_static_field:
                    # Создание статического поля между точками
                    static_field = pymunk.Segment(static_body, static_field_start, static_field_end, 10)
                    static_field.friction = 1.0
                    space.add(static_field)
                    creating_static_field = False
                else:
                    # Начало создания статического поля
                    static_field_start = pygame.mouse.get_pos()
                    creating_static_field = True

        # Обработка событий мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # Средняя кнопка мыши
                # Начало перемещения камеры
                camera_dragging = True
                camera_drag_start = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Средняя кнопка мыши
                # Завершение перемещения камеры
                camera_dragging = False

    # Обновление физического мира
    dt = 1.0 / 60.0
    space.step(dt)

    # Перемещение камеры
    if camera_dragging:
        # Вычисление вектора смещения камеры
        dx = camera_drag_start[0] - pygame.mouse.get_pos()[0]
        dy = camera_drag_start[1] - pygame.mouse.get_pos()[1]
        camera_drag_start = pygame.mouse.get_pos()

        # Обновление смещения камеры
        camera_offset[0] += dx
        camera_offset[1] += dy

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка статических полей
    for shape in space.shapes:
        if isinstance(shape, pymunk.Segment):
            start = shape.a + camera_offset
            end = shape.b + camera_offset
            pygame.draw.line(screen, (255, 255, 255), start, end)

    # Отрисовка динамических объектов
    for body, shape in objects:
        position = body.position + camera_offset
        pygame.draw.circle(screen, (255, 0, 0), position, int(shape.radius))

    # Создание статического поля при создании
    if creating_static_field:
        print("создается барьер")
        static_field_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), static_field_start, static_field_end)

    # Обновление экрана
    fps_debug = f2.render('FPS: ' + (str(round(clock.get_fps()))), True, (180, 0, 0))
    screen.blit(fps_debug, (10, 10))
    pygame.display.flip()
    clock.tick(60)

# Завершение Pygame
pygame.quit()
