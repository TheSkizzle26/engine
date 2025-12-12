import random

import engine
from engine import Particle


class Main(engine.Program):
    def __init__(self):
        super().__init__()
        engine.init(
            (800, 600),
            "particle test",
            image_path="assets/images",
            input_map_path="assets/input_map.json"
        )

        self.camera = engine.Camera((0, 0), 4, 1)

        self.particle_textures = engine.assets.load_texture_group("particles")
        self.particles = engine.ParticleManager()

        self.last_particle_time = 0

    def update(self):
        if engine.input.is_pressed("quit"):
            self.quit()

        if engine.input.is_down("log") and engine.get_time() - self.last_particle_time >= 0.01:
            self.last_particle_time = engine.get_time()

            m_pos = (
                (engine.get_mouse_x() - 400) / 4,
                (engine.get_mouse_y() - 300) / 4
            )

            offset = 250
            p_type = random.randint(0, 1)

            self.particles.add_particle(Particle(
                self.particle_textures[p_type],
                m_pos,
                velocity=(
                    random.random() * offset - offset/2,
                    random.random() * -offset/2,
                ),
                gravity=(0, 100),
                fade_expo=3
            ), -p_type)

        self.particles.update()

    def render(self):
        engine.begin_drawing()
        engine.clear_background(engine.BLACK)

        self.camera.begin()
        self.particles.render()
        self.camera.end()

        engine.draw_text(f"FPS: {engine.get_fps()}", 2, 0, 60, engine.WHITE)

        engine.end_drawing()


if __name__ == "__main__":
    Main().run()