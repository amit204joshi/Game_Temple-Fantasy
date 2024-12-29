from classes.unit import Unit
from utils import constants


class Wizard2(Unit):
    def __init__(self):
        super().__init__(name='Wizard2', unit_type='Wizard2', hp=constants.WIZARD_HP, atk_points=constants.WIZARD_ATK,
                         def_points=constants.WIZARD_DEFENSE)

    # Implement the special method
    def special(self, target):
        target.set_is_poisoned(True)
