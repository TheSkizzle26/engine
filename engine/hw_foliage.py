import moderngl
import engine
import numpy as np
from _cffi_backend import buffer as cffi_buffer
import array


class HWFoliageManager:
    def __init__(self, ctx, foliage_assets, chunk_size=16):
        self.assets = foliage_assets
        self.ctx = ctx


        buf = self.ctx.buffer(np.array([
            0, 0,
            1, 0,
            0, 1,
            1, 1
        ], dtype=np.float32))
        self.program = self.load_program("engine/assets/foliage/foliage.vert", "engine/assets/foliage/foliage.frag")
        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (buf, "2f", "in_vert")
            ]
        )

        self.chunks = {}
        self.chunk_size = chunk_size
        self.visible_chunks = []
        self.num_rendered_objects = 0

        self.gpu_chunk_buffer = None
        self.gpu_texture_data_buffer = None

        for texture in engine.assets.load_texture_group("grass"):
            self.assets.add_texture(texture)
        self.assets.upload_gpu_atlas()
        self.assets.upload_gpu_texture_data()

        self.spawn_object((10, 0), 0)
        #self.spawn_object((30, 10), 2)

    def load_program(self, vert_path, frag_path):
        with open(vert_path, "r") as file:
            vert = file.read()
        with open(frag_path, "r") as file:
            frag = file.read()

        return self.ctx.program(vertex_shader=vert, fragment_shader=frag)

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def get_visible_chunks(self):
        chunks = []

        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.chunk_size,
            camera_topleft[1] // self.chunk_size
        )

        for cy in range(int(topleft_chunk_pos[1] - 1),
                        int(topleft_chunk_pos[1] + camera_size[1] // self.chunk_size + 4)):
            for cx in range(int(topleft_chunk_pos[0] - 1),
                            int(topleft_chunk_pos[0] + camera_size[0] // self.chunk_size + 2)):
                chunk_id = self.chunk_id((cx, cy))

                if chunk_id in self.chunks:
                    chunks.append(self.chunks[chunk_id])

        return chunks

    def upload_gpu_chunk_data(self):
        if len(self.visible_chunks) == 0:
            self.visible_chunks = self.get_visible_chunks()

        if self.gpu_chunk_buffer: self.gpu_chunk_buffer.release()

        self.num_rendered_objects = 0
        data = array.array("f", [])
        for chunk in self.visible_chunks:
            for value in chunk.get_data():
                data.append(value)
                self.num_rendered_objects += 1

        self.gpu_chunk_buffer = self.ctx.buffer(data)
        self.gpu_chunk_buffer.bind_to_storage_buffer(0)

    def set_program_uniforms(self):
        self.program["RES"] = engine.data.internal_size
        #self.program["camera_pos"] = engine.vector2_to_list(engine.elems["Camera"].get_raylib_pos())
        self.program["camera_scale"] = engine.elems["Camera"].get_raylib_zoom()
        self.program["atlas_width"] = self.assets.get_atlas_width()

    def spawn_object(self, pos, texture_idx):
        # find correct idx to insert (sorted by y coord)
        chunk_pos = (
            pos[0] // self.chunk_size,
            pos[1] // self.chunk_size
        )

        chunk_id = self.chunk_id(chunk_pos)
        self.chunks.setdefault(chunk_id, HWFoliageChunk(self, chunk_pos)).spawn_object(pos, texture_idx)

        self.upload_gpu_chunk_data()

    def update_and_render(self):
        self.visible_chunks = self.get_visible_chunks()

        self.assets.use_atlas()
        self.set_program_uniforms()
        self.vao.render(mode=moderngl.TRIANGLE_STRIP, instances=self.num_rendered_objects)

class HWFoliageChunk:
    def __init__(self, manager, chunk_pos):
        self.manager = manager
        self.chunk_pos = chunk_pos

        self.objects = []

    def spawn_object(self, pos, texture_idx):
        idx = 0
        while idx < len(self.objects):
            if self.objects[idx]["pos"][1] > pos[1]:
                break

            idx += 1

        self.objects.insert(idx, {
            "texture": texture_idx,
            "pos": pos,
            "angle": 0
        })

    def get_data(self):
        data = array.array("f")

        for i, object in enumerate(self.objects):
            data.append(object["pos"][0])
            data.append(object["pos"][1])
            data.append(object["texture"])
            data.append(object["angle"])

        return data

class HWFoliageAssets:
    def __init__(self, ctx):
        self.ctx = ctx

        self.textures = []
        self.gpu_atlas = None
        self.atlas_width = 0

        self.gpu_texture_data = None

    def get_atlas_width(self):
        return self.atlas_width

    def use_atlas(self):
        self.gpu_atlas.use(0)

    def upload_gpu_atlas(self):
        # release previous atlas
        if self.gpu_atlas: self.gpu_atlas.release()

        # generate new atlas
        final_width, final_height = 0, 0
        for texture in self.textures:
            texture = texture["texture"]
            final_width += texture.width

            if texture.height > final_height:
                final_height = texture.height

        self.atlas_width = final_width

        atlas = engine.load_render_texture(final_width, final_height)
        engine.begin_texture_mode(atlas)
        current_x = 0

        # draw texture onto atlas
        for texture in self.textures:
            texture["atlas_x"] = current_x
            texture = texture["texture"]
            engine.draw_texture(texture, current_x, 0, engine.WHITE)
            current_x += texture.width

        engine.end_texture_mode()

        # upload atlas to gpu
        atlas_texture = atlas.texture
        image = engine.load_image_from_texture(atlas_texture)

        byte_count = atlas_texture.width * atlas_texture.height * 4
        data = cffi_buffer(image.data, byte_count)

        self.gpu_atlas = self.ctx.texture(
            (final_width, final_height),
            4,
            data=bytes(data)
        )
        self.gpu_atlas.filter = (self.ctx.NEAREST, self.ctx.NEAREST)

        engine.unload_image(image)

    def upload_gpu_texture_data(self):
        if self.gpu_texture_data: self.gpu_texture_data.release()

        data = array.array("f")

        for texture in self.textures:
            data.append(texture["texture"].width)
            data.append(texture["texture"].height)
            data.append(texture["origin"][0])
            data.append(texture["origin"][1])
            data.append(texture["atlas_x"])
            data.append(0)
            data.append(0)
            data.append(0)

        self.gpu_texture_data = self.ctx.buffer(data)
        self.gpu_texture_data.bind_to_storage_buffer(1)

    def add_texture(self, texture: engine.Texture):
        self.textures.append({
            "texture": texture,
            "origin": (texture.width // 2, texture.height // 2),
            "atlas_x": 0
        })