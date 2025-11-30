import engine


class Main(engine.Program):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "grass test",
            image_path="assets/images",
            input_map_path="assets/input_map.json"
        )

        self.camera = engine.Camera((0, 0), 1, 5)

    def update(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        #movement = (
        #    (engine.input.is_down("right") - engine.input.is_down("left")),
        #    (engine.input.is_down("down") - engine.input.is_down("up"))
        #)
        #self.camera.move_target(movement)
        #self.camera.update()
        #self.camera.set_zoom(10)

        delta = engine.get_frame_time()

        self.camera.move_target((0, -delta*10))
        self.camera.set_zoom(self.camera._zoom * 1.0001)

        self.camera.update()

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)
        self.camera.begin()

        engine.draw_rectangle(0, 0, 100, 100, engine.WHITE)

        self.camera.end()
        engine.end_drawing()


if __name__ == "__main__":
    Main().run()