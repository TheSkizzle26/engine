import math
import time

import pyray

import engine


class CPUFoliageManager:
    def __init__(self, foliage_assets: "CPUFoliageAssets", chunk_size=16, adaptivity=5, wind_force=10, wind_speed=1.3, shadows=True):
        self.assets = foliage_assets
        self.adaptivity = adaptivity
        self.wind_force = wind_force
        self.wind_speed = wind_speed

        self.render_shadows = shadows

        self.chunks = {}
        self.chunk_size = chunk_size

        self.visible_chunks = []

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def spawn_object(self, pos, texture_idx):
        chunk_pos = (
            pos[0] // self.chunk_size,
            pos[1] // self.chunk_size
        )

        chunk = self.chunks.setdefault(self.chunk_id(chunk_pos), CPUFoliageChunk(self, chunk_pos))
        chunk.spawn_object(pos, texture_idx)

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

        for cy in range(int(topleft_chunk_pos[1] - 1),
                        int(topleft_chunk_pos[1] + camera_size[1]//self.chunk_size + 4)):
            for cx in range(int(topleft_chunk_pos[0] - 1),
                            int(topleft_chunk_pos[0] + camera_size[0]//self.chunk_size + 2)):
                chunk_id = self.chunk_id((cx, cy))

                if chunk_id in self.chunks:
                    chunks.append(self.chunks[chunk_id])

        return chunks

    def update(self):
        time = engine.get_time()

        for chunk in self.visible_chunks:
            chunk.master_angle = math.sin(time * self.wind_speed + (chunk.pos[0] * self.chunk_size) / 80 + (chunk.pos[1] * self.chunk_size) / 40) * self.wind_force
            chunk.calculate_forces()
            chunk.update()

    def render(self):
        if self.render_shadows:
            for chunk in self.visible_chunks:
                chunk.render_shadows()
        for chunk in self.visible_chunks:
            chunk.render()

class CPUFoliageChunk:
    def __init__(self, manager, pos):
        self.manager = manager
        self.assets = manager.assets
        self.adaptivity = manager.adaptivity

        self.pos = pos

        self.objects = []
        self.master_angle = 0

        self.forces = []

    def spawn_object(self, pos, texture_idx):
        # find correct idx to insert (sorted by y coord)
        idx = 0
        while idx < len(self.objects):
            if self.objects[idx]["pos"][1] > pos[1]:
                break

            idx += 1

        self.objects.insert(idx, {
            "texture": texture_idx,
            "pos": pos,
            "angle": 0,
            "target_angle": 0
        })

    def prepare_update(self):
        self.forces = []

        for object in self.objects:
            object["target_angle"] = 0

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

            for blade in self.objects:
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

        for blade in self.objects:
            blade["angle"] += (blade["target_angle"] - blade["angle"]) * delta * self.adaptivity

    def render_shadows(self):
        for object in self.objects:
            shadow = self.assets.get_shadow()
            engine.draw_texture(
                shadow,
                int(object["pos"][0] - shadow.width / 2),
                int(object["pos"][1] - shadow.height / 2),
                engine.WHITE
            )

    def render(self):
        for object in self.objects:
            texture = self.assets.textures[object["texture"]]

            engine.draw_texture_pro(
                texture["texture"],
                (0, 0, texture["texture"].width, texture["texture"].height),
                (object["pos"][0], object["pos"][1], texture["texture"].width, texture["texture"].height),
                texture["origin"],
                self.master_angle + object["angle"],
                engine.WHITE
            )

class CPUFoliageAssets:
    def __init__(self, compute_ao=True, shadow_size=(32, 16), shadow_darkness=0.55, custom_shadow_texture=None):
        self.textures: list[dict] = []
        self.shadow = engine.load_render_texture(*shadow_size)
        self.grass_shader = engine.load_shader("", "engine/assets/cpu_foliage/ao.frag")
        engine.set_texture_filter(self.shadow.texture, engine.TextureFilter.TEXTURE_FILTER_BILINEAR)

        self.compute_ao = compute_ao
        self.shadow_darkness = shadow_darkness
        self.custom_shadow_texture = custom_shadow_texture

        self.calculate_shadow()

    def get(self, idx) -> dict:
        return self.textures[idx]

    def get_shadow(self):
        return self.shadow.texture

    def get_grass_shader(self):
        return self.grass_shader

    def calculate_shadow(self):
        if self.custom_shadow_texture: # not sure if this works
            self.shadow.texture = self.custom_shadow_texture
            return

        temp = engine.load_render_texture(self.shadow.texture.width, self.shadow.texture.height)
        shader = engine.load_shader("", "engine/assets/cpu_foliage/shadow.frag")
        engine.set_shader_value(shader, 1, pyray.ffi.new("float *", self.shadow_darkness), engine.ShaderUniformDataType.SHADER_UNIFORM_FLOAT)

        width = self.shadow.texture.width
        height = self.shadow.texture.height

        engine.begin_texture_mode(temp)
        engine.draw_rectangle(0, 0, width, height, engine.WHITE)
        engine.end_texture_mode()

        engine.begin_texture_mode(self.shadow)
        engine.begin_shader_mode(shader)
        engine.draw_texture(temp.texture, 0, 0, engine.WHITE)
        engine.end_shader_mode()
        engine.end_texture_mode()

        engine.unload_render_texture(temp)
        engine.unload_shader(shader)

    def _add_single_image(self, texture, origin=None, use_center_as_origin=None):
        if use_center_as_origin:
            origin = (
                int(texture.width / 2),
                int(texture.height / 2),
            )

        temp = engine.load_render_texture(texture.width, texture.height)

        engine.begin_texture_mode(temp)
        engine.clear_background(engine.BLANK)
        if self.compute_ao: engine.begin_shader_mode(self.grass_shader)

        engine.draw_texture_rec(
            texture,
            (0, 0, texture.width, -texture.height),
            (0, 0),
            engine.WHITE
        )

        if self.compute_ao: engine.end_shader_mode()
        engine.end_texture_mode()

        image = engine.load_image_from_texture(temp.texture)
        new_texture = engine.load_texture_from_image(image)

        engine.unload_image(image)
        engine.unload_render_texture(temp)
        engine.unload_texture(texture)

        self.textures.append({
            "texture": new_texture,
            "origin": origin
        })

    def add_image(self, textures, origin=None, use_center_as_origin=None):
        if type(textures) == engine.Texture:
            self._add_single_image(textures, origin, use_center_as_origin)
        else:
            for texture in textures:
                self._add_single_image(texture, origin, use_center_as_origin)