import random
import engine

"""
Horrible code, but its only for testing anyway.
"""


class Player(engine.EntitySingleton):
    def __init__(self):
        super().__init__((0, 0), (50, 50))

        self.speed = 3

        self.collision_rects = []

        for i in range(10):
            self.collision_rects.append(engine.Rect(
                random.random() * 800,
                random.random() * 600,
                25 + random.random() * 75,
                25 + random.random() * 75
            ))

    def update(self):
        movement = engine.Vector2(
            engine.input.is_down("right") - engine.input.is_down("left"),
            engine.input.is_down("down") - engine.input.is_down("up")
        )

        movement = engine.vector2_normalize(movement)
        movement = engine.vector2_multiply(movement, engine.Vector2(self.speed, self.speed))

        self.move_and_collide(self.collision_rects, engine.vector2_to_list(movement))

    def render_rects(self):
        for rect in self.collision_rects:
            engine.draw_rectangle(rect.x, rect.y, rect.width, rect.height, engine.GOLD)

    def render(self):
        m_pos = engine.get_mouse_pos()
        rect = engine.Rect(m_pos[0]-25, m_pos[1]-25, 50, 50)

        color = engine.RED if engine.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]).colliderect(rect) else engine.WHITE

        engine.draw_rectangle(int(self.pos[0]), int(self.pos[1]), 50, 50, color)

        self.render_rects()


class Main(engine.Program):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "test window",
            target_fps=60,
            image_path="assets/images",
            audio_path="assets/audio",
            input_map_path="assets/input_map.json",
        )

        engine.assets.load_assets()

        self.player = Player()
        self.bg_texture = engine.textures["dog"]

        engine.log.init_font()

    def handle_inputs(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        if engine.input.is_pressed("log"):
            engine.log.write("Playing sound.")
            engine.play_sound_ex(engine.sounds["sound"])

    def update(self):
        self.handle_inputs()
        self.player.update()

        engine.log.update()

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)

        engine.draw_texture(self.bg_texture, 0, 0, engine.WHITE)
        self.player.render()

        m_pos = engine.get_mouse_pos()
        engine.draw_rectangle(m_pos[0]-25, m_pos[1]-25, 50, 50, engine.ORANGE)

        engine.log.render()

        engine.end_drawing()


if __name__ == "__main__":
    Main().run()