import time
import traceback

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
import subprocess
import threading
#import numpy as np
#from numba import jit
guide_text = (
    "L: show this guide"
    "\nF: Spawn object"
    "\nclamped F: Auto spawn objects"
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
             "(str(len(space.gravity))) +'\nThreads: ' + (str(round(space.threads)))\nstatic_lines: "

show_guide = True
fullscreen = False
use_system_dpi = True
key_f11_pressed = False
screen_width, screen_height = 1920, 1080

pygame.init()
pygame.display.set_icon(pygame.image.load("laydigital.png"))
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
version = "Newgodoo a0.1.6"
version_save = version
pygame.display.set_caption(version)
COLLTYPE_DEFAULT = 0

if fullscreen:
    user32 = ctypes.windll.user32
    if use_system_dpi:
        screen_width = int(user32.GetSystemMetrics(0))
        screen_height = int(user32.GetSystemMetrics(1))
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        user32.SetProcessDPIAware()
        screen_width = int(user32.GetSystemMetrics(0))
        screen_height = int(user32.GetSystemMetrics(1))
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
else:
    user32 = ctypes.windll.user32
    if use_system_dpi:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        user32.SetProcessDPIAware()
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)


clock = pygame.time.Clock()

space = pymunk.Space(threaded=True)
space.threads = 8
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

shift_speed = 1
KEY_HOLD_TIME = 1000  #в миллисекундах
key_f_pressed = False
key_f_hold_start_time = 0

# Создание кнопок для спавна предметов
spawn_buttons = []
force_field_buttons = []
force_field_images = []
spawn_button_width = 120
spawn_button_height = 50
button_x = 10
button_y = 10
button_spacing = 10

X, Y = 0, 1

set_elasticity = 0.25
set_square_size = [30, 30]
set_circle_radius = 30
set_triangle_size = 30
set_friction = 0.7

set_number_faces = 5
gear_radius = 30
gear_thickness = 5

segment_length = 50
segment_thickness = 2
segment_color = pygame.Color("white")

draw_options = pymunk.pygame_util.DrawOptions(screen)

running_physics = True

image_force_field_paths = [
    "sprites/gui/force_field/attraction.png",
    "sprites/gui/force_field/repulsion.png",
    "sprites/gui/force_field/ring.png"
]
force_field_button_positions = [
    (screen_width-135, screen_height-300 + (50 + 1) * i) for i in range(3)
]

for i, pos in enumerate(force_field_button_positions):
    image_rect = pygame.Rect(pos[0]-50, pos[1]+1, 47, 47)
    button_rect = pygame.Rect(pos, (110, 50))
    button_text = ""
    if i == 0:
        button_text = "attraction"
    elif i == 1:
        button_text = "repulsion"
    elif i == 2:
        button_text = "ring"
    image = pygame_gui.elements.UIImage(
        relative_rect=image_rect,
        image_surface=pygame.image.load(image_force_field_paths[i]),
        manager=gui_manager
    )
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect, text=button_text, manager=gui_manager
    )
    force_field_buttons.append(button)
    force_field_images.append(image)
selected_force_field_button = force_field_buttons[0]


image_spawn_paths = [
    "sprites/gui/spawn/circle.png",#1
    "sprites/gui/spawn/square.png",#2
    "sprites/gui/spawn/triangle.png",#3
    "sprites/gui/spawn/polyhedron.png",#4
    "sprites/gui/spawn/spam.png",#5
    "sprites/gui/spawn/placeholder.png",#6
    "sprites/gui/spawn/placeholder.png",#7
    "sprites/gui/spawn/placeholder.png",#8
    "sprites/gui/spawn/placeholder.png",#9
    "sprites/gui/spawn/placeholder.png",#9
    "sprites/gui/spawn/placeholder.png",#10
    "sprites/gui/spawn/placeholder.png",#11
    "sprites/gui/spawn/placeholder.png",#12
    "sprites/gui/spawn/placeholder.png",#13
    "sprites/gui/spawn/placeholder.png",#13
    "sprites/gui/spawn/placeholder.png",#14
    "sprites/gui/spawn/placeholder.png",#15
    "sprites/gui/spawn/placeholder.png",#16
    "sprites/gui/spawn/placeholder.png",#17
    "sprites/gui/spawn/placeholder.png",#18
    "sprites/gui/spawn/placeholder.png",#19
]

