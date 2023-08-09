import pygame_gui
import pygame
from core_main import *
class Gui:
    def __init__(self):
        pygame.init()
        self.theme_path = 'theme.json'
        self.gui_manager = pygame_gui.UIManager((self.screen_width, self.screen_height), self.theme_path)
    def Gui(self):

        self.force_field_button_positions = [
            (self.screen_width - 135, self.screen_height - 500 + (50 + 1) * i) for i in range(5)
        ]

        for i, pos in enumerate(self.force_field_button_positions):
            image_rect = pygame.Rect(pos[0] - 50, pos[1] + 1, 47, 47)
            button_rect = pygame.Rect(pos, (110, 50))
            button_text = ""
            if i == 0:
                button_text = "attraction"
            elif i == 1:
                button_text = "repulsion"
            elif i == 2:
                button_text = "ring"
            elif i == 3:
                button_text = "spiral"
            elif i == 4:
                button_text = "freeze"
            image = pygame_gui.elements.UIImage(
                relative_rect=image_rect,
                image_surface=pygame.image.load(self.image_force_field_paths[i]),
                manager=self.gui_manager
            )
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect, text=button_text, manager=self.gui_manager
            )
            self.force_field_buttons.append(button)
            self.force_field_images.append(image)
        self.selected_force_field_button = self.force_field_buttons[0]

        self.spawn_button_positions = [
            (10, 10 + (50 + 1) * i) for i in range(5)
        ]
        for i, pos in enumerate(self.spawn_button_positions):
            image_rect = pygame.Rect(pos[0] + 118, pos[1] + 2, 45, 45)
            button_rect = pygame.Rect(pos, (115, 50))
            button_text = ""
            if i == 0:
                button_text = "Circle"
            elif i == 1:
                button_text = "rectangle"
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
                relative_rect=button_rect, text=button_text, manager=self.gui_manager
            )
            image = pygame_gui.elements.UIImage(
                relative_rect=image_rect,
                image_surface=pygame.image.load(self.image_spawn_paths[i]),
                manager=self.gui_manager
            )
            self.spawn_buttons.append(button)
        self.selected_spawn_button = None

        self.window_console = pygame_gui.windows.UIConsoleWindow(
            pygame.Rect(1500, self.screen_height-200, 800, 210),
            manager=self.gui_manager,
        )
        
        #SETTINGS######################################################################################
        window_settings = pygame_gui.elements.UIWindow(
            pygame.Rect(200, 10, 800, 600),
            manager=self.gui_manager,
            window_display_title="Settings"
        )
        window_settings.hide()
        
        self.resolution_options = ["800x600", "1024x768", "1280x720", "1920x1080"]
        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.resolution_options,
            starting_option="800x600",
            relative_rect=pygame.Rect(50, 50, 150, 30),
            manager=self.gui_manager,
            container=window_settings
        )

        options_list = [f"option {x}" for x in range(20)]
        self.dropdown = pygame_gui.elements.UIDropDownMenu(options_list, "option 0", relative_rect=pygame.Rect(50, 50, 400, 50),
                                  manager=self.gui_manager, expansion_height_limit=100, container=window_settings)

        self.hertz_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(50, 100, 150, 30),
            start_value=60,
            value_range=(30, 144),
            manager=self.gui_manager,
            container=window_settings
        )

        theme_options = ["theme_light.json", "theme_dark.json", "theme_custom.json"]
        self.theme_dropdown = pygame_gui.elements.UIDropDownMenu(theme_options, "option 0", relative_rect=pygame.Rect(50, 200, 400, 50),
                                  manager=self.gui_manager, container=window_settings, expansion_height_limit=100)
        
        
        #FORCE_FIELD######################################################################################
        self.strength_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(400, 10, 200, 20),
            start_value=self.force_field_strength,
            value_range=(0, 5000),
            manager=self.gui_manager,
        )
        
        self.text_label_strength = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(380, 10, 250, 50),
            text="force field strength: {}".format(self.force_field_strength),
            manager=self.gui_manager,
        )
        
        self.radius_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(400, 40, 200, 20),
            start_value=self.force_field_radius,
            value_range=(0, 10000),
            manager=self.gui_manager,
        )
        
        self.text_label_radius = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(400, 40, 200, 50),
            text="force field radius: {}".format(self.force_field_radius),
            manager=self.gui_manager,
        )
        
        
        #rectangle######################################################################################
        self.window_rectangle = pygame_gui.elements.UIWindow(
            pygame.Rect(200, 10, 400, 300),
            manager=self.gui_manager,
            window_display_title="rectangle settings"
        )
        self.rectangle_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(215, 5, 50, 50),
            image_surface=pygame.image.load(self.image_spawn_paths[1]),
            container=self.window_rectangle,
            manager=self.gui_manager
        )
        self.rectangle_size_input_x = pygame_gui.elements.UITextEntryLine(
            initial_text=str(self.set_rectangle_size[0]),
            relative_rect=pygame.Rect(30, 10, 100, 20),
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.text_rectangle_size_x = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 20, 20),
            text="X:",
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.rectangle_size_input_y = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(30, 30, 100, 20),
            initial_text=str(self.set_rectangle_size[1]),
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        
        self.text_rectangle_size_y = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 30, 20, 20),
            text="Y:",
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.rectangle_friction_input = pygame_gui.elements.UITextEntryLine(
            initial_text=str(self.set_friction),
            relative_rect=pygame.Rect(80, 55, 100, 20),
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.text_rectangle_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 55, 80, 20),
            text="friction:",
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.rectangle_elasticity_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(90, 75, 105, 20),
            initial_text=str(self.set_elasticity),
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        self.rectangle_text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 75, 85, 20),
            text="elasticity:",
            container=self.window_rectangle,
            manager=self.gui_manager,
        )
        
        
        self.rectangle_color = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(5, 100, self.window_rectangle.get_relative_rect().width-45, 130),
            manager=self.gui_manager,
            container=self.window_rectangle,
        )
        
        
        
        self.rectangle_color_red_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 10, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            manager=self.gui_manager,
            container=self.rectangle_color,
        )
        self.text_rectangle_red_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 10, 85, 20),
            text="Red:",
            container=self.rectangle_color,
            manager=self.gui_manager,
        )
        
        self.rectangle_color_green_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 30, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            container=self.rectangle_color,
            manager=self.gui_manager,
        )
        
        self.text_rectangle_green_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 30, 85, 20),
            text="Green:",
            container=self.rectangle_color,
            manager=self.gui_manager,
        )
        
        self.rectangle_color_blue_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 50, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            container=self.rectangle_color,
            manager=self.gui_manager,
        )
        self.text_rectangle_blue_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 50, 85, 20),
            text="Blue:",
            container=self.rectangle_color,
            manager=self.gui_manager,
        )
        
        
        
        
        self.rectangle_color_mode = True
        self.rectangle_color_mode_checkbox = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(5, 75, 130, 45),
            manager=self.gui_manager,
            container=self.rectangle_color,
        )
        self.rectangle_color_mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(-1, -1, 85, 40),
            manager=self.gui_manager,
            container=self.rectangle_color_mode_checkbox,
            text="random"
        )
        self.rectangle_color_mode_checkbox_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(self.rectangle_color_mode_button.get_relative_rect().width, 2, 35, 35),
            image_surface=pygame.image.load(self.checkbox_true_texture),
            container=self.rectangle_color_mode_checkbox,
            manager=self.gui_manager
        )
        
        #CIRCLE######################################################################################
        self.window_circle = pygame_gui.elements.UIWindow(
            pygame.Rect(200, 10, 400, 300),
            manager=self.gui_manager,
            window_display_title="circle settings"
        )
        
        self.circle_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(215, 5, 50, 50),
            image_surface=pygame.image.load(self.image_spawn_paths[0]),
            container=self.window_circle,
            manager=self.gui_manager
        )
        self.circle_radius_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(30, 10, 100, 20),
            initial_text=str(self.set_circle_radius),
            container=self.window_circle,
            manager=self.gui_manager,
        )
        text_circle_radius = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 20, 20),
            text="R:",
            container=self.window_circle,
            manager=self.gui_manager,
        )
        self.circle_friction_input = pygame_gui.elements.UITextEntryLine(
            initial_text=str(self.set_friction),
            relative_rect=pygame.Rect(80, 55, 100, 20),
            container=self.window_circle,
            manager=self.gui_manager,
        )
        self.text_circle_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 55, 80, 20),
            text="friction:",
            container=self.window_circle,
            manager=self.gui_manager,
        )
        self.circle_elasticity_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(90, 75, 105, 20),
            initial_text=str(self.set_elasticity),
            container=self.window_circle,
            manager=self.gui_manager,
        )
        self.circle_text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 75, 85, 20),
            text="elasticity:",
            container=self.window_circle,
            manager=self.gui_manager,
        )
        
        
        self.circle_color = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(5, 100, self.window_rectangle.get_relative_rect().width-45, 130),
            manager=self.gui_manager,
            container=self.window_circle,
        )
        self.circle_color_red_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 10, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            manager=self.gui_manager,
            container=self.circle_color,
        )
        self.text_circle_red_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 10, 85, 20),
            text="Red:",
            container=self.circle_color,
            manager=self.gui_manager,
        )
        
        self.circle_color_green_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 30, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            container=self.circle_color,
            manager=self.gui_manager,
        )
        
        self.text_circle_green_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 30, 85, 20),
            text="Green:",
            container=self.circle_color,
            manager=self.gui_manager,
        )
        
        self.circle_color_blue_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(90, 50, 150, 20),
            start_value=self.force_field_radius,
            value_range=(0, 255),
            container=self.circle_color,
            manager=self.gui_manager,
        )
        self.text_circle_blue_color = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 50, 85, 20),
            text="Blue:",
            container=self.circle_color,
            manager=self.gui_manager,
        )
        
        
        
        
        self.circle_color_mode = True
        self.circle_color_mode_checkbox = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(5, 75, 130, 45),
            manager=self.gui_manager,
            container=self.circle_color,
        )
        self.circle_color_mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(-1, -1, 85, 40),
            manager=self.gui_manager,
            container=self.circle_color_mode_checkbox,
            text="random"
        )
        self.circle_color_mode_checkbox_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(self.circle_color_mode_button.get_relative_rect().width, 2, 35, 35),
            image_surface=pygame.image.load(self.checkbox_true_texture),
            container=self.circle_color_mode_checkbox,
            manager=self.gui_manager
        )
        #TRIANGLE##########################################
        self.window_triangle = pygame_gui.elements.UIWindow(
            pygame.Rect(200, 10, 400, 300),
            manager=self.gui_manager,
            window_display_title="triangle settings"
        )
        self.triangle_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(215, 5, 50, 50),
            image_surface=pygame.image.load(self.image_spawn_paths[2]),
            container=self.window_triangle,
            manager=self.gui_manager
        )
        self.triangle_size_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(60, 10, 100, 20),
            container=self.window_triangle,
            initial_text=str(self.set_triangle_size),
            manager=self.gui_manager,
        )
        self.text_triangle_size = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 50, 20),
            text="Size:",
            container=self.window_triangle,
            manager=self.gui_manager,
        )
        
        self.triangle_friction_input = pygame_gui.elements.UITextEntryLine(
            initial_text=str(self.set_friction),
            relative_rect=pygame.Rect(80, 55, 100, 20),
            container=self.window_triangle,
            manager=self.gui_manager,
        )
        self.text_triangle_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 55, 80, 20),
            text="friction:",
            container=self.window_triangle,
            manager=self.gui_manager,
        )
        self.triangle_elasticity_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(90, 75, 105, 20),
            initial_text=str(self.set_elasticity),
            container=self.window_triangle,
            manager=self.gui_manager,
        )
        self.triangle_text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 75, 85, 20),
            text="elasticity:",
            container=self.window_triangle,
            manager=self.gui_manager,
        )
        
        #POLYHENDRON##########################################################
        self.window_polyhedron = pygame_gui.elements.UIWindow(
            pygame.Rect(200, 10, 400, 300),
            manager=self.gui_manager,
            window_display_title="polyhedron settings"
        )
        self.polyhedron_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(215, 5, 50, 50),
            image_surface=pygame.image.load(self.image_spawn_paths[3]),
            container=self.window_polyhedron,
            manager=self.gui_manager
        )
        self.polyhedron_size_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(60, 10, 100, 20),
            container=self.window_polyhedron,
            initial_text=str(self.set_polyhedron_size),
            manager=self.gui_manager,
        )
        self.text_polyhedron_size = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 50, 20),
            text="Size:",
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        self.polyhedron_faces_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(60, 30, 100, 20),
            container=self.window_polyhedron,
            initial_text=str(self.set_number_faces),
            manager=self.gui_manager,
        )
        self.text_faces_size = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 30, 50, 20),
            text="Faces:",
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        
        self.polyhedron_friction_input = pygame_gui.elements.UITextEntryLine(
            initial_text=str(self.set_friction),
            relative_rect=pygame.Rect(80, 55, 100, 20),
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        self.text_polyhedron_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 55, 80, 20),
            text="friction:",
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        self.polyhedron_elasticity_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(90, 75, 105, 20),
            initial_text=str(self.set_elasticity),
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        self.polyhedron_text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(5, 75, 85, 20),
            text="elasticity:",
            container=self.window_polyhedron,
            manager=self.gui_manager,
        )
        # OTHER_GUI######################################################################################
        self.text_guide_gui = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(self.screen_width - 280, 150, 240, 300),
            html_text=self.guide_text,
            visible=self.show_guide,
            manager=self.gui_manager,
        )
        self.text_guide_gui.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        
        self.iterations_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width - 250, self.screen_height - 30, 200, 20),
            start_value=self.set_rectangle_size[0],
            value_range=(1, 128),
            manager=self.gui_manager,
        )
        self.text_iterations = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width - 260, self.screen_height - 30, 300, 20),
            text="iterations        :{}".format(self.space.iterations),
            manager=self.gui_manager,
        )
        self.simulation_frequency_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width - 250, self.screen_height - 60, 200, 20),
            start_value=self.set_rectangle_size[0],
            value_range=(1, 300),
            manager=self.gui_manager,
        )
        self.text_simulation_frequency = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width - 260, self.screen_height - 60, 300, 20),
            text="sim. frequency     :{}".format(self.simulation_frequency),
            manager=self.gui_manager,
        )
        
        self.pause_icon_image = pygame.image.load("sprites/gui/pause.png").convert_alpha()
        self.pause_icon_rect = pygame.Rect(self.screen_width - 450, 10, 50, 50)
        
        self.pause_icon = pygame_gui.elements.UIImage(
            relative_rect=self.pause_icon_rect,
            image_surface=self.pause_icon_image,
            manager=self.gui_manager
        )
        
        
        # FRICTION######################################################################
        self.friction_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(200, 50, 200, 20),
            start_value=self.set_rectangle_size[0],
            value_range=(0.01, 10),
            manager=self.gui_manager,
        )
        self.text_friction = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width - 260, self.screen_height - 90, 300, 20),
            text="friction     :{}".format(self.set_friction),
            manager=self.gui_manager,
        )
        # elasticity@#####################################################################
        self.elasticity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(self.screen_width - 250, self.screen_height - 120, 200, 20),
            start_value=self.set_rectangle_size[0],
            value_range=(0.01, 10),
            manager=self.gui_manager,
        )
        self.text_elasticity = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.screen_width - 260, self.screen_height - 120, 300, 20),
            text="elasticity     :{}".format(self.set_friction),
            manager=self.gui_manager,
        )
        #SAVE/LOAD BUTTONS#####################################################################
        self.save_world_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.screen_width - 135, 10, 125, 40),
                text="Save World",
                manager=self.gui_manager
        )
        self.load_world_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.screen_width - 135, 60, 125, 40),
                text="Load World",
                manager=self.gui_manager
        )
        #DELETE_ALL_BUTTON##########################################################################
        self.delete_all_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(10, self.screen_height-50, 125, 40),
                text="Delete all",
                manager=self.gui_manager
        )
        self.pause_icon.hide()