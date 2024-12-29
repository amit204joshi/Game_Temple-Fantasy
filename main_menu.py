from time import sleep
import pygame
from button import Button
from utils.resources_manager import ResourcesManager

class MainMenu:
    def __init__(self, surface):
        # Get the display surface
        self.__surface = surface
        # Import images resources for main menu
        self.__main_menu_resources = ResourcesManager.main_menu_resources
        # Create a Button instance for start button
        self.__start_button = Button(385, 320, 230, 110, 0,
                                     self.__main_menu_resources['start_normal'].convert_alpha(),
                                     self.__main_menu_resources['start_hover'].convert_alpha(),
                                     self.__main_menu_resources['start_click'].convert_alpha())
        # Create a Button instance for exit button
        self.__exit_button = Button(385, 430, 220, 110, 0,
                                    self.__main_menu_resources['exit_normal'].convert_alpha(),
                                    self.__main_menu_resources['exit_hover'].convert_alpha(),
                                    self.__main_menu_resources['exit_click'].convert_alpha())
        # Check if the game is running
        self.__running = True
        # Check if the game is start
        self.__is_start = False
        # Import buttons bubble sound
        self.__bubble_sound = pygame.mixer.Sound("resources/sounds/bubble_sound.mp3")
        # Check if the bubble sound for start button is played
        self.__start_is_played = False
        # Check if the bubble sound for exit button is played
        self.__exit_is_played = False

    def stop_sound(self):
        # Stop bubble sound
        self.__bubble_sound.stop()

    def handle_events(self):
        # Check to see if user wants to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user wants to quit, stop running the game
                self.__running = False
            # Handle mouse motion events
            if event.type == pygame.MOUSEMOTION:
                # If the mouse is hover on the start button, set the status to hover on(1)
                if self.__start_button.is_hover_on(event.pos):
                    self.__start_button.set_status(1)
                else:
                    # If the mouse is not hover on the start button, set the status to normal(0)
                    self.__start_button.set_status(0)
                # If the mouse is hover on the exit button, set the status to hover on(1)
                if self.__exit_button.is_hover_on(event.pos):
                    self.__exit_button.set_status(1)
                else:
                    # If the mouse is not hover on the exit button, set the status to normal(0)
                    self.__exit_button.set_status(0)
            # Handle mouse button down events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the start button is clicked, set the status to click(2)
                if self.__start_button.is_hover_on(event.pos):
                    self.__start_button.set_status(2)
                    # Delay 1 second before entering next surface
                    sleep(1)
                    # Set the start game flag to True
                    self.__is_start = True
                # If the exit button is clicked, set the running game flag to False
                if self.__exit_button.is_hover_on(event.pos):
                    self.__running = False

    def draw(self):
        # Fill the display with static assets
        self.__surface.blit(self.__main_menu_resources['background'].convert_alpha(), (0, 0))
        self.__surface.blit(self.__main_menu_resources['title'].convert_alpha(), (250, 70))
        # Draw the button
        self.__start_button.draw(self.__surface)
        self.__exit_button.draw(self.__surface)

    def update_surface(self):
        # update surface
        self.handle_events()
        self.draw()
        self.play_sound()
        # return the running status
        return self.__running

    def is_start(self):
        # Check if the game is start
        return self.__is_start

    def play_sound(self):
        # If the start button is hovered on or clicked be the mouse (status 1 or 2), and the sound has not been played yet
        if (self.__start_button.get_status() == 1 or self.__start_button.get_status() == 2) and not self.__start_is_played:
            # Play the sound
            self.__bubble_sound.play()
            # Set flag to prevent playing the sound multiple times
            self.__start_is_played = True
        # If the exit button is hovered on or clicked be the mouse (status 1 or 2), and the sound has not been played yet
        if (self.__exit_button.get_status() == 1 or self.__exit_button.get_status() == 2) and not self.__exit_is_played:
            # Play the sound
            self.__bubble_sound.play()
            # Set flag to prevent playing the sound multiple times
            self.__exit_is_played = True
        # If the start button's status is normal (0), reset the flag to allow the sound to play again
        if self.__start_button.get_status() == 0:
            self.__start_is_played = False
        # If the exit button's status is normal (0), reset the flag to allow the sound to play again
        if self.__exit_button.get_status() == 0:
            self.__exit_is_played = False