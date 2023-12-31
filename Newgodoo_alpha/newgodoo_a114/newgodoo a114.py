import pygame
import pymunk
from random import *
import pygame_gui
import random
from pymunk import Vec2d
import pymunk.pygame_util
import pickle
import tkinter as tk
from tkinter import filedialog
import ctypes
import math


#import numpy as np
#from numba import jit
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
    "\nShift: Move faster"
)

debug_info = "'FPS: ' + (str(round(clock.get_fps()))) +'\nEntities: ' + (str(len(space.bodies))) +'\nGravity: ' + " \
             "(str(len(space.gravity))) +'\nThreads: ' + (str(round(space.threads)))\nstatick_lines"

show_guide = True
fullscreen = False
screen_width, screen_height = 1920, 1080
shift_speed = 1
pygame.init()
pygame.display.set_icon(pygame.image.load("laydigital.png"))
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
pygame.display.set_caption("Newgodoo a0.1.3")
COLLTYPE_DEFAULT = 0

if fullscreen == True:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    screen_width = int(user32.GetSystemMetrics(0))
    screen_height = int(user32.GetSystemMetrics(1))
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
else:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)


clock = pygame.time.Clock()

space = pymunk.Space()

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
selected_force_field = None
camera_offset = Vec2d(0, 0)

camera_dragging = False
camera_drag_start = (0, 0)

f1 = pygame.font.Font(None, 25)
f2 = pygame.font.Font(None, 25)

static_field_start = (0, 0)
static_field_end = (0, 0)
creating_static_field = False
creating_spring = False
creating_attraction = False
creating_repulsion = False
creating_force_ring = False
creating_object_drag = False
force_field_strength = 500  # Сила притяжения поля
force_field_radius = 500  # Радиус действия поля

# Инициализация gui Manager
gui_manager = pygame_gui.UIManager((screen_width, screen_height))
clock = pygame.time.Clock()


KEY_HOLD_TIME = 1000  #в миллисекундах
key_f_pressed = False
key_f_hold_start_time = 0

# Создание кнопок для спавна предметов
spawn_buttons = []
force_field_buttons = []
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

set_number_faces = 5
gear_radius = 30
gear_thickness = 5

segment_length = 50
segment_thickness = 2
segment_color = pygame.Color("white")
options = pymunk.pygame_util.DrawOptions(screen)

running_physics = True

force_field_button_positions = [
    (screen_width-135, screen_height-300 + (50 + 1) * i) for i in range(3)
]

for i, pos in enumerate(force_field_button_positions):
    button_rect = pygame.Rect(pos, (120, 50))
    button_text = ""
    if i == 0:
        button_text = "attraction"
    elif i == 1:
        button_text = "repulsion"
    elif i == 2:
        button_text = "ring"
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect, text=button_text, manager=gui_manager
    )
    force_field_buttons.append(button)
selected_force_field_button = force_field_buttons[0]


spawn_button_positions = [
    (10, 10 + (50 + 1) * i) for i in range(19)
]
for i, pos in enumerate(spawn_button_positions):
    button_rect = pygame.Rect(pos, (120, 50))
    button_text = ""
    if i == 0:
        button_text = "Circle"
    elif i == 1:
        button_text = "Square"
    elif i == 2:
        button_text = "Triangle"
    elif i == 3:
        button_text = "Polyhedron"
    elif i == 4:
        button_text = "Spam"
    elif i == 5:
        button_text = "Gear"
    elif i == 6:
        button_text = "Static line"
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
selected_spawn_button = None

from GUI import *

debug_info_lines = debug_info.split('\n')
debug_info_labels = []
debug_y_pos = 10

for line in debug_info_lines:
    label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(screen_height+400, debug_y_pos, 300, 50),
        text=line,
        manager=gui_manager,
    )
    debug_info_labels.append(label)
    debug_y_pos += 20


def mouse_get_pos():
    mouse_pos = world_mouse_pos
    return mouse_pos


def toolset(position):
    shape_mapping = {
        "circle": spawn_circle,
        "square": spawn_square,
        "triangle": spawn_triangle,
        "polyhedron": spawn_polyhedron,
        "spam": random_spam,
    }

    spawn_func = shape_mapping.get(selected_shape)
    if spawn_func:
        spawn_func(position)

def toolset_force_field():
    type_mapping = {
        "attraction": attraction,
        "repulsion": repulsion,
        "ring": ring,
    }
    if selected_force_field_button is not None:
        force_field_function = type_mapping.get(button_text)
        if force_field_function is not None:
            force_field_function()
    return selected_force_field


def random_spam(position):
    for i in range(100):
        if random.randrange(0, 15) == 1:
            spawn_circle(position)
        if random.randrange(0, 15) == 1:
            spawn_square(position)
        if random.randrange(0, 15) == 1:
            spawn_triangle(position)
        if random.randrange(0, 15) == 1:
            spawn_polyhedron(position)


