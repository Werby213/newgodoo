import pygame
import pymunk
from random import *
import pygame_gui
import random
from pymunk import Vec2d
import math
import numpy as np
import pymunk.pygame_util
import pickle
import tkinter as tk
from tkinter import filedialog
from numba import jit

guide_text = (
    "L: show this guide"
    "\nF: Spawn object"
    "\nB: Make border"
    "\nN: Enable gravity field"
    "\nSPACE: Pause physic"
    "\nArrow keys: camera position"
    "\nA/Z: Camera zoom"
    "\nS/X: Camera roll"
    "\nP: Screenshot"
)

debug_info = "'FPS: ' + (str(round(clock.get_fps()))) +'\nEntities: ' + (str(len(space.bodies))) +'\nGravity: ' + (str(len(space.gravity))) +'\nThreads: ' + (str(round(space.threads)))"

show_guide = True
pygame.init()
pygame.display.set_caption("Newgodoo a0.1.2")
COLLTYPE_DEFAULT = 0
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

space = pymunk.Space(threaded=True)

space.threads = 2
space.iterations = 30
simulation_frequency = 60
static_body = space.static_body
floor = pymunk.Segment(
    static_body, (-10000, screen_height - 100), (10000, screen_height - 100), 100
)
floor.friction = 1.0
space.add(floor)

objects = []
static_lines = []
line_point1 = None
selected_shape = None
camera_offset = Vec2d(0, 0)

camera_dragging = False
camera_drag_start = (0, 0)

f1 = pygame.font.Font(None, 25)
f2 = pygame.font.Font(None, 25)

static_field_start = (0, 0)
static_field_end = (0, 0)
creating_static_field = False
creating_force_field = False
force_field_strength = 500  # Сила притяжения поля
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

X, Y = 0, 1

set_elasticity = 0
set_square_size = [30, 30]
set_circle_radius = 30
set_friction = 0.7

segment_length = 50
segment_thickness = 2
segment_color = pygame.Color("white")


running_physics = True

spawn_button_positions = [
    (button_x, button_y + (spawn_button_height + button_spacing) * i) for i in range(11)
]

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
    elif i == 7:
        button_text = "spawner"
    elif i == 8:
        button_text = "button"
    elif i == 9:
        button_text = "spawner"
    elif i == 10:
        button_text = "deleter"
    if selected_shape == button_text.lower():
        button_text += " (selected)"
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect, text=button_text, manager=gui_manager
    )
    spawn_buttons.append(button)
# FORCE_FIELD######################################################################################
strength_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(350, 10, 200, 20),
    start_value=force_field_strength,
    value_range=(0, 5000),
    manager=gui_manager,
)

text_label_strength = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(330, 10, 250, 50),
    text="force field strength: {}".format(force_field_strength),
    manager=gui_manager,
)

radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(350, 40, 200, 20),
    start_value=force_field_radius,
    value_range=(0, 1000),
    manager=gui_manager,
)

text_label_radius = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(350, 40, 200, 50),
    text="force field radius: {}".format(force_field_radius),
    manager=gui_manager,
)

# SQUARE######################################################################################
square_size_slider_x = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(150, 70, 200, 20),
    start_value=set_square_size[0],
    value_range=(1, 1000),
    manager=gui_manager,
)

text_square_size_x = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 55, 600, 50),
    text="square X        :{}".format(set_square_size[0]),
    manager=gui_manager,
)
square_size_slider_y = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(150, 100, 200, 20),
    start_value=set_square_size[1],
    value_range=(1, 1000),
    manager=gui_manager,
)

text_square_size_y = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 85, 600, 50),
    text="square Y        :{}".format(set_square_size[1]),
    manager=gui_manager,
)
# CIRCLE######################################################################################
circle_radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(150, 10, 200, 20),
    start_value=set_square_size[0],
    value_range=(1, 100),
    manager=gui_manager,
)
text_circle_radius = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(150, 10, 200, 50),
    text="Circle R: {}".format(set_circle_radius),
    manager=gui_manager,
)


