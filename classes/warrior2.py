from classes.unit import Unit
from utils import constants


class Warrior2(Unit):
    def __init__(self):
        super().__init__(name='Warrior2', unit_type='Warrior2', hp=constants.WARRIOR_HP,
                         atk_points=constants.WARRIOR_ATK, def_points=constants.WARRIOR_DEFENSE)

    # Implement the special method
    def special(self, oppo_team):
        # AOE (Area of effect)
        for unit in oppo_team:
            hp_after_atk = max(unit.get_hp() - self.get_atk_points() * constants.AOE_RATE,0)
            unit.set_hp(hp_after_atk)
