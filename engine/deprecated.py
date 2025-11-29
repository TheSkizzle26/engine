from warnings import deprecated


@deprecated("Use engine.Rect instead.")
class Rectangle: ...

@deprecated("Use engine.Camera instead.")
class Camera2D: ...
@deprecated("3D cameras not supported.")
class Camera3D: ...