from classes.unit import Unit
from utils import constants


class Tank2(Unit):
    def __init__(self):
        super().__init__(name='Tank2', unit_type='Tank2', hp=constants.TANK_HP, atk_points=constants.TANK_ATK,
                         def_points=constants.TANK_DEFENSE)

    # Implement the special method
    def special(self, team):
        # Find the unit with the least hp and add permanent defense points
        min_hp_unit = min(team, key=lambda unit: unit.get_hp())
        increased_def = min_hp_unit.get_def_points() + constants.PERMANENT_DEF_INCREASE
        min_hp_unit.set_def_points(increased_def)
