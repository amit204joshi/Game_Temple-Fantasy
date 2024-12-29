import os
import pygame
from button import Button
from utils.resources_manager import ResourcesManager

class EndScene:
    def __init__(self, surface, player_win):
        self.__surface = surface
        self.__end_scene_running = True
        self.__is_start = False
        self.__should_exit = False
        self.__player_win = player_win

        self.__bubble_sound = pygame.mixer.Sound("resources/sounds/bubble_sound.mp3")
        self.__start_is_played = False
        self.__exit_is_played = False

        self.__end_scene_resources = ResourcesManager.end_scene_resources
        # Create restart and exit buttons
        self.__restart_button = Button(385, 320, 230, 110, 0,
                                       self.__end_scene_resources['restart_normal'].convert_alpha(),
                                       self.__end_scene_resources['restart_hover'].convert_alpha(),
                                       self.__end_scene_resources['restart_click'].convert_alpha())
        self.__exit_button = Button(385, 430, 220, 110, 0,
                                    self.__end_scene_resources['exit_normal'].convert_alpha(),
                                    self.__end_scene_resources['exit_hover'].convert_alpha(),
                                    self.__end_scene_resources['exit_click'].convert_alpha())
        # Win game sound
        self.__win_sound = pygame.mixer.Sound("resources/sounds/win_sound.wav")
        self.__win_sound.set_volume(0.6)
        self.__is_win_sound_played = False
        # Lose game sound
        self.__lose_sound = pygame.mixer.Sound("resources/sounds/lose_sound.wav")
        self.__lose_sound.set_volume(0.3)
        self.__is_lose_sound_played = False

    def stop_sound(self):
        # Stop bubble sound
        self.__bubble_sound.stop()

    def handle_events(self):
        # Process each event that have occurred
        for event in pygame.event.get():
            # Check if the user wants to close the window and exit the game
            if event.type == pygame.QUIT:
                self.__end_scene_running = False
                self.__should_exit = True

            if event.type == pygame.MOUSEMOTION:
                # Handle button hover states
                if self.__restart_button.is_hover_on(event.pos):
                    self.__restart_button.set_status(1)
                else:
                    self.__restart_button.set_status(0)

                if self.__exit_button.is_hover_on(event.pos):
                    self.__exit_button.set_status(1)
                else:
                    self.__exit_button.set_status(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                if self.__restart_button.is_hover_on(event.pos):
                    self.__restart_button.set_status(2)
                    self.__is_start = True
                    self.__end_scene_running = False

                if self.__exit_button.is_hover_on(event.pos):
                    self.__end_scene_running = False
                    self.__should_exit = True  # Set exit flag on window close

    # Add new method to check if should exit
    def should_exit(self):
        return self.__should_exit

    def draw(self):
        # Draw background
        self.__surface.blit(self.__end_scene_resources['background'].convert_alpha(), (0, 0))

        # Draw win/lose text
        if self.__player_win:
            self.__surface.blit(self.__end_scene_resources['win_text'].convert_alpha(), (180, 10))
            # Play win game sound
            if not self.__is_win_sound_played:
                self.__win_sound.play()
                self.__is_win_sound_played = True
        else:
            self.__surface.blit(self.__end_scene_resources['lose_text'].convert_alpha(), (180, 10))
            # Play lose game sound
            if not self.__is_lose_sound_played:
                self.__lose_sound.play()
                self.__is_lose_sound_played = True

        # Draw buttons
        self.__restart_button.draw(self.__surface)
        self.__exit_button.draw(self.__surface)

    # Update the end scene surface
    def update_surface(self):
        self.handle_events()
        self.draw()
        self.play_sound()
        # Returns a bool: Whether the end scene is still running
        return self.__end_scene_running

    def is_start(self):
        return self.__is_start

    def play_sound(self):
        # If the restart button is hovered on or clicked be the mouse (status 1 or 2), and the sound has not been played yet
        if (self.__restart_button.get_status() == 1 or self.__restart_button.get_status() == 2) and not self.__start_is_played:
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
        # If the restart button's status is normal (0), reset the flag to allow the sound to play again
        if self.__restart_button.get_status() == 0:
            self.__start_is_played = False
        # If the exit button's status is normal (0), reset the flag to allow the sound to play again
        if self.__exit_button.get_status() == 0:
            self.__exit_is_played = False