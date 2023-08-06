import dearpygui.dearpygui as dpg
import pymunk

# Функции создания предметов
def spawn_square():
    body = pymunk.Body(1, 1666)
    shape = pymunk.Poly.create_box(body, (50, 50))
    shape.body.position = (400, 400)
    space.add(body, shape)

def spawn_circle():
    body = pymunk.Body(1, 1666)
    shape = pymunk.Circle(body, 25)
    shape.body.position = (400, 400)
    space.add(body, shape)

def spawn_triangle():
    body = pymunk.Body(1, 1666)
    shape = pymunk.Poly.create_box(body, (50, 50))
    shape.body.position = (400, 400)
    space.add(body, shape)

# Настройка окна Dear PyGui
dpg.create_context()
dpg.create_viewport(title="Физическая песочница")
dpg.setup_dearpygui()

# Создание физического пространства
space = pymunk.Space()
space.gravity = (0.0, 1000.0)

# Создание главного окна и установка его в качестве родительского элемента для кнопок
with dpg.window(label="Главное окно"):
    # Создание кнопок спавна предметов
    dpg.add_button(label="Спавн квадрата", callback=spawn_square)
    dpg.add_button(label="Спавн круга", callback=spawn_circle)
    dpg.add_button(label="Спавн треугольника", callback=spawn_triangle)

# Цикл Dear PyGui
while True:
    dpg.render_dearpygui_frame()

# Очистка ресурсов
dpg.cleanup_dearpygui()
