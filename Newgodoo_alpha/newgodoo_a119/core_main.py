from gui import *

import pygame
import pygame_gui
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
from random import *
import random

import ctypes
import pickle
import tkinter as tk
from tkinter import filedialog

import math
import subprocess
import threading
import os
import time
import traceback

class Core:
    def __init__(self):
        #main
        self.version = "Newgodoo a0.1.9"
        self.version_save = self.version
        self.fullscreen = False
        self.use_system_dpi = False
        self.screen_width, self.screen_height = 2560, 1400

        pygame.init()
        pygame.display.set_icon(pygame.image.load("laydigital.png"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        pygame.display.set_caption(self.version)
        self.clock = pygame.time.Clock()

        if self.fullscreen:
            user32 = ctypes.windll.user32
            if self.use_system_dpi:
                screen_width = int(user32.GetSystemMetrics(0))
                screen_height = int(user32.GetSystemMetrics(1))
                self.screen = pygame.display.set_mode((screen_width, screen_height),
                                                 pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else:
                user32.SetProcessDPIAware()
                screen_width = int(user32.GetSystemMetrics(0))
                screen_height = int(user32.GetSystemMetrics(1))
                self.screen = pygame.display.set_mode((screen_width, screen_height),
                                                 pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            user32 = ctypes.windll.user32
            if self.use_system_dpi:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                 pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else:
                user32.SetProcessDPIAware()
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                 pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)

        #pymunk
        self.space = pymunk.Space(threaded=True)
        self.space.threads = os.cpu_count()
        self.space.threaded = False
        self.COLLTYPE_DEFAULT = 1
        self.draw_force_field_radius = True
        self.running_physics = True
        self.running = True
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.translation = pymunk.Transform()

        self.set_elasticity = 0.5
        self.set_rectangle_size = [30, 30]
        self.set_circle_radius = 30
        self.set_triangle_size = 30
        self.set_polyhedron_size = 30
        self.set_friction = 0.7
        self.set_number_faces = 6
        self.gear_radius = 30
        self.gear_thickness = 5
        self.segment_length = 50
        self.segment_thickness = 2
        self.segment_color = pygame.Color("white")
        self.zoom_speed = 0.02
        self.rotation_speed = 0.01
        self.scaling = 1
        self.rotation = 0


        #sound
        self.sound_enable = True
        self.sound_volume = 100
        self.sound_click = pygame.mixer.Sound("sounds/gui/click.mp3")
        self.sound_click_2 = pygame.mixer.Sound("sounds/gui/click_2.mp3")
        self.sound_click_3 = pygame.mixer.Sound("sounds/gui/click_3.mp3")
        self.sound_click_4 = pygame.mixer.Sound("sounds/gui/click_4.mp3")
        self.sound_hovering = pygame.mixer.Sound("sounds/gui/hovering.mp3")
        self.sound_error = pygame.mixer.Sound("sounds/gui/error.mp3")
        self.sound_spawn = pygame.mixer.Sound("sounds/spawn.mp3")
        self.sound_slider = pygame.mixer.Sound("sounds/gui/slider.mp3")
        self.sound_beep_1 = pygame.mixer.Sound("sounds/gui/beep_1.mp3")
        self.sound_pause = pygame.mixer.Sound("sounds/pause.mp3")
        self.sound_pause_in = pygame.mixer.Sound("sounds/pause_in.mp3")
        self.sound_close = pygame.mixer.Sound("sounds/close.mp3")
        self.sound_settings = pygame.mixer.Sound("sounds/pause_in.mp3")
        self.sound_screenshot = pygame.mixer.Sound("sounds/gui/screenshot.mp3")
        self.sound_save_done = pygame.mixer.Sound("sounds/gui/save_done.mp3")
        self.sound_load_error = pygame.mixer.Sound("sounds/gui/save_error.mp3")
        self.sound_beep_1.set_volume(0.2)
        self.sound_spawn.set_volume(0.2)
        self.sound_hovering.set_volume(0.01)

        #Game settings
        self.force_field_strength = 500
        self.force_field_radius = 500
        self.shift_speed = 1
        self.KEY_HOLD_TIME = 1000
        self.space.sleep_time_threshold = 0.5

        #keys
        self.camera_dragging = False
        self.key_f11_pressed = False
        self.key_esc_pressed = False
        self.center_button = False
        self.key_space = False
        self.key_f_pressed = False
        self.key_z_pressed = False
        self.key_f_hold_start_time = 0
        self.key_z_hold_start_time = 0

        self.pause_icon_visible = False
        self.show_guide = True
        self.static_lines = []
        self.camera_offset = Vec2d(0, 0)
        self.camera_drag_start = (0, 0)
        self.line_point1 = None
        self.selected_shape = None
        self.selected_force_field = None
        self.object_dragging = None
        self.selected_body = None
        self.dragging_body = None
        self.mouse_joint = None
        self.creating_static_field = False
        self.creating_spring = False
        self.creating_attraction = False
        self.creating_repulsion = False
        self.creating_force_ring = False
        self.creating_force_spiral = False
        self.creating_force_freeze = False
        self.creating_object_drag = False
        self.static_field_start = (0, 0)
        self.static_field_end = (0, 0)

        self.spawn_buttons = []
        self.force_field_buttons = []
        self.force_field_images = []
        self.spawn_button_width = 120
        self.spawn_button_height = 50
        self.button_x = 10
        self.button_y = 10
        self.button_spacing = 10
        self.X, self.Y = 0, 1

        #sprites
        self.checkbox_true_texture = "sprites/gui/checkbox_true.png"
        self.checkbox_false_texture = "sprites/gui/checkbox_false.png"

        self.image_force_field_paths = [
            "sprites/gui/force_field/attraction.png",
            "sprites/gui/force_field/repulsion.png",
            "sprites/gui/force_field/ring.png",
            "sprites/gui/force_field/spiral.png",
            "laydigital.png"
        ]
        self.image_spawn_paths = [
            "sprites/gui/spawn/circle.png",  # 1
            "sprites/gui/spawn/rectangle.png",  # 2
            "sprites/gui/spawn/triangle.png",  # 3
            "sprites/gui/spawn/polyhedron.png",  # 4
            "sprites/gui/spawn/spam.png",  # 5
        ]

        self.debug_info = [
            f"FPS: {round(self.clock.get_fps())}",
            f"Entities: {len(self.space.bodies)}",
            f"Gravity: {self.space.gravity}",
            f"Threads: {self.space.threads}",
            f"static_lines: {self.static_lines}",
            f"Pygame version: {pygame.version.ver}",
            f"Pymunk version: {pymunk.version}",
            f"window: {pygame.display.get_window_size(), pygame.display.get_current_refresh_rate()}",
            f"Mouse position: {pygame.mouse.get_pos()}",
        ]

        self.guide_text = (
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

        self.help_console_text = (
            "help: display this"
            "\nexec: execute the Python commands contained in the string as opposed to the program text itself."
            "\neval: executes the expression string passed to it as a mandatory argument and returns the result of executing this string."
            "\npython: open a new python thread"
            "\nclear: clears the output console"
        )

    def mouse_get_pos(self):
        mouse_pos = self.world_mouse_pos
        return mouse_pos

    def toolset(self, position):
        shape_mapping = {
            "circle": self.spawn_circle,
            "rectangle": self.spawn_rectangle,
            "triangle": self.spawn_triangle,
            "polyhedron": self.spawn_polyhedron,
            "spam": self.random_spam,
            "human": self.spawn_human
        }

        spawn_func = shape_mapping.get(self.selected_shape)
        if spawn_func:
            try:
                spawn_func(position)
                if ValueError != True:
                    self.sound_spawn.play()
            except Exception as e:
                self.sound_error.play()
                traceback.print_exc()
                self.window_console.add_output_line_to_log("Error while spawning object: " + str(e))

    def toolset_force_field(self):
        self.sound_click_2.play()
        type_mapping = {
            "attraction": self.attraction,
            "repulsion": self.repulsion,
            "ring": self.ring,
        }
        if self.selected_force_field_button is not None:
            force_field_function = type_mapping.get(self.button_text)
            if force_field_function is not None:
                force_field_function()
        return self.selected_force_field

    def random_spam(self, position):
        for i in range(100):
            if random.randrange(0, 15) == 1:
                self.spawn_circle((position[0] + random.randrange(-150, 150), position[1] + random.randrange(-150, 150)))
            if random.randrange(0, 15) == 1:
                self.spawn_rectangle((position[0] + random.randrange(-150, 150), position[1] + random.randrange(-150, 150)))
            if random.randrange(0, 15) == 1:
                self.spawn_triangle((position[0] + random.randrange(-150, 150), position[1] + random.randrange(-150, 150)))
            if random.randrange(0, 15) == 1:
                self.spawn_polyhedron((position[0] + random.randrange(-150, 150), position[1] + random.randrange(-150, 150)))

    def delete_all(self):
        self.sound_error.play()
        global static_lines
        for constr in self.space.constraints:
            self.space.remove(constr)
        for body in self.space.bodies:
            for shape in body.shapes:
                self.space.remove(body, shape)

        for static_body in static_lines:
            self.space.remove(static_body)

    def save_data(self, space, iterations, simulation_frequency, floor_friction, version_save, translation, scaling,
                  static_field, static_body):
        data = (
        space, iterations, simulation_frequency, floor_friction, version_save, translation, scaling, static_field,
        static_body)
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
            self.window_console.add_output_line_to_log("save done!")
            self.sound_save_done.play()
        else:
            print("Отменено сохранение.")
            self.sound_load_error.play()

    def load_data(self):
        root = tk.Tk()
        root.withdraw()
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Newgodoo Save Files", "*.ngsv")]
            )
            if file_path:
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                if len(data) == 9:
                    space, iterations, simulation_frequency, floor_friction, version_save, translation, scaling, static_field, static_body = data
                    print("Загрузка успешна.")
                    self.sound_save_done.play()
                    return space, iterations, simulation_frequency, floor_friction, version_save, translation, scaling, static_field, static_body
                else:
                    print("Неправильный формат данных.")
                    self.sound_load_error.play()
            else:
                print("Отменена загрузка.")
                self.sound_load_error.play()
        except:
            print("Что-то пошло не так")

    def update(self):
        global num_bodies
        if self.running_physics == True:
            num_bodies = len(self.space.bodies)
            dt = 2.0 / self.simulation_frequency
            self.space.step(dt)
            self.space.gravity = self.rotation * 1000, 1000
            self.attraction()
            self.repulsion()
            self.ring()
            self.spiral()
            self.freeze_positions()
            self.object_drag()
            pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), 10, 2)

    def spawn_polyhedron(self, position):
        tooth_angle = 2 * math.pi / int(self.polyhedron_faces_input.get_text())
        radius = float(self.polyhedron_size_input.get_text())
        tooth_radius = radius * 0.4
        points = []
        for i in range(int(self.polyhedron_faces_input.get_text()) * 2):
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
        shape.collision_type = self.COLLTYPE_DEFAULT
        shape.friction = float(self.polyhedron_friction_input.get_text())
        shape.elasticity = float(self.polyhedron_elasticity_input.get_text())
        shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)
        self.space.add(body, shape)

    circle_color_random = True

    def spawn_circle(self, position):
        radius = float(self.circle_radius_input.get_text())
        mass = radius * math.pi / 10
        moment = pymunk.moment_for_circle(
            mass, 0, radius
        )
        body = pymunk.Body(mass, moment)
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.collision_type = self.COLLTYPE_DEFAULT
        shape.friction = float(self.circle_friction_input.get_text())
        shape.elasticity = float(self.circle_elasticity_input.get_text())
        self.space.add(body, shape)
        if self.circle_color_random == True:
            shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)
        else:
            shape.color = (
                int(self.circle_color_red_input.get_current_value()), int(self.circle_color_green_input.get_current_value()),
                int(self.circle_color_blue_input.get_current_value()), 255)

    rectangle_color_random = True

    def spawn_rectangle(self, position):
        size = (float(self.rectangle_size_input_x.get_text()), float(self.rectangle_size_input_y.get_text()))
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
        shape.collision_type = self.COLLTYPE_DEFAULT
        shape.friction = float(self.rectangle_friction_input.get_text())
        shape.elasticity = float(self.rectangle_elasticity_input.get_text())
        self.space.add(body, shape)
        if self.rectangle_color_random == True:
            shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)
        else:
            shape.color = (
            int(self.rectangle_color_red_input.get_current_value()), int(self.rectangle_color_green_input.get_current_value()),
            int(self.rectangle_color_blue_input.get_current_value()), 255)

    def spawn_triangle(self, position):
        tooth_angle = 2 * math.pi / 3
        radius = float(self.triangle_size_input.get_text())
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
        shape.collision_type = self.COLLTYPE_DEFAULT
        shape.friction = float(self.triangle_friction_input.get_text())
        shape.elasticity = float(self.triangle_elasticity_input.get_text())
        shape.color = (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255), 255)
        self.space.add(body, shape)

    def attraction(self):
        if self.creating_attraction:
            if self.draw_force_field_radius == True:
                pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), self.force_field_radius * self.scaling, 2)
            for body in self.space.bodies:

                distance = ((self.world_mouse_pos[0] - body.position.x) ** 2 + (
                        self.world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
                if distance <= self.force_field_radius:
                    force_vector = (
                        (self.world_mouse_pos[0] - body.position[0]) * 2, (self.world_mouse_pos[1] - body.position[1]) * 2)
                    body.velocity = force_vector

    def repulsion(self):
        if self.creating_repulsion:
            if self.draw_force_field_radius == True:
                pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), self.force_field_radius * self.scaling, 2)
            for body in self.space.bodies:
                distance = ((self.world_mouse_pos[0] - body.position.x) ** 2 + (
                        self.world_mouse_pos[1] - body.position.y) ** 2) ** 0.5
                if distance <= self.force_field_radius:
                    force_vector = (
                            (self.world_mouse_pos - body.position).rotated(-body.angle).normalized()
                            * self.force_field_strength
                            * 30
                    )
                    body.apply_force_at_local_point(-force_vector, (0, 0))

    def ring(self):
        global num_bodies, shuffled_bodies
        if self.creating_force_ring:
            if num_bodies == 0:
                return
            angle_increment = 2 * math.pi / num_bodies
            angle = 0

            for body in shuffled_bodies:
                x = self.world_mouse_pos[0] + self.force_field_radius * math.cos(angle)
                y = self.world_mouse_pos[1] + self.force_field_radius * math.sin(angle)

                force_vector = ((x - body.position[0]) * 2, (y - body.position[1]) * 2)
                body.velocity = force_vector

                angle += angle_increment

    def spiral(self):
        if self.creating_force_spiral:
            num_bodies = len(self.space.bodies)
            if num_bodies == 0:
                return

            spiral_radius = 50
            spiral_spacing = self.force_field_radius / 100
            angle_increment = math.pi / 10

            angle = 0

            for body in self.space.bodies:
                x = self.world_mouse_pos[0] + spiral_radius * math.cos(angle)
                y = self.world_mouse_pos[1] + spiral_radius * math.sin(angle)

                force_vector = ((x - body.position[0]) * 2, (y - body.position[1]) * 2)
                body.velocity = force_vector

                spiral_radius += spiral_spacing
                angle += angle_increment

    def freeze_positions(self):
        if self.creating_force_freeze:
            for body in self.space.bodies:
                self.distance = ((self.world_mouse_pos[0] - body.position.x) ** 2 + (
                        self.world_mouse_pos[1] - body.position.y) ** 2) ** 0.5

                angle = math.atan2(self.world_mouse_pos[1] - body.position.y, self.world_mouse_pos[0] - body.position.x)

                tangential_velocity = 0

                velocity_x = tangential_velocity * math.cos(angle + math.pi / 2)
                velocity_y = tangential_velocity * math.sin(angle + math.pi / 2)

                body.velocity = (velocity_x, velocity_y)

    object_dragging = None

    def object_drag(self):
        global object_dragging, key_space
        if key_space == False:
            if object_dragging is not None:
                object_dragging.velocity = (
                    (self.world_mouse_pos[0] - object_dragging.position[0]) * 10,
                    (self.world_mouse_pos[1] - object_dragging.position[1]) * 10)
        else:
            if object_dragging is not None:
                object_dragging.position = self.world_mouse_pos
                object_dragging.velocity = (0, 0)

    def hide_all_windows(self):
        self.window_rectangle.hide()
        self.window_circle.hide()
        self.window_triangle.hide()
        self.window_polyhedron.hide()

        self.strength_slider.hide()
        self.radius_slider.hide()
        self.text_label_radius.hide()
        self.text_label_strength.hide()

    def show_force_field_settings(self):
        self.strength_slider.show()
        self.radius_slider.show()
        self.text_label_radius.show()
        self.text_label_strength.show()

    def vis_pause_icon(self, show):
        global pause_icon_visible
        if show:
            self.pause_icon.show()
            pause_icon_visible = True
            pygame.display.set_caption(self.version + " (simulation paused)")

        else:
            self.pause_icon.hide()
            pause_icon_visible = False
            pygame.display.set_caption(self.version)
    def run(self):
        while self.running:
            self.screen.fill((20, 20, 20))
            time_delta = self.clock.tick(60) / 1000

            # Получить позицию курсора относительно мира игры
            mouse_pos = pymunk.pygame_util.get_mouse_pos(self.screen)

            cursor_pos = pymunk.Vec2d(mouse_pos[0], mouse_pos[1])

            inverse_translation = pymunk.Transform.translation(-self.screen_width / 2, -self.screen_height / 2)
            inverse_rotation = pymunk.Transform.rotation(-self.rotation)
            inverse_scaling = pymunk.Transform.scaling(1 / self.scaling)

            inverse_transform = inverse_scaling @ inverse_rotation @ inverse_translation

            inverse_translation_cam = pymunk.Transform.translation(
                -self.translation.tx, -self.translation.ty
            )

            world_cursor_pos = inverse_transform @ cursor_pos
            world_translation = inverse_translation_cam @ pymunk.Vec2d(0, 0)

            world_mouse_pos = (
                world_cursor_pos.x + world_translation.x + self.screen_width / 2,
                world_cursor_pos.y + world_translation.y + self.screen_height / 2,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.sound_pause.play()
                        self.window_settings.hide()
                        self.key_esc_pressed = not self.key_esc_pressed
                    if event.key == pygame.K_F11:
                        self.sound_close.play()
                        key_f11_pressed = True
                    if event.key == pygame.K_f:
                        key_f_pressed = True
                        key_f_hold_start_time = pygame.time.get_ticks()
                    if event.key == pygame.K_n:
                        self.sound_beep_1.play()
                        if self.selected_force_field_button is not None:
                            if self.selected_force_field_button == self.force_field_buttons[0]:
                                self.creating_attraction = not self.creating_attraction
                            elif self.selected_force_field_button == self.force_field_buttons[1]:
                                self.creating_repulsion = not self.creating_repulsion
                            elif self.selected_force_field_button == self.force_field_buttons[2]:
                                self.creating_force_ring = not self.creating_force_ring
                                self.shuffled_bodies = random.sample(self.space.bodies, self.num_bodies)
                            elif self.selected_force_field_button == self.force_field_buttons[3]:
                                self.creating_force_spiral = not self.creating_force_spiral
                            elif self.selected_force_field_button == self.force_field_buttons[4]:
                                self.creating_force_freeze = not self.creating_force_freeze
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_f:
                            self.toolset(tuple(map(sum, zip(world_mouse_pos, self.camera_offset))))
                            shuffled_bodies = self.space.bodies
                            key_f_pressed = False
                            key_f_hold_start_time = 0
                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                            self.sound_hovering.play()
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            # random color checkbox
                            if event.ui_element == self.rectangle_color_mode_button:
                                self.sound_click_3.play()
                                rectangle_color_random = False
                                self.rectangle_color_mode_checkbox_image.set_image(
                                    new_image=pygame.image.load(self.checkbox_false_texture))
                                rectangle_color_mode = not self.rectangle_color_mode
                                if rectangle_color_mode == True:
                                    self.sound_click_3.play()
                                    rectangle_color_random = True
                                    self.rectangle_color_mode_checkbox_image.set_image(
                                        new_image=pygame.image.load(self.checkbox_true_texture))
                            if event.ui_element == self.circle_color_mode_button:
                                self.sound_click_3.play()
                                circle_color_random = False
                                self.circle_color_mode_checkbox_image.set_image(
                                    new_image=pygame.image.load(self.checkbox_false_texture))
                                self.circle_color_mode = not self.circle_color_mode
                                if self.circle_color_mode == True:
                                    self.sound_click_3.play()
                                    circle_color_random = True
                                    self.circle_color_mode_checkbox_image.set_image(
                                        new_image=pygame.image.load(self.checkbox_true_texture))
                            if event.ui_element == self.save_world_button:
                                self.sound_click.play()
                                self.save_data(self.space, self.space.iterations, self.simulation_frequency, self.floor.friction, self.version_save,
                                          self.translation, self.scaling, self.static_lines, self.static_body)
                            elif event.ui_element == self.load_world_button:
                                self.sound_click.play()
                                loaded_space, iterations, simulation_frequency, floor_friction, version_save, translation, loaded_scaling, static_field, static_body = self.load_data()
                                if loaded_space:
                                    self.space = loaded_space
                                    self.scaling = loaded_scaling
                                    self.space.iterations = iterations
                            elif event.ui_element == self.delete_all_button:
                                self.delete_all()
                            elif event.ui_element in self.force_field_buttons:
                                self.selected_force_field_button = event.ui_element
                                self.toolset_force_field()
                                self.show_force_field_settings()
                            if event.ui_element in self.spawn_buttons:
                                self.sound_click_2.play()
                                selected_spawn_button = event.ui_element
                                if selected_spawn_button == self.spawn_buttons[0]:
                                    self.selected_shape = "circle"
                                    self.hide_all_windows()
                                    self.window_circle.show()
                                elif selected_spawn_button == self.spawn_buttons[1]:
                                    self.selected_shape = "rectangle"
                                    self.hide_all_windows()
                                    self.window_rectangle.show()
                                elif selected_spawn_button == self.spawn_buttons[2]:
                                    self.selected_shape = "triangle"
                                    self.hide_all_windows()
                                    self.window_triangle.show()
                                elif selected_spawn_button == self.spawn_buttons[3]:
                                    self.selected_shape = "polyhedron"
                                    self.hide_all_windows()
                                    self.window_polyhedron.show()
                                elif selected_spawn_button == self.spawn_buttons[4]:
                                    self.selected_shape = "spam"
                                elif selected_spawn_button == self.spawn_buttons[5]:
                                    self.selected_shape = "delete all"
                                elif selected_spawn_button == self.spawn_buttons[6]:
                                    self.selected_shape = "force field"
                                elif selected_spawn_button == self.spawn_buttons[7]:
                                    self.selected_shape = "None"
                                elif selected_spawn_button == self.spawn_buttons[8]:
                                    self.selected_shape = "None"
                                elif selected_spawn_button == self.spawn_buttons[9]:
                                    self.selected_shape = "None"
                                elif selected_spawn_button == self.spawn_buttons[10]:
                                    self.selected_shape = "None"
                                elif selected_spawn_button == self.spawn_buttons[11]:
                                    self.selected_shape = "human"


                        elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element in self.spawn_buttons:
                                self.toolset(tuple(map(sum, zip(world_mouse_pos, self.camera_offset))))
                        elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                            if event.ui_element == self.strength_slider:
                                force_field_strength = int(event.value)
                                self.text_label_strength.set_text(
                                    "Force Field Strength: {}".format(force_field_strength)
                                )
                            elif event.ui_element == self.radius_slider:
                                force_field_radius = int(event.value)
                                self.text_label_radius.set_text(
                                    "Force Field Radius: {}".format(force_field_radius)
                                )

                            elif event.ui_element == self.iterations_slider:
                                self. space.iterations = int(event.value)
                                self.text_iterations.set_text(
                                    "iterations        :{}".format(self.space.iterations)
                                )

                            elif event.ui_element == self.simulation_frequency_slider:
                                simulation_frequency = int(event.value)
                                self.text_simulation_frequency.set_text(
                                    "sim. frequency     :{}".format(simulation_frequency)
                                )

                            elif event.ui_element == self.friction_slider:
                                set_friction = int(event.value)
                                self.text_friction.set_text("friction       :{}".format(set_friction))

                            elif event.ui_element == self.elasticity_slider:
                                set_elasticity = int(event.value)
                                self.text_elasticity.set_text(
                                    "elasticity       :{}".format(set_elasticity)
                                )

                    self.debug_info_labels[0].set_text(f"FPS: {round(self.clock.get_fps())}")
                    self.debug_info_labels[1].set_text(f"Entities: {len(self.space.bodies)}")
                    self.debug_info_labels[2].set_text(f"Gravity: {self.space.gravity}")
                    self.debug_info_labels[3].set_text(f"Threads: {self.space.threads}")
                    self.debug_info_labels[4].set_text(f"static_lines: {static_lines}")  # Update static_lines accordingly
                    self.debug_info_labels[8].set_text(f"Mouse position: {pygame.mouse.get_pos()}")  # Update mouse position

                    if self.key_esc_pressed:
                        self.window_settings.show()
                    if self.key_f11_pressed:
                        self.fullscreen = not self.fullscreen
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                        self.shift_speed = 5
                    if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                        self.shift_speed = 1
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
                        self.shift_speed = 5
                    if event.type == pygame.KEYUP and event.key == pygame.K_RSHIFT:
                        self.shift_speed = 1
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        self.key_z_pressed = True
                        self.key_z_hold_start_time = pygame.time.get_ticks()
                        if self.shift_speed > 1:
                            self.num_bodies -= 1
                            for i in range(5):
                                if self.space.bodies:
                                    last_body = self.space.bodies[-1]
                                    for shape in last_body.shapes:
                                        self.space.remove(shape)
                                        # window_console.add_output_line_to_log("Undo: " + str(shape)[8:])
                                    self.space.remove(last_body)
                                    self.sound_slider.play()
                        else:
                            if self.space.bodies:
                                last_body = self.space.bodies[-1]
                                for shape in last_body.shapes:
                                    self.space.remove(shape)
                                    self.window_console.add_output_line_to_log("Undo: " + str(shape)[8:])
                                self.space.remove(last_body)
                                num_bodies -= 1
                                self.sound_slider.play()
                    if event.type == pygame.KEYUP and event.key == pygame.K_z:
                        key_z_pressed = False
                        key_z_hold_start_time = 0
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                        self.sound_click_3.play()
                        static_field_start = world_mouse_pos
                        creating_static_field = True
                    elif event.type == pygame.KEYUP and event.key == pygame.K_b:
                        self.sound_click_4.play()
                        static_field_end = world_mouse_pos
                        static_field = pymunk.Segment(
                            static_body, static_field_start, static_field_end, 10
                        )
                        static_field.friction = set_friction
                        static_field.elasticity = 0.5
                        try:
                            self.space.add(static_field)
                        except Exception as e:
                            traceback.print_exc()
                            self.window_console.add_output_line_to_log("Error while spawning static: " + str(e))
                        creating_static_field = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DELETE:
                            info = self.space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
                            if info is not None:
                                self.space.remove(info.shape)

                        if event.key == pygame.K_SPACE:
                            self.sound_pause.play()
                            self.vis_pause_icon(show=not pause_icon_visible)
                            running_physics = not running_physics
                            key_space = not key_space

                        elif event.key == pygame.K_l:
                            show_guide = not show_guide
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            pygame.image.save(self.screen, "../screenshot.png")
                            self.window_console.add_output_line_to_log("Screenshot saved!")
                            self.sound_screenshot.play()

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
                        if event.button == 2:
                            center_button = True
                            mouse_x_start_pos, mouse_y_start_pos = world_mouse_pos

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 2:
                            mouse_x_start_pos, mouse_y_start_pos = world_mouse_pos
                            center_button = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            info = self.space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
                            if info is not None:
                                if info.shape.body != static_body:
                                    self.object_dragging = info.shape.body

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            if self.object_dragging is not None:
                                self.object_dragging.is_dragging = False
                                self.object_dragging = None

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        info = self.space.point_query_nearest(world_mouse_pos, 0, pymunk.ShapeFilter())
                        if info is not None:
                            if info.shape.body != static_body:
                                self.context_menu_window.show()
                                self.context_menu_window.set_position(position=event.pos)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            self.target_scaling += 0.1 * self.target_scaling
                        elif event.button == 5:
                            self.target_scaling -= 0.1 * self.target_scaling
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if not self.context_menu_window.rect.collidepoint(event.pos):
                            self.context_menu_window.hide()
                    if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                        selected_button_index = self.context_menu_list.selected_option
                        print(f"Selected button index: {selected_button_index}")

                    if self.center_button or (event.type == pygame.MOUSEMOTION and event.buttons[1] == 1):
                        if event.type == pygame.MOUSEMOTION:
                            self.translation = self.translation.translated(world_mouse_pos[0] - self.mouse_x_start_pos,
                                                                 world_mouse_pos[1] - self.mouse_y_start_pos)

                if self.key_f_pressed:
                    hold_time = pygame.time.get_ticks() - self.key_f_hold_start_time
                    fill_fraction = min(hold_time / self.KEY_HOLD_TIME, 1.0)
                    radius = int(20 * fill_fraction)
                    if hold_time >= 100:
                        pygame.draw.circle(self.screen, (255, 255, 255),
                                           (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] - 20), 20, 1)
                        pygame.draw.circle(self.screen, (255, 255, 255),
                                           (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] - 20), radius, 20)
                    if self.hold_time >= self.KEY_HOLD_TIME:
                        self.toolset(tuple(map(sum, zip(world_mouse_pos, self.camera_offset))))
                if self.key_z_pressed:
                    hold_time = pygame.time.get_ticks() - self.key_z_hold_start_time
                    fill_fraction = min(hold_time / self.KEY_HOLD_TIME, 1.0)
                    radius = int(20 * fill_fraction)
                    if hold_time >= 100:
                        pygame.draw.circle(self.screen, (255, 0, 0),
                                           (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] - 20), 20, 1)
                        pygame.draw.circle(self.screen, (255, 0, 0),
                                           (pygame.mouse.get_pos()[0] + 30, pygame.mouse.get_pos()[1] - 20), radius, 20)
                    if self.hold_time >= self.KEY_HOLD_TIME:
                        if self.shift_speed > 1:
                            self.num_bodies -= 1
                            for i in range(5):
                                if self.space.bodies:
                                    last_body = self.space.bodies[-1]
                                    for shape in last_body.shapes:
                                        try:
                                            self.space.remove(shape)
                                        except Exception as e:
                                            self.window_console.add_output_line_to_log(str(e))
                                    self.space.remove(last_body)
                                    self.sound_slider.play()
                        else:
                            if self.space.bodies:
                                last_body = self.space.bodies[-1]
                                for shape in last_body.shapes:
                                    try:
                                        self.space.remove(shape)
                                    except Exception as e:
                                        self.window_console.add_output_line_to_log(str(e))
                                self.space.remove(last_body)
                                self.num_bodies -= 1
                                self.sound_slider.play()

                self.scaling += (self.target_scaling - self.scaling) * self.smoothness
                translate_speed = 10 * self.shift_speed / self.scaling
                keys = pygame.key.get_pressed()
                left = int(keys[pygame.K_LEFT])
                up = int(keys[pygame.K_UP])
                down = int(keys[pygame.K_DOWN])
                right = int(keys[pygame.K_RIGHT])

                zoom_in = int(keys[pygame.K_EQUALS])
                zoom_out = int(keys[pygame.K_MINUS])
                rotate_left = int(keys[pygame.K_KP_6])
                rotate_right = int(keys[pygame.K_KP_4])

                translation = translation.translated(
                    translate_speed * left - translate_speed * right,
                    translate_speed * up - translate_speed * down,
                )
                self.draw_options.transform = (
                        pymunk.Transform.translation(self.screen_width / 2, self.screen_height / 2)
                        @ pymunk.Transform.scaling(self.scaling)
                        @ translation
                        @ pymunk.Transform.rotation(self.rotation)
                        @ pymunk.Transform.translation(-self.screen_width / 2, -self.screen_height / 2)
                )

                self.scaling *= 1 + (self.zoom_speed * zoom_in - self.zoom_speed * zoom_out)
                self.rotation += self.rotation_speed * rotate_left - self.rotation_speed * rotate_right

                if self.show_guide:
                    self.text_guide_gui.visible = True

                if self.creating_static_field:
                    self.static_field_end = pygame.mouse.get_pos()
                    pygame.draw.line(self.screen, (255, 255, 255), ((static_field_start[0] + self.screen_width) / self.scaling,
                                                               (static_field_start[1] + self.screen_height) / self.scaling),
                                     (pygame.mouse.get_pos()[0],
                                      pygame.mouse.get_pos()[1]), 10)
                # if creating_spring:
                #    spring_end = pygame.mouse.get_pos()
                #    pygame.draw.line(screen, (255, 255, 255), (spring_start[0] - world_translation[0],
                #                                               spring_start[1] - world_translation[1]), spring_end, 10)

                for line in static_lines:
                    body = line.body
                    pv1 = body.position + line.a.rotated(body.angle)
                    pv2 = body.position + line.b.rotated(body.angle)

                self.gui_manager.process_events(event)
                self.gui_manager.update(time_delta)
                self.space.debug_draw(self.draw_options)
                self.gui_manager.draw_ui(self.screen)
                self.update()
                pygame.display.flip()








