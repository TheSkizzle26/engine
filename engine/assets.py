import engine
import os


class Assets:
    def __init__(self):
        self.texture_path = None
        self.sound_path = None

        self.textures = {}
        self.sounds = {}

        self.textures_suffixes = ["png", "jpg"]
        self.sound_suffixes = ["wav", "mp3", "flac"]

    @staticmethod
    def dict2list(dictionary, sort_by_number=False):
        items = sorted(
            dictionary.items(),
            key=(lambda x: int(x[0])) if sort_by_number else None
        )
        return [item[1] for item in items]

    def set_image_path(self, path):
        self.texture_path = path.removesuffix("/")

    def set_sound_path(self, path):
        self.sound_path = path.removesuffix("/")

    @staticmethod
    def insert_asset(target, ids, name, value):
        cur = target

        for i, id in enumerate(ids):
            cur.setdefault(id, {})
            cur = cur[id]

        cur[name] = value

    def load_texture(self, full_path, path):
        ids = path.split("/")
        name = ids.pop().split(".")[0]
        texture = engine.load_texture(full_path)

        print(f"loading image: {path}")

        self.insert_asset(self.textures, ids, name, texture)

    def load_sound(self, full_path, path):
        ids = path.split("/")
        name = ids.pop().split(".")[0]
        sound = engine.load_sound(full_path)

        print(f"loading sound: {path}")

        self.insert_asset(self.sounds, ids, name, sound)

    def file_op_recursive(self, start_path, path, func, suffixes):
        path = path.removesuffix("/")

        for p in os.listdir(path):
            parts = p.split(".")

            if parts[len(parts) - 1] in suffixes:
                func(f"{path}/{p}", f"{path}/{p}".removeprefix(start_path + "/"))
            elif os.path.isdir(path):
                self.file_op_recursive(start_path, f"{path}/{p}", func, suffixes)

    def load_asset_type(self, path, func, suffixes):
        self.file_op_recursive(path, path, func, suffixes)

    def load_assets(self):
        start_time = engine.get_time()
        engine.log.write("Loading assets...")

        if self.texture_path: self.load_asset_type(self.texture_path, self.load_texture, self.textures_suffixes)
        if self.sound_path: self.load_asset_type(self.sound_path, self.load_sound, self.sound_suffixes)

        engine.log.write(f"Asset loading took {round(engine.get_time() - start_time, 2)} seconds.")


assets = Assets()
textures = assets.textures
sounds = assets.sounds