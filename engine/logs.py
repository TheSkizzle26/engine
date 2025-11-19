import engine
from dataclasses import dataclass
from enum import Enum, auto


class LogType(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass
class Log:
    message: str
    send_time: float
    type: LogType

class LogSystem:
    def __init__(self):
        self.logs: list[Log] = []
        self.log_duration = 4.0

        self.padding = 8
        self.font_size = 30
        self.shadow_offset = 1
        self.font = engine.load_font("")

        self.type_colors = {
            LogType.INFO: (255, 255, 255),
            LogType.WARNING: (255, 255, 0),
            LogType.ERROR: (255, 0, 0),
        }

        self.log_path = "log.txt"

        with open(self.log_path, "w") as file:
            file.write("") # clear log file

        self._is_font_initialized = False

    def init_font(self):
        self.font = engine.load_font_ex("engine/assets/font.ttf", self.font_size, None, 0)
        self._is_font_initialized = True

    def write(self, message: str, log_type: LogType = LogType.INFO):
        message = f"{f"[{str(log_type).split(".")[1]}] " if log_type != LogType.INFO else ""}{message}"

        self.logs.insert(
            0,
            Log(message, engine.get_time(), log_type)
        )

        with open(self.log_path, "a") as file:
            file.write(f"[{round(engine.get_time(), 3)}] {message}\n")

    def update(self):
        if len(self.logs) == 0:
            return

        now = engine.get_time()

        if now - self.logs[len(self.logs) - 1].send_time >= self.log_duration:
            self.logs.pop()

    def render(self):
        if not self._is_font_initialized:
            raise BaseException("Font not initialized! Call engine.log.init_font() to fix.")

        now = engine.get_time()
        bottom_y = engine.data.screen_size[1] - self.padding

        for log in self.logs:
            alpha = 1 - ((now - log.send_time) - (self.log_duration * 0.85)) / (self.log_duration * 0.15)
            alpha = engine.clamp(alpha, 0, 1)

            pos = (self.padding, bottom_y - self.font.baseSize)
            color = self.type_colors[log.type]

            engine.draw_text_ex(
                self.font,
                log.message,
                (pos[0] + self.shadow_offset, pos[1] + self.shadow_offset),
                self.font_size,
                0,
                (0, 0, 0, int(alpha * 255))
            )
            engine.draw_text_ex(
                self.font,
                log.message,
                pos,
                self.font_size,
                0,
                (color[0], color[1], color[2], int(alpha*255))
            )
            bottom_y -= self.font.baseSize

log = LogSystem()