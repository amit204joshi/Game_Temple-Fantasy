import random
from abc import ABC, abstractmethod
from utils import constants


class Unit(ABC):
    # constructor
    def __init__(self, name, unit_type, hp, atk_points, def_points):
        self.__name = name
        self.__type = unit_type
        self.__hp = hp
        self.__full_hp = hp
        self.__atk_points = atk_points
        self.__def_points = def_points
        self.__cooldown_time = 2
        self.__defending = False
        self.__special_used = False
        self.__is_poisoned = False

    # Getters
    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_hp(self):
        return self.__hp

    def get_full_hp(self):
        return self.__full_hp

    def get_atk_points(self):
        return self.__atk_points

    def get_def_points(self):
        return self.__def_points

    def get_cooldown_time(self):
        return self.__cooldown_time

    def get_defending(self):
        return self.__defending

    def get_special_used(self):
        return self.__special_used

    def get_is_poisoned(self):
        return self.__is_poisoned

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_type(self, unit_type):
        self.__type = unit_type

    def set_hp(self, hp):
        self.__hp = hp

    def set_atk_points(self, atk_points):
        self.__atk_points = atk_points

    def set_def_points(self, def_points):
        self.__def_points = def_points

    def set_cooldown_time(self, time):
        self.__cooldown_time = time

    def set_defending(self):
        self.__defending = False

    def set_special_used(self, status):
        self.__special_used = status

    def set_is_poisoned(self, status):
        self.__is_poisoned = status

    # Check if the unit is still alive
    def is_alive(self):
        return self.__hp > 0

    # If the unit is poisoned, decrease hp for the rest of the game
    def poison_loss(self):
        self.__hp = self.__hp * (1 - constants.POISON_RATE)

    # Ordinary attack ability
    def attack(self, target):
        self.set_special_used(False)
        if not target.get_defending():
            hp_after_atk = target.get_hp() - max(0, self.__atk_points - target.__def_points + random.randint(
                constants.RANDOM_RANGE_START, constants.RANDOM_RANGE_END))
            target.set_hp(max(0, hp_after_atk))
        else:
            hp_after_atk = target.get_hp() - constants.HALF * max(0,
                                                                  self.__atk_points - target.__def_points + random.randint(
                                                                      constants.RANDOM_RANGE_START,
                                                                      constants.RANDOM_RANGE_END))
            target.set_hp(max(0, hp_after_atk))

    # AI attack ability
    def ai_attack(self, oppo_team):
        alive_units = [unit for unit in oppo_team if unit.is_alive()]
        # select unit with the minimum hp from the opponent's team
        min_hp_target = min(alive_units, key=lambda unit: unit.get_hp())
        # attack the target
        self.attack(min_hp_target)
        return min_hp_target

    # Ordinary defend ability
    def defend(self):
        self.set_special_used(False)
        self.__defending = True

    # Abstract method for special attack
    @abstractmethod
    def special(self, obj):
        pass

    # Override the __str__ method
    def __str__(self):
        return (f'Name: {self.__name}\nType: {self.__type}\nHP: {self.__hp}\n'
                f'ATK: {self.__atk_points}\nDEF: {self.__def_points}')
