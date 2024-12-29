import pygame
import unit_animation
import random
from end_scene import EndScene
from status_bar import StatusBar
from utils import constants
from utils.resources_manager import ResourcesManager
from utils.helper_function import get_ai_chosen, get_player_chosen, get_uid
from utils.constants import POISON_RATE
from collections import deque
import os


class GameMenu:
    def __init__(self, surface):
        # Display surface where all game elements will be rendered
        self.__surface = surface

        # Button's original coordinates
        self.__x, self.__y = 350, 340

        # Delay configurations for AI actions
        self.__ai_delay = 2500  # Delay in milliseconds before AI acts
        self.__ai_action_pending = False
        self.__ai_action_start_time = 0

        # Delay configurations for drawing the action arrow
        self.__arrow_delay = 500
        self.__arrow_pending = False
        self.__arrow_start_time = 0

        # Define rectangles for action buttons (Attack, Defend, Special Attack)
        self.__atk_rect = pygame.rect.Rect(self.__x, self.__y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        self.__def_rect = pygame.rect.Rect(self.__x + 120, self.__y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)
        self.__sp_atk_rect = pygame.rect.Rect(self.__x + 240, self.__y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT)

        # Get the currently chosen player and AI units
        self.__player_chosen = get_player_chosen()
        self.__ai_chosen = get_ai_chosen()

        # Dictionary to store AI units' rectangles for target selection
        self.__ai_rect = {}
        # Queue to manage turn order of units
        self.__queue = deque()

        # Current unit taking action, the chosen action, and the current target
        self.__cur_unit = None
        self.__action_chosen = None
        self.__cur_target = None

        # Counter to track the number of game rounds
        self.__counter = 1

        # Flags to manage game state
        self.__game_begin = False
        self.__game_over = False
        self.__action_prompted = False
        self.__target_prompted = False

        # List to store messages displayed to the player
        self.__messages = []
        self.__message_duration = 6000  # Duration to display each message in milliseconds
        self.__messages_font = pygame.font.SysFont(None, 24)

        # Flags to control sound effects, ensuring each sound plays only once per action
        self.__atk_is_play = False
        self.__def_is_play = False
        self.__sp_atk_is_play = False
        self.__target_is_play = False

        # Load sound effects for button actions and unit actions
        self.__knock_sound = pygame.mixer.Sound("resources/sounds/knock_sound.mp3")

        # Attack sounds for different units
        self.__wa1_atk = pygame.mixer.Sound('resources/sounds/wa1_atk.wav')
        self.__wa2_atk = pygame.mixer.Sound('resources/sounds/wa2_atk.ogg')
        self.__t1_atk = pygame.mixer.Sound('resources/sounds/t1_atk.wav')
        self.__t2_atk = pygame.mixer.Sound('resources/sounds/t2_atk.ogg')
        self.__wi1_atk = pygame.mixer.Sound('resources/sounds/wi1_atk.wav')
        self.__wi2_atk = pygame.mixer.Sound('resources/sounds/wi2_atk.wav')

        # Defend sound for units
        self.__def_sound = pygame.mixer.Sound('resources/sounds/defend_sound.wav')

        # Death sound for units
        self.__death_sound = pygame.mixer.Sound('resources/sounds/death_sound.wav')

        # Set the overall music volume
        pygame.mixer.music.set_volume(0.8)

        # Flags to check if certain sounds have been played
        self.__is_played = False
        self.__death_is_played = False

        # Load game menu resources such as images
        self.__game_menu_resources = ResourcesManager.game_menu_resources

        # Dictionaries to store animations for player and AI units
        self.__player_unit_animations = {}
        self.__ai_unit_animations = {}

    def handle_events(self):
        """
        Handle user input events, specifically mouse button clicks for selecting actions and targets.
        """
        if self.__cur_unit in self.__player_chosen.values():
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.__action_chosen:
                        self.select_action(event.pos)
                        # If action is chosen and doesn't require a target, proceed to execute
                        if self.__action_chosen and not self.action_requires_target():
                            self.__cur_target = None  # No target needed
                    elif self.__action_chosen and self.action_requires_target() and not self.__cur_target:
                        self.select_target(event.pos)
        else:
            # It's not the player's turn, ignore input
            pass

    def add_message(self, text):
        """
        Add a message to the message queue to be displayed to the player.
        """
        current_time = pygame.time.get_ticks()
        message = {'text': text, 'time': current_time}
        self.__messages.append(message)
        # Keep only the latest 6 messages to avoid clutter
        if len(self.__messages) > 6:
            self.__messages = self.__messages[-6:]

        # Write the newly added message to a text file for logging
        # The file will be created if it doesn't exist, and each new message will be appended at the end of the file.
        with open("messages_log.txt", "a", encoding="utf-8") as logfile:
            logfile.write(f"{message['time']}: {message['text']}\n")

    def create_queue(self):
        """
        Initialize the action queue with player and AI units in alternating order.
        """
        self.__queue.clear()
        player_units = list(self.__player_chosen.values())
        ai_units = list(self.__ai_chosen.values())
        for i in range(max(len(player_units), len(ai_units))):
            if i < len(player_units):
                self.__queue.append(player_units[i])
            if i < len(ai_units):
                self.__queue.append(ai_units[i])

    def action_requires_target(self):
        """
        Determine if the currently chosen action requires selecting a target.
        """
        if self.__action_chosen == 1:  # Attack
            return True
        elif self.__action_chosen == 2:  # Defend
            return False
        elif self.__action_chosen == 3:  # Special Ability
            unit_type = self.__cur_unit.get_type()
            # Certain special abilities require a target
            if unit_type in ['Warrior1', 'Wizard2']:
                return True
            else:
                return False

    def select_target(self, pos):
        """
        Select an AI unit as the target based on the mouse click position.
        """
        for unit_id, rect in self.__ai_rect.items():
            if rect.collidepoint(pos):
                target = self.__ai_chosen.get(unit_id)
                if not target.is_alive():
                    self.add_message("You cannot target a dead unit!")
                    return
                self.__cur_target = unit_id
                if not self.__target_is_play:
                    self.__knock_sound.play()
                    self.__target_is_play = True
                break

    def select_action(self, pos):
        """
        Select an action (Attack, Defend, Special Attack) based on the mouse click position.
        """
        # If player clicks the Attack button
        if self.__atk_rect.collidepoint(pos):
            self.__action_chosen = 1
            if not self.__atk_is_play:
                self.__knock_sound.play()
                self.__atk_is_play = True
        # If player clicks the Defend button
        elif self.__def_rect.collidepoint(pos):
            self.__action_chosen = 2
            if not self.__def_is_play:
                self.__knock_sound.play()
                self.__def_is_play = True

            # Play defend sound if not already played
            if not self.__is_played:
                self.__def_sound.play()
                self.__is_played = True

        # If player clicks the Special Attack button
        elif self.__sp_atk_rect.collidepoint(pos):
            # Conditions to enable special attack
            if (self.__cur_unit.get_cooldown_time() == 0 and
                    (self.__cur_unit.get_type() != "Wizard2" or not self.check_all_poisoned(
                        self.__ai_chosen.values()))):
                self.__action_chosen = 3
            if not self.__sp_atk_is_play:
                self.__knock_sound.play()
                self.__sp_atk_is_play = True

    def player_turn(self, unit):
        """
        Execute the player's turn for the given unit based on the chosen action.
        """
        # Update special ability effects for Tank1
        if unit.get_type() == 'Tank1':
            # Reverse effects if special ability was used
            if unit.get_special_used():
                unit.reverse_special(self.__player_chosen.values())

        # Execute the chosen action
        if self.__action_chosen == 1:
            # Handle Attack action
            player_uid = get_uid(unit.get_name())
            player_animation = self.__player_unit_animations[player_uid]
            player_animation.set_status(1)  # Set animation to attack

            # Play attack sound based on unit type
            if not self.__is_played:
                if player_uid == 1:
                    self.__wa1_atk.play()
                elif player_uid == 2:
                    self.__wa2_atk.play()
                elif player_uid == 3:
                    self.__t1_atk.play()
                elif player_uid == 4:
                    self.__t2_atk.play()
                elif player_uid == 5:
                    self.__wi1_atk.play()
                elif player_uid == 6:
                    self.__wi2_atk.play()
                self.__is_played = True

            if self.__cur_target is not None:
                # Apply damage to the targeted AI unit
                ai_uid = get_uid(self.__ai_chosen[self.__cur_target].get_name())
                ai_animation = self.__ai_unit_animations[ai_uid]
                ai_animation.set_status(3)  # Set animation to hurt

        elif self.__action_chosen == 3:
            # Handle Special Attack action
            player_uid = get_uid(unit.get_name())
            player_animation = self.__player_unit_animations[player_uid]
            player_animation.set_status(2)  # Set animation to special attack

            # Play attack sound based on unit type
            if not self.__is_played:
                if player_uid == 1:
                    self.__wa1_atk.play()
                elif player_uid == 2:
                    self.__wa2_atk.play()
                elif player_uid == 3:
                    self.__t1_atk.play()
                elif player_uid == 4:
                    self.__t2_atk.play()
                elif player_uid == 5:
                    self.__wi1_atk.play()
                elif player_uid == 6:
                    self.__wi2_atk.play()
                self.__is_played = True

            if self.__cur_target is not None:
                # Apply damage or effects to the targeted AI unit
                ai_uid = get_uid(self.__ai_chosen[self.__cur_target].get_name())
                ai_animation = self.__ai_unit_animations[ai_uid]
                ai_animation.set_status(3)  # Set animation to hurt

        # Perform the action and check if it's completed
        action_completed = self.player_take_action(unit)
        if action_completed:
            # Update cooldowns based on the action taken
            self.update_cd(self.__action_chosen, unit)
        return action_completed

    def player_take_action(self, unit):
        """
        Execute the chosen action for the player unit and update game messages.
        """
        action_completed = False
        if self.__action_chosen == 1:  # Attack
            target = self.__ai_chosen[self.__cur_target]
            unit.attack(target)
            self.add_message(f"{unit.get_name()} attacked {target.get_name()}!")
            action_completed = True
        elif self.__action_chosen == 2:  # Defend
            unit.defend()
            self.add_message(f"{unit.get_name()} defends for one turn.")
            action_completed = True
        elif self.__action_chosen == 3:  # Special Ability
            action_completed = self.special_action(unit)
        return action_completed

    def special_action(self, unit):
        """
        Execute the special ability of the unit based on its type.
        """
        action_completed = False
        if unit.get_type() == 'Warrior1':
            # Double attack a specific target
            target = self.__ai_chosen[self.__cur_target]
            unit.special(target)
            self.add_message(f"{unit.get_name()} double attacked {target.get_name()}!")
            action_completed = True
        elif unit.get_type() == 'Warrior2':
            # Area of Effect (AOE) attack on all enemy units
            unit.special(self.__ai_chosen.values())
            self.add_message(f"{unit.get_name()} dealt an AOE!")
            action_completed = True
        elif unit.get_type() == 'Tank1':
            # Enhance team's defense for one turn
            unit.special(self.__player_chosen.values())
            self.add_message("Your team's defense enhanced for one turn!")
            action_completed = True
        elif unit.get_type() == 'Tank2':
            # Permanently enhance one ally's defense
            unit.special(self.__player_chosen.values())
            self.add_message("One ally's defense enhanced forever!")
            action_completed = True
        elif unit.get_type() == 'Wizard1':
            # Recover some health for the team
            unit.special(self.__player_chosen.values())
            self.add_message("Your team recovered some health!")
            action_completed = True
        elif unit.get_type() == 'Wizard2':
            # Poison a target enemy unit if not already poisoned
            target = self.__ai_chosen[self.__cur_target]
            if not target:
                # Wait for the player to select a target
                action_completed = False
                return action_completed
            if target.get_is_poisoned():
                self.add_message("It's already poisoned!")
                self.__cur_target = None
                action_completed = False
                return action_completed
            # Apply poison to the target unit
            unit.special(target)
            self.add_message(f"{target.get_name()} was poisoned!")
            action_completed = True
        return action_completed

    def ai_turn(self, unit):
        """
        Execute the AI's turn for the given unit.
        """
        # Update special ability effects for Tank1
        if unit.get_type() == 'Tank1':
            # Reverse effects if special ability was used
            if unit.get_special_used():
                unit.reverse_special(self.__ai_chosen.values())

        # Execute the AI's chosen action
        self.ai_take_action(unit)

    def ai_take_action(self, unit):
        """
        Determine and execute the AI's action based on its current state and abilities.
        """
        # Conditions to use special ability
        if (unit.get_cooldown_time() == 0 and
                (unit.get_type() != "Wizard2" or not self.check_all_poisoned(self.__player_chosen.values()))):
            self.ai_special_action(unit)
            # Update cooldown after using special ability
            self.update_cd(3, unit)
        else:
            # Randomly choose between Attack and Defend
            basic_ability = random.randint(0, 1)
            if basic_ability == 0:
                # Perform Attack
                target_unit = unit.ai_attack(self.__player_chosen.values())
                self.add_message(f" -AI {unit.get_name()} attacked {target_unit.get_name()}.")
                # Update cooldown after attacking
                self.update_cd(1, unit)
            else:
                # Perform Defend
                unit.defend()
                self.add_message(f" -AI {unit.get_name()} defends for one turn.")
                # Update cooldown after defending
                self.update_cd(2, unit)

    def ai_special_action(self, unit):
        """
        Execute the AI's special ability based on its type.
        """
        if unit.get_type() == 'Warrior1':
            # Double attack the enemy with the lowest HP
            alive_units = [unit for unit in self.__player_chosen.values() if unit.is_alive()]
            min_hp_target = min(alive_units, key=lambda unit1: unit1.get_hp())
            unit.special(min_hp_target)
            self.add_message(f" -AI {unit.get_name()} double attacked {min_hp_target.get_name()}!")
        elif unit.get_type() == 'Warrior2':
            # Perform an AOE attack on all enemy units
            unit.special(self.__player_chosen.values())
            self.add_message(f" -AI {unit.get_name()} dealt an AOE!")
        elif unit.get_type() == 'Tank1':
            # Enhance AI team's defense for one turn
            unit.special(self.__ai_chosen.values())
            self.add_message(" -AI team's defense enhanced for one turn!")
        elif unit.get_type() == 'Tank2':
            # Permanently enhance one AI ally's defense
            unit.special(self.__ai_chosen.values())
            self.add_message(" -One AI ally's defense enhanced forever!")
        elif unit.get_type() == 'Wizard1':
            # Recover health for AI team
            unit.special(self.__ai_chosen.values())
            self.add_message(" -AI team recovered some health!")
        elif unit.get_type() == 'Wizard2':
            # Poison a player unit that is not already poisoned
            target = None
            for oppo_unit in self.__player_chosen.values():
                if not oppo_unit.get_is_poisoned():
                    target = oppo_unit
                    break
            unit.special(target)
            self.add_message(f" -AI {unit.get_name()} poisoned {target.get_name()}!")

    def update_cd(self, action, unit):
        """
        Update the cooldown time for a unit based on the action performed.
        """
        cur_cd_time = unit.get_cooldown_time()
        if action in [1, 2]:  # Attack or Defend
            if cur_cd_time > 0:
                unit.set_cooldown_time(cur_cd_time - 1)
        elif action == 3:  # Special Ability
            unit.set_cooldown_time(2)  # Reset cooldown to 2 turns

    def check_poison(self, unit):
        """
        Apply poison damage to a unit if it is poisoned.
        """
        if unit.get_is_poisoned():
            hp_after_poison = unit.get_hp() * (1 - POISON_RATE)
            unit.set_hp(max(0, hp_after_poison))
            self.add_message(f"{unit.get_name()} is poisoned, HP dropped!")

    def check_all_poisoned(self, team):
        """
        Check if all alive units in the specified team are poisoned.
        """
        all_poisoned = True
        alive_units = [unit for unit in team if unit.is_alive()]
        for oppo_unit in alive_units:
            if not oppo_unit.get_is_poisoned():
                all_poisoned = False
                break
        return all_poisoned

    def remove_dead_unit(self):
        """
        Remove dead units from the action queue and handle their death animations and sounds.
        """
        alive_units = []
        for unit in self.__queue:
            if unit.is_alive():
                alive_units.append(unit)
            else:
                # If unit is dead, set its animation status to death
                uid = get_uid(unit.get_name())
                if uid in self.__player_chosen:
                    self.__player_unit_animations[uid].set_status(4)  # Death animation
                else:
                    self.__ai_unit_animations[uid].set_status(4)  # Death animation

                # Play death sound effect if not already played
                if not self.__death_is_played:
                    self.__death_sound.play()
                    self.__death_is_played = True

        # Update the queue with only alive units
        self.__queue = deque(alive_units)

    def is_game_over(self):
        """
        Determine if the game has ended by checking if all units of one team are dead.
        """
        player_units_alive = any(unit.is_alive() for unit in self.__player_chosen.values())
        ai_units_alive = any(unit.is_alive() for unit in self.__ai_chosen.values())
        # The game is over if one team has no alive units
        return not player_units_alive or not ai_units_alive

    def get_winner(self):
        """
        Identify the winner of the game based on which team still has alive units.
        """
        player_units_alive = any(unit.is_alive() for unit in self.__player_chosen.values())
        ai_units_alive = any(unit.is_alive() for unit in self.__ai_chosen.values())
        if not player_units_alive:
            return "AI"
        elif not ai_units_alive:
            return "Player"
        else:
            return None

    def game_begin(self):
        """
        Initialize the game by creating the action queue and setting the first unit.
        """
        if not self.__queue:
            self.create_queue()
        if self.__queue:
            self.__cur_unit = self.__queue.popleft()

    def reset_attributes(self):
        """
        Reset key attributes after a unit has taken its turn.
        """
        self.__action_chosen = None
        self.__cur_target = None
        self.__ai_action_pending = False
        self.__atk_is_play = False
        self.__def_is_play = False
        self.__is_played = False
        self.__death_is_played = False
        self.__sp_atk_is_play = False
        self.__target_is_play = False
        self.__action_prompted = False
        self.__target_prompted = False

    def draw_units(self):
        """
        Render all player and AI units on the screen with their respective animations.
        """
        # Draw player team
        player_i = 0
        for uid, unit in self.__player_chosen.items():
            if uid not in self.__player_unit_animations:
                # Initialize animation for new player units
                self.__player_unit_animations[uid] = unit_animation.UnitAnimation(
                    self.__surface, 140 + player_i * 100, 473, unit.get_name(), False
                )
            else:
                # Update and draw existing animations
                self.__player_unit_animations[uid].update()
                self.__player_unit_animations[uid].draw()
            player_i += 1

        # Draw AI team
        ai_i = 4
        for uid, unit in self.__ai_chosen.items():
            if uid not in self.__ai_unit_animations:
                # Initialize animation for new AI units
                self.__ai_unit_animations[uid] = unit_animation.UnitAnimation(
                    self.__surface, 140 + ai_i * 100, 473, unit.get_name(), True
                )
                # Store AI unit's rectangle for target selection
                self.__ai_rect[uid] = self.__ai_unit_animations[uid].get_rect()
            else:
                # Update and draw existing animations
                self.__ai_unit_animations[uid].update()
                self.__ai_unit_animations[uid].draw()
            ai_i += 1

    def update_game_logic(self):
        """
        Update the game state each frame, handling turns, actions, and game over conditions.
        """
        if not self.__game_begin:
            # Start the game by initializing the queue and setting the first unit
            self.__game_begin = True
            self.game_begin()

        if self.is_game_over():
            # If the game is over, transition to the end scene with the appropriate winner
            winner = self.get_winner()
            if winner == "Player":
                return EndScene(self.__surface, True)
            elif winner == "AI":
                return EndScene(self.__surface, False)
            else:
                return None

        if self.__cur_unit in self.__player_chosen.values():
            # Handle player's unit turn
            if not self.__action_chosen and not self.__action_prompted:
                # Prompt player to choose an action
                self.add_message(f"Choose action for {self.__cur_unit.get_name()}")
                self.__action_prompted = True
            elif self.action_requires_target() and not self.__cur_target and not self.__target_prompted:
                # Prompt player to choose a target if the action requires one
                self.add_message("Choose a target...")
                self.__target_prompted = True

            if self.__action_chosen is not None:
                if not self.action_requires_target() or self.__cur_target is not None:
                    # Apply poison effects if any
                    self.check_poison(self.__cur_unit)
                    # Set defending state if applicable
                    self.__cur_unit.set_defending()
                    # Execute player's action
                    action_completed = self.player_turn(self.__cur_unit)
                    if action_completed:
                        self.__counter += 1
                        # Add the unit back to the queue for the next round
                        self.__queue.append(self.__cur_unit)
                        # Reset attributes for the next turn
                        self.reset_attributes()
                        # Remove any dead units from the queue
                        self.remove_dead_unit()
                        # Check if the game has ended
                        self.__game_over = self.is_game_over()
                        # Set the next unit as the current unit
                        if self.__queue:
                            self.__cur_unit = self.__queue.popleft()
                        return
                    else:
                        # Action not completed, wait for further input (e.g., target selection)
                        pass
                else:
                    # Wait for target selection
                    pass
            else:
                # Wait for action selection
                pass
        elif self.__cur_unit in self.__ai_chosen.values():
            # Handle AI's unit turn
            if not self.__ai_action_pending:
                # Start delay timer before AI acts
                self.__ai_action_pending = True
                self.__ai_action_start_time = pygame.time.get_ticks()
                self.add_message(f" -AI {self.__cur_unit.get_name()} is taking action...")
            else:
                # Check if the delay has passed to execute AI's action
                current_time = pygame.time.get_ticks()
                if current_time - self.__ai_action_start_time >= self.__ai_delay:
                    # Apply poison effects if any
                    self.check_poison(self.__cur_unit)
                    # Set defending state if applicable
                    self.__cur_unit.set_defending()
                    # Execute AI's action
                    self.ai_turn(self.__cur_unit)
                    self.__counter += 1
                    # Add the unit back to the queue for the next round
                    self.__queue.append(self.__cur_unit)
                    # Reset attributes for the next turn
                    self.reset_attributes()
                    # Remove any dead units from the queue
                    self.remove_dead_unit()
                    # Check if the game has ended
                    self.__game_over = self.is_game_over()
                    # Set the next unit as the current unit
                    if self.__queue:
                        self.__cur_unit = self.__queue.popleft()

    def draw_status_bars_and_name(self):
        """
        Render health bars, cooldown bars, poison icons, and unit names for all units.
        """
        # Create a single StatusBar instance to manage drawing
        status_bar = StatusBar(self.__surface)
        player_dict = self.__player_chosen
        ai_dict = self.__ai_chosen

        def draw_unit_status(x, y, unit):
            """
            Helper function to draw HP and CD bars for a single unit.
            """
            # Draw HP (Health Points) bar
            status_bar.draw_single_hp_bar(x, y, unit)
            # Draw CD (Cooldown) bar below the HP bar
            status_bar.draw_single_cd_bar(x, y + constants.CD_BAR_HEIGHT + 5, unit)

        # Draw status bars and names for player team
        i = 0
        for unit_id, unit in player_dict.items():
            draw_unit_status(constants.LEFT_X, constants.TOP_Y + (constants.SPACING + constants.HP_BAR_HEIGHT) * i,
                             unit)
            # Draw poisoned icon for each unit if applicable
            status_bar.draw_single_poisoned_icon(constants.POISON_LEFT_X + 100 * i, constants.POISON_TOP_Y, unit)
            # Draw unit name above each unit
            status_bar.draw_unit_name(constants.UNIT_NAME_LEFT_X + 105 * i, constants.UNIT_NAME_Y, unit)
            i += 1

        # Draw status bars and names for AI team
        i = 0
        for unit_id, unit in ai_dict.items():
            draw_unit_status(constants.RIGHT_X, constants.TOP_Y + (constants.SPACING + constants.HP_BAR_HEIGHT) * i,
                             unit)
            # Draw poisoned icon for each unit if applicable
            status_bar.draw_single_poisoned_icon(constants.POISON_RIGHT_X + 100 * i, constants.POISON_TOP_Y, unit)
            # Draw unit name above each unit
            status_bar.draw_unit_name(constants.UNIT_NAME_RIGHT_X + 105 * i, constants.UNIT_NAME_Y, unit)
            i += 1

    def draw_current_unit_arrow(self):
        """
        Draw an arrow pointing to the current unit whose turn it is, after a specified delay.
        """
        if self.__cur_unit:  # Only draw if there is a current unit
            if not self.__arrow_pending:
                # Start delay timer
                self.__arrow_pending = True
                self.__arrow_start_time = pygame.time.get_ticks()
            else:
                # Check if the delay has passed
                current_time = pygame.time.get_ticks()
                if current_time - self.__arrow_start_time >= self.__arrow_delay:
                    # Load the arrow image
                    arrow_img = self.__game_menu_resources['arrow'].convert_alpha()
                    player_dict = self.__player_chosen
                    ai_dict = self.__ai_chosen

                    # Position arrow for player team
                    if self.__cur_unit in player_dict.values():
                        # Find the index of the current unit to determine arrow position
                        i = 0
                        for unit_id, unit in player_dict.items():
                            if unit == self.__cur_unit:
                                self.__surface.blit(arrow_img,
                                                    (constants.POISON_LEFT_X + 100 * i, constants.ARROW_TOP_Y))
                                break
                            i += 1

                    # Position arrow for AI team
                    elif self.__cur_unit in ai_dict.values():
                        # Find the index of the current unit to determine arrow position
                        i = 0
                        for unit_id, unit in ai_dict.items():
                            if unit == self.__cur_unit:
                                self.__surface.blit(arrow_img,
                                                    (constants.POISON_RIGHT_X + 100 * i, constants.ARROW_TOP_Y))
                                break
                            i += 1

    def draw_round_counter(self):
        """
        Render the current round number on the screen.
        """
        if self.__counter > 0:  # Only draw if rounds have started
            # Load and draw the round image/icon
            round_img = self.__game_menu_resources['round'].convert_alpha()
            self.__surface.blit(round_img, (constants.ROUND_X, constants.ROUND_Y))

            # Load the font for displaying the round number
            font_path = os.path.join(constants.FONT_PATH, 'Gixel.ttf')
            font_number_text = pygame.font.Font(font_path, 100)
            number_text = str(self.__counter)
            number_surface = font_number_text.render(number_text, True, constants.WHITE)

            # Position the round number next to the round image
            number_x = constants.ROUND_X + round_img.get_width() + constants.ROUND_SPACING
            self.__surface.blit(number_surface, (number_x, constants.NUMBER_Y))

    def draw_message_box(self):
        """
        Render the background for the message box where game messages are displayed.
        """
        bg_surface = pygame.Surface((constants.MESSAGE_BG_WIDTH, constants.MESSAGE_BG_HEIGHT), pygame.SRCALPHA)
        bg_surface.fill(constants.MESSAGE_BG_COLOR)
        self.__surface.blit(bg_surface, (constants.MESSAGE_BG_START_X, constants.MESSAGE_BG_START_Y))

    def draw_messages(self):
        """
        Render all messages in the message queue onto the message box.
        """
        # Starting Y position for the first message
        message_start_y = constants.MESSAGE_TEXT_START_Y
        for msg in self.__messages:
            # Render the text of the message
            text_surface = self.__messages_font.render(msg['text'], True, constants.MESSAGE_COLOR)
            self.__surface.blit(text_surface, (constants.MESSAGE_TEXT_START_X, message_start_y))
            # Increment Y position for the next message
            message_start_y += text_surface.get_height() + 5

    def draw(self):
        """
        Render all visual elements of the game menu, including background, buttons, units, and UI elements.
        """
        # Draw the game background
        self.__surface.blit(self.__game_menu_resources['background'], (0, 0))

        # Draw action buttons with their respective images
        # Ordinary attack button
        atk_button_img = self.__game_menu_resources['attack'].convert_alpha()
        self.__surface.blit(atk_button_img, self.__atk_rect.topleft)
        # Defend button
        def_button_img = self.__game_menu_resources['defend'].convert_alpha()
        self.__surface.blit(def_button_img, self.__def_rect.topleft)
        # Special attack button
        # Change the button appearance based on whether the special attack is available
        if self.__cur_unit and (self.__cur_unit.get_cooldown_time() == 0 and
                                (self.__cur_unit.get_type() != "Wizard2" or not self.check_all_poisoned(
                                    self.__ai_chosen.values()))):
            sp_atk_rect_img = self.__game_menu_resources['sp_atk'].convert_alpha()  # Bright color
        else:
            sp_atk_rect_img = self.__game_menu_resources['sp_atk_no'].convert_alpha()  # Dark color

        self.__surface.blit(sp_atk_rect_img, self.__sp_atk_rect.topleft)

        # Draw status bars, unit names, and other UI elements
        self.draw_status_bars_and_name()
        self.draw_current_unit_arrow()
        self.draw_round_counter()
        self.draw_message_box()
        self.draw_messages()

        # Draw all units (player and AI) on the screen
        self.draw_units()

    def update_surface(self):
        """
        Update the game surface by rendering visuals and handling user input events.
        """
        # Render all visual elements
        self.draw()
        # Handle user input events
        self.handle_events()
