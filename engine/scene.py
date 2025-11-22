import engine


class Scene(engine.ElementSingleton):
    def on_load(self):
        ...

    def on_unload(self):
        ...

    def update(self, *args, **kwargs):
        ...

    def render(self, *args, **kwargs):
        ...

class SceneManager:
    def __init__(self):
        super().__init__()

        self._scene: Scene = Scene()

    def switch(self, scene: Scene):
        self._scene.on_unload()
        self._scene = scene
        self._scene.on_load()

    def update(self, *args, **kwargs):
        self._scene.update(*args, **kwargs)

    def render(self, *args, **kwargs):
        self._scene.render(*args, **kwargs)


scene = SceneManager()