# OTHER_GUI######################################################################################
text_guide_gui = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect(screen_width - 280, 150, 240, 300),
    html_text=guide_text,
    visible=show_guide,
    manager=gui_manager,
)
iterations_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(screen_width - 250, screen_height - 30, 200, 20),
    start_value=set_square_size[0],
    value_range=(1, 128),
    manager=gui_manager,
)
text_iterations = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(screen_width - 260, screen_height - 30, 300, 20),
    text="iterations        :{}".format(space.iterations),
    manager=gui_manager,
)
simulation_frequency_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(screen_width - 250, screen_height - 60, 200, 20),
    start_value=set_square_size[0],
    value_range=(1, 300),
    manager=gui_manager,
)
text_simulation_frequency = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(screen_width - 260, screen_height - 60, 300, 20),
    text="sim. frequency     :{}".format(simulation_frequency),
    manager=gui_manager,
)
# FRICTION######################################################################
friction_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(screen_width - 250, screen_height - 90, 200, 20),
    start_value=set_square_size[0],
    value_range=(0.01, 10),
    manager=gui_manager,
)
text_friction = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(screen_width - 260, screen_height - 90, 300, 20),
    text="friction     :{}".format(set_friction),
    manager=gui_manager,
)
# elasticity@#####################################################################
elasticity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(screen_width - 250, screen_height - 120, 200, 20),
    start_value=set_square_size[0],
    value_range=(0.01, 10),
    manager=gui_manager,
)
text_elasticity = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(screen_width - 260, screen_height - 120, 300, 20),
    text="elasticity     :{}".format(set_friction),
    manager=gui_manager,
)
#SAVE/LOAD BUTTONS#####################################################################
save_world_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(screen_width - 135, 10, 125, 40),
        text="Save World",
        manager=gui_manager
    )
load_world_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(screen_width - 135, 60, 125, 40),
        text="Load World",
        manager=gui_manager
    )
selected_button = None


def mouse_get_pos():
    mouse_pos = world_mouse_pos
    return mouse_pos


def toolset(position):
    shape_mapping = {
        "circle": spawn_circle,
        "square": spawn_square,
        "triangle": spawn_triangle,
        "random": spawn_random,
        "spam": random_spam,
    }

    spawn_func = shape_mapping.get(selected_shape)
    if spawn_func:
        spawn_func(position)


def random_spam(position):
    for i in range(100):
        if random.randrange(0, 15) == 1:
            spawn_circle(position)
        if random.randrange(0, 15) == 1:
            spawn_square(position)
        if random.randrange(0, 15) == 1:
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
    radius = set_circle_radius
    mass = set_circle_radius / 10
    moment = pymunk.moment_for_circle(
        mass, 0, radius
    )  # Calculate moment of inertia for a circle
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    add_body_shape(body, shape)


def spawn_square(position):
    size = set_square_size
    points = [
        (-size[0], -size[1]),
        (-size[0], size[1]),
        (size[0], size[1]),
        (size[0], -size[1]),
    ]
    mass = (set_square_size[0] * set_square_size[1]) / 200
    moment = pymunk.moment_for_box(
        mass, (2 * size[0], 2 * size[1])
    )  # Calculate moment of inertia for a square
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    shape.elasticity = set_elasticity
    add_body_shape(body, shape)


def spawn_triangle(position):
    size = random.randrange(10, 40)
    points = [(0, 0), (-size, -size), (size, -size)]
    mass = 1
    moment = pymunk.moment_for_poly(
        mass, points
    )  # Calculate moment of inertia for an isosceles triangle
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    add_body_shape(body, shape)


def add_body_shape(body, shape):
    space.add(body, shape)
    objects.append((body, shape))


