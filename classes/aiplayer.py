from classes.player import Player
import random

class AIPlayer(Player):
    def __init__(self):
        super().__init__(name="AI", is_ai=True)