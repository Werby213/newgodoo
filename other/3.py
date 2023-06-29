import pygame
import tkinter as tk
from tkinter import ttk
import pymunk

class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pygame + Tkinter")

        self.canvas = pygame.Surface((800, 600))
        self.canvas_id = None

        self.pygame_initialized = False
        self.pygame_clock = pygame.time.Clock()
        self.pygame_space = None
        self.pygame_objects = []
        self.camera_offset = [0, 0]
        self.camera_dragging = False
        self.camera_drag_start = (0, 0)

        self.create_widgets()

    def create_widgets(self):
        # Frame for the Pygame canvas
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pygame canvas
        self.pygame_canvas = tk.Canvas(canvas_frame, width=800, height=600)
        self.pygame_canvas.pack(fill=tk.BOTH, expand=True)
        self.pygame_canvas.bind("<Configure>", self.on_canvas_resize)
        self.pygame_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.pygame_canvas.bind("<Button-2>", self.on_middle_mouse_button_press)
        self.pygame_canvas.bind("<B2-Motion>", self.on_middle_mouse_button_drag)

        # Frame for the Tkinter controls
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Spawn options
        spawn_label = ttk.Label(controls_frame, text="Spawn Options")
        spawn_label.pack()

        self.spawn_var = tk.StringVar()
        self.spawn_var.set("Circle")  # Default selection

        spawn_radio_circle = ttk.Radiobutton(
            controls_frame,
            text="Circle",
            variable=self.spawn_var,
            value="Circle"
        )
        spawn_radio_circle.pack()

        spawn_radio_segment = ttk.Radiobutton(
            controls_frame,
            text="Segment",
            variable=self.spawn_var,
            value="Segment"
        )
        spawn_radio_segment.pack()

        # Quit button
        quit_button = ttk.Button(controls_frame, text="Quit", command=self.quit)
        quit_button.pack()

    def on_canvas_resize(self, event):
        self.canvas = pygame.Surface((event.width, event.height))
        if self.pygame_initialized:
            self.update_pygame_canvas()

    def on_mouse_wheel(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        self.camera_offset[0] *= zoom_factor
        self.camera_offset[1] *= zoom_factor
        if self.pygame_initialized:
            self.update_pygame_canvas()

    def on_middle_mouse_button_press(self, event):
        self.camera_dragging = True
        self.camera_drag_start = event.x, event.y

    def on_middle_mouse_button_drag(self, event):
        dx = event.x - self.camera_drag_start[0]
        dy = event.y - self.camera_drag_start[1]
        self.camera_offset[0] += dx
        self.camera_offset[1] += dy
        self.camera_drag_start = event.x, event.y
        if self.pygame_initialized:
            self.update_pygame_canvas()

    def update_pygame_canvas(self):
        self.canvas.fill((0, 0, 0))

        for shape in self.pygame_space.shapes:
            if isinstance(shape, pymunk.Segment):
                start = shape.a + self.camera_offset
                end = shape.b + self.camera_offset
                pygame.draw.line(self.canvas, (255, 255, 255), start, end)

        for body, shape in self.pygame_objects:
            position = body.position + self.camera_offset
            pygame.draw.circle(self.canvas, (255, 0, 0), position, int(shape.radius))

        if self.pygame_space.creating_static_field:
            static_field_end = pygame.mouse.get_pos()
            pygame.draw.line(
                self.canvas, (255, 255, 255),
                self.pygame_space.static_field_start, static_field_end
            )

        self.pygame_canvas.delete(self.canvas_id)
        self.canvas_id = self.pygame_canvas.create_image(
            0, 0, image=self.pygame_surface_to_tk(self.canvas), anchor=tk.NW
        )

    def pygame_surface_to_tk(self, surface):
        photo = pygame.image.tostring(surface, "RGB")
        width, height = surface.get_size()
        return tk.PhotoImage(data=photo, width=width, height=height)

    def pygame_initialize(self):
        pygame.init()
        self.pygame_initialized = True

        self.pygame_space = pymunk.Space()
        self.pygame_space.gravity = 0, 1000

        static_body = self.pygame_space.static_body
        floor = pymunk.Segment(static_body, (0, 500), (800, 500), 0)
        floor.friction = 1.0
        self.pygame_space.add(floor)

    def spawn_object(self):
        if self.spawn_var.get() == "Circle":
            body = pymunk.Body(1, 1)
            body.position = pygame.mouse.get_pos()
            shape = pymunk.Circle(body, randrange(5, 30))
            shape.friction = 0.7
            self.pygame_space.add(body, shape)
            self.pygame_objects.append((body, shape))
        elif self.spawn_var.get() == "Segment":
            if self.pygame_space.creating_static_field:
                static_field = pymunk.Segment(
                    self.pygame_space.static_body,
                    self.pygame_space.static_field_start,
                    pygame.mouse.get_pos(),
                    10
                )
                static_field.friction = 1.0
                self.pygame_space.add(static_field)
                self.pygame_space.creating_static_field = False
            else:
                self.pygame_space.static_field_start = pygame.mouse.get_pos()
                self.pygame_space.creating_static_field = True

    def run(self):
        self.pygame_initialize()

        self.update_pygame_canvas()
        self.root.after(100, self.pygame_tick)
        self.root.mainloop()

    def pygame_tick(self):
        if self.pygame_initialized:
            dt = 1.0 / 60.0
            self.pygame_space.step(dt)
            self.update_pygame_canvas()
        self.root.after(16, self.pygame_tick)

    def quit(self):
        self.root.quit()


if __name__ == "__main__":
    game_window = GameWindow()
    game_window.run()
