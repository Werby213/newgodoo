import pygame_gui.elements as pgui_elements
import pygame
def create_force_field_elements(gui_manager, force_field_strength, force_field_radius):
    strength_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(350, 10, 200, 20),
        start_value=force_field_strength,
        value_range=(0, 5000),
        manager=gui_manager,
    )

    text_label_strength = pgui_elements.UILabel(
        relative_rect=pygame.Rect(330, 10, 250, 50),
        text="force field strength: {}".format(force_field_strength),
        manager=gui_manager,
    )

    radius_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(350, 40, 200, 20),
        start_value=force_field_radius,
        value_range=(0, 1000),
        manager=gui_manager,
    )

    text_label_radius = pgui_elements.UILabel(
        relative_rect=pygame.Rect(350, 40, 200, 50),
        text="force field radius: {}".format(force_field_radius),
        manager=gui_manager,
    )

    return strength_slider, text_label_strength, radius_slider, text_label_radius

# Создайте аналогичные функции для других элементов интерфейса, такие как "create_square_elements", "create_circle_elements", и т.д.

def create_square_elements(gui_manager, set_square_size):
    square_size_slider_x = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(150, 70, 200, 20),
        start_value=set_square_size[0],
        value_range=(1, 1000),
        manager=gui_manager,
    )

    text_square_size_x = pgui_elements.UILabel(
        relative_rect=pygame.Rect(5, 55, 600, 50),
        text="square X        :{}".format(set_square_size[0]),
        manager=gui_manager,
    )

    square_size_slider_y = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(150, 100, 200, 20),
        start_value=set_square_size[1],
        value_range=(1, 1000),
        manager=gui_manager,
    )

    text_square_size_y = pgui_elements.UILabel(
        relative_rect=pygame.Rect(5, 85, 600, 50),
        text="square Y        :{}".format(set_square_size[1]),
        manager=gui_manager,
    )

    return square_size_slider_x, text_square_size_x, square_size_slider_y, text_square_size_y


def create_circle_elements(gui_manager, set_circle_radius):
    circle_radius_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(150, 10, 200, 20),
        start_value=set_circle_radius[0],
        value_range=(1, 100),
        manager=gui_manager,
    )
    text_circle_radius = pgui_elements.UILabel(
        relative_rect=pygame.Rect(150, 10, 200, 50),
        text="Circle R: {}".format(set_circle_radius),
        manager=gui_manager,
    )
    return circle_radius_slider, text_circle_radius

def create_other_elements(gui_manager, guide_text, show_guide, screen_width, screen_height, space, simulation_frequency):
    text_guide_gui = pgui_elements.UITextBox(
        relative_rect=pygame.Rect(screen_width - 280, 150, 240, 300),
        html_text=guide_text,
        visible=show_guide,
        manager=gui_manager,
    )
    iterations_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(screen_width - 250, screen_height - 30, 200, 20),
        start_value=30,
        value_range=(1, 128),
        manager=gui_manager,
    )
    text_iterations = pgui_elements.UILabel(
        relative_rect=pygame.Rect(screen_width - 260, screen_height - 30, 300, 20),
        text="iterations        :{}".format(space.iterations),
        manager=gui_manager,
    )
    simulation_frequency_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(screen_width - 250, screen_height - 60, 200, 20),
        start_value=60,
        value_range=(1, 300),
        manager=gui_manager,
    )
    text_simulation_frequency = pgui_elements.UILabel(
        relative_rect=pygame.Rect(screen_width - 260, screen_height - 60, 300, 20),
        text="sim. frequency     :{}".format(simulation_frequency),
        manager=gui_manager,
    )
    return text_guide_gui, iterations_slider, text_iterations, simulation_frequency_slider, text_simulation_frequency

def create_friction_elements(gui_manager, screen_width, screen_height, set_friction):
    friction_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(screen_width - 250, screen_height - 90, 200, 20),
        start_value=1,
        value_range=(0.01, 10),
        manager=gui_manager,
    )
    text_friction = pgui_elements.UILabel(
        relative_rect=pygame.Rect(screen_width - 260, screen_height - 90, 300, 20),
        text="friction     :{}".format(set_friction),
        manager=gui_manager,
    )
    return friction_slider, text_friction
def create_elasticity_elements(gui_manager, screen_width, screen_height, set_friction):
    elasticity_slider = pgui_elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(screen_width - 250, screen_height - 120, 200, 20),
        start_value=1,
        value_range=(0.01, 10),
        manager=gui_manager,
    )
    text_elasticity = pgui_elements.UILabel(
        relative_rect=pygame.Rect(screen_width - 260, screen_height - 120, 300, 20),
        text="elasticity     :{}".format(set_friction),
        manager=gui_manager,
    )
    return elasticity_slider, text_elasticity
def create_save_load_elements(gui_manager, screen_width):
    save_world_button = pgui_elements.UIButton(
        relative_rect=pygame.Rect(screen_width - 135, 10, 125, 40),
        text="Save World",
        manager=gui_manager
    )
    load_world_button = pgui_elements.UIButton(
        relative_rect=pygame.Rect(screen_width - 135, 60, 125, 40),
        text="Load World",
        manager=gui_manager
    )
    return save_world_button, load_world_button

def create_delete_elements(gui_manager, screen_height):
    delete_all_button = pgui_elements.UIButton(
        relative_rect=pygame.Rect(10, screen_height - 50, 125, 40),
        text="Delete all",
        manager=gui_manager
    )
    return delete_all_button
# FORCE_FIELD######################################################################################
# SQUARE######################################################################################
# CIRCLE######################################################################################
# OTHER_GUI######################################################################################
# FRICTION######################################################################

# elasticity@#####################################################################

#SAVE/LOAD BUTTONS#####################################################################

#DELETE_ALL_BUTTON##########################################################################


