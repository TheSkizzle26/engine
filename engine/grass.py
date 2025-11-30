import engine

"""
chunk syntax:

{
    {"texture": ..., "pos": (x, y), "angle": radians}
}

angle is 0 facing top
"""


class GrassManager:
    def __init__(self, chunk_size=64):
        self.chunks = {}
        self.chunk_size = chunk_size

    def chunk_id(self, chunk_pos):
        return f"{int(chunk_pos[0])};{int(chunk_pos[1])}"

    def spawn_blade(self, pos, texture):
        chunk_pos = (
            pos[0] // self.chunk_size,
            pos[1] // self.chunk_size
        )

        chunk = self.chunks[self.chunk_id(chunk_pos)]

        idx = 0
        while idx < len(chunk):
            if chunk[idx]["pos"][1] > pos[1]:
                break

            idx += 1

        chunk.insert({
            "texture": texture,
            "pos": pos,
            "angle": 0
        })

    def update(self):
        ...

    def render(self):
        # TODO: only render visible chunks

        for chunk in self.chunks:
            for blade in chunk:
                engine.draw_texture(blade["texture"], blade["pos"][0], blade["pos"][1], engine.WHITE)
