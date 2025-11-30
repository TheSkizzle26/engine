import engine


class Camera(engine.ElementSingleton):
    def __init__(self, pos, zoom, speed):
        super().__init__()

        self._pos = list(pos)
        self._target_pos = pos
        self._zoom = zoom
        self._target_zoom = zoom
        self._speed = speed

        self._camera = engine.Camera2D()

    def set_pos(self, pos):
        self._pos = list(pos)
        self._target_pos = pos

    def set_target_pos(self, pos):
        self._target_pos = pos

    def move_target(self, offset):
        self._target_pos = (
            self._target_pos[0] + offset[0],
            self._target_pos[1] + offset[1],
        )

    def set_zoom(self, zoom):
        self._zoom = zoom
        self._target_zoom = zoom

    def set_target_zoom(self, zoom):
        self._target_zoom = zoom

    def set_speed(self, speed):
        self._speed = speed

    def get_world_pos(self):
        return (
            self._pos[0],
            self._pos[1]
        )

    def get_world_topleft(self):
        return (
            (self._pos[0] - engine.data.internal_size[0]*0.5 / self._zoom),
            (self._pos[1] - engine.data.internal_size[1]*0.5 / self._zoom)
        )

    def update(self):
        delta = engine.get_frame_time()

        self._pos[0] += (self._target_pos[0] - self._pos[0]) * self._speed * delta
        self._pos[1] += (self._target_pos[1] - self._pos[1]) * self._speed * delta
        self._zoom += (self._target_zoom - self._zoom) * self._speed * delta

    def begin(self):
        self._camera.offset = engine.Vector2(
            -self._pos[0] * self._zoom + engine.data.internal_size[0]*0.5,
            -self._pos[1] * self._zoom + engine.data.internal_size[1]*0.5
        )
        self._camera.zoom = self._zoom

        engine.begin_mode_2d(self._camera)

    @staticmethod
    def end():
        engine.end_mode_2d()