import math


def clamp(val, min, max):
    if val < min: return min
    if val > max: return max
    return val

def sign(val):
    return 1 if val > 0 else (-1 if val < 0 else 0)