spawn_button_positions = [
    (10, 10 + (50 + 1) * i) for i in range(19)
]
for i, pos in enumerate(spawn_button_positions):
    image_rect = pygame.Rect(pos[0] + 118, pos[1]+2, 45, 45)
    button_rect = pygame.Rect(pos, (115, 50))
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
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect, text=button_text, manager=gui_manager
    )
    image = pygame_gui.elements.UIImage(
        relative_rect=image_rect,
        image_surface=pygame.image.load(image_spawn_paths[i]),
        manager=gui_manager
    )
    spawn_buttons.append(button)
selected_spawn_button = None

window_console = pygame_gui.windows.UIConsoleWindow(
    pygame.Rect(screen_width-410, screen_height-600, 400, 300),
    manager=gui_manager,
)

#FORCE_FIELD######################################################################################
strength_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(400, 10, 200, 20),
    start_value=force_field_strength,
    value_range=(0, 5000),
    manager=gui_manager,
)

text_label_strength = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(380, 10, 250, 50),
    text="force field strength: {}".format(force_field_strength),
    manager=gui_manager,
)

radius_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(400, 40, 200, 20),
    start_value=force_field_radius,
    value_range=(0, 1000),
    manager=gui_manager,
)

text_label_radius = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(400, 40, 200, 50),
    text="force field radius: {}".format(force_field_radius),
    manager=gui_manager,
)


#SQUARE######################################################################################
window_square = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 300, 200),
    manager=gui_manager,
    window_display_title="square settings"
)
square_image = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(215, 5, 50, 50),
    image_surface=pygame.image.load(image_spawn_paths[1]),
    container=window_square,
    manager=gui_manager
)
square_size_input_x = pygame_gui.elements.UITextEntryLine(
    initial_text=str(set_square_size[0]),
    relative_rect=pygame.Rect(30, 10, 100, 20),
    container=window_square,
    manager=gui_manager,
)
text_square_size_x = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 10, 20, 20),
    text="X:",
    container=window_square,
    manager=gui_manager,
)
square_size_input_y = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(30, 30, 100, 20),
    initial_text=str(set_square_size[1]),
    container=window_square,
    manager=gui_manager,
)

text_square_size_y = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 30, 20, 20),
    text="Y:",
    container=window_square,
    manager=gui_manager,
)
square_friction_input = pygame_gui.elements.UITextEntryLine(
    initial_text=str(set_friction),
    relative_rect=pygame.Rect(80, 55, 100, 20),
    container=window_square,
    manager=gui_manager,
)
text_square_friction = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 55, 80, 20),
    text="friction:",
    container=window_square,
    manager=gui_manager,
)
square_elasticity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(90, 75, 105, 20),
    initial_text=str(set_elasticity),
    container=window_square,
    manager=gui_manager,
)
square_text_elasticity = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 75, 85, 20),
    text="elasticity:",
    container=window_square,
    manager=gui_manager,
)
#CIRCLE######################################################################################
window_circle = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 300, 200),
    manager=gui_manager,
    window_display_title="circle settings"
)

circle_image = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(215, 5, 50, 50),
    image_surface=pygame.image.load(image_spawn_paths[0]),
    container=window_circle,
    manager=gui_manager
)
circle_radius_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(30, 10, 100, 20),
    initial_text=str(set_circle_radius),
    container=window_circle,
    manager=gui_manager,
)
text_circle_radius = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 10, 20, 20),
    text="R:",
    container=window_circle,
    manager=gui_manager,
)
circle_friction_input = pygame_gui.elements.UITextEntryLine(
    initial_text=str(set_friction),
    relative_rect=pygame.Rect(80, 55, 100, 20),
    container=window_circle,
    manager=gui_manager,
)
text_circle_friction = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 55, 80, 20),
    text="friction:",
    container=window_circle,
    manager=gui_manager,
)
circle_elasticity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(90, 75, 105, 20),
    initial_text=str(set_elasticity),
    container=window_circle,
    manager=gui_manager,
)
circle_text_elasticity = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 75, 85, 20),
    text="elasticity:",
    container=window_circle,
    manager=gui_manager,
)
#TRIANGLE##########################################
window_triangle = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 300, 200),
    manager=gui_manager,
    window_display_title="triangle settings"
)
triangle_image = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(215, 5, 50, 50),
    image_surface=pygame.image.load(image_spawn_paths[2]),
    container=window_triangle,
    manager=gui_manager
)
triangle_size_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(60, 10, 100, 20),
    container=window_triangle,
    initial_text=str(set_triangle_size),
    manager=gui_manager,
)
text_triangle_size = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 10, 50, 20),
    text="Size:",
    container=window_triangle,
    manager=gui_manager,
)

