import math

import engine

"""
chunk syntax:

{
    {"texture": ..., "pos": (x, y), "angle": radians}
}

angle is 0 facing top
"""


class GrassManager:
    def __init__(self, grass_assets: "GrassAssets", chunk_size=16):
        self.assets = grass_assets

        self.chunks = {}
        self.chunk_size = chunk_size

        self.visible_chunks = []

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def spawn_blade(self, pos, texture_idx):
        chunk_pos = (
            pos[0] // self.chunk_size,
            pos[1] // self.chunk_size
        )

        chunk = self.chunks.setdefault(self.chunk_id(chunk_pos), GrassChunk(self, chunk_pos))
        chunk.spawn_blade(pos, texture_idx)

    def apply_force(self, pos, dist, force):
        center_chunk_pos = (
            pos[0] // self.chunk_size,
            pos[1] // self.chunk_size
        )

        num_chunks = dist // self.chunk_size

        for dx in range(-num_chunks-1, num_chunks+2):
            for dy in range(-num_chunks-1, num_chunks+2):
                chunk_pos = (
                    center_chunk_pos[0] + dx,
                    center_chunk_pos[1] + dy,
                )
                chunk_id = self.chunk_id(chunk_pos)

                if chunk_id in self.chunks:
                    self.chunks[chunk_id].apply_force(pos, dist, force)

    def prepare_update(self):
        self.visible_chunks = self.get_visible_chunks()

        for chunk in self.visible_chunks:
            chunk.prepare_update()

    def get_visible_chunks(self):
        chunks = []

        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.chunk_size,
            camera_topleft[1] // self.chunk_size
        )

        for cx in range(int(topleft_chunk_pos[0] - 1),
                        int(topleft_chunk_pos[0] + camera_size[0]//self.chunk_size + 2)):
            for cy in range(int(topleft_chunk_pos[1] - 1),
                            int(topleft_chunk_pos[1] + camera_size[1]//self.chunk_size + 4)):
                chunk_id = self.chunk_id((cx, cy))

                if chunk_id in self.chunks:
                    chunks.append(self.chunks[chunk_id])

        return chunks

    def update(self):
        time = engine.get_time()

        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.chunk_size,
            camera_topleft[1] // self.chunk_size
        )

        for chunk in self.visible_chunks:
            chunk.master_angle = math.sin(time * 1.3 + (chunk.pos[0] * self.chunk_size) / 80 + (chunk.pos[1] * self.chunk_size) / 40) * 10
            chunk.calculate_forces()
            chunk.update()

    def render(self):
        for chunk in self.visible_chunks:
            chunk.render()

class GrassChunk:
    def __init__(self, manager, pos):
        self.manager = manager
        self.assets = manager.assets

        self.pos = pos

        self.blades = []
        self.master_angle = 0

        self.forces = []

    def spawn_blade(self, pos, texture_idx):
        # find correct idx to insert (sorted by y coord)
        idx = 0
        while idx < len(self.blades):
            if self.blades[idx]["pos"][1] > pos[1]:
                break

            idx += 1

        self.blades.insert(idx, {
            "texture": texture_idx,
            "pos": pos,
            "angle": 0,
            "target_angle": 0
        })

    def prepare_update(self):
        self.forces = []

        for blade in self.blades:
            blade["target_angle"] = 0

    def apply_force(self, pos, dist, force):
        self.forces.append({
            "pos": pos,
            "dist": dist,
            "force": force
        })

    def calculate_forces(self):
        for force_dict in self.forces:
            pos = force_dict["pos"]
            dist = force_dict["dist"]
            force = force_dict["force"]

            for blade in self.blades:
                dist_to_pos = engine.vector2_distance(
                    (0, 0),
                    (
                        abs(blade["pos"][0] - pos[0]),
                        abs((blade["pos"][1] - pos[1]) ** 1.4)
                    )
                )

                blade_force = 1 - (dist_to_pos / dist) ** 0.8
                blade_force = max(0, blade_force)

                mult = (1 if blade["pos"][0] > pos[0] else -1)
                blade["target_angle"] += blade_force * force * mult

    def update(self):
        delta = engine.get_frame_time()

        for blade in self.blades:
            blade["angle"] += (blade["target_angle"] - blade["angle"]) * delta * 5

    def render(self):
        for blade in self.blades:
            texture = self.assets.get(blade["texture"])
            engine.draw_texture_pro(
                texture["texture"],
                (0, 0, texture["texture"].width, texture["texture"].height),
                (blade["pos"][0], blade["pos"][1], texture["texture"].width, texture["texture"].height),
                texture["origin"],
                self.master_angle + blade["angle"],
                engine.WHITE
            )

class GrassAssets:
    def __init__(self):
        self.textures: list[dict] = []

    def get(self, idx) -> dict:
        return self.textures[idx]

    def add_image(self, textures, origin=None, use_center_as_origin=None):
        if type(textures) == engine.Texture:
            if use_center_as_origin:
                origin = (
                    int(textures.width / 2),
                    int(textures.height / 2),
                )

            self.textures.append({
                "texture": textures,
                "origin": origin
            })
        else:
            for texture in textures:
                if use_center_as_origin:
                    origin = (
                        int(texture.width / 2),
                        int(texture.height / 2),
                    )

                self.textures.append({
                    "texture": texture,
                    "origin": origin
                })