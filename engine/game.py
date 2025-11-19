import engine
import sys


def init(size, title, target_fps=0, flags=0, monitor=0,
         image_path="", audio_path=""):
    engine.set_config_flags(flags)
    engine.init_window(size[0], size[1], title)
    engine.set_window_monitor(monitor)
    engine.set_target_fps(target_fps)

    engine.assets.set_image_path(image_path)
    engine.assets.set_sound_path(audio_path)

class Game(engine.ElementSingleton):
    def __init__(self):
        super().__init__()

    @staticmethod
    def quit():
        engine.close_window()
        engine.close_audio_device()

        sys.exit()

    def run(self):
        while True:
            self.update()
            self.render()