import engine


class Entity(engine.Element):
    def __init__(self, pos, size, singleton=False, custom_id=None):
        super().__init__(singleton=singleton, custom_id=custom_id)

        self.pos = list(pos)
        self.size = size

        self.collisions = {"up": False, "down": False, "left": False, "right": False}

    def rect(self) -> engine.Rect:
        return engine.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def move_and_collide(self, collision_rects: list[engine.Rect], frame_movement):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        self.pos[0] += frame_movement[0]
        rect = self.rect()

        for other in collision_rects:
            if not rect.colliderect(other):
                continue

            if frame_movement[0] > 0:
                rect.right = other.left
                self.collisions["right"] = True
            elif frame_movement[0] < 0:
                rect.left = other.right
                self.collisions["left"] = True

            self.pos[0] = rect.x

        self.pos[1] += frame_movement[1]
        rect = self.rect()

        for other in collision_rects:
            if not rect.colliderect(other):
                continue

            if frame_movement[1] > 0:
                rect.bottom = other.top
                self.collisions["bottom"] = True
            elif frame_movement[1] < 0:
                rect.top = other.bottom
                self.collisions["top"] = True

            self.pos[1] = rect.y

class EntitySingleton(Entity):
    def __init__(self, pos, size, custom_id=None):
        super().__init__(pos, size, singleton=True, custom_id=custom_id)