import pygame
import pymunk
from random import *
import pygame_gui
import random
from pymunk import Vec2d
import math
import pymunk.pygame_util
import pickle
import tkinter as tk
from tkinter import filedialog


guide_text = "L: show this guide" \
             "\nF: Spawn object" \
             "\nB: Make border" \
             "\nN: Enable gravity field" \
             "\nSPACE: Pause physic" \
             "\nArrow keys: camera position" \
             "\nA/Z: Camera zoom" \
             "\nS/X: Camera roll" \
             "\nP: Screenshot" \
             "\nI: Save current world" \
             "\nO: Load World"

debug_info = "'FPS: ' + (str(round(clock.get_fps()))) +'\nEntities: ' + (str(len(space.bodies))) +'\nGravity: ' + (str(len(space.gravity))) +'\nThreads: ' + (str(round(space.threads)))"


space = pymunk.Space()
space.threads = 2
space.iterations = 30
pygame.init()
pygame.display.set_caption('PhysicsGame')

class PhysicsGame:
    def __init__(self):
        self.show_guide = True
        self.running_physics = True

        self.COLLTYPE_DEFAULT = 0
        self.mouse_pos = self.mouse_get_pos()
        self.screen_width, self.screen_height = 1920, 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.simulation_frequency = 60
        self.static_body = space.static_body
        self.floor = pymunk.Segment(self.static_body, (0, self.screen_height - 100), (self.screen_width, self.screen_height - 100), 0)
        self.floor.friction = 1.0
        space.add(self.floor)

        self.objects = []
        self.static_lines = []
        self.line_point1 = None
        self.selected_shape = None
        self.camera_offset = Vec2d(0, 0)

        self.camera_dragging = False
        self.camera_drag_start = (0, 0)

        self.f1 = pygame.font.Font(None, 35)
        self.f2 = pygame.font.Font(None, 25)

        self.static_field_start = (0, 0)
        self.static_field_end = (0, 0)
        self.creating_static_field = False
        self.creating_force_field = False
        self.force_field_strength = 5000  # Сила притяжения поля
        self.force_field_radius = 500  # Радиус действия поля

        # Инициализация GUI Manager
        self.gui_manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.spawn_buttons = []
        self.spawn_button_width = 120
        self.spawn_button_height = 50
        self.button_x = 10
        self.button_y = 10
        self.button_spacing = 10
        self.X, self.Y = 0, 1

        self.set_elasticity = 0
        self.set_square_size = [30, 30]
        self.set_circle_radius = 30
        self.set_friction = 0.7

        self.segment_length = 50
        self.segment_thickness = 2
        self.segment_color = pygame.Color('white')

        running_physics = True
        self.translate_speed = 10
        self.zoom_speed = 0.01
        self.rotation_speed = 0.01
        self.scaling = 1
        self.rotation = 0
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.translation = pymunk.Transform()

        self.dragging_body = None
        self.mouse_joint = None
        self.running = True
        self.guide = self.f2.render(str(guide_text), True, (180, 180, 0))
        space.sleep_time_threshold = 0.5
        self.keys = pygame.key.get_pressed()
        self.left = int(self.keys[pygame.K_LEFT])
        self.up = int(self.keys[pygame.K_UP])
        self.down = int(self.keys[pygame.K_DOWN])
        self.right = int(self.keys[pygame.K_RIGHT])

        self.zoom_in = int(self.keys[pygame.K_a])
        self.zoom_out = int(self.keys[pygame.K_z])
        self.rotate_left = int(self.keys[pygame.K_s])
        self.rotate_right = int(self.keys[pygame.K_x])
        self.translation = self.translation.translated(
            self.translate_speed * self.left - self.translate_speed * self.right,
            self.translate_speed * self.up - self.translate_speed * self.down,
        )

        self.spawn_button_positions = [(self.button_x, self.button_y + (self.spawn_button_height + self.button_spacing) * i) for i in range(11)]
        for i, pos in enumerate(self.spawn_button_positions):
            button_rect = pygame.Rect(pos, (self.spawn_button_width, self.spawn_button_height))
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
            if self.selected_shape == button_text.lower():
                button_text += " (selected)"
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=button_text,
                manager=self.gui_manager
            )
            self.spawn_buttons.append(button)
        #FORCE_FIELD######################################################################################
        strength_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(350, 10, 200, 20),
            start_value=self.force_field_strength,
            value_range=(0, 50000),
            manager=self.gui_manager
        )

        text_label_strength = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(330, 10, 250, 50),
            text="force field strength: {}".format(self.force_field_strength),
            manager=self.gui_manager
        )

        radius_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(350, 40, 200, 20),
            start_value=self.force_field_radius,
            value_range=(0, 1000),
            manager=self.gui_manager
        )

        text_label_radius = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(350, 40, 200, 50),
            text="force field radius: {}".format(self.force_field_radius),
            manager=self.gui_manager
        )

        #SQUARE######################################################################################
        square_size_slider_x = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 70, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(1, 1000),
            manager=self.gui_manager
        )

        text_square_size_x = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 55, 600, 50),
            text="square X        :{}".format(self.set_square_size[0]),
            manager=self.gui_manager
        )
        square_size_slider_y = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 100, 200, 20),
            start_value=self.set_square_size[1],
            value_range=(1, 1000),
            manager=self.gui_manager
        )

        text_square_size_y = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 85, 600, 50),
            text="square Y        :{}".format(self.set_square_size[1]),
            manager=self.gui_manager
        )
        #CIRCLE######################################################################################
        circle_radius_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(150, 10, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(1, 100),
            manager=self.gui_manager
        )
        text_circle_radius = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(150, 10, 200, 50),
            text="Circle R: {}".format(self.set_circle_radius),
            manager=self.gui_manager
        )


        #OTHER_GUI######################################################################################
        text_guide_gui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width-300, self.screen_height/2, 200, 200),
            text=guide_text,
            manager=self.gui_manager
        )
        iterations_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width-250, self.screen_height-30, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(1, 128),
            manager=self.gui_manager
        )
        text_iterations = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width-260, self.screen_height-30, 300, 20),
            text="iterations        :{}".format(space.iterations),
            manager=self.gui_manager
        )
        simulation_frequency_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width-250, self.screen_height-60, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(1, 300),
            manager=self.gui_manager
        )
        text_simulation_frequency = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width-260, self.screen_height-60, 300, 20),
            text="sim. frequency     :{}".format(self.simulation_frequency),
            manager=self.gui_manager
        )
        #FRICTION######################################################################
        friction_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width-250, self.screen_height-90, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(0.01, 10),
            manager=self.gui_manager
        )
        text_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width-260, self.screen_height-90, 300, 20),
            text="friction     :{}".format(self.set_friction),
            manager=self.gui_manager
        )
        #elasticity@#####################################################################
        elasticity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width-250, self.screen_height-120, 200, 20),
            start_value=self.set_square_size[0],
            value_range=(0.01, 10),
            manager=self.gui_manager
        )
        text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width-260, self.screen_height-120, 300, 20),
            text="elasticity     :{}".format(self.set_friction),
            manager=self.gui_manager
        )
        tooltip = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(self.screen_width-280, 150, 240, 300),
            html_text =guide_text,
            visible=self.show_guide,
            manager=self.gui_manager
        )




        self.selected_button = None

    def flipy(y):
        """Small hack to convert chipmunk physics to pygame coordinates"""
        return -y + 600

    def mouse_get_pos(self):
        self.mouse_pos = pymunk.pygame_util.get_mouse_pos(space)
        self.mouse_pos -= self.camera_offset  # Учитываем смещение камеры
        self.mouse_pos = self.mouse_pos.rotated(-self.rotation)  # Учитываем поворот
        self.mouse_pos /= self.scaling  # Учитываем зум
        return self.mouse_pos

    def toolset(self, position):
        shape_mapping = {
            "circle": self.spawn_circle,
            "square": self.spawn_square,
            "triangle": self.spawn_triangle,
            "random": self.spawn_random,
            "spam": self.random_spam
        }

        self.spawn_func = shape_mapping.get(self.selected_shape)
        if self.spawn_func:
            self.spawn_func(position)

    def random_spam(self, position):
        for i in range(100):
            if random.randrange(0,15) == 1:
                self.spawn_circle(position)
            if random.randrange(0,15) == 1:
                self.spawn_square(position)
            if random.randrange(0,15) == 1:
                self.spawn_triangle(position)

    def spawn_random(self, position):
        shape_type = random.choice(["circle", "square", "triangle"])
        self.toolset(position, shape_type)

    def delete_all(self, position):
        for self.body, self.shape in self.objects:
            space.remove(self.body, self.shape)
        self.objects.clear()

    def spawn_circle(self, position):
        self.radius = self.set_circle_radius
        self.mass = self.set_circle_radius/10
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)  # Calculate moment of inertia for a circle
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = self.COLLTYPE_DEFAULT
        self.shape.friction = self.set_friction
        self.add_body_shape(self.body, self.shape)

    def spawn_square(self, position):
        self.size = self.set_square_size
        self.points = [(-self.size[0], -self.size[1]), (-self.size[0], self.size[1]), (self.size[0], self.size[1]), (self.size[0], -self.size[1])]
        self.mass = (self.set_square_size[0] * self.set_square_size[1]) / 200
        self.moment = pymunk.moment_for_box(self.mass, (2*self.size[0], 2*self.size[1]))  # Calculate moment of inertia for a square
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = position
        self.shape = pymunk.Poly(self.body, self.points)
        self.shape.collision_type = self.COLLTYPE_DEFAULT
        self.shape.friction = self.set_friction
        self.shape.elasticity = self.set_elasticity
        self.add_body_shape(self.body, self.shape)

    def spawn_triangle(self, position):
        self.size = random.randrange(10, 40)
        self.points = [(0, 0), (-self.size, -self.size), (self.size, -self.size)]
        self.mass = 1
        self.moment = pymunk.moment_for_poly(self.mass, self.points)  # Calculate moment of inertia for an isosceles triangle
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = position
        self.shape = pymunk.Poly(self.body, self.points)
        self.shape.collision_type = self.COLLTYPE_DEFAULT
        self.shape.friction = self.set_friction
        self.add_body_shape(self.body, self.shape)


    def add_body_shape(self, body, shape):
        space.add(body, shape)
        self.objects.append((body, shape))


    def force_field_update(self):
        for self.body, self.shape in self.objects:
            self.mouse_pos = pymunk.pygame_util.get_mouse_pos(space) - self.camera_offset
            distance = self.mouse_pos.get_distance(self.body.position)
            if distance <= self.force_field_radius:
                if self.creating_force_field and self.shape.point_query(self.mouse_get_pos()):
                    pygame.draw.circle(self.screen, (100, 0, 0), self.mouse_pos, self.force_field_radius, 2)
                    force_vector = (self.mouse_get_pos() - self.body.position).rotated(-self.body.angle).normalized() * self.force_field_strength
                    self.body.apply_force_at_local_point(force_vector, (0, 0))

    def update(self):
        if self.running_physics == True:
            space.step(self.dt)
            self.force_field_update()
            pygame.draw.circle(self.screen, (255, 255, 255), (self.mouse_pos[0] * self.scaling, self.mouse_pos[1] + self.translation[1]), 20, 2)


    def save_data(data):
        root = tk.Tk()
        root.withdraw()  # Скрыть основное окно tkinter

        # Открыть диалоговое окно проводника для выбора пути сохранения и имени файла
        file_path = filedialog.asksaveasfilename(defaultextension=".pickle",
                                                 filetypes=[("Pickle files", "*.pickle")])

        # Если путь и имя файла выбраны
        if file_path:
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
            print("Сохранение успешно.")
        else:
            print("Отменено сохранение.")


    # Функция для загрузки данных
    def load_data(self):
        root = tk.Tk()
        root.withdraw()  # Скрыть основное окно tkinter

        # Открыть диалоговое окно проводника для выбора файла
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pickle")])

        # Если файл выбран
        if file_path:
            with open(file_path, "rb") as f:
                data = pickle.load(f)
            print("Загрузка успешна.")
            return data
        else:
            print("Отменена загрузка.")
            return None



    def run(self):
        while True:
            self.time_delta = self.clock.tick(60)



            # to zoom with center of screen as origin we need to offset with
            # center of screen, scale, and then offset back


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Обработка событий GUI Manager
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element in self.spawn_buttons:
                            selected_button = event.ui_element
                            if selected_button == self.spawn_buttons[0]:
                                self.selected_shape = "circle"
                            elif selected_button == self.spawn_buttons[1]:
                                self.selected_shape = "square"
                            elif selected_button == self.spawn_buttons[2]:
                                self.selected_shape = "triangle"
                            elif selected_button == self.spawn_buttons[3]:
                                self.selected_shape = "random"
                            elif selected_button == self.spawn_buttons[4]:
                                self.selected_shape = "spam"
                            elif selected_button == self.spawn_buttons[5]:
                                self.selected_shape = "delete all"
                                self.delete_all(0)
                            elif selected_button == self.spawn_buttons[6]:
                                self.selected_shape = "force field"
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element in self.spawn_buttons:
                            self.toolset(tuple(map(sum, zip(pymunk.pygame_util.get_mouse_pos(self.draw_options.surface), self.camera_offset))))
                    elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        if event.ui_element == self.strength_slider:
                            force_field_strength = int(event.value)
                            self.text_label_strength.set_text("Force Field Strength: {}".format(force_field_strength))
                        elif event.ui_element == self.radius_slider:
                            force_field_radius = int(event.value)
                            self.text_label_radius.set_text("Force Field Radius: {}".format(force_field_radius))

                        elif event.ui_element == self.square_size_slider_x:
                            self.set_square_size[0] = int(event.value)
                            self.text_square_size_x.set_text("square X        :{}".format(self.set_square_size[0]))
                        elif event.ui_element == self.square_size_slider_y:
                            self.set_square_size[1] = int(event.value)
                            self.text_square_size_y.set_text("square Y        :{}".format(self.set_square_size[1]))

                        elif event.ui_element == self.circle_radius_slider:
                            set_circle_radius = int(event.value)
                            self.text_circle_radius.set_text("Circle R: {}".format(set_circle_radius))

                        elif event.ui_element == self.iterations_slider:
                            space.iterations = int(event.value)
                            self.text_iterations.set_text("iterations        :{}".format(space.iterations))

                        elif event.ui_element == self.simulation_frequency_slider:
                            simulation_frequency = int(event.value)
                            self.text_simulation_frequency.set_text("sim. frequency     :{}".format(simulation_frequency))

                        elif event.ui_element == self.friction_slider:
                            set_friction = int(event.value)
                            self.text_friction.set_text("friction       :{}".format(set_friction))

                        elif event.ui_element == self.elasticity_slider:
                            set_elasticity = int(event.value)
                            self.text_elasticity.set_text("elasticity       :{}".format(set_elasticity))


                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging_body = None
                    elif event.button == 2:
                        self.camera_dragging = False


                # Обработка событий клавиатуры
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running_physics = not self.running_physics
                    elif event.key == pygame.K_f:
                        self.toolset(tuple(map(sum, zip((pymunk.pygame_util.get_mouse_pos(space)), self.camera_offset))))
                    elif event.key == pygame.K_n:
                        self.creating_force_field = not self.creating_force_field
                    elif event.key == pygame.K_l:
                        self.show_guide = not self.show_guide
                    elif event.type == pygame.K_b:
                        print("создается барьер")
                        if self.creating_static_field:
                            # Создание статического поля между точками
                            static_field = pymunk.Segment(self.static_body, self.static_field_start, self.static_field_end, 10)
                            self.static_field.friction = 1.0
                            space.add(static_field)
                            self.creating_static_field = False
                        else:
                            # Начало создания статического поля
                            self.static_field_start = pymunk.pygame_util.get_mouse_pos(space)
                            self.creating_static_field = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pygame.image.save(self.screen, "screenshot.png")

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                        self.save_data(space)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                        loaded_data = self.load_data()
                        if loaded_data:
                            space = loaded_data

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        if self.line_point1 is None:
                            line_point1 = Vec2d(event.pos[self.X], self.flipy(event.pos[self.Y]))
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        if self.line_point1 is not None:

                            line_point2 = Vec2d(event.pos[self.X], self.flipy(event.pos[self.Y]))
                            shape = pymunk.Segment(
                                space.static_body, line_point1, line_point2, 0.0
                            )
                            shape.friction = 0.99
                            space.add(shape)
                            self.static_lines.append(shape)
                            line_point1 = None

                # Обработка событий мыши
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        self.camera_dragging = True
                        self.camera_drag_start = None
                        # Другие обработчики событий мыши


                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        camera_dragging = False




            self.draw_options.transform = (
                    pymunk.Transform.translation(300, 300)
                    @ pymunk.Transform.scaling(self.scaling)
                    @ self.translation
                    @ pymunk.Transform.rotation(self.rotation)
                    @ pymunk.Transform.translation(-300, -300)
            )
            mouse_pos = pymunk.pygame_util.get_mouse_pos(self.screen)

            self.scaling *= 1 + (self.zoom_speed * self.zoom_in - self.zoom_speed * self.zoom_out)

            self.rotation += self.rotation_speed * self.rotate_left - self.rotation_speed * self.rotate_right
            # Отрисовка
            self.screen.fill((0, 0, 0))

           # fps_debug = f1.render('FPS: ' + (str(round(clock.get_fps()))) +
           #                       '\nEntities: ' + (str(len(space.bodies))) +
           #                       '\nGravity: ' + (str(len(space.gravity))) +
           #                       '\nThreads: ' + (str(round(space.threads))), True, (180, 0, 0))
           # screen.blit(fps_debug, (screen_width - 300, 10))
           # if show_guide == True:
           #     screen.blit(self.guide, (screen_width - 300, 200))


            if self.creating_static_field:
                self.static_field_end = pymunk.pygame_util.get_mouse_pos(space)
                pygame.draw.line(self.screen, (255, 255, 255), self.static_field_start, self.static_field_end)

            #if self.line_point1 is not None:
            #    p1 = int(self.line_point1.x), int(self.flipy(line_point1.y))
            #    p2 = self.mouse_pos.x, self.flipy(mouse_pos.y)
            #    pygame.draw.lines(screen, pygame.Color("black"), False, [p1, p2])

            for line in self.static_lines:
                body = line.body

                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                p1 = int(pv1.x), int(self.flipy(pv1.y))
                p2 = int(pv2.x), int(self.flipy(pv2.y))
                pygame.draw.lines(self.screen, pygame.Color("lightgray"), False, [p1, p2])
            space.gravity = self.rotation*3000, 1000
            self.dt = 1.0 / self.simulation_frequency
            if self.running_physics == True:
                space.step(self.dt)
            # Обновление GUI Manager
            self.gui_manager.process_events(event)
            self.gui_manager.update(self.time_delta)
            self.update()
            # Отрисовка GUI Manager
            space.debug_draw(self.draw_options)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    app = PhysicsGame()
    app.run()
