from typing import List

from game.game_config import GameConfig
from game.letter_accuracy import LetterAccuracy
from game.util import Board, InvalidGuess
from ui.wordle_ui import WordleUI


class NullUI(WordleUI):

    def __init__(self, config: GameConfig):
        super().__init__(config)

    # override all methods to do exactly nothing

    def show_game_state(self, board: Board):
        pass

    def show_error(self, e: InvalidGuess):
        pass

    def show_result(self, guess: str, result: List[LetterAccuracy]):
        pass

    def show_win(self, board: Board):
        pass

    def show_lose(self):
        pass
