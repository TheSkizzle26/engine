"""
Not very efficient for big projects since it keeps every asset
loaded at all times and doesn't allow to remove an asset since
a reference to it is always stored.
"""

import os
import engine
import random


class Assets:
    def __init__(self, no_file_extension=False):
        self.texture_path = ""
        self.sound_path = ""

        self.assets = {
            "textures": {},
            "sounds": {}
        }

        self.file_types = {
            "textures": ["png", "jpg"],
            "sounds": ["wav", "mp3"]
        }

    @staticmethod
    def hash(item):
        random.seed(item)
        return int.from_bytes(random.randbytes(4))

    def set_texture_path(self, path):
        self.texture_path = path + ("" if path.endswith("/") else "/")

    def set_sound_path(self, path):
        self.sound_path = path + ("" if path.endswith("/") else "/")

    def _load_asset(self, path, base_path, group, func):
        hash = self.hash(path)
        if hash in self.assets[group]:
            return self.assets[group][hash]

        full_path = base_path + path
        asset = func(full_path)

        self.assets[group][hash] = asset
        return asset

    def load_texture(self, path):
        return self._load_asset(path, self.texture_path, "textures", engine.load_texture)

    def load_texture_group(self, path):
        textures = []

        path = path.removesuffix("/")
        full_path = self.texture_path + path

        file_names = [ # should sort the file names by number
            str(i) for i in sorted(
                [int(f[:(len(f)-1) - f[::-1].index(".")]) for f in os.listdir(full_path)]
            )
        ]

        for file in file_names:
            textures.append(self.load_texture(f"{path}/{file}"))

        return textures

    def load_sound(self, path):
        return self._load_asset(path, self.sound_path, "sounds", engine.load_sound)


assets = Assets()