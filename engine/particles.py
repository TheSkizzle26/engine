import engine


class Particle(engine.Entity):
    def __init__(self, texture, pos,
                 velocity=(0, 0), drag=0.9,
                 gravity=(0, 10), bounce_mult=0.7):
        super().__init__(pos, (0, 0))

        self.texture = texture
        self.velocity = list(velocity)
        self.drag = drag
        self.gravity = gravity
        self.bounce_mult = bounce_mult

        self.collision_rects = []

    def set_collision_rects(self, collision_rects):
        self.collision_rects = collision_rects

    def update(self):
        delta = engine.get_frame_time()

        self.velocity[0] *= delta * self.drag
        self.velocity[1] *= delta * self.drag

        self.velocity[0] += self.gravity[0]
        self.velocity[1] += self.gravity[1]

        self.move_and_collide(self.collision_rects, self.velocity)

        if self.collisions["left"] or self.collisions["right"]:
            self.velocity[0] *= -1
        if self.collisions["up"] or self.collisions["down"]:
            self.velocity[1] *= -1

    def render(self):
        x = self.pos[0] - self.texture.width/2
        y = self.pos[1] - self.texture.height/2

        engine.draw_texture(self.texture, int(x), int(y), engine.WHITE)


class ParticleManager(engine.ElementSingleton):
    """
    Not sure how fast this is.
    """

    def __init__(self, chunk_size):
        super().__init__()

        self.chunks = {}
        self.chunk_size = chunk_size

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def add_particle(self, particle: Particle):
        chunk_pos = (
            particle.pos[0] // self.chunk_size,
            particle.pos[1] // self.chunk_size
        )

        self.chunks.setdefault(self.chunk_id(chunk_pos), []).append(particle)

    def update_particle_chunk_pos(self, particle):
        chunk_pos = (
            particle.pos[0] // self.chunk_size,
            particle.pos[1] // self.chunk_size
        )

    def update(self):
        new_chunks = {}

        for chunk in self.chunks.values():
            for particle in chunk:
                particle.update()

                chunk_pos = (
                    particle.pos[0] // self.chunk_size,
                    particle.pos[1] // self.chunk_size
                )

                new_chunks.setdefault(self.chunk_id(chunk_pos), []).append(particle)

        self.chunks = new_chunks

    def get_visible_chunks(self):
        chunks = []

        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.chunk_size,
            camera_topleft[1] // self.chunk_size
        )

        for cy in range(int(topleft_chunk_pos[1] - 1),
                        int(topleft_chunk_pos[1] + camera_size[1]//self.chunk_size + 4)):
            for cx in range(int(topleft_chunk_pos[0] - 1),
                            int(topleft_chunk_pos[0] + camera_size[0]//self.chunk_size + 2)):
                chunk_id = self.chunk_id((cx, cy))

                if chunk_id in self.chunks:
                    chunks.append(self.chunks[chunk_id])

        return chunks

    def render(self):
        for chunk in self.get_visible_chunks():
            for particle in chunk:
                particle.render()