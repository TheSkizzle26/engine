import engine


class Particle(engine.Entity):
    def __init__(self, texture, pos,
                 velocity=(0, 0), drag=0.9,
                 gravity=(0, 20), bounce_mult=0.7,
                 lifetime=2, fade=True,
                 fade_expo=1, z=0):
        super().__init__(pos, (0, 0))

        self.texture = texture
        self.velocity = list(velocity)
        self.drag = drag
        self.gravity = gravity
        self.bounce_mult = bounce_mult

        self.lifetime = lifetime
        self.spawn_time = engine.get_time()

        self.fade = fade
        self.fade_expo = fade_expo

        self.z = z
        self.collision_rects = []

        self.manager = None

    def set_manager(self, manager):
        self.manager = manager

    def set_collision_rects(self, collision_rects):
        self.collision_rects = collision_rects

    def is_dead(self):
        now = engine.get_time()
        return now - self.spawn_time > self.lifetime

    def update(self):
        delta = engine.get_frame_time()

        self.velocity[0] *= (1 - self.drag * delta)
        self.velocity[1] *= (1 - self.drag * delta)

        self.velocity[0] += self.gravity[0] * delta
        self.velocity[1] += self.gravity[1] * delta

        frame_movement = (
            self.velocity[0] * delta,
            self.velocity[1] * delta,
        )
        self.move_and_collide(self.collision_rects, frame_movement)

        if self.collisions["left"] or self.collisions["right"]:
            self.velocity[0] *= -self.bounce_mult
        if self.collisions["up"] or self.collisions["down"]:
            self.velocity[1] *= -self.bounce_mult

    def render(self):
        time = engine.get_time()
        t = (time - self.spawn_time) / self.lifetime
        t **= self.fade_expo
        a = min(max(1 - t, 0), 1)

        x = self.pos[0] - self.texture.width/2
        y = self.pos[1] - self.texture.height/2
        color = (
            255,
            255,
            255,
            int(a*255)
        )

        engine.draw_texture(self.texture, int(x), int(y), color)


class ParticleManager(engine.ElementSingleton):
    """
    Not sure how fast this is.
    """

    def __init__(self, chunk_size=32):
        super().__init__()

        self.z_groups = {}
        self.chunk_size = chunk_size

        self.num_particles = 0

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def add_particle(self, particle: Particle, z=0):
        chunk_pos = (
            particle.pos[0] // self.chunk_size,
            particle.pos[1] // self.chunk_size
        )

        self.z_groups.setdefault(float(z), {}).setdefault(self.chunk_id(chunk_pos), []).append(particle)
        particle.set_manager(self)

    def update_z_group(self, group_id):
        new_chunks = {}

        for chunk in self.z_groups[group_id].values():
            for particle in chunk:
                if particle.is_dead():
                    continue  # delete it from new dict

                particle.update()

                chunk_pos = (
                    particle.pos[0] // self.chunk_size,
                    particle.pos[1] // self.chunk_size
                )

                new_chunks.setdefault(self.chunk_id(chunk_pos), []).append(particle)

        self.z_groups[group_id] = new_chunks

    def update(self):
        for group_id in self.z_groups:
            self.update_z_group(group_id)

    def get_visible_chunks(self):
        groups = {}

        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.chunk_size,
            camera_topleft[1] // self.chunk_size
        )

        for cy in range(int(topleft_chunk_pos[1] - 1),
                        int(topleft_chunk_pos[1] + camera_size[1]//self.chunk_size + 2)):
            for cx in range(int(topleft_chunk_pos[0] - 1),
                            int(topleft_chunk_pos[0] + camera_size[0]//self.chunk_size + 2)):
                chunk_id = self.chunk_id((cx, cy))

                for group_id in self.z_groups:
                    if chunk_id in self.z_groups[group_id]:
                        groups.setdefault(group_id, []).append(self.z_groups[group_id][chunk_id])

        return groups

    def render(self):
        groups = self.get_visible_chunks()
        group_ids = sorted(groups.keys())

        for group_id in group_ids:
            for chunk in groups[group_id]:
                for particle in chunk:
                    particle.render()