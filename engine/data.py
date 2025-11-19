from dataclasses import dataclass


@dataclass
class EngineData:
    screen_size: tuple[int, int] = (0, 0)


data = EngineData()