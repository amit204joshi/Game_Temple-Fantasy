from classes.team import Team

class Player:
    def __init__(self, name="Player_name", is_ai=False):
        self.__name = name
        self.__team = Team(name)
        self.__is_ai = is_ai

    # getters
    def get_name(self):
        return self.__name
    def get_team(self):
        return self.__team
    def get_is_ai(self):
        return self.__is_ai

    # setters
    def set_name(self, name):
        self.__name = name
    def set_team(self, name):
        self.__team.set_name(name)

    # Add unit to team
    def add_unit_to_team(self, unit):
        self.__team.add_unit(unit)
    def remove_unit_from_team(self, unit):
        self.__team.remove_unit(unit)