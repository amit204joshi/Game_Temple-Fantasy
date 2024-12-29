import os
import pygame
from utils import constants
from utils.resources_manager import ResourcesManager

class StatusBar:
    def __init__(self, surface):
        self.__surface = surface
        self.__cd_bar_resources = ResourcesManager.cd_bar_resources
        self.__poisoned_resources = ResourcesManager.poisoned_resources

    def draw_single_hp_bar(self, x, y, unit):
        # Calculate current health ratio
        ratio = unit.get_hp() / unit.get_full_hp()

        # Draw the background bar (max HP) in light gray
        pygame.draw.rect(self.__surface, constants.LIGHTGRAY, (x, y, constants.HP_BAR_WIDTH, constants.HP_BAR_HEIGHT))
        # Draw the current HP bar in firebrick color, scaled by ratio
        current_width = constants.HP_BAR_WIDTH * ratio
        pygame.draw.rect(self.__surface, constants.FIREBRICK, (x, y, current_width, constants.HP_BAR_HEIGHT))
        # Draw border in white
        pygame.draw.rect(self.__surface, constants.WHITE, (x, y, constants.HP_BAR_WIDTH, constants.HP_BAR_HEIGHT), 2)

        font_path = os.path.join(constants.FONT_PATH, 'Gixel.ttf')

        # Draw HP text
        font_hp_text = pygame.font.Font(font_path, 18)
        hp_text = "HP"
        # Create a surface that displays the hp_text string
        hp_text_surface = font_hp_text.render(hp_text, True, constants.WHITE)
        # Align hp_text rectangle to the left of the bar with a gap of 20 pixels
        hp_text_rect = hp_text_surface.get_rect(midright=(x - 20, y + constants.HP_BAR_HEIGHT // 2))
        self.__surface.blit(hp_text_surface, hp_text_rect)

        # Draw HP value text
        font_hp_value = pygame.font.Font(font_path, 15)
        hp_value_text = f"{int(unit.get_hp())}/{int(unit.get_full_hp())}"
        # Create a surface that displays the hp_value_text string
        hp_value_surface = font_hp_value.render(hp_value_text, True, constants.WHITE)
        # Set the hp_value_text rectangle's center to be centered horizontally and vertically within the bar
        hp_value_text_rect = hp_value_surface.get_rect(center=(x + constants.HP_BAR_WIDTH // 2, y + constants.HP_BAR_HEIGHT // 2))
        self.__surface.blit(hp_value_surface, hp_value_text_rect)

        # Create name surface for status bar
        font_status_name = pygame.font.Font(font_path, 20)
        status_name_surface = font_status_name.render(unit.get_name(), True, constants.WHITE)
        # Set the unit name of the player team top left corner to the top left of the HP bar
        status_name_rect = status_name_surface.get_rect(topleft=(x, y - constants.HP_BAR_HEIGHT))
        self.__surface.blit(status_name_surface, status_name_rect)

    # Draw names above units
    def draw_unit_name(self, x, y, unit):
        # Load the font from the specified path and set its size to 16
        font_path = os.path.join(constants.FONT_PATH, 'Gixel.ttf')
        font_unit_name = pygame.font.Font(font_path, 16)
        # Render the unit's name as white text
        unit_name_surface = font_unit_name.render(unit.get_name(), True, constants.WHITE)
        # Position the text's rectangle with its bottom-left corner at (x, y)
        unit_name_rect = unit_name_surface.get_rect(bottomleft=(x, y))
        # Draw the rendered text onto the surface
        self.__surface.blit(unit_name_surface, unit_name_rect)

    def draw_single_cd_bar(self, x, y, unit):
        # Get the unit's current cooldown time
        cd_time = unit.get_cooldown_time()

        # Select the appropriate CD bar image based on cooldown time
        if cd_time == 0:
            cd_img = self.__cd_bar_resources['cd_2'].convert_alpha()  # Full CD bar
        elif cd_time == 1:
            cd_img = self.__cd_bar_resources['cd_1'].convert_alpha()  # Half CD bar
        else:  # cd_time == 2
            cd_img = self.__cd_bar_resources['cd_0'].convert_alpha()  # Empty CD bar

        # Draw CD text
        font_path = os.path.join(constants.FONT_PATH, 'Gixel.ttf')
        font_cd_text = pygame.font.Font(font_path, 18)
        cd_text = "CD"
        # Create a surface that displays the cd_text string
        cd_text_surface = font_cd_text.render(cd_text, True, constants.WHITE)
        # Align cd_text rectangle to the left of the bar with a gap of 20 pixels
        cd_text_rect = cd_text_surface.get_rect(midright=(x - 20, y + cd_img.get_height() // 2))
        self.__surface.blit(cd_text_surface, cd_text_rect)

        # Draw the CD bar image at the specified position
        self.__surface.blit(cd_img, (x, y))

    def draw_single_poisoned_icon(self, x, y, unit):
        # Draw poisoned icon
        if unit.get_is_poisoned():
            poisoned_icon = self.__poisoned_resources['poisoned'].convert_alpha()
            self.__surface.blit(poisoned_icon, (x, y))