triangle_friction_input = pygame_gui.elements.UITextEntryLine(
    initial_text=str(set_friction),
    relative_rect=pygame.Rect(80, 55, 100, 20),
    container=window_triangle,
    manager=gui_manager,
)
text_triangle_friction = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 55, 80, 20),
    text="friction:",
    container=window_triangle,
    manager=gui_manager,
)
triangle_elasticity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(90, 75, 105, 20),
    initial_text=str(set_elasticity),
    container=window_triangle,
    manager=gui_manager,
)
triangle_text_elasticity = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 75, 85, 20),
    text="elasticity:",
    container=window_triangle,
    manager=gui_manager,
)
# OTHER_GUI######################################################################################
text_guide_gui = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect(screen_width - 280, 150, 240, 300),
    html_text=guide_text,
    visible=show_guide,
    manager=gui_manager,
)
text_guide_gui.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

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





pause_icon_image = pygame.image.load("sprites/gui/pause.png").convert_alpha()
pause_icon_rect = pygame.Rect(screen_width - 450, 10, 50, 50)

pause_icon = pygame_gui.elements.UIImage(
    relative_rect=pause_icon_rect,
    image_surface=pause_icon_image,
    manager=gui_manager
)





# FRICTION######################################################################
friction_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(200, 50, 200, 20),
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
#DELETE_ALL_BUTTON##########################################################################
delete_all_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(10, screen_height-50, 125, 40),
        text="Delete all",
        manager=gui_manager
)



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
        try:
            spawn_func(position)
            if ValueError != True:
                sound_spawn.play()
        except:
            sound_error.play()
            traceback.print_exc()

def toolset_force_field():
    sound_click_2.play()
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
    sound_error.play()
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
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)
    add_body_shape(body, shape)


def spawn_circle(position):
    radius = float(circle_radius_input.get_text())
    mass = radius * math.pi / 10
    moment = pymunk.moment_for_circle(
        mass, 0, radius
    )
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    shape.elasticity = set_elasticity
    add_body_shape(body, shape)
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)


def spawn_square(position):
    size = (float(square_size_input_x.get_text()), float(square_size_input_y.get_text()))
    points = [
        (-size[0], -size[1]),
        (-size[0], size[1]),
        (size[0], size[1]),
        (size[0], -size[1]),
    ]
    mass = (size[0] * size[1]) / 200
    moment = pymunk.moment_for_box(
        mass, (2 * size[0], 2 * size[1])
    )  # Calculate moment of inertia for a square
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = float(square_friction_input.get_text())
    shape.elasticity = float(square_elasticity_input.get_text())
    add_body_shape(body, shape)
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)



def spawn_triangle(position):
    size = set_triangle_size * 2
    height = size * math.sqrt(3) / 2
    points = [
        (0, height / 2),
        (-size / 2, -height / 2),
        (size / 2, -height / 2)
    ]
    mass = size * height / 100
    moment = pymunk.moment_for_poly(mass, points)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = set_friction
    shape.elasticity = set_elasticity
    add_body_shape(body, shape)
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)


def add_body_shape(body, shape):
    space.add(body, shape)
    objects.append((body, shape))


def attraction():
    if creating_attraction:
        for body, shape in objects:
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


def save_data(space, objects, iterations, simulation_frequency, floor_friction, version_save, world_translation):
    data = (space, objects, iterations, simulation_frequency, floor_friction, version_save, world_translation)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ngsv", filetypes=[("Newgodoo Save File", "*.ngsv")]
    )

    if file_path:
        with open(file_path, "wb") as f:
            try:
                pickle.dump(data, f)
            except:
                print("Что-то пошло не так")
        print("Сохранение успешно.")
    else:
        print("Отменено сохранение.")


