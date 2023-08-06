import pygame
import dearpygui.dearpygui as dpg

# Инициализация Pygame
pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dear PyGui with Pygame Integration")

# Функция для рендеринга GUI
def render_gui():
    dpg.render_dearpygui_frame()

# Основной цикл Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление GUI и рендеринг
    dpg.set_viewport_title("Dear PyGui with Pygame Integration")
    dpg.set_viewport_width(window_size[0])
    dpg.set_viewport_height(window_size[1])
    render_gui()

    # Обновление окна Pygame
    pygame.display.flip()

# Завершение работы Pygame и Dear PyGui
dpg.cleanup_dearpygui()
pygame.quit()
