import engine


def vector2_to_list(vec: engine.Vector2):
    return vec.x, vec.y

def vector3_to_list(vec: engine.Vector3):
    return vec.x, vec.y, vec.z

def list_to_vector2(l):
    return engine.Vector2(l[0], l[1])

def list_to_vector3(l):
    return engine.Vector3(l[0], l[1], l[2])