def load_data():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Newgodoo Save Files", "*.ngsv")]
    )

    if file_path:
        with open(file_path, "rb") as f:
            try:
                data = pickle.load(f)
            except:
                print("Что-то пошло не так")

        if len(data) == 7:
            space, objects, iterations, simulation_frequency, floor_friction, version_save, world_translation = data
            print("Загрузка успешна.")
            return space, objects, iterations, simulation_frequency, floor_friction, version_save, world_translation
        else:
            print("Неправильный формат данных.")
    else:
        print("Отменена загрузка.")
    return None, None, None, None, None, None, None

def update():
    if running_physics == True:
        dt = 2.0 / simulation_frequency
        space.step(dt)
        space.gravity = rotation * 1000, 1000
        attraction()
        repulsion()
        ring()
        object_drag()
        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 10, 2)


zoom_speed = 0.02
rotation_speed = 0.01
scaling = 1
rotation = 0

sound_click = pygame.mixer.Sound("sounds/gui/click.mp3")
sound_click_2 = pygame.mixer.Sound("sounds/gui/click_2.mp3")
sound_click_3 = pygame.mixer.Sound("sounds/gui/click_3.mp3")
sound_click_4 = pygame.mixer.Sound("sounds/gui/click_4.mp3")
sound_error = pygame.mixer.Sound("sounds/gui/error.mp3")
sound_spawn = pygame.mixer.Sound("sounds/spawn.mp3")
sound_slider = pygame.mixer.Sound("sounds/gui/slider.mp3")
sound_beep_1 = pygame.mixer.Sound("sounds/gui/beep_1.mp3")
sound_pause = pygame.mixer.Sound("sounds/pause.mp3")
sound_close = pygame.mixer.Sound("sounds/close.mp3")
sound_beep_1.set_volume(0.2)
sound_spawn.set_volume(0.2)

translation = pymunk.Transform()

dragging_body = None
mouse_joint = None
running = True
space.sleep_time_threshold = 0.5
def create_spring(body1, body2):
    global spring
    spring = pymunk.DampedSpring(body1, body2, (0, 0), (0, 0), 100, 100, 0.1)

def hide_all_windows():
    window_square.hide()
    window_circle.hide()
    window_triangle.hide()

    strength_slider.hide()
    radius_slider.hide()
    text_label_radius.hide()
    text_label_strength.hide()


def show_force_field_settings():
    strength_slider.show()
    radius_slider.show()
    text_label_radius.show()
    text_label_strength.show()

pause_icon.hide()
pause_icon_visible = False


def vis_pause_icon(show):
    global pause_icon_visible
    if show:
        pause_icon.show()
        pause_icon_visible = True
        pygame.display.set_caption(version + " (simulation paused)")

    else:
        pause_icon.hide()
        pause_icon_visible = False
        pygame.display.set_caption(version)

hide_all_windows()
class ConsoleOutput:
    def __init__(self):
        self.text = ''


python_process = None

output_str = None
data_lock = None


