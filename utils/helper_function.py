import unit_menu

# some helper functions

# get the units dictionary the player chose
def get_ai_chosen():
    return unit_menu.UnitMenu.ai_chosen

# get the units dictionary the AI chose
def get_player_chosen():
    return unit_menu.UnitMenu.player_chosen

# get the units queue for fight
def get_queue():
    return unit_menu.UnitMenu.queue

# get the units' uid by names
def get_uid(name):
    if name == 'Warrior1':
        return 1
    if name == 'Warrior2':
        return 2
    if name == 'Tank1':
        return 3
    if name == 'Tank2':
        return 4
    if name == 'Wizard1':
        return 5
    if name == 'Wizard2':
        return 6