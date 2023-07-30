import os
import time
import traceback

import pygame
import pymunk
from random import *
import pygame_gui
from pygame_gui.elements import UIDropDownMenu
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

help_console_text = (
    "help: display this"
    "\nexec: execute the Python commands contained in the string as opposed to the program text itself."
    "\neval: executes the expression string passed to it as a mandatory argument and returns the result of executing this string."
    "\npython: open a new python thread"
    "\nclear: clears the output console"
)

debug_info = "'FPS: ' + (str(round(clock.get_fps()))) +'\nEntities: ' + (str(len(space.bodies))) +'\nGravity: ' + " \
             "(str(len(space.gravity))) +'\nThreads: ' + (str(round(space.threads)))\nstatic_lines: "

show_guide = True
fullscreen = False
use_system_dpi = False
key_f11_pressed = False
screen_width, screen_height = 2560, 1400

pygame.init()
pygame.display.set_icon(pygame.image.load("laydigital.png"))
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
version = "Newgodoo a0.1.7"
version_save = version
pygame.display.set_caption(version)
COLLTYPE_DEFAULT = 1

sound_enable = True
sound_volume = 100

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
space.threads = os.cpu_count()
space.iterations = 256
simulation_frequency = 60
static_body = space.static_body
vertices = [(-10000, screen_height - 100), (-10000, screen_height), (10000, screen_height), (10000, screen_height - 100)]
floor = pymunk.Poly(static_body, vertices)
floor.friction = 1.0
floor.elasticity = 0.5
space.add(floor)

space.threads = os.cpu_count()
space.threaded = False

static_lines = []
line_point1 = None
selected_shape = None
selected_force_field = None
camera_offset = Vec2d(0, 0)

camera_dragging = False
camera_drag_start = (0, 0)

f1 = pygame.font.Font(None, 25)
f2 = pygame.font.Font(None, 25)

object_dragging = None
selected_body = None
dragging_body = None
mouse_joint = None
draw_force_field_radius = True
static_field_start = (0, 0)
static_field_end = (0, 0)
creating_static_field = False
creating_spring = False
creating_attraction = False
creating_repulsion = False
creating_force_ring = False
creating_object_drag = False
key_space = False
force_field_strength = 500  # Сила притяжения поля
force_field_radius = 500  # Радиус действия поля

# Инициализация gui Manager
theme_path = './theme.json'
gui_manager = pygame_gui.UIManager((screen_width, screen_height), theme_path)

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

set_elasticity = 0.5
set_square_size = [30, 30]
set_circle_radius = 30
set_triangle_size = 30
set_polyhedron_size = 30
set_friction = 0.7

set_number_faces = 6
gear_radius = 30
gear_thickness = 5

segment_length = 50
segment_thickness = 2
segment_color = pygame.Color("white")

draw_options = pymunk.pygame_util.DrawOptions(screen)

running_physics = True




checkbox_true_texture = "sprites/gui/checkbox_true.png"
checkbox_false_texture = "sprites/gui/checkbox_false.png"



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
]

spawn_button_positions = [
    (10, 10 + (50 + 1) * i) for i in range(5)
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
    elif i == 11:
        button_text = "human"
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

#SETTINGS######################################################################################
window_settings = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 800, 600),
    manager=gui_manager,
    window_display_title="Settings"
)
window_settings.hide()



resolution_options = ["800x600", "1024x768", "1280x720", "1920x1080"]
resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=resolution_options,
    starting_option="800x600",
    relative_rect=pygame.Rect(50, 50, 150, 30),
    manager=gui_manager,
    container=window_settings
)

options_list = [f"option {x}" for x in range(20)]
dropdown = UIDropDownMenu(options_list, "option 0", relative_rect=pygame.Rect(50, 50, 400, 50),
                          manager=gui_manager, expansion_height_limit=100, container=window_settings)

hertz_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(50, 100, 150, 30),
    start_value=60,
    value_range=(30, 144),
    manager=gui_manager,
    container=window_settings
)



# Выбор темы оформления в формате JSON для библиотеки pygame_gui
theme_options = ["theme_light.json", "theme_dark.json", "theme_custom.json"]
theme_dropdown = UIDropDownMenu(theme_options, "option 0", relative_rect=pygame.Rect(50, 200, 400, 50),
                          manager=gui_manager, container=window_settings, expansion_height_limit=100)


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
    value_range=(0, 10000),
    manager=gui_manager,
)

