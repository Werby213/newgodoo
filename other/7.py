import pygame
import pymunk
from random import *
import pygame_gui
import random
from pymunk import Vec2d
import math


guide_text = "L: show this guide" \
             "\nF: Spawn object" \
             "\nB: Make border" \
             "\nN: Enable gravity field" \
             "\n."
show_guide = True


pygame.init()
pygame.display.set_caption('PhysicsGame')
COLLTYPE_DEFAULT = 0
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, 1000
space.threads = 2
#space.iterations = 10
static_body = space.static_body
floor = pymunk.Segment(static_body, (0, screen_height - 100), (screen_width, screen_height - 100), 0)
floor.friction = 1.0
space.add(floor)

objects = []
selected_shape = None
camera_offset = Vec2d(0, 0)

camera_dragging = False
camera_drag_start = (0, 0)

f1 = pygame.font.Font(None, 35)
f2 = pygame.font.Font(None, 25)

static_field_start = (0, 0)
static_field_end = (0, 0)
creating_static_field = False
creating_force_field = False
force_field_strength = 5000  # Сила притяжения поля
force_field_radius = 500  # Радиус действия поля

# Инициализация gui Manager
gui_manager = pygame_gui.UIManager((screen_width, screen_height))
clock = pygame.time.Clock()

# Создание кнопок для спавна предметов
spawn_buttons = []
spawn_button_width = 120
spawn_button_height = 50
button_x = 10
button_y = 10
button_spacing = 10

set_elasticity = 0



running_physics = True

spawn_button_positions = [(button_x, button_y + (spawn_button_height + button_spacing) * i) for i in range(7)]

for i, pos in enumerate(spawn_button_positions):
    button_rect = pygame.Rect(pos, (spawn_button_width, spawn_button_height))
    button_text = ""
    if i == 0:
        button_text = "Circle"
    elif i == 1:
        button_text = "Square"
    elif i == 2:
        button_text = "Triangle"
    elif i == 3:
        button_text = "Random"
    elif i == 4:
        button_text = "Spam"
    elif i == 5:
        button_text = "delete all"
    elif i == 6:
        button_text = "force field"
    if selected_shape == button_text.lower():
        button_text += " (selected)"
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect,
        text=button_text,
        manager=gui_manager
    )
    spawn_buttons.append(button)
strength_slider_rect = pygame.Rect(150, 10, 200, 20)
strength_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=strength_slider_rect,
    start_value=force_field_strength,
    value_range=(0, 20000),
    manager=gui_manager
)

text_strength_slider_rect = pygame.Rect(130, 10, 250, 50)
text_label_strength = pygame_gui.elements.UILabel(
    relative_rect=text_strength_slider_rect,
    text="force field strength: {}".format(force_field_strength),
    manager=gui_manager
)

radius_slider_rect = pygame.Rect(150, 40, 200, 20)
radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=radius_slider_rect,
    start_value=force_field_radius,
    value_range=(0, 1000),
    manager=gui_manager
)

text_radius_slider_rect = pygame.Rect(150, 40, 200, 50)
text_label_radius = pygame_gui.elements.UILabel(
    relative_rect=text_radius_slider_rect,
    text="force field radius: {}".format(force_field_radius),
    manager=gui_manager
)

selected_button = None

def mouse_get_pos():
    return pygame.mouse.get_pos() - camera_offset

def toolset(position):
    shape_mapping = {
        "circle": spawn_circle,
        "square": spawn_square,
        "triangle": spawn_triangle,
        "random": spawn_random,
        "spam": random_spam,
        "delete all": delete_all,
    }

    spawn_func = shape_mapping.get(selected_shape)
    if spawn_func:
        spawn_func(position)

def random_spam(position):
    for i in range(100):
        if random.randrange(0,15) == 1:
            spawn_circle(position)
        if random.randrange(0,15) == 1:
            spawn_square(position)
        if random.randrange(0,15) == 1:
            spawn_triangle(position)

def spawn_random(position):
    shape_type = random.choice(["circle", "square", "triangle"])
    toolset(position, shape_type)

def delete_all(position):
    global objects
    for body, shape in objects:
        space.remove(body, shape)
    objects = []

def spawn_circle(position):
    radius = random.randrange(5, 30)
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, radius)  # Calculate moment of inertia for a circle
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = 0.7
    add_body_shape(body, shape)

def spawn_square(position):
    size = random.randrange(10, 40)
    points = [(-size, -size), (-size, size), (size, size), (size, -size)]
    mass = 1
    moment = pymunk.moment_for_box(mass, (2*size, 2*size))  # Calculate moment of inertia for a square
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = 0.7
    shape.elasticity = set_elasticity
    add_body_shape(body, shape)

def spawn_triangle(position):
    size = random.randrange(10, 40)
    points = [(0, 0), (-size, -size), (size, -size)]
    mass = 1
    moment = pymunk.moment_for_poly(mass, points)  # Calculate moment of inertia for an isosceles triangle
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = 0.7
    add_body_shape(body, shape)


def add_body_shape(body, shape):
    space.add(body, shape)
    objects.append((body, shape))


