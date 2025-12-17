import math
import moderngl
import engine
import numpy as np


class FoliageManager:
    def __init__(self, ctx: moderngl.Context, assets: "FoliageAssets",
                 adaptivity=5, wind_force=10,
                 wind_speed=1.3, render_shadows=True,
                 shadow_size=(32, 16), shadow_darkness=0.1,
                 render_ao=True):
        self.ctx = ctx
        self.ctx.disable(self.ctx.CULL_FACE) # why do I feel like I'll regret this?

        self.assets = assets

        self.adaptivity = adaptivity
        self.wind_force = wind_force
        self.wind_speed = wind_speed

        self.render_shadows = render_shadows
        self.shadow_size = shadow_size
        self.shadow_darkness = shadow_darkness

        self.render_ao = render_ao

        # objects
        self.objects = []
        self.num_objects = 0
        self.object_buffer = self.ctx.buffer(np.array([0], dtype=np.float32))
        self.object_buffer.bind_to_storage_buffer(1)

        self.forces = []
        self.num_forces = 0
        self.force_buffer = self.ctx.buffer(np.array([0], dtype=np.float32))
        self.force_buffer.bind_to_storage_buffer(2)

        self.quad_buffer = self.ctx.buffer(np.array([
            0, 0,
            1, 0,
            0, 1,
            1, 1
        ], dtype=np.float32))

        self.grass_prog = engine.mgl.load_program(self.ctx, "engine/assets/foliage/grass.vert", "engine/assets/foliage/grass.frag")
        self.grass_vao = self.ctx.vertex_array(
            self.grass_prog,
            [
                (self.quad_buffer, "2f", "in_vert")
            ]
        )
        self.shadow_prog = engine.mgl.load_program(self.ctx, "engine/assets/foliage/shadow.vert", "engine/assets/foliage/shadow.frag")
        self.shadow_vao = self.ctx.vertex_array(
            self.shadow_prog,
            [
                (self.quad_buffer, "2f", "in_vert")
            ]
        )

    def spawn_object(self, pos, texture_id):
        self.objects.append({
            "pos": pos,
            "texture": texture_id
        })

    def clear_forces(self):
        self.forces = []

    def add_force(self, pos, dist, force):
        self.forces.append({
            "pos": pos,
            "dist": dist,
            "force": force
        })

    def _compute_gpu_force_data(self):
        self.num_forces = len(self.forces)

        data = []
        for force in self.forces:
            data.append(force["pos"][0])
            data.append(force["pos"][1])
            data.append(force["dist"])
            data.append(math.radians(force["force"]))

        np_data = np.array(data, dtype=np.float32)
        self.force_buffer.orphan(np_data.nbytes)
        self.force_buffer.write(np_data)
        self.force_buffer.bind_to_storage_buffer(2)

    def compute_gpu_data(self):
        self.objects.sort(key=lambda x: x["pos"][1])

        objects = []
        self.num_objects = 0
        for obj in self.objects:
            objects.append(obj["pos"][0])
            objects.append(obj["pos"][1])
            objects.append(0)
            objects.append(obj["texture"])
            self.num_objects += 1

        data = np.array(objects, dtype=np.float32)
        self.object_buffer.orphan(data.nbytes)
        self.object_buffer.write(data)
        self.object_buffer.bind_to_storage_buffer(1)

    def update_and_render(self):
        res = engine.data.internal_size
        camera_offset = engine.vector2_to_list(engine.elems["Camera"].get_raylib_pos())
        camera_scale = engine.elems["Camera"].get_raylib_zoom()

        self._compute_gpu_force_data()

        if self.render_shadows:
            self.shadow_prog["RES"] = res
            self.shadow_prog["camera_offset"] = camera_offset
            self.shadow_prog["camera_scale"] = camera_scale

            self.shadow_prog["shadow_size"] = self.shadow_size
            self.shadow_prog["shadow_darkness"] = self.shadow_darkness

            self.shadow_vao.render(mode=moderngl.TRIANGLE_STRIP, instances=self.num_objects)

        atlas = self.assets.get_atlas()

        atlas.use(0)
        self.grass_prog["atlas"] = 0
        self.grass_prog["num_forces"] = self.num_forces

        self.grass_prog["RES"] = res
        self.grass_prog["atlas_size"] = (atlas.width, atlas.height)

        self.grass_prog["camera_offset"] = camera_offset
        self.grass_prog["camera_scale"] = camera_scale

        self.grass_prog["time"] = engine.get_time()
        self.grass_prog["delta"] = engine.get_frame_time()
        self.grass_prog["adaptivity"] = self.adaptivity
        self.grass_prog["wind_speed"] = self.wind_speed
        self.grass_prog["wind_force"] = math.radians(self.wind_force)

        self.grass_prog["render_ao"] = self.render_ao

        self.grass_vao.render(mode=moderngl.TRIANGLE_STRIP, instances=self.num_objects)

class FoliageAssets:
    def __init__(self, ctx, compute_ao=True):
        self.ctx = ctx
        self.compute_ao = compute_ao

        self.textures = []
        self.texture_buffer = None
        self.atlas = None # computed later

    def get_atlas(self):
        return self.atlas

    def compute_gpu_data(self):
        texture_data = []

        # compute atlas size
        final_width, final_height = 0, 0
        for texture in self.textures:
            final_width += texture["texture"].width

            tex_height = texture["texture"].height
            if tex_height > final_height:
                final_height = tex_height

        # render textures onto atlas
        atlas = engine.load_render_texture(final_width, final_height)
        engine.begin_texture_mode(atlas)

        cur_x = 0
        for texture in self.textures:
            tex = texture["texture"]

            texture_data.append(tex.width)
            texture_data.append(tex.height)
            texture_data.append(texture["origin"][0])
            texture_data.append(texture["origin"][1])
            texture_data.append(cur_x)
            texture_data.append(0) # padding

            engine.draw_texture_rec(
                tex,
                (0, 0, tex.width, -tex.height),
                (cur_x, atlas.texture.height - tex.height),
                engine.WHITE
            )
            cur_x += texture["texture"].width

        engine.end_texture_mode()

        # convert atlas to moderngl texture
        self.atlas = engine.mgl.rl_tex_to_mgl_tex(self.ctx, atlas.texture)

        # upload texture data buffer
        if self.texture_buffer: self.texture_buffer.release()
        self.texture_buffer = self.ctx.buffer(np.array(texture_data, dtype=np.float32))
        self.texture_buffer.bind_to_storage_buffer(0)

        # unload stuff
        engine.unload_texture(atlas.texture)

    def add_texture(self, texture, origin=None):
        if origin is None:
            origin = (
                int(texture.width / 2),
                int(texture.height / 2),
            )

        self.textures.append({
            "texture": texture,
            "origin": origin
        })