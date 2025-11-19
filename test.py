import engine


class TestClass(engine.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.test = "Hello World!"


class Main(engine.Game):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "test window"
        )

        self.test_class = TestClass()

    def handle_inputs(self):
        if engine.is_key_pressed(engine.KeyboardKey.KEY_ESCAPE):
            self.quit()

    def update(self):
        self.handle_inputs()

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)

        engine.end_drawing()


if __name__ == "__main__":
    Main().run()