def force_field_update():
    for body, shape in objects:
        # distance = world_mouse_pos.get_distance(body.position)
        # if distance <= force_field_radius:
        if creating_force_field and shape.point_query(world_mouse_pos):
            pygame.draw.circle(
                screen,
                (100, 0, 0),
                pygame.mouse.get_pos(),
                force_field_radius + (world_mouse_pos[0] + world_mouse_pos[1]),
                2,
            )
            force_vector = (
                (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                * force_field_strength
                * 30
            )
            body.apply_force_at_local_point(force_vector, (0, 0))
    # if world_mouse_pos[0] == body.position <= force_field_radius or world_mouse_pos[1] == body.position <= force_field_radius:

def object_drag():
    for body, shape in objects:
        if world_mouse_pos.get_distance(body.position) <= 10:
            if object_dragging and shape.point_query(world_mouse_pos):
                force_vector = (
                    (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                    * force_field_strength
                    * 30
                )
                body.apply_force_at_local_point(force_vector, (0, 0))

def save_data(data):
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно tkinter

    # Открыть диалоговое окно проводника для выбора пути сохранения и имени файла
    file_path = filedialog.asksaveasfilename(
        defaultextension=".grsv", filetypes=[("Newgodoo Save File", "*.grsv")]
    )

    # Если путь и имя файла выбраны
    if file_path:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
        print("Сохранение успешно.")
    else:
        print("Отменено сохранение.")


# Функция для загрузки данных
def load_data():
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно tkinter

    # Открыть диалоговое окно проводника для выбора файла
    file_path = filedialog.askopenfilename(
        filetypes=[("Newgodoo Save Files", "*.grsv")]
    )

    # Если файл выбран
    if file_path:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        print("Загрузка успешна.")
        return data
    else:
        print("Отменена загрузка.")
        return None

def update():
    if running_physics == True:
        space.step(dt)
        force_field_update()
        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 20, 2)


translate_speed = 10
zoom_speed = 0.02
rotation_speed = 0.01
scaling = 1
rotation = 0
draw_options = pymunk.pygame_util.DrawOptions(screen)
translation = pymunk.Transform()

dragging_body = None
mouse_joint = None
running = True
guide = f2.render(str(guide_text), True, (180, 180, 0))
space.sleep_time_threshold = 0.5


while running:
    time_delta = clock.tick(60)

    # Получить позицию курсора относительно окна игры
    mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)

    # Преобразовать координаты курсора в объект Vec2d
    cursor_pos = pymunk.Vec2d(mouse_pos[0], mouse_pos[1])

    # Выполнить обратные операции трансформации
    inverse_translation = pymunk.Transform.translation(-300, -300)
    inverse_rotation = pymunk.Transform.rotation(-rotation)
    inverse_scaling = pymunk.Transform.scaling(1 / scaling)

    # Объединить обратные операции в одну трансформацию
    inverse_transform = inverse_scaling @ inverse_rotation @ inverse_translation

    # Вычислить обратную трансформацию позиции камеры
    inverse_translation_cam = pymunk.Transform.translation(
        -translation.tx, -translation.ty
    )

    # Применить обратные трансформации к позиции курсора и позиции камеры
    world_cursor_pos = inverse_transform @ cursor_pos
    world_translation = inverse_translation_cam @ pymunk.Vec2d(0, 0)

    # Вычислить позицию курсора в мире игры с учетом позиции камеры
    world_mouse_pos = (
        world_cursor_pos.x + world_translation.x + 300,
        world_cursor_pos.y + world_translation.y + 300,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Обработка событий gui Manager
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == save_world_button:
                    save_data(space)
                if event.ui_element == load_world_button:
                    loaded_data = load_data()
                    if loaded_data:
                        space = loaded_data
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
                    toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == strength_slider:
                    force_field_strength = int(event.value)
                    text_label_strength.set_text(
                        "Force Field Strength: {}".format(force_field_strength)
                    )
                elif event.ui_element == radius_slider:
                    force_field_radius = int(event.value)
                    text_label_radius.set_text(
                        "Force Field Radius: {}".format(force_field_radius)
                    )

                elif event.ui_element == square_size_slider_x:
                    set_square_size[0] = int(event.value)
                    text_square_size_x.set_text(
                        "square X        :{}".format(set_square_size[0])
                    )
                elif event.ui_element == square_size_slider_y:
                    set_square_size[1] = int(event.value)
                    text_square_size_y.set_text(
                        "square Y        :{}".format(set_square_size[1])
                    )

                elif event.ui_element == circle_radius_slider:
                    set_circle_radius = int(event.value)
                    text_circle_radius.set_text(
                        "Circle R: {}".format(set_circle_radius)
                    )

                elif event.ui_element == iterations_slider:
                    space.iterations = int(event.value)
                    text_iterations.set_text(
                        "iterations        :{}".format(space.iterations)
                    )

                elif event.ui_element == simulation_frequency_slider:
                    simulation_frequency = int(event.value)
                    text_simulation_frequency.set_text(
                        "sim. frequency     :{}".format(simulation_frequency)
                    )

                elif event.ui_element == friction_slider:
                    set_friction = int(event.value)
                    text_friction.set_text("friction       :{}".format(set_friction))

                elif event.ui_element == elasticity_slider:
                    set_elasticity = int(event.value)
                    text_elasticity.set_text(
                        "elasticity       :{}".format(set_elasticity)
                    )
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            # Начало создания статического поля
            init_static_field_start = pygame.mouse.get_pos()
            static_field_start = world_mouse_pos
            creating_static_field = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_b:
            print("Создается барьер")
            # Создание статического поля между точками
            static_field_end = world_mouse_pos
            static_field = pymunk.Segment(
                static_body, static_field_start, static_field_end, 10
            )
            static_field.friction = set_friction
            space.add(static_field)
            creating_static_field = False

        # Обработка событий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running_physics = not running_physics
            elif event.key == pygame.K_f:
                toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))
            elif event.key == pygame.K_n:
                creating_force_field = not creating_force_field
            elif event.key == pygame.K_l:
                show_guide = not show_guide
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "../screenshot.png")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if line_point1 is None:
                    line_point1 = world_mouse_pos

        # Обработка событий мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                object_dragging = True
                # Другие обработчики событий мыш

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                object_dragging = False

    keys = pygame.key.get_pressed()
    left = int(keys[pygame.K_LEFT])
    up = int(keys[pygame.K_UP])
    down = int(keys[pygame.K_DOWN])
    right = int(keys[pygame.K_RIGHT])

    zoom_in = int(keys[pygame.K_a])
    zoom_out = int(keys[pygame.K_z])
    rotate_left = int(keys[pygame.K_s])
    rotate_right = int(keys[pygame.K_x])

    translation = translation.translated(
        translate_speed * left - translate_speed * right,
        translate_speed * up - translate_speed * down,
    )
    draw_options.transform = (
        pymunk.Transform.translation(300, 300)
        @ pymunk.Transform.scaling(scaling)
        @ translation
        @ pymunk.Transform.rotation(rotation)
        @ pymunk.Transform.translation(-300, -300)
    )

    scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

    rotation += rotation_speed * rotate_left - rotation_speed * rotate_right
    # Отрисовка
    screen.fill((0, 0, 0))

    fps_debug = f1.render(
        "FPS: "
        + (str(round(clock.get_fps())))
        + "\nEntities: "
        + (str(len(space.bodies)))
        + "\nGravity: "
        + (str(len(space.gravity)))
        + "\nThreads: "
        + (str(round(space.threads))),
        True,
        (180, 0, 0),
    )
    screen.blit(fps_debug, (screen_width - 300, 10))
    if show_guide == True:
        text_guide_gui.visible = True

    if creating_static_field:
        static_field_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (static_field_start[0] - world_translation[0], static_field_start[1] - world_translation[1]), static_field_end, 10)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
    space.gravity = rotation * 1000, 1000
    dt = 1.0 / simulation_frequency
    if running_physics == True:
        space.step(dt)
    # Обновление gui Manager
    gui_manager.process_events(event)
    gui_manager.update(time_delta)
    update()
    # Отрисовка gui Manager
    space.debug_draw(draw_options)
    gui_manager.draw_ui(screen)
    pygame.display.flip()
pygame.quit()


# elif event.type == pygame.MOUSEBUTTONDOWN:
#    if event.button == 1:
#        for body, shape in objects:
#            if shape.point_query(mouse_get_pos()):
#                selected_shape = shape
#                dragging_body = body
#                break
#    elif event.button == 2:
#        camera_dragging = True
#        camera_drag_start = Vec2d(event.pos[0], event.pos[1])