text_label_radius = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(400, 40, 200, 50),
    text="force field radius: {}".format(force_field_radius),
    manager=gui_manager,
)


#SQUARE######################################################################################
window_square = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 400, 300),
    manager=gui_manager,
    window_display_title="Square settings"
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


square_color = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(5, 100, window_square.get_relative_rect().width-45, 100),
    manager=gui_manager,
    container=window_square,
)

square_color_red_input = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(90, 10, 150, 20),
    start_value=force_field_radius,
    value_range=(0, 255),
    manager=gui_manager,
    container=square_color,
)
text_square_red_color = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 10, 85, 20),
    text="Red:",
    container=square_color,
    manager=gui_manager,
)

square_color_green_input = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(90, 30, 150, 20),
    start_value=force_field_radius,
    value_range=(0, 255),
    container=square_color,
    manager=gui_manager,
)

text_square_green_color = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 30, 85, 20),
    text="Green:",
    container=square_color,
    manager=gui_manager,
)

square_color_blue_input = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(90, 50, 150, 20),
    start_value=force_field_radius,
    value_range=(0, 255),
    container=square_color,
    manager=gui_manager,
)
text_square_blue_color = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 50, 85, 20),
    text="Blue:",
    container=square_color,
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

#POLYHENDRON##########################################################
window_polyhedron = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 10, 300, 200),
    manager=gui_manager,
    window_display_title="polyhedron settings"
)
polyhedron_image = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(215, 5, 50, 50),
    image_surface=pygame.image.load(image_spawn_paths[3]),
    container=window_polyhedron,
    manager=gui_manager
)
polyhedron_size_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(60, 10, 100, 20),
    container=window_polyhedron,
    initial_text=str(set_polyhedron_size),
    manager=gui_manager,
)
text_polyhedron_size = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 10, 50, 20),
    text="Size:",
    container=window_polyhedron,
    manager=gui_manager,
)
polyhedron_faces_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(60, 30, 100, 20),
    container=window_polyhedron,
    initial_text=str(set_number_faces),
    manager=gui_manager,
)
text_faces_size = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 30, 50, 20),
    text="Faces:",
    container=window_polyhedron,
    manager=gui_manager,
)

polyhedron_friction_input = pygame_gui.elements.UITextEntryLine(
    initial_text=str(set_friction),
    relative_rect=pygame.Rect(80, 55, 100, 20),
    container=window_polyhedron,
    manager=gui_manager,
)
text_polyhedron_friction = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 55, 80, 20),
    text="friction:",
    container=window_polyhedron,
    manager=gui_manager,
)
polyhedron_elasticity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(90, 75, 105, 20),
    initial_text=str(set_elasticity),
    container=window_polyhedron,
    manager=gui_manager,
)
polyhedron_text_elasticity = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(5, 75, 85, 20),
    text="elasticity:",
    container=window_polyhedron,
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
debug_info = [
    f"FPS: {round(clock.get_fps())}",
    f"Entities: {len(space.bodies)}",
    f"Gravity: {space.gravity}",
    f"Threads: {space.threads}",
    f"static_lines: {static_lines}",
    f"Pygame version: {pygame.version.ver}",
    f"Pymunk version: {pymunk.version}",
    f"window: {pygame.display.get_window_size(), pygame.display.get_current_refresh_rate()}",
    f"Mouse position: {pygame.mouse.get_pos()}",
]

debug_info_labels = []
debug_y_pos = 10

for info in debug_info:
    label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(screen_height + 400, debug_y_pos, 300, 50),
        text=info,
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
        "human": spawn_human
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
    global static_lines
    for body in space.bodies:
        for shape in body.shapes:
            space.remove(body, shape)

    for static_body in static_lines:
        space.remove(static_body)

