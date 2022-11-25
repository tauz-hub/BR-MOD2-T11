from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import *
from dino_runner.components.power_ups.power_up import PowerUp
import random


class Sword(PowerUp):
    def __init__(self):
        self.image = SWORD
        PowerUp.__init__(self, self.image, SWORD_TYPE,
                         5000, random.randint(5, 10))