def update_rotation():
    global mouse_pos
    for body, shape in objects:
        if isinstance(shape, pymunk.Circle):
            position = body.position
            radius = shape.radius
            angle_degrees = math.degrees(body.angle)
            rotated_shape = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
            rotated_shape.fill((0, 0, 0, 0))
            pygame.draw.circle(rotated_shape, (255, 0, 0), (radius, radius), radius)
            rotated_shape = pygame.transform.rotate(rotated_shape, angle_degrees)
            position -= pymunk.Vec2d(rotated_shape.get_width() / 2, rotated_shape.get_height() / 2)
            screen.blit(rotated_shape, position)

        elif isinstance(shape, pymunk.Poly):
            position = body.position
            angle_degrees = -math.degrees(body.angle)
            vertices = shape.get_vertices()
            min_x = min(vertices, key=lambda v: v.x).x
            max_x = max(vertices, key=lambda v: v.x).x
            min_y = min(vertices, key=lambda v: v.y).y
            max_y = max(vertices, key=lambda v: v.y).y
            width = max_x - min_x
            height = max_y - min_y
            rotated_shape = pygame.Surface((width, height), pygame.SRCALPHA)
            rotated_shape.fill((0, 0, 0, 0))
            pygame.draw.polygon(rotated_shape, (255, 0, 0), [(v.x - min_x, v.y - min_y) for v in vertices])
            rotated_shape = pygame.transform.rotate(rotated_shape, angle_degrees)
            position -= pymunk.Vec2d(rotated_shape.get_width() / 2, rotated_shape.get_height() / 2)
            screen.blit(rotated_shape, position)

        mouse_pos = pygame.mouse.get_pos() - camera_offset
        distance = mouse_pos.get_distance(body.position)
        if distance <= force_field_radius:
            if creating_force_field and shape.point_query(mouse_get_pos()):
                force_vector = (mouse_get_pos() - body.position).rotated(-body.angle).normalized() * force_field_strength
                body.apply_force_at_local_point(force_vector, (0, 0))


# Перемещение камеры
def move_camera(dx, dy):
    camera_offset[0] += dx
    camera_offset[1] += dy

dragging_body = None
mouse_joint = None
running = True
guide = f2.render(str(guide_text), True, (180, 180, 0))
while running:
    time_delta = clock.tick(60) / 1000.0
    if dragging_body is not None:
        dragging_body.position = Vec2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - camera_offset

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Обработка событий gui Manager
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in spawn_buttons:
                    selected_button = event.ui_element
                    if selected_button == spawn_buttons[0]:
                        selected_shape = "circle"
                    elif selected_button == spawn_buttons[1]:
                        selected_shape = "square"
                    elif selected_button == spawn_buttons[2]:
                        selected_shape = "triangle"
                    elif selected_button == spawn_buttons[3]:
                        selected_shape = "random"
                    elif selected_button == spawn_buttons[4]:
                        selected_shape = "spam"
                    elif selected_button == spawn_buttons[5]:
                        selected_shape = "delete all"
                        delete_all(0)
                    elif selected_button == spawn_buttons[6]:
                        selected_shape = "force field"
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in spawn_buttons:
                    toolset(tuple(map(sum, zip(pygame.mouse.get_pos(), camera_offset))))
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == strength_slider:
                    force_field_strength = int(event.value)
                    text_label_strength.set_text("Force Field Strength: {}".format(force_field_strength))
                elif event.ui_element == radius_slider:
                    force_field_radius = int(event.value)
                    text_label_radius.set_text("Force Field Radius: {}".format(force_field_radius))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_body = None
            elif event.button == 2:
                camera_dragging = False


        # Обработка событий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                print("stopped")
                running_physics = not running_physics
            if event.key == pygame.K_f:
                toolset(tuple(map(sum, zip(pygame.mouse.get_pos(), camera_offset))))
            if event.key == pygame.K_n:
                creating_force_field = not creating_force_field
            if event.key == pygame.K_l:
                show_guide = True
            if event.type == pygame.K_b:  # Клавиша B
                print("создается барьер")
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
            if event.button == 2:
                camera_dragging = True
                camera_drag_start = event.pos
            elif event.button == 4:  # Колесо мыши вверх (приближение)
                space.gravity = 0, 1000 / 1.1
            elif event.button == 5:  # Колесо мыши вниз (отдаление)
                space.gravity = 0, 1000 * 1.1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                camera_dragging = False

    # Обновление gui Manager
    gui_manager.process_events(event)

    # Обновление состояния камеры
    if camera_dragging:
        dx = camera_drag_start[0] - event.pos[0]
        dy = camera_drag_start[1] - event.pos[1]
        camera_drag_start = Vec2d(event.pos[0], event.pos[1])
        move_camera(dx, dy)

    # Отрисовка
    screen.fill((0, 0, 0))

    fps_debug = f1.render('FPS: ' + (str(round(clock.get_fps()))) +
                          '\nEntities: ' + (str(len(space.bodies))) +
                          '\nGravity: ' + (str(len(space.gravity))) +
                          '\nThreads: ' + (str(round(space.threads))), True, (180, 0, 0))
    screen.blit(fps_debug, (screen_width - 300, 10))
    if show_guide == True:
        screen.blit(guide, (screen_width - 300, 200))
    for shape in space.shapes:
        if isinstance(shape, pymunk.Segment):
            start = shape.a + camera_offset
            end = shape.b + camera_offset
            pygame.draw.line(screen, (255, 255, 255), start, end, width=10)

    if creating_static_field:
        static_field_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), static_field_start, static_field_end)

    dt = 1.0 / 60.0
    if running_physics:
        space.step(dt)
        update_rotation()
    # Обновление gui Manager
    gui_manager.update(time_delta)

    # Отрисовка gui Manager
    gui_manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()



        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    if event.button == 1:
        #        for body, shape in objects:
        #            if shape.point_query(mouse_get_pos()):
        #                selected_shape = shape
        #                dragging_body = body
        #                break
        #    elif event.button == 2:
        #        camera_dragging = True
        #        camera_drag_start = Vec2d(event.pos[0], event.pos[1])