def spawn_human(position):
    # Создание головы
    head_radius = 30
    head_mass = 10
    head_moment = pymunk.moment_for_circle(head_mass, 0, head_radius)
    head_body = pymunk.Body(head_mass, head_moment)
    head_body.position = position
    head_shape = pymunk.Circle(head_body, head_radius)
    space.add(head_body, head_shape)

    # Создание туловища
    torso_width = 20
    torso_height = 80
    torso_mass = 20
    torso_moment = pymunk.moment_for_box(torso_mass, (torso_width, torso_height))
    torso_body = pymunk.Body(torso_mass, torso_moment)
    torso_body.position = position[0], position[1] - head_radius - torso_height / 2
    torso_shape = pymunk.Poly.create_box(torso_body, (torso_width, torso_height))
    space.add(torso_body, torso_shape)

    # Создание ног
    leg_width = 15
    leg_height = 60
    leg_mass = 15
    leg_moment = pymunk.moment_for_box(leg_mass, (leg_width, leg_height))
    left_leg_body = pymunk.Body(leg_mass, leg_moment)
    left_leg_body.position = position[0] - torso_width / 2 + leg_width / 2, position[1] - head_radius - torso_height - leg_height / 2
    left_leg_shape = pymunk.Poly.create_box(left_leg_body, (leg_width, leg_height))
    space.add(left_leg_body, left_leg_shape)

    right_leg_body = pymunk.Body(leg_mass, leg_moment)
    right_leg_body.position = position[0] + torso_width / 2 - leg_width / 2, position[1] - head_radius - torso_height - leg_height / 2
    right_leg_shape = pymunk.Poly.create_box(right_leg_body, (leg_width, leg_height))
    space.add(right_leg_body, right_leg_shape)

    # Создание рук
    arm_width = 12
    arm_height = 50
    arm_mass = 10
    arm_moment = pymunk.moment_for_box(arm_mass, (arm_width, arm_height))
    left_arm_body = pymunk.Body(arm_mass, arm_moment)
    left_arm_body.position = position[0] - torso_width / 2 - arm_width / 2, position[1] - head_radius - torso_height / 2
    left_arm_shape = pymunk.Poly.create_box(left_arm_body, (arm_width, arm_height))
    space.add(left_arm_body, left_arm_shape)

    right_arm_body = pymunk.Body(arm_mass, arm_moment)
    right_arm_body.position = position[0] + torso_width / 2 + arm_width / 2, position[1] - head_radius - torso_height / 2
    right_arm_shape = pymunk.Poly.create_box(right_arm_body, (arm_width, arm_height))
    space.add(right_arm_body, right_arm_shape)

    # Создание сочленений
    head_torso_joint = pymunk.PinJoint(head_body, torso_body, (0, head_radius), (0, torso_height / 2))
    space.add(head_torso_joint)

    left_leg_torso_joint = pymunk.PinJoint(left_leg_body, torso_body, (0, leg_height / 2), (-torso_width / 2, -torso_height / 2))
    space.add(left_leg_torso_joint)

    right_leg_torso_joint = pymunk.PinJoint(right_leg_body, torso_body, (0, leg_height / 2), (torso_width / 2, -torso_height / 2))
    space.add(right_leg_torso_joint)

    left_arm_torso_joint = pymunk.PinJoint(left_arm_body, torso_body, (0, arm_height / 2), (-torso_width / 2, 0))
    space.add(left_arm_torso_joint)

    right_arm_torso_joint = pymunk.PinJoint(right_arm_body, torso_body, (0, arm_height / 2), (torso_width / 2, 0))
    space.add(right_arm_torso_joint)

def spawn_polyhedron(position):
    tooth_angle = 2 * math.pi / int(polyhedron_faces_input.get_text())
    radius = float(polyhedron_size_input.get_text())
    tooth_radius = radius * 0.4
    points = []
    for i in range(int(polyhedron_faces_input.get_text()) * 2):
        angle = i * tooth_angle / 2
        if i % 2 == 0:
            points.append((radius * math.cos(angle), radius * math.sin(angle)))
        else:
            points.append((tooth_radius * math.cos(angle), tooth_radius * math.sin(angle)))
    area = 0

    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += (x1 * y2 - x2 * y1)

    area = abs(area) / 2
    mass = (area * 2) / 200
    moment = pymunk.moment_for_poly(mass, points)

    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = float(polyhedron_friction_input.get_text())
    shape.elasticity = float(polyhedron_elasticity_input.get_text())
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)
    space.add(body, shape)


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
    shape.friction = float(circle_friction_input.get_text())
    shape.elasticity = float(circle_elasticity_input.get_text())
    space.add(body, shape)
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)

square_color_random = True
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
    )
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = float(square_friction_input.get_text())
    shape.elasticity = float(square_elasticity_input.get_text())
    space.add(body, shape)
    if square_color_random == True:
        shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)
    else:
        shape.color = (int(square_color_red_input.get_current_value()), int(square_color_green_input.get_current_value()), int(square_color_blue_input.get_current_value()), 255)



