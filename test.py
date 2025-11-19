import engine


class Player(engine.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.texture = engine.textures["icon"]

        self.pos = [0, 0]

    def update(self):
        ...

    def render(self):
        engine.draw_texture_ex(self.texture, self.pos, 0, 0.35, engine.WHITE)


class Main(engine.Game):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "test window",
            image_path="assets/images",
            input_map_path="assets/input_map.json",
        )

        engine.assets.load_assets()

        self.player = Player()
        self.bg_texture = engine.textures["office"]["74"]

        engine.log.init_font()

    def handle_inputs(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        if engine.input.is_pressed("shoot"):
            print("log written!")
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