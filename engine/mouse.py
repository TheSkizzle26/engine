import engine


def get_mouse_pos():
    return (
        engine.get_mouse_x(),
        engine.get_mouse_y()
    )

def get_internal_mouse_pos():
    return (
        get_internal_mouse_x(),
        get_internal_mouse_y()
    )

def get_internal_mouse_x():
    return int(engine.get_mouse_x() / engine.data.screen_size[0] * engine.data.internal_size[0])

def get_internal_mouse_y():
    return int(engine.get_mouse_y() / engine.data.screen_size[1] * engine.data.internal_size[1])