def spawn_triangle(position):
    tooth_angle = 2 * math.pi / 3
    radius = float(triangle_size_input.get_text())
    tooth_radius = radius * 0.4
    points = []
    for i in range(6):
        angle = i * tooth_angle / 2
        if i % 2 == 0:
            points.append((radius * math.cos(angle), radius * math.sin(angle)))
        else:
            points.append((tooth_radius * math.cos(angle), tooth_radius * math.sin(angle)))
    area = 0

    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += (x1 * y2 - x2 * y1)

    area = abs(area) / 2
    mass = (area * 2) / 200
    moment = pymunk.moment_for_poly(mass, points)

    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Poly(body, points)
    shape.collision_type = COLLTYPE_DEFAULT
    shape.friction = float(triangle_friction_input.get_text())
    shape.elasticity = float(triangle_elasticity_input.get_text())
    shape.color = (random.randrange(100,255), random.randrange(100,255), random.randrange(100,255), 255)
    space.add(body, shape)


def attraction():
    if creating_attraction:
        if draw_force_field_radius == True:
            pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), force_field_radius * scaling, 2)
        for body in space.bodies:

            distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (
                        world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
            if distance <= force_field_radius:
                force_vector = (
                (world_mouse_pos[0] - body.position[0])*2, (world_mouse_pos[1] - body.position[1])*2)
                body.velocity = force_vector

def repulsion():
    if creating_repulsion:
        if draw_force_field_radius == True:
            pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), force_field_radius * scaling, 2)
        for body in space.bodies:
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
    global num_bodies, shuffled_bodies
    if creating_force_ring:
        if num_bodies == 0:
            return
        angle_increment = 2 * math.pi / num_bodies
        angle = 0

        for body in shuffled_bodies:
            x = world_mouse_pos[0] + force_field_radius * math.cos(angle)
            y = world_mouse_pos[1] + force_field_radius * math.sin(angle)

            force_vector = ((x - body.position[0]) * 2, (y - body.position[1]) * 2)
            body.velocity = force_vector

            angle += angle_increment

def freeze_positions():
    if creating_force_ring:
        for body in space.bodies:
            distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (
                        world_mouse_pos[1] - body.position.y) ** 2) ** 0.5

            angle = math.atan2(world_mouse_pos[1] - body.position.y, world_mouse_pos[0] - body.position.x)

            tangential_velocity = math.sqrt(1 / distance)

            velocity_x = tangential_velocity * math.cos(angle + math.pi / 2)
            velocity_y = tangential_velocity * math.sin(angle + math.pi / 2)

            body.velocity = (velocity_x, velocity_y)

object_dragging=None
def object_drag():
    global object_dragging, key_space
    if key_space == False:
        if object_dragging is not None:
            object_dragging.velocity = (
                (world_mouse_pos[0] - object_dragging.position[0]) * 10,
                (world_mouse_pos[1] - object_dragging.position[1]) * 10)
    else:
        if object_dragging is not None:
            object_dragging.position = world_mouse_pos
            object_dragging.velocity = (0, 0)


# def object_drag():
#     for body, shape in objects:
#         distance = ((world_mouse_pos[0] - body.position.x) ** 2 + (world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
#
#         if distance <= 50:
#             if object_dragging and shape.point_query(world_mouse_pos):
#                 force_vector = (
#                     (world_mouse_pos - body.position).rotated(-body.angle).normalized()
#                     * 100012
#                     * 30
#                 )
#                 body.apply_force_at_local_point(force_vector, (0, 0))


def save_data(space, iterations, simulation_frequency, floor_friction, version_save, world_translation):
    data = (space, iterations, simulation_frequency, floor_friction, version_save, world_translation)
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
        window_console.add_output_line_to_log("save done!")
        sound_save_done.play()
    else:
        print("Отменено сохранение.")
        sound_load_error.play()


def load_data():
    root = tk.Tk()
    root.withdraw()
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Newgodoo Save Files", "*.ngsv")]
        )
        if file_path:
            with open(file_path, "rb") as f:
                    data = pickle.load(f)
            if len(data) == 7:
                space, iterations, simulation_frequency, floor_friction, version_save, world_translation = data
                print("Загрузка успешна.")
                sound_save_done.play()
                return space, iterations, simulation_frequency, floor_friction, version_save, world_translation
            else:
                print("Неправильный формат данных.")
                sound_load_error.play()
        else:
            print("Отменена загрузка.")
            sound_load_error.play()
    except:
        print("Что-то пошло не так")


