# Constants for defending
HALF = 0.5

# Constants for random range
RANDOM_RANGE_START = -5
RANDOM_RANGE_END = 10

# Constants for warrior type
WARRIOR_HP = 150
WARRIOR_ATK = 50
WARRIOR_DEFENSE = 10

# Constants for tank type
TANK_HP = 200
TANK_ATK = 35
TANK_DEFENSE = 15

# Constants for wizard type
WIZARD_HP = 150
WIZARD_ATK = 35
WIZARD_DEFENSE = 10

# Constant for AOE (Area of Effect) rate
AOE_RATE = 0.5
# Constant for defense increase
DEF_INCREASE = 5
# Constant for hp increase rate
HP_INCREASE_RATE = 0.1
# Constant for permanent defense increase
PERMANENT_DEF_INCREASE = 2
# Constant for poison rate
POISON_RATE = 0.05

# Constant for zooming in the size of button
ZOOM_IN = 0.2

# Constants of width of display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Constants for message bars
MESSAGE_TEXT_START_X = 10
MESSAGE_TEXT_START_Y = 285
MESSAGE_COLOR = (255,255,255)
MESSAGE_BG_WIDTH = 330
MESSAGE_BG_HEIGHT = 140
MESSAGE_BG_START_X = 5
MESSAGE_BG_START_Y = 275
MESSAGE_BG_COLOR = (0, 0, 0, 128)

# Constants for health bars and cooldown bars
HP_BAR_WIDTH = 150
HP_BAR_HEIGHT = 20
CD_BAR_WIDTH = 150
CD_BAR_HEIGHT = 20
SPACING = 60
LEFT_X = 70
RIGHT_X = WINDOW_WIDTH - HP_BAR_WIDTH - 35
TOP_Y = 60

# Constants for poisoned icon
POISON_WIDTH = 35
POISON_HEIGHT = 35
POISON_LEFT_X = 185
POISON_RIGHT_X = 585
POISON_TOP_Y = 420

# Constants for arrow
ARROW_TOP_Y = 550

# Constants for round
ROUND_HEIGHT = 110
ROUND_WIDTH = ROUND_HEIGHT * 3.535
ROUND_X = 250
ROUND_Y = 165
NUMBER_Y = 185
ROUND_SPACING = 5

# Constants for unit name
UNIT_NAME_LEFT_X = 175
UNIT_NAME_RIGHT_X = 575
UNIT_NAME_Y = 470

# Path of resources
IMG_PATH = 'resources/images/menu'
UNITS_IDLE_IMG_PATH = 'resources/images/units/idle'
UNITS_ATK_IMG_PATH = 'resources/images/units/atk'
UNITS_SP_IMG_PATH = 'resources/images/units/sp'
UNITS_HURT_IMG_PATH = 'resources/images/units/hurt'
UNITS_DEAD_IMG_PATH = 'resources/images/units/dead'
CD_PATH = 'resources/images/cd'
POISON_PATH = 'resources/images/poison'

# Path of font
FONT_PATH = 'resources/font'

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (216, 191, 216)
FIREBRICK =	(178, 34, 34)
LIGHTGRAY = (185, 185, 185)

# Special attack ability
WARRIOR1_SP_ATK = 'Double Attack'
WARRIOR2_SP_ATK = 'AOE'
TANK1_SP_ATK = 'Fortify'
TANK2_SP_ATK = 'Shield'
WIZARD1_SP_ATK = 'Restore HP'
WIZARD2_SP_ATK = 'Poison Enemy'

# Unit menu's width and height
UNIT_SURFACE_WIDTH = 420
UNIT_SURFACE_HEIGHT = 160

# button's width and height
BUTTON_WIDTH = 65
BUTTON_HEIGHT = 65