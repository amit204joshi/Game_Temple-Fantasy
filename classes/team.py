class Team:
    # constructor
    def __init__(self, name):
        self.__name = name
        self.__units = []

    # getters
    def get_name(self):
        return self.__name
    def get_units(self):
        return self.__units

    # setters
    def set_name(self, name):
        self.__name = name

    # Add unit to team
    def add_unit(self, unit):
        self.__units.append(unit)

    # Remove unit from team
    def remove_unit(self, unit):
        self.__units.remove(unit)

    # Rearrange unit in team
    def rearrange_unit(self, order):
        self.__units = [self.__units[i - 1] for i in order]

    # Override the __str__ method
    def __str__(self):
        return f"Team {self.__name}:\n" + "\n".join([str(unit) for unit in self.__units])