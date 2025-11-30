import random

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

        grass_assets = engine.GrassAssets()
        grass_assets.add_image(engine.assets.load_texture_group("grass"), use_center_as_origin=True)
        grass_assets.calculate_atlas()

        self.grass = engine.GrassManager(grass_assets)

        num = (350, 60)
        print(num[0] * num[1], "blades of grass")

        for x in range(-num[0]//2, num[0]//2+1):
            for y in range(-num[1]//2, num[1]//2+1):
                if random.random() > 1: continue

                texture_ids = [i for i in range(6)]
                chosen_ids = [texture_ids.pop(random.randint(0, len(texture_ids)-1)) for i in range(3)]

                offset = (
                    random.randint(-3, 3),
                    random.randint(-7, 7),
                )

                for idx in chosen_ids:
                    self.grass.spawn_blade(
                        (
                            x*5*0.9 + offset[0],
                            y*19*0.9 + offset[1]
                        ),
                        idx
                    )

    def update(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        delta = engine.get_frame_time()

        movement = (
            (engine.input.is_down("right") - engine.input.is_down("left")),
            (engine.input.is_down("down") - engine.input.is_down("up"))
        )

        movement = engine.vector2_multiply(movement, (delta*250, delta*250))
        movement = engine.vector2_to_list(movement)

        self.camera.move_target(movement)
        self.camera.update()

        self.grass.prepare_update()

        m_pos = engine.get_mouse_pos()
        c_pos = self.camera.get_world_topleft()
        world_pos = (
            c_pos[0] + m_pos[0] / self.camera._zoom,
            c_pos[1] + m_pos[1] / self.camera._zoom
        )
        self.grass.apply_force(world_pos, 35, 70)
        self.grass.update()

        engine.set_window_title(f"FPS: {engine.get_fps()}")

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)
        self.camera.begin()

        self.grass.render()

        self.camera.end()
        engine.end_drawing()


if __name__ == "__main__":
    Main().run()