def update():
    global num_bodies
    if running_physics == True:
        num_bodies = len(space.bodies)
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
sound_hovering = pygame.mixer.Sound("sounds/gui/hovering.mp3")
sound_error = pygame.mixer.Sound("sounds/gui/error.mp3")
sound_spawn = pygame.mixer.Sound("sounds/spawn.mp3")
sound_slider = pygame.mixer.Sound("sounds/gui/slider.mp3")
sound_beep_1 = pygame.mixer.Sound("sounds/gui/beep_1.mp3")
sound_pause = pygame.mixer.Sound("sounds/pause.mp3")
sound_pause_in = pygame.mixer.Sound("sounds/pause_in.mp3")
sound_close = pygame.mixer.Sound("sounds/close.mp3")
sound_settings = pygame.mixer.Sound("sounds/pause_in.mp3")
sound_screenshot = pygame.mixer.Sound("sounds/gui/screenshot.mp3")

sound_save_done = pygame.mixer.Sound("sounds/gui/save_done.mp3")
sound_load_error = pygame.mixer.Sound("sounds/gui/save_error.mp3")

sound_beep_1.set_volume(0.2)
sound_spawn.set_volume(0.2)
sound_hovering.set_volume(0.01)
translation = pymunk.Transform()

running = True
space.sleep_time_threshold = 0.5
def create_spring(body1, body2):
    global spring
    spring = pymunk.DampedSpring(body1, body2, (0, 0), (0, 0), 100, 100, 0.1)

def hide_all_windows():
    window_square.hide()
    window_circle.hide()
    window_triangle.hide()
    window_polyhedron.hide()

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


context_menu_window = pygame_gui.elements.UIPanel(
    pygame.Rect(0, 0, 200, 300),
    manager=gui_manager,
)
context_menu_list = pygame_gui.elements.UISelectionList(
    relative_rect=pygame.Rect(0, 0, 200, 300),
    item_list=['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8'],
    container=context_menu_window
)
context_menu_window.hide()
# for i in range(20):
#     button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, i * 30), (200, 30)),
#                                          text=f'Кнопка {i}',
#                                          manager=gui_manager,
#                                          container=scrolling_container)

