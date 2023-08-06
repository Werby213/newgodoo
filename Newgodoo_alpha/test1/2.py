import pygame
import pygame_gui

pygame.init()

# Определение размеров окна
WINDOW_SIZE = (400, 300)

# Создание окна Pygame
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Toggle Window Visibility')

# Создание менеджера рендеринга pygame_gui
gui_manager = pygame_gui.UIManager(WINDOW_SIZE)

# Создание кнопки
toggle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 100), (100, 30)),
    text='Toggle',
    manager=gui_manager
)

# Флаг для контроля видимости окна
window_visible = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Передача событий pygame_gui менеджеру
        gui_manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == toggle_button:
                    window_visible = not window_visible
                    pygame.draw.circle(window, (100,100,100,255), (100,100), 10)

    # Обновление элементов pygame_gui
    gui_manager.update(1 / 60)

    # Отрисовка элементов
    window.fill((255, 255, 255))
    gui_manager.draw_ui(window)
    pygame.display.flip()

pygame.quit()
