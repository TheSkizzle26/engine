import engine


def play_sound_ex(sound, volume, pitch, pan):
    engine.play_sound(sound)
    engine.set_sound_volume(sound, volume)
    engine.set_sound_pitch(sound, pitch)
    engine.set_sound_pan(sound, pan)