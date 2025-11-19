import engine
import json


class Input:
    def __init__(self):
        self.input_map = {}

    def load_input_map(self, path):
        if not path:
            return

        with open(path, "r") as file:
            self.input_map = json.loads(file.read())

    def is_pressed(self, key):
        keycode = self.input_map[key]

        return eval(
            f"engine.is_key_pressed(engine.KeyboardKey.{keycode})"
        ) if keycode.startswith("KEY_") else eval(
            f"engine.is_mouse_button_pressed(engine.MouseButton.{keycode})"
        )

    def is_down(self, key):
        keycode = self.input_map[key]

        return eval(
            f"engine.is_key_down(engine.KeyboardKey.{keycode})"
        ) if keycode.startswith("KEY_") else eval(
            f"engine.is_mouse_button_down(engine.MouseButton.{keycode})"
        )


input = Input()