def spawn_random(position):
    shape_type = random.choice(["circle", "square", "triangle"])
    toolset(position, shape_type)


def delete_all():
    global objects, static_lines
    for body, shape in objects:
        space.remove(body, shape)
    objects = []

    for static_line in static_lines:
        space.remove(static_line)
    static_lines = []

def spawn_polyhedron(position):
    tooth_angle = 2 * math.pi / set_number_faces

    radius = set_circle_radius / 2

    tooth_radius = radius * 0.4

    points = []
    for i in range(set_number_faces * 2):
        angle = i * tooth_angle / 2
        if i % 2 == 0:
            points.append((radius * math.cos(angle), radius * math.sin(angle)))
        else:
            points.append((tooth_radius * math.cos(angle), tooth_radius * math.sin(angle)))

    mass = (set_circle_radius ** 2) / 200
    moment = pymunk.moment_for_poly(mass, points)

    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    shape.elasticity = set_elasticity
    shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)
    add_body_shape(body, shape)

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
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)


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
    shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)



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
    shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)


def add_body_shape(body, shape):
    space.add(body, shape)
    objects.append((body, shape))


def attraction():
    if creating_attraction:
        for body, shape in objects:
             if shape.point_query(world_mouse_pos):
                distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
    
                if distance <= force_field_radius:
    
                        force_vector = (
                            (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                            * force_field_strength
                            * 30
                        )
                        body.apply_force_at_local_point(force_vector, (0, 0))


def repulsion():
    if creating_repulsion:
        for body, shape in objects:
            if shape.point_query(world_mouse_pos):
                distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (
                            world_mouse_pos[1] - body.position.y) ** 2) ** 0.5

                if distance <= force_field_radius:
                    force_vector = (
                            (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                            * force_field_strength
                            * 30
                    )
                    body.apply_force_at_local_point(-force_vector, (0, 0))
def ring():
    if creating_force_ring:
        for body, shape in objects:
        # if distance <= force_field_radius:
            if shape.point_query(world_mouse_pos):
                distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (
                            world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
                force_vector = (
                    (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                    * force_field_strength
                    * 30
                )
                body.apply_force_at_local_point(force_vector, (0, 0))
    
                if distance <= force_field_radius-300:
                    if shape.point_query(world_mouse_pos):
                        force_vector_in = (
                                (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                                * force_field_strength
                                * 50
                        )
    
                        body.apply_force_at_local_point(-force_vector_in, (0, 0))

def object_drag():
    for body, shape in objects:
        distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (world_mouse_pos[1] - body.position.y) ** 2) ** 0.5

        if distance <= 50:
            if object_dragging and shape.point_query(world_mouse_pos):
                force_vector = (
                    (world_mouse_pos - body.position).rotated(-body.angle).normalized()
                    * 1000
                    * 30
                )
                body.apply_force_at_local_point(force_vector, (0, 0))

def save_data(data):
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно tkinter

    # Открыть диалоговое окно проводника для выбора пути сохранения и имени файла
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ngsv", filetypes=[("Newgodoo Save File", "*.grsv")]
    )

    # Если путь и имя файла выбраны

    if file_path:
        with open(file_path, "wb") as f:
            try:
                pickle.dump(data, f)
            except:
                print("Что-то пошло не так")
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
            try:
                delete_all(space)
                data = pickle.load(f)
            except:
                print("Что-то пошло не так")

        print("Загрузка успешна.")
        return data
    else:
        print("Отменена загрузка.")
        return None

def update():
    if running_physics == True:
        dt = 2.0 / simulation_frequency
        space.step(dt)
        space.gravity = rotation * 1000, 1000
        attraction()
        repulsion()
        ring()
        object_drag()
        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 20, 2)


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
def create_spring(body1, body2):
    global spring
    spring = pymunk.DampedSpring(body1, body2, (0, 0), (0, 0), 100, 100, 0.1)

while running:
    time_delta = clock.tick(60)

    # Получить позицию курсора относительно мира игры
    mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)

    cursor_pos = pymunk.Vec2d(mouse_pos[0], mouse_pos[1])

    inverse_translation = pymunk.Transform.translation(-screen_width/2, -screen_height/2)
    inverse_rotation = pymunk.Transform.rotation(-rotation)
    inverse_scaling = pymunk.Transform.scaling(1 / scaling)

    inverse_transform = inverse_scaling @ inverse_rotation @ inverse_translation

    inverse_translation_cam = pymunk.Transform.translation(
        -translation.tx, -translation.ty
    )

    world_cursor_pos = inverse_transform @ cursor_pos
    world_translation = inverse_translation_cam @ pymunk.Vec2d(0, 0)

    world_mouse_pos = (
        world_cursor_pos.x + world_translation.x + screen_width/2,
        world_cursor_pos.y + world_translation.y + screen_height/2,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Обработка событий gui Manager
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                key_f_pressed = True
                key_f_hold_start_time = pygame.time.get_ticks()
            if event.key == pygame.K_n:
                if selected_force_field_button is not None:
                    if selected_force_field_button == force_field_buttons[0]:
                        creating_attraction = not creating_attraction
                    elif selected_force_field_button == force_field_buttons[1]:
                        creating_repulsion = not creating_repulsion
                    elif selected_force_field_button == force_field_buttons[2]:
                        creating_force_ring = not creating_force_ring
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))
                key_f_pressed = False
                key_f_hold_start_time = 0
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == save_world_button:
                    save_data(space)
                elif event.ui_element == load_world_button:
                    loaded_data = load_data()
                    if loaded_data:
                        space = loaded_data
                elif event.ui_element == delete_all_button:
                    delete_all()
                elif event.ui_element in force_field_buttons:
                    selected_force_field_button = event.ui_element
                    toolset_force_field()
                if event.ui_element in spawn_buttons:
                    selected_spawn_button = event.ui_element
                    if selected_spawn_button == spawn_buttons[0]:
                        selected_shape = "circle"
                    elif selected_spawn_button == spawn_buttons[1]:
                        selected_shape = "square"
                    elif selected_spawn_button == spawn_buttons[2]:
                        selected_shape = "triangle"
                    elif selected_spawn_button == spawn_buttons[3]:
                        selected_shape = "polyhedron"
                    elif selected_spawn_button == spawn_buttons[4]:
                        selected_shape = "spam"
                    elif selected_spawn_button == spawn_buttons[5]:
                        selected_shape = "delete all"
                    elif selected_spawn_button == spawn_buttons[6]:
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

        debug_info_labels[0].set_text(f"FPS: {round(clock.get_fps())}")
        debug_info_labels[1].set_text(f"Entities: {len(space.bodies)}")
        debug_info_labels[2].set_text(f"Gravity: {len(space.gravity)}")
        debug_info_labels[3].set_text(f"static_lines: {len(static_lines)}")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            shift_speed = 5
        if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_speed = 1
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            # Начало создания статического поля
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
            
            elif event.key == pygame.K_l:
                show_guide = not show_guide
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "../screenshot.png")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if line_point1 is None:
                    line_point1 = world_mouse_pos

        #elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #    # Check if mouse is hovering over a Pymunk shape
        #    for shape in space.shapes:
        #        if shape.point_query(world_mouse_pos):
        #            selected_body = shape.body
        #elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #    # Check if mouse is hovering over a Pymunk shape
        #    for shape in space.shapes:
        #        if shape.point_query(world_mouse_pos):
        #            if selected_body != shape.body:
        #                create_spring(selected_body, shape.body)
        #            selected_body = None
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
        #    # Check if two bodies are selected and create a spring joint between them
        #    if spring and spring.a and spring.b:
        #        space.add(spring)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                object_dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                object_dragging = False

    if key_f_pressed:
        hold_time = pygame.time.get_ticks() - key_f_hold_start_time
        if hold_time >= KEY_HOLD_TIME:
            toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))

    translate_speed = 10 * shift_speed
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
        pymunk.Transform.translation(screen_width/2, screen_height/2)
        @ pymunk.Transform.scaling(scaling)
        @ translation
        @ pymunk.Transform.rotation(rotation)
        @ pymunk.Transform.translation(-screen_width/2, -screen_height/2)
    )

    scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

    rotation += rotation_speed * rotate_left - rotation_speed * rotate_right
    # Отрисовка
    screen.fill((0, 0, 0))

    #fps_debug = f1.render(
    #    "FPS: "
    #    + (str(round(clock.get_fps())))
    #    + "\nEntities: "
    #    + (str(len(space.bodies)))
    #    + "\nGravity: "
    #    + (str(len(space.gravity)))
    #    + "\nThreads: "
    #    + (str(round(space.threads))),
    #    True,
    #    (180, 0, 0),
    #)
    #screen.blit(fps_debug, (screen_width - 300, 10))

    if show_guide == True:
        text_guide_gui.visible = True

    if creating_static_field:
        static_field_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (static_field_start[0] - world_translation[0],
                                                   static_field_start[1] - world_translation[1]), static_field_end, 10)
    #if creating_spring:
    #    spring_end = pygame.mouse.get_pos()
    #    pygame.draw.line(screen, (255, 255, 255), (spring_start[0] - world_translation[0],
    #                                               spring_start[1] - world_translation[1]), spring_end, 10)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)


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
