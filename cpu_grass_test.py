import random
import time

import engine


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

        self.camera = engine.Camera((0, 0), 4, 5)

        grass_assets = engine.CPUFoliageAssets()
        grass_assets.add_image(engine.assets.load_texture_group("grass"), use_center_as_origin=True)

        self.grass = engine.CPUFoliageManager(
            grass_assets,
            adaptivity=15,
            wind_force=30,
            shadows=True
        )

        self.num_blades = 0

        #for x in range(-20, 21):
        #    for y in range(-20, 21):
        #        self.grass.spawn_object((x*5, y*5), random.randint(0, 5))
        #        self.num_blades += 1

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

        self.grass.prepare_update()

        m_pos = engine.get_mouse_pos()
        c_pos = self.camera.get_world_topleft()
        pos = (
            c_pos[0] + m_pos[0] / self.camera._zoom,
            c_pos[1] + m_pos[1] / self.camera._zoom
        )

        self.cursor_movement += engine.vector2_distance(
            pos,
            self.last_mouse_world_pos
        )

        if engine.input.is_down("log") and self.cursor_movement > 7.5:
            self.cursor_movement = 0

            random_offset = self.cursor_size

            for i in range(self.cursor_size // 6):
                blade_pos = (
                    pos[0] + random.random() * random_offset - random_offset/2,
                    pos[1] + random.random() * random_offset - random_offset/2,
                )

                self.grass.spawn_object(blade_pos, random.randint(0, 5))

                self.num_blades += 1

        self.grass.apply_force(pos, self.cursor_size*3, 60)
        self.grass.update()

        engine.set_window_title(f"FPS: {engine.get_fps()}")

        self.last_mouse_world_pos = pos

    def render(self):
        engine.begin_drawing()
        engine.clear_background((23, 70, 36))

        self.camera.begin()
        self.grass.render()
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