while running:

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
                    space.add(cb, s)

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

                if command == 'help':
                    window_console.add_output_line_to_log("-----------CONSOLE HELP-----------")
                    window_console.add_output_line_to_log(help_console_text, is_bold=False)
                    window_console.add_output_line_to_log("-----------GAME HELP-----------")
                    window_console.add_output_line_to_log(guide_text, is_bold=False)



                if command.startswith('exec '):
                    code = command[5:]
                    try:
                        result = str(exec(code, globals()))
                        print(result)
                        window_console.add_output_line_to_log(result)
                    except Exception as e:
                        sound_error.play()
                        result = 'Error executing Python code:', e
                        print(result)
                        result_str = str(result)
                        window_console.add_output_line_to_log(result_str)

                if command.startswith('eval '):
                    code = command[5:]
                    try:
                        result = str(eval(code, globals()))
                        print(result)
                        window_console.add_output_line_to_log(result)
                    except Exception as e:
                        sound_error.play()
                        result = 'Error executing Python code:', e
                        print(result)
                        result_str = str(result)
                        window_console.add_output_line_to_log(result_str)

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
                window_console.add_output_line_to_log('Python finished')
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
                        shuffled_bodies = random.sample(space.bodies, num_bodies)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                toolset(tuple(map(sum, zip(world_mouse_pos, camera_offset))))
                shuffled_bodies = space.bodies
                key_f_pressed = False
                key_f_hold_start_time = 0
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:

                sound_hovering.play()
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == save_world_button:
                    sound_click.play()
                    save_data(space, space.iterations, simulation_frequency, floor.friction, version_save, world_translation)
                elif event.ui_element == load_world_button:
                    sound_click.play()
                    loaded_space, iterations, simulation_frequency, floor_friction, version_save, world_translation = load_data()
                    if loaded_space:
                        space = loaded_space
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
                        hide_all_windows()
                        window_polyhedron.show()
                    elif selected_spawn_button == spawn_buttons[4]:
                        selected_shape = "spam"
                    elif selected_spawn_button == spawn_buttons[5]:
                        selected_shape = "delete all"
                    elif selected_spawn_button == spawn_buttons[6]:
                        selected_shape = "force field"
                    elif selected_spawn_button == spawn_buttons[7]:
                        selected_shape = "None"
                    elif selected_spawn_button == spawn_buttons[8]:
                        selected_shape = "None"
                    elif selected_spawn_button == spawn_buttons[9]:
                        selected_shape = "None"
                    elif selected_spawn_button == spawn_buttons[10]:
                        selected_shape = "None"
                    elif selected_spawn_button == spawn_buttons[11]:
                        selected_shape = "human"


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
        debug_info_labels[2].set_text(f"Gravity: {space.gravity}")
        debug_info_labels[3].set_text(f"Threads: {space.threads}")
        debug_info_labels[4].set_text(f"static_lines: {static_lines}")  # Update static_lines accordingly
        debug_info_labels[8].set_text(f"Mouse position: {pygame.mouse.get_pos()}")  # Update mouse position


        if key_f11_pressed:
            fullscreen = not fullscreen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            shift_speed = 5
        if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_speed = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            if shift_speed > 1:
                num_bodies -= 1
                for i in range(5):
                    if space.bodies:
                        last_body = space.bodies[-1]
                        for shape in last_body.shapes:
                            space.remove(shape)
                        space.remove(last_body)
            else:
                if space.bodies:
                    last_body = space.bodies[-1]
                    for shape in last_body.shapes:
                        space.remove(shape)
                    space.remove(last_body)
                    num_bodies -= 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            sound_click_3.play()
            static_field_start = world_mouse_pos
            creating_static_field = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_b:
            sound_click_4.play()
            print("Создается барьер")
            static_field_end = world_mouse_pos
            static_field = pymunk.Segment(
                static_body, static_field_start, static_field_end, 10
            )
            static_field.friction = set_friction
            static_field.elasticity = 0.5
            try:
                space.add(static_field)
            except:
                traceback.print_exc()
            creating_static_field = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                info = space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
                if info is not None and info.shape in [obj[1] for obj in space.bodies]:
                    space.remove(info.shape)
                    space.bodies = [(body, shape) for body, shape in space.bodies if shape != info.shape]

            if event.key == pygame.K_SPACE:
                sound_pause.play()

                vis_pause_icon(show=not pause_icon_visible)
                running_physics = not running_physics
                key_space = not key_space

            elif event.key == pygame.K_l:
                show_guide = not show_guide
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "../screenshot.png")
                sound_screenshot.play()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if line_point1 is None:
                    line_point1 = world_mouse_pos

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_j:
        #    # Check if mouse is hovering over a Pymunk shape
        #        info = space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
        #        if info is not None:
        #            if info.shape.body != static_body:
        #                selected_body = info.shape.body
        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_j:
        #         if selected_body is not None:
        #             selected_body.is_dragging = False
        #             selected_body = None
        #             create_spring(selected_body, selected_body)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                info = space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
                if info is not None:
                    if info.shape.body != static_body:
                        object_dragging = info.shape.body

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if object_dragging is not None:
                    object_dragging.is_dragging = False
                    object_dragging = None

        # Обработка событий правой кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            info = space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
            if info is not None:
                if info.shape.body != static_body:
                    context_menu_window.show()
                    context_menu_window.set_position(position=event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not context_menu_window.rect.collidepoint(event.pos):
                context_menu_window.hide()
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            selected_button_index = context_menu_list.selected_option
            print(f"Selected button index: {selected_button_index}")

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
        pygame.draw.line(screen, (255, 255, 255), (static_field_start[0] - world_mouse_pos[0],
                                                   static_field_start[1]- world_mouse_pos[1]),
                         static_field_end, 10)
    #if creating_spring:
    #    spring_end = pygame.mouse.get_pos()
    #    pygame.draw.line(screen, (255, 255, 255), (spring_start[0] - world_translation[0],
    #                                               spring_start[1] - world_translation[1]), spring_end, 10)

    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
    screen.fill((20, 20, 20))
    gui_manager.process_events(event)
    gui_manager.update(time_delta)
    space.debug_draw(draw_options)
    gui_manager.draw_ui(screen)
    update()
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
