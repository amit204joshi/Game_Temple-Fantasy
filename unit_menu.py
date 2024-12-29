from time import sleep
import pygame
import unit_surface
from classes.tank1 import Tank1
from classes.tank2 import Tank2
from classes.warrior1 import Warrior1
from classes.warrior2 import Warrior2
from classes.wizard1 import Wizard1
from classes.wizard2 import Wizard2
from utils import constants
from utils.resources_manager import ResourcesManager
from collections import deque

class UnitMenu:
    player_chosen = {}
    ai_chosen = {}
    queue = deque()

    def __init__(self, surface):
        # import display surface
        self.__surface = surface
        # import image resources for unit menu
        self.__unit_menu_resources = ResourcesManager.unit_menu_resources
        # Initialize surface for all the six units
        self.__warrior1_surface = None
        self.__warrior2_surface = None
        self.__tank1_surface = None
        self.__tank2_surface = None
        self.__wizard1_surface = None
        self.__wizard2_surface = None
        # The user can only choose 3 units
        self.__click_times = 3
        # Check if the game is start
        self.__start_game = False
        self.__is_initialized = False
        # Set up the unit pool (6 units)
        self.__unit_pool = [1,2,3,4,5,6]
        # import the knock sound
        self.__knock_sound = pygame.mixer.Sound("resources/sounds/knock_sound.mp3")

    @staticmethod
    def reset():
        # reset static attributes
        UnitMenu.player_chosen = {}
        UnitMenu.ai_chosen = {}
        UnitMenu.queue = deque()

    # getters
    def get_start_game(self):
        return self.__start_game

    def draw(self):
        # Draw the background
        self.__surface.blit(self.__unit_menu_resources['background'].convert_alpha(), (0, 0))

        # Draw all the six unit surfaces and draw them on the display surface
        # Draw Warrior1 surface
        warrior1 = unit_surface.UnitSurface(self.__unit_menu_resources['Warrior1'].convert_alpha(), 'Warrior1', constants.WARRIOR_HP, constants.WARRIOR_ATK, constants.WARRIOR_DEFENSE, constants.WARRIOR1_SP_ATK)
        self.__warrior1_surface = warrior1.draw_rects_on_unit_rect()
        self.__surface.blit(self.__warrior1_surface, (40, 30))

        # Draw Warrior2 surface
        warrior2 = unit_surface.UnitSurface(self.__unit_menu_resources['Warrior2'].convert_alpha(), 'Warrior2', constants.WARRIOR_HP, constants.WARRIOR_ATK, constants.WARRIOR_DEFENSE, constants.WARRIOR2_SP_ATK)
        self.__warrior2_surface = warrior2.draw_rects_on_unit_rect()
        self.__surface.blit(self.__warrior2_surface, (540, 30))

        # Draw Tank1 surface
        tank1 = unit_surface.UnitSurface(self.__unit_menu_resources['Tank1'].convert_alpha(), 'Tank1', constants.TANK_HP, constants.TANK_ATK, constants.TANK_DEFENSE, constants.TANK1_SP_ATK)
        self.__tank1_surface = tank1.draw_rects_on_unit_rect()
        self.__surface.blit(self.__tank1_surface, (40, 220))

        # Draw Tank1 surface
        tank2 = unit_surface.UnitSurface(self.__unit_menu_resources['Tank2'].convert_alpha(), 'Tank2', constants.TANK_HP, constants.TANK_ATK, constants.TANK_DEFENSE, constants.TANK2_SP_ATK)
        self.__tank2_surface = tank2.draw_rects_on_unit_rect()
        self.__surface.blit(self.__tank2_surface, (540, 220))

        # Draw Wizard1 surface
        wizard1 = unit_surface.UnitSurface(self.__unit_menu_resources['Wizard1'].convert_alpha(), 'Wizard1', constants.WIZARD_HP, constants.WIZARD_ATK, constants.WIZARD_DEFENSE, constants.WIZARD1_SP_ATK)
        self.__wizard1_surface = wizard1.draw_rects_on_unit_rect()
        self.__surface.blit(self.__wizard1_surface, (40, 410))

        # Draw Wizard2 surface
        wizard2 = unit_surface.UnitSurface(self.__unit_menu_resources['Wizard2'].convert_alpha(), 'Wizard2', constants.WIZARD_HP,constants.WIZARD_ATK, constants.WIZARD_DEFENSE, constants.WIZARD2_SP_ATK)
        self.__wizard2_surface = wizard2.draw_rects_on_unit_rect()
        self.__surface.blit(self.__wizard2_surface, (540, 410))

    def handle_events(self):
        for event in pygame.event.get():
            # If the user has already chosen 3 units, start the game
            if self.__click_times == 0:
                # Set the start game flag to True
                self.__start_game = True
                # Delay 1s for better user experience
                sleep(1)
                break
            # Handle mouse button down events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the player clicked on the Warrior1's surface
                if self.__warrior1_surface.get_rect(topleft=(60, 30)).collidepoint(event.pos):
                    # If Warrior1 has not been chosen, add it to the player's team
                    if 1 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[1] = self.choose_unit(1)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(1)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Check if the player clicked on the Warrior2's surface
                elif self.__warrior2_surface.get_rect(topleft=(520, 30)).collidepoint(event.pos):
                    if 2 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[2] = self.choose_unit(2)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(2)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Check if the player clicked on the Tank1's surface
                elif self.__tank1_surface.get_rect(topleft=(60, 220)).collidepoint(event.pos):
                    if 3 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[3] = self.choose_unit(3)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(3)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Check if the player clicked on the Tank2's surface
                elif self.__tank2_surface.get_rect(topleft=(520, 220)).collidepoint(event.pos):
                    if 4 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[4] = self.choose_unit(4)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(4)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Check if the player clicked on the Wizard1's surface
                elif self.__wizard1_surface.get_rect(topleft=(60, 410)).collidepoint(event.pos):
                    if 5 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[5] = self.choose_unit(5)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(5)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Check if the player clicked on the Wizard2's surface
                elif self.__wizard2_surface.get_rect(topleft=(520, 410)).collidepoint(event.pos):
                    if 6 not in UnitMenu.player_chosen:
                        UnitMenu.player_chosen[6] = self.choose_unit(6)
                        # Remove the unit from the pool
                        self.__unit_pool.remove(6)
                        # Decrease the number of units the player can choose
                        self.__click_times -= 1
                        # Play the knock sound effect
                        self.__knock_sound.play()
                # Set up AI's team
                self.set_up_ai_chosen()

    def set_up_ai_chosen(self):
        # Check if the player has already chosen exactly 3 units
        if len(UnitMenu.player_chosen) == 3:
            # Add the remaining 3 units in the unit pool to AI's team
            for idx in self.__unit_pool:
                UnitMenu.ai_chosen[idx] = self.choose_unit(idx)

    # helper function to determine the unit chosen
    def choose_unit(self, num_choice):
        if num_choice == 1:  # Warrior1
            return Warrior1()
        elif num_choice == 2:  # Warrior2
            return Warrior2()
        elif num_choice == 3:  # Tank1
            return Tank1()
        elif num_choice == 4:  # Tank2
            return Tank2()
        elif num_choice == 5:  # Wizard1
            return Wizard1()
        else:  # Wizard2
            return Wizard2()

    def update_surface(self):
        # update surface
        self.draw()
        self.handle_events()