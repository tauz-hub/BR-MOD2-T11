from dino_runner.utils.constants import SHIELD
from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import *
from dino_runner.components.power_ups.power_up import PowerUp
import random


class Shield(PowerUp):
    def __init__(self):
        self.image = SHIELD
        PowerUp.__init__(self, self.image, SHIELD_TYPE,
                         5000, random.randint(5, 10))
