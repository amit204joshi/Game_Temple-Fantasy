from time import sleep
import pygame
import main_menu as main_menu_module
import unit_menu as unit_menu_module
import game_menu as game_menu_module
from utils import constants

#Initialize pygame
pygame.init()

#Set display menu
display_surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Temple Fantasy 2024")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set sounds and music
pygame.mixer.music.load('resources/sounds/main_menu_music.mp3')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

# Create instances of different menu modules
main_menu = main_menu_module.MainMenu(display_surface)
unit_menu = unit_menu_module.UnitMenu(display_surface)
game_menu = game_menu_module.GameMenu(display_surface)

#The main game loop
running = True
is_music_playing = False

# Start game
while running:
    # Main menu surface updates
    running = main_menu.update_surface()

    if main_menu.is_start():
        # If the user choose to start the game, stop the main menu music
        main_menu.stop_sound()
        # Show the unit selection menu
        unit_menu.update_surface()

        # If the user select three units, automatically start fighting
        if unit_menu.get_start_game():
            # reset unit selection data
            unit_menu.reset()

            # Change to battle music
            if not is_music_playing:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(500)
                    pygame.time.delay(500)
                pygame.mixer.music.load('resources/sounds/game_menu_music.mp3')
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)
                is_music_playing = True

            # Draw battle surface and units
            game_menu.draw_units()
            game_menu.update_surface()

            # Get the end scene if game is over
            end_scene = game_menu.update_game_logic()

            # If game is over and end scene is returned
            if end_scene:
                # Delay before showing end scene
                sleep(1.5)
                # Change to main game music again
                is_music_playing = False
                if not is_music_playing:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.fadeout(500)
                    pygame.mixer.music.load('resources/sounds/main_menu_music.mp3')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    is_music_playing = True

                # Control flag for end scene loop
                end_running = True
                # Loop for handling end scene
                while end_running and running:
                    # Update and draw end scene
                    end_running = end_scene.update_surface()
                    # Check if player clicked exit button
                    if end_scene.should_exit():
                        # Exit entire game
                        running = False
                        break
                    # Check if player clicked restart button
                    if end_scene.is_start():
                        # Reset game state by creating new instances
                        unit_menu = unit_menu_module.UnitMenu(display_surface)
                        game_menu = game_menu_module.GameMenu(display_surface)
                        is_music_playing = False
                        # Exit end scene loop and return to unit selection
                        end_running = False
                        break
                    # Update display and maintain frame rate
                    pygame.display.update()
                    clock.tick(FPS)

                # After breaking from end scene loop
                if end_scene.is_start():
                    continue  # Return to unit selection screen if restart clicked
                if not running:
                    break  # Exit main game loop if exit was clicked

    #Update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()