import random
import time
import engine
import moderngl


class Main(engine.Program):
    def __init__(self):
        super().__init__()
        engine.init(
            (1920, 1080),
            "grass test",
            image_path="assets/images",
            input_map_path="assets/input_map.json",
            flags=engine.ConfigFlags.FLAG_FULLSCREEN_MODE
        )
        self.ctx = moderngl.create_context()

        self.camera = engine.Camera((0, 0), 4, 5)

        grass_assets = engine.FoliageAssets(self.ctx)
        for tex in engine.assets.load_texture_group("grass"):
            grass_assets.add_texture(tex)
        grass_assets.compute_gpu_data()

        self.grass = engine.FoliageManager(
            self.ctx,
            grass_assets,
            adaptivity=15,
            wind_force=30,
            render_shadows=True
        )

        self.num_blades = 0

        # setup objects, just for testing
        # size = (1550*2, 1300*2)
        size = (200, 200)
        print(size[0] * size[1])
        offset = (6, 4)
        # offset = (40, 40)
        random_offset = (6, 3.5)
        for x in range(-size[0] // 2, size[0] // 2):
            for y in range(-size[1] // 2, size[1] // 2):
                self.num_blades += 1
                self.grass.spawn_object(
                    (
                        x * offset[0] + random.random() * random_offset[0] - random_offset[0] / 2,
                        y * offset[1] + random.random() * random_offset[1] - random_offset[1] / 2
                    ),
                    random.randint(0, 5)
                )

            if x % 25 != 0:
                continue

            # render progress bar
            engine.begin_drawing()

            center = (engine.data.internal_size[0] // 2, engine.data.internal_size[1] // 2)
            width = 500
            height = 30

            engine.draw_rectangle(
                int(center[0] - width / 2),
                int(center[1] - height / 2),
                int(width * (x + size[0] // 2) / size[0]),
                int(height),
                engine.WHITE
            )
            engine.draw_rectangle_lines(
                int(center[0] - width / 2),
                int(center[1] - height / 2),
                int(width),
                int(height),
                engine.WHITE
            )

            engine.end_drawing()
        self.grass.compute_gpu_data()

        engine.hide_cursor()

        self.cursor_size = 18

        self.last_mouse_world_pos = [0, 0]
        self.cursor_movement = 0

    def update(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        self.cursor_size += int(engine.get_mouse_wheel_move()*3)

        delta = engine.get_frame_time()

        movement = engine.vector2_normalize((
            engine.input.is_down("right") - engine.input.is_down("left"),
            engine.input.is_down("down") - engine.input.is_down("up")
        ))
        movement = (
            movement.x * delta * 200,
            movement.y * delta * 200,
        )

        self.camera.move_target(movement)
        self.camera.update()

        self.grass.clear_forces()

        m_pos = engine.get_mouse_pos()
        c_pos = self.camera.get_world_topleft()
        pos = (
            c_pos[0] + m_pos[0] / self.camera._zoom,
            c_pos[1] + m_pos[1] / self.camera._zoom
        )

        self.grass.add_force(pos, self.cursor_size*3, 60)

        engine.set_window_title(f"FPS: {engine.get_fps()}")

        self.last_mouse_world_pos = pos

    def render(self):
        engine.begin_drawing()
        engine.clear_background((23, 70, 36))

        self.camera.begin()
        self.grass.update_and_render(self.camera)
        self.camera.end()

        engine.draw_text(f"{self.num_blades} blades", 6, 0, 60, engine.WHITE)
        engine.draw_text(f"FPS: {engine.get_fps()}", 6, 60-11, 60, engine.WHITE)

        texture = engine.assets.load_texture("cursor.png")
        cursor_pos = (
            engine.get_mouse_x() - texture.width/2*self.cursor_size/3,
            engine.get_mouse_y() - texture.height/2*self.cursor_size/3
        )
        engine.draw_texture_ex(texture, cursor_pos, 0, self.cursor_size/3, engine.WHITE)

        engine.end_drawing()


if __name__ == "__main__":
    Main().run()
