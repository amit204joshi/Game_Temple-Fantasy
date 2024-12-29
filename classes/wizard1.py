from classes.unit import Unit
from utils import constants


class Wizard1(Unit):
    def __init__(self):
        super().__init__(name='Wizard1', unit_type='Wizard1', hp=constants.WIZARD_HP, atk_points=constants.WIZARD_ATK,
                         def_points=constants.WIZARD_DEFENSE)

    # Implement the special method
    def special(self, team):
        # Increase overall hp
        for unit in team:
            hp_after_healing = min(unit.get_hp() * (1 + constants.HP_INCREASE_RATE), unit.get_full_hp())
            unit.set_hp(hp_after_healing)
