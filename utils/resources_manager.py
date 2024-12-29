import os
import pygame
from utils import constants

class ResourcesManager:
    # image resources for game menu
    game_menu_resources = {
            'background': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'background3.png')),(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)),
            'attack': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'attack.png')),(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)),
            'defend': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'defend.png')),(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)),
            'sp_atk': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'sp_atk.png')),(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)),
            'sp_atk_no': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'sp_atk_no.png')),
                                                (constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)),
            'arrow': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'arrow.png')),
                                        (constants.POISON_WIDTH, constants.POISON_HEIGHT)),
            'round': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'round.png')),
                                        (constants.ROUND_WIDTH, constants.ROUND_HEIGHT))
    }

    # image resources for main menu
    main_menu_resources = {
        'background': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'background1.png')),(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)),
        'title': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'title.png')),(500, 250)),
        'start_normal': pygame.image.load(os.path.join(constants.IMG_PATH, 'start_normal.png')),
        'start_hover': pygame.image.load(os.path.join(constants.IMG_PATH, 'start_hover.png')),
        'start_click': pygame.image.load(os.path.join(constants.IMG_PATH, 'start_hover.png')),
        'exit_normal': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_normal.png')),
        'exit_hover': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_hover.png')),
        'exit_click': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_hover.png'))
    }

    # image resources for unit menu
    unit_menu_resources = {
        'background': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'background2.png')),(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)),
        'Warrior1': pygame.image.load(os.path.join(constants.IMG_PATH, 'warrior1_avatar.png')),
        'Warrior2': pygame.image.load(os.path.join(constants.IMG_PATH, 'warrior2_avatar.png')),
        'Tank1': pygame.image.load(os.path.join(constants.IMG_PATH, 'tank1_avatar.png')),
        'Tank2': pygame.image.load(os.path.join(constants.IMG_PATH, 'tank2_avatar.png')),
        'Wizard1': pygame.image.load(os.path.join(constants.IMG_PATH, 'wizard1_avatar.png')),
        'Wizard2': pygame.image.load(os.path.join(constants.IMG_PATH, 'wizard2_avatar.png'))
    }

    # image resources for cd bar
    cd_bar_resources = {
        'cd_0': pygame.transform.scale(pygame.image.load(os.path.join(constants.CD_PATH, 'cd_0.png')),(constants.CD_BAR_WIDTH, constants.CD_BAR_HEIGHT)),
        'cd_1': pygame.transform.scale(pygame.image.load(os.path.join(constants.CD_PATH, 'cd_1.png')),(constants.CD_BAR_WIDTH, constants.CD_BAR_HEIGHT)),
        'cd_2': pygame.transform.scale(pygame.image.load(os.path.join(constants.CD_PATH, 'cd_2.png')),(constants.CD_BAR_WIDTH, constants.CD_BAR_HEIGHT)),
    }

    # image resources for poisoned
    poisoned_resources = {'poisoned': pygame.transform.scale(pygame.image.load(os.path.join(constants.POISON_PATH, 'poisoned.png')),(constants.POISON_WIDTH, constants.POISON_HEIGHT))}

    # image resources for end scene
    end_scene_resources = {
        'background': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'background2.png')),
                                             (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)),
        'win_text': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'win_text.png')), (650, 350)),
        'lose_text': pygame.transform.scale(pygame.image.load(os.path.join(constants.IMG_PATH, 'lose_text.png')), (650, 350)),
        'restart_normal': pygame.image.load(os.path.join(constants.IMG_PATH, 'restart_normal.png')),
        'restart_hover': pygame.image.load(os.path.join(constants.IMG_PATH, 'restart_hover.png')),
        'restart_click': pygame.image.load(os.path.join(constants.IMG_PATH, 'restart_hover.png')),
        'exit_normal': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_normal.png')),
        'exit_hover': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_hover.png')),
        'exit_click': pygame.image.load(os.path.join(constants.IMG_PATH, 'exit_hover.png'))
    }