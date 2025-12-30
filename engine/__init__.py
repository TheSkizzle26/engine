try:
    from pyray import *
except ImportError:
    raise ImportError('Package "raylib" needs to be installed!')

import engine.mgl
from engine.utils import sign
from engine.data import data
from engine.vector import vector2_to_list, vector3_to_list, list_to_vector2, list_to_vector3
from engine.rect import Rect, FRect
from engine.assets import assets
from engine.input import input
from engine.mouse import get_mouse_pos, get_internal_mouse_pos, get_internal_mouse_x, get_internal_mouse_y
from engine.event_bus import event
from engine.sound import play_sound_ex
from engine.elements import Element, ElementSingleton, Elements, elems
from engine.entities import Entity, EntitySingleton
from engine.scene import scene, Scene
from engine.camera import Camera
from engine.cpu_foliage import CPUFoliageManager, CPUFoliageAssets
from engine.foliage import FoliageManager, FoliageAssets
from engine.particles import ParticleManager, Particle
from engine.logs import log, LogType
from engine.game import Program, init

from engine.deprecated import Rectangle, Camera2D, load_texture, load_sound

print("Engine loaded successfully!")
log.write("Engine loaded successfully!")