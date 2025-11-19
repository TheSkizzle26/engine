import engine
import json


class Input:
    def __init__(self):
        self.input_map = {}

    def load_input_map(self, path):
        if not path:
            return

        with open(path, "r") as file:
            mappings = json.loads(file.read())

        for mapping in mappings.items():
            if type(mapping[1]) in [list, tuple]:
                self.input_map[mapping[0]] = mapping[1]
            else:
                self.input_map[mapping[0]] = [mapping[1]]

    def is_pressed(self, key):
        return any(
            eval(
                f"engine.is_key_pressed(engine.KeyboardKey.{keycode})"
            ) if keycode.startswith("KEY_") else eval(
                f"engine.is_mouse_button_pressed(engine.MouseButton.{keycode})"
            )
            for keycode in self.input_map[key]
        )

    def is_down(self, key):
        return any(
            eval(
                f"engine.is_key_down(engine.KeyboardKey.{keycode})"
            ) if keycode.startswith("KEY_") else eval(
                f"engine.is_mouse_button_down(engine.MouseButton.{keycode})"
            )
            for keycode in self.input_map[key]
        )


input = Input()