while running:
    screen.fill((20, 20, 20))
    time_delta = clock.tick(60) / 1000

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

        if (event.type == pygame_gui.UI_CONSOLE_COMMAND_ENTERED and
                event.ui_element == window_console):
            command = event.command
            if python_process is not None and output_str is not None:
                bytes_command = (command + '\n').encode()
                python_process.stdin.write(bytes_command)
                python_process.stdin.flush()

            else:
                if command == "web":
                    simulation_frequency = 120
                    space.gravity = 0, -900
                    space.damping = 0.5
                    web_group = 1
                    bs = []
                    dist = 0.5
                    c = Vec2d(world_mouse_pos[0], world_mouse_pos[1])
                    cb = pymunk.Body(1, 1)
                    cb.position = c
                    s = pymunk.Circle(cb, 15)  # to have something to grab
                    s.filter = pymunk.ShapeFilter(group=web_group)
                    s.ignore_draw = True
                    add_body_shape(cb, s)

                    # generate each crossing in the net
                    for x in range(0, 101):
                        b = pymunk.Body(1, 1)
                        v = Vec2d(1, 0).rotated_degrees(x * 18)
                        scale = screen_height / 2.0 / 6.0 * 0.5

                        dist += 1 / 18.0
                        dist = dist ** 1.005

                        offset = 100.0
                        offset = [0.0, -0.80, -1.0, -0.80][((x * 18) % 360) // 18 % 4]
                        offset = 0.8 + offset

                        offset *= dist ** 2.8 / 100.0

                        v = v.scale_to_length(scale * (dist + offset))

                        b.position = c + v
                        s = pymunk.Circle(b, 15)
                        s.filter = pymunk.ShapeFilter(group=web_group)
                        s.ignore_draw = True
                        space.add(b, s)
                        bs.append(b)


                    def add_joint(a, b):
                        rl = a.position.get_distance(b.position) * 0.9
                        stiffness = 5000.0
                        damping = 100
                        j = pymunk.DampedSpring(a, b, (0, 0), (0, 0), rl, stiffness, damping)
                        j.max_bias = 1000
                        # j.max_force = 50000
                        space.add(j)


                    for b in bs[:20]:
                        add_joint(cb, b)

                    for i in range(len(bs) - 1):
                        add_joint(bs[i], bs[i + 1])

                        i2 = i + 20
                        if len(bs) > i2:
                            add_joint(bs[i], bs[i2])

                    ### WEB ATTACH POINTS
                    static_bs = []
                    for b in bs[-17::4]:
                        static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
                        static_body.position = b.position
                        static_bs.append(static_body)

                        # j = pymunk.PivotJoint(static_body, b, static_body.position)
                        j = pymunk.DampedSpring(static_body, b, (0, 0), (0, 0), 0, 0, 0)
                        j.damping = 100
                        j.stiffness = 20000
                        space.add(j)

                if command == 'planet':
                    gravityStrength = 5.0e6
                    def planetGravity(body, gravity, damping, dt):
                        # Gravitational acceleration is proportional to the inverse square of
                        # distance, and directed toward the origin. The central planet is assumed
                        # to be massive enough that it affects the satellites but not vice versa.
                        sq_dist = body.position.get_dist_sqrd((300, 300))
                        g = (
                                (body.position - pymunk.Vec2d(300, 300))
                                * -gravityStrength
                                / (sq_dist * math.sqrt(sq_dist))
                        )
                        pymunk.Body.update_velocity(body, g, damping, dt)


                    def add_box(space):
                        body = pymunk.Body()
                        body.position = pymunk.Vec2d(random.randint(50, 550), random.randint(50, 550))
                        body.velocity_func = planetGravity

                        # Set the box's velocity to put it into a circular orbit from its
                        # starting position.
                        r = body.position.get_distance((300, 300))
                        v = math.sqrt(gravityStrength / r) / r
                        body.velocity = (body.position - pymunk.Vec2d(300, 300)).perpendicular() * v
                        # Set the box's angular velocity to match its orbital period and
                        # align its initial angle with its position.
                        body.angular_velocity = v
                        body.angle = math.atan2(body.position.y, body.position.x)

                        box = pymunk.Poly.create_box(body, size=(10, 10))
                        box.mass = 1
                        box.friction = 0.7
                        box.elasticity = 0
                        box.color = pygame.Color("white")
                        space.add(body, box)


                    for x in range(30):
                        add_box(space)

                if command == 'exit':
                    pygame.quit()

                if command.startswith('exec '):
                    code = command[5:]
                    try:
                        exec(code, globals())
                    except Exception as e:
                        sound_error.play()
                        result = 'Error executing Python code:', e
                        result_str = str(result)
                        window_console.add_output_line_to_log(result_str)

                if command.startswith('eval '):
                    code = command[5:]
                    try:
                        result = eval(code, globals())
                        result_str = str(result)
                        window_console.add_output_line_to_log(result_str)
                    except Exception as e:
                        sound_error.play()
                        result = 'Error executing Python code:', e
                        result_str = str(result)
                        window_console.add_output_line_to_log(result_str)

 #               if command == 'exec':
 #                   try:
 #                       exec(command)
 #                       print('Command executed successfully')
 #                   except Exception as e:
 #                       print('Error executing command:', str(e))

                if command == 'python':
                    window_console.set_log_prefix(" ")
                    python_process = subprocess.Popen(['python', '-i'],
                                                      stdin=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.STDOUT, shell=False)
                    output_str = ConsoleOutput()
                    data_lock = threading.Lock()

                    def write_all(process, output, lock):
                        while True:
                            data = process.stdout.read(1).decode("utf-8")
                            if not data:
                                break
                            with lock:
                                output.text += data


                    writer = threading.Thread(target=write_all, args=(python_process,
                                                                      output_str,
                                                                      data_lock))
                    writer.start()

                elif command == 'clear':
                    window_console.clear_log()

        if python_process is not None:
            if "\n" in output_str.text:
                split_output = output_str.text.split('\n', 1)
                with data_lock:
                    output_str.text = split_output[1]
                output_line_to_print = split_output[0].strip()
                window_console.add_output_line_to_log(output_line_to_print)
            elif len(output_str.text) > 0:
                output_line_to_print = output_str.text.strip()
                with data_lock:
                    output_str.text = ""
                window_console.add_output_line_to_log(output_line_to_print, remove_line_break=True)

            if python_process.poll() is not None:
                print('Python finished')
                python_process = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sound_close.play()
                pygame.quit()
            if event.key == pygame.K_F11:
                sound_close.play()
                key_f11_pressed = True
            if event.key == pygame.K_f:
                key_f_pressed = True
                key_f_hold_start_time = pygame.time.get_ticks()
            if event.key == pygame.K_n:
                sound_beep_1.play()
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
                    sound_click.play()
                    save_data(space, objects, space.iterations, simulation_frequency, floor.friction, version_save, world_translation)
                elif event.ui_element == load_world_button:
                    sound_click.play()
                    loaded_space, loaded_objects, iterations, simulation_frequency, floor_friction, version_save, world_translation = load_data()
                    if loaded_space and loaded_objects:
                        space = loaded_space
                        objects = loaded_objects
                        space.iterations = iterations
                elif event.ui_element == delete_all_button:
                    delete_all()
                elif event.ui_element in force_field_buttons:
                    selected_force_field_button = event.ui_element
                    toolset_force_field()
                    show_force_field_settings()
                if event.ui_element in spawn_buttons:
                    sound_click_2.play()
                    selected_spawn_button = event.ui_element
                    if selected_spawn_button == spawn_buttons[0]:
                        selected_shape = "circle"
                        hide_all_windows()
                        window_circle.show()
                    elif selected_spawn_button == spawn_buttons[1]:
                        selected_shape = "square"
                        hide_all_windows()
                        window_square.show()
                    elif selected_spawn_button == spawn_buttons[2]:
                        selected_shape = "triangle"
                        hide_all_windows()
                        window_triangle.show()
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



        if key_f11_pressed:
            fullscreen = not fullscreen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            shift_speed = 5
        if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_speed = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            sound_click_3.play()
            # Начало создания статического поля
            static_field_start = world_mouse_pos
            creating_static_field = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_b:
            sound_click_4.play()
            print("Создается барьер")
            # Создание статического поля между точками
            static_field_end = world_mouse_pos
            static_field = pymunk.Segment(
                static_body, static_field_start, static_field_end, 10
            )
            static_field.friction = set_friction
            try:
                space.add(static_field)
            except:
                traceback.print_exc()
            creating_static_field = False


        # Обработка событий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound_pause.play()
                vis_pause_icon(show=not pause_icon_visible)
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
        fill_fraction = min(hold_time / KEY_HOLD_TIME, 1.0)
        radius = int(20 * fill_fraction)

        if hold_time >= 100:
            pygame.draw.circle(screen, (255, 255, 255),
                               (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] - 20), 20, 1)
            pygame.draw.circle(screen, (255, 255, 255),
                               (pygame.mouse.get_pos()[0]+30,pygame.mouse.get_pos()[1]-20) , radius, 20)
        if hold_time >= KEY_HOLD_TIME:
            toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))

    translate_speed = 10 * shift_speed / scaling
    keys = pygame.key.get_pressed()
    left = int(keys[pygame.K_LEFT])
    up = int(keys[pygame.K_UP])
    down = int(keys[pygame.K_DOWN])
    right = int(keys[pygame.K_RIGHT])

    zoom_in = int(keys[pygame.K_KP_PLUS])
    zoom_out = int(keys[pygame.K_KP_MINUS])
    rotate_left = int(keys[pygame.K_KP_6])
    rotate_right = int(keys[pygame.K_KP_4])

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

    if show_guide:
        text_guide_gui.visible = True

    if creating_static_field:
        static_field_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (static_field_start[0],
                                                   static_field_start[1]),
                         static_field_end, 10)
    #if creating_spring:
    #    spring_end = pygame.mouse.get_pos()
    #    pygame.draw.line(screen, (255, 255, 255), (spring_start[0] - world_translation[0],
    #                                               spring_start[1] - world_translation[1]), spring_end, 10)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)

    gui_manager.process_events(event)
    gui_manager.update(time_delta)
    update()
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
