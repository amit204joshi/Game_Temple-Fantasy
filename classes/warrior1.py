from classes.unit import Unit
from utils import constants


class Warrior1(Unit):
    def __init__(self):
        super().__init__(name='Warrior1', unit_type='Warrior1', hp=constants.WARRIOR_HP,
                         atk_points=constants.WARRIOR_ATK, def_points=constants.WARRIOR_DEFENSE)

    # Implement the special method
    def special(self, target):
        # Double attack
        super().attack(target)
        super().attack(target)
