from dino_runner.utils.constants import HAMMER
from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import *
from dino_runner.components.power_ups.power_up import PowerUp
import random


class Hammer(PowerUp):
    def __init__(self):
        self.image = HAMMER
        PowerUp.__init__(self, self.image, HAMMER_TYPE,
                         2000, random.randint(5, 15))
