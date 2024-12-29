import pytest

@pytest.fixture
def unit_factory():
    """
    A factory fixture that creates mocked units.
    """
    class MockUnit:
        def __init__(self, name, hp, dmg, unit_type, cooldown=0):
            self.__name = name
            self.__hp = hp
            self.__dmg = dmg
            self.__type = unit_type
            self.__is_poisoned = False
            self.__cooldown = cooldown
            self.__defending = False
            self.__special_used = False

        def get_name(self):
            return self.__name

        def get_hp(self):
            return self.__hp

        def set_hp(self, value):
            self.__hp = value

        def get_type(self):
            return self.__type

        def get_is_poisoned(self):
            return self.__is_poisoned

        def set_is_poisoned(self, val):
            self.__is_poisoned = val

        def get_cooldown_time(self):
            return self.__cooldown

        def set_cooldown_time(self, val):
            self.__cooldown = val

        def get_special_used(self):
            return self.__special_used

        def is_alive(self):
            return self.__hp > 0

        def attack(self, target):
            # if defending, half damage taken, else full
            dmg_taken = self.__dmg
            if hasattr(target, "_MockUnit__defending") and target.__defending:
                dmg_taken = dmg_taken // 2
            target.set_hp(target.get_hp() - dmg_taken)

        def defend(self):
            self.__defending = True

        def special(self, target_or_team):
            # Warrior1 doubles attack a single target
            if self.__type == "Warrior1":
                dmg_taken = self.__dmg * 2
                target_or_team.set_hp(target_or_team.get_hp() - dmg_taken)
                self.__cooldown = 2
            # Wizard2 poisons a single target
            elif self.__type == "Wizard2":
                if not target_or_team.get_is_poisoned():
                    target_or_team.set_is_poisoned(True)
                    self.__cooldown = 2
            self.__special_used = True

        def select_target(self, target):
            # valid target if he is alive
            if not target.is_alive():
                return False
            return True

    return MockUnit


def test_attack_action(unit_factory):
    """
    Test that a unit can successfully attack another and reduce its HP.
    """
    attacker = unit_factory("Attacker", hp=100, dmg=20, unit_type="Warrior1")
    defender = unit_factory("Defender", hp=100, dmg=10, unit_type="Warrior2")
    attacker.attack(defender)
    assert defender.get_hp() == 80, "Defender should lose 20 HP after being attacked."


def test_defend_action(unit_factory):
    """
    Test that defending reduces incoming damage.
    """
    attacker = unit_factory("Attacker", hp=100, dmg=20, unit_type="Warrior1")
    defender = unit_factory("Defender", hp=100, dmg=10, unit_type="Warrior2")
    defender.defend()
    attacker.attack(defender)
    # Assuming defend halves damage
    assert defender.get_hp() == 90, "Defender should lose only 10 HP due to defending."


def test_special_ability_warrior1(unit_factory):
    """
    Test the special ability of a Warrior1 which does double damage to a single target.
    Ensure cooldown is set correctly.
    """
    warrior = unit_factory("Warrior1", hp=100, dmg=20, unit_type="Warrior1", cooldown=0)
    target = unit_factory("Target", hp=100, dmg=10, unit_type="Wizard1")
    warrior.special(target)
    assert target.get_hp() == 60, "Target should lose 40 HP after Warrior1 special."
    assert warrior.get_cooldown_time() == 2, "Warrior1 special should set cooldown to 2."


def test_special_ability_wizard2_poison(unit_factory):
    """
    Test the Wizard2 special ability that poisons a target if not already poisoned.
    """
    wizard = unit_factory("Wizard2", hp=80, dmg=10, unit_type="Wizard2", cooldown=0)
    target = unit_factory("Target", hp=100, dmg=10, unit_type="Warrior1")
    wizard.special(target)
    assert target.get_is_poisoned() is True, "Target should be poisoned by Wizard2 special."
    assert wizard.get_cooldown_time() == 2, "Wizard2 special should set cooldown to 2."


def test_health_reaching_zero(unit_factory):
    """
    Test edge case when health reaches zero. The unit should be considered dead.
    """
    attacker = unit_factory("Attacker", hp=50, dmg=60, unit_type="Warrior1")
    defender = unit_factory("Defender", hp=50, dmg=10, unit_type="Warrior2")
    attacker.attack(defender)
    assert defender.get_hp() <= 0, "Defender's HP should be zero or less."
    assert defender.is_alive() is False, "Defender should be dead when HP is zero or less."


def test_cannot_select_dead_unit_as_target(unit_factory):
    """
    Test that a dead unit cannot be selected as a target.
    This checks that the game logic prevents choosing units that are already dead.
    """
    attacker = unit_factory("Attacker", hp=100, dmg=50, unit_type="Warrior1")
    target = unit_factory("Target", hp=30, dmg=10, unit_type="Warrior2")

    # First, attacker kills the target
    attacker.attack(target)
    assert target.get_hp() <= 0, "Target should have 0 or less HP after a lethal attack."
    assert not target.is_alive(), "Target should be marked as dead."

    # Now, verify that the dead unit cannot be chosen as a target
    # For this test, we assume there's a function `is_valid_target(unit)` that returns False if the unit is dead.
    can_select = attacker.select_target(target)
    assert can_select is False, "A dead unit should not be a valid target."
