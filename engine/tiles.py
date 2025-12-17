import engine


class Tile:
    def __init__(self, pos, tile_size,
                 texture, collision_type):
        self.pos = pos
        self.tile_size = tile_size
        self.texture = texture
        self.collision_type = collision_type

    def render(self):
        engine.draw_texture(self.texture, self.pos[0] * self.tile_size[0], self.pos[1] * self.tile_size[1], engine.WHITE)


class TileMap:
    def __init__(self, tile_size):
        self.tiles = {}
        self.tile_size = tile_size

    def tile_id(self, pos):
        return f"{int(pos[0])};{int(pos[1])}"

    def set_at(self, pos, tile):
        self.tiles[self.tile_id(pos)] = tile

    def del_at(self, pos):
        tile_id = self.tile_id(pos)

        if tile_id in self.tiles:
            del self.tiles[tile_id]

    def render(self):
        camera_topleft = engine.elems["Camera"].get_world_topleft()
        camera_size = engine.elems["Camera"].get_world_size()

        topleft_chunk_pos = (
            camera_topleft[0] // self.tile_size[0],
            camera_topleft[1] // self.tile_size[1]
        )

        for cy in range(int(topleft_chunk_pos[1] - 1),
                        int(topleft_chunk_pos[1] + camera_size[1] // self.tile_size[1] + 4)):
            for cx in range(int(topleft_chunk_pos[0] - 1),
                            int(topleft_chunk_pos[0] + camera_size[0] // self.tile_size[0] + 2)):
                tile_id = self.tile_id((cx, cy))

                if tile_id in self.tiles:
                    self.tiles[tile_id].render()