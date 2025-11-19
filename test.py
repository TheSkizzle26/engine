import engine


class Player(engine.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.pos = [0, 0]
        self.speed = 3

    def update(self):
        movement = engine.Vector2(
            engine.input.is_down("right") - engine.input.is_down("left"),
            engine.input.is_down("down") - engine.input.is_down("up")
        )

        movement = engine.vector2_normalize(movement)
        movement = engine.vector2_multiply(movement, engine.Vector2(self.speed, self.speed))

        self.pos[0] += movement.x
        self.pos[1] += movement.y

    def render(self):
        engine.draw_rectangle(int(self.pos[0]), int(self.pos[1]), 50, 50, engine.WHITE)


class Main(engine.Game):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "test window",
            target_fps=60,
            image_path="assets/images",
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
            engine.log.write("Test log message.")

    def update(self):
        self.handle_inputs()
        self.player.update()

        engine.log.update()

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)

        engine.draw_texture(self.bg_texture, 0, 0, engine.WHITE)
        self.player.render()

        engine.log.render()

        engine.end_drawing()


if __name__ == "__main__":
    Main().run()