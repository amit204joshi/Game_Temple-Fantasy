import os
import pygame
from utils import constants
from utils.resources_manager import ResourcesManager


class UnitSurface:
    def __init__(self, avatar, unit_name, hp, atk_points, def_points, sp_atk):
        # unit's avatar image
        self.__avatar = avatar
        # unit's name
        self.__unit_name = unit_name
        # unit hp
        self.__hp = hp
        # unit's atk points
        self.__atk_points = atk_points
        # unit's def points
        self.__def_points = def_points
        # unit's special atk ability
        self.__sp_atk = sp_atk

    def draw_rects_on_unit_rect(self):
        # Create a unit surface
        unit_surface = pygame.Surface((constants.UNIT_SURFACE_WIDTH, constants.UNIT_SURFACE_HEIGHT), pygame.SRCALPHA)
        # Load the unit surface image
        surface_img = pygame.image.load(os.path.join(constants.IMG_PATH, 'unit_surface.png')).convert_alpha()
        # Scale the surface image to match the size of the unit surface
        surface_img = pygame.transform.scale(surface_img, (constants.UNIT_SURFACE_WIDTH, constants.UNIT_SURFACE_HEIGHT))
        # Draw the surface image onto the unit surface
        unit_surface.blit(surface_img, (0, 0))

        # Draw the avatar rectangle on the unit rectangle
        # Set the width and height of the avatar
        avatar_width = 120
        avatar_height = 120
        # Calculate the x and y positions for the avatar
        avatar_x = 20
        avatar_y = (unit_surface.get_height() - avatar_height) / 2
        # Create the avatar rect
        avatar_rect = pygame.Rect(avatar_x, avatar_y, avatar_width, avatar_height)
        # Scale the avatar image
        self.__avatar = pygame.transform.scale(self.__avatar, (avatar_width, avatar_height))
        # Draw the avatar image on the avatar rect
        unit_surface.blit(self.__avatar, avatar_rect)

        # Import the path of font
        font_path = os.path.join(constants.FONT_PATH, 'Gixel.ttf')
        # Set the font attributes
        font = pygame.font.Font(font_path, 20)

        # Create texts for attributes
        type_text = font.render(f'Name: {self.__unit_name}', True, constants.WHITE)
        hp_text = font.render(f"HP: {self.__hp}", True, constants.WHITE)
        atk_text = font.render(f"ATK: {self.__atk_points}", True, constants.WHITE)
        def_text = font.render(f"DEF: {self.__def_points}", True, constants.WHITE)
        sp_atk_text = font.render(f"SPECIALITY: {self.__sp_atk}", True, constants.WHITE)

        # Draw the texts on the unit surface
        unit_surface.blit(type_text, (avatar_x + avatar_width + 10, avatar_y + 5))
        unit_surface.blit(hp_text, (avatar_x + avatar_width + 10, avatar_y + 30))
        unit_surface.blit(atk_text, (avatar_x + avatar_width + 10, avatar_y + 55))
        unit_surface.blit(def_text, (avatar_x + avatar_width + 10, avatar_y + 80))
        unit_surface.blit(sp_atk_text, (avatar_x + avatar_width + 10, avatar_y + 105))

        # Return the created unit surface
        return unit_surface