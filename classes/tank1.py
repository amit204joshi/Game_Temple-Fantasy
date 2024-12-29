from classes.unit import Unit
from utils import constants


class Tank1(Unit):
    def __init__(self):
        super().__init__(name='Tank1', unit_type='Tank1', hp=constants.TANK_HP, atk_points=constants.TANK_ATK,
                         def_points=constants.TANK_DEFENSE)

    # Implement the special method
    def special(self, team):
        # Increase overall defense for one turn
        for unit in team:
            increased_defense = unit.get_def_points() + constants.DEF_INCREASE
            unit.set_def_points(increased_defense)
        super().set_special_used(True)

    def reverse_special(self, team):
        self.set_special_used(False)
        # Reverse overall defense after one turn
        for unit in team:
            decreased_defense = unit.get_def_points() - constants.DEF_INCREASE
            unit.set_def_points(decreased_defense)
