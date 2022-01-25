from abc import ABC, abstractmethod
from typing import List

from game.game_config import GameConfig
from game.letter_accuracy import LetterAccuracy
from game.util import Board, InvalidGuess


class WordleUI(ABC):

    def __init__(self, config: GameConfig):
        self.n_chars = config.n_chars
        self.n_guesses = config.n_guesses

    @abstractmethod
    def show_game_state(self, board: Board):
        pass

    @abstractmethod
    def show_error(self, e: InvalidGuess):
        pass

    @abstractmethod
    def show_result(self, guess: str, result: List[LetterAccuracy]):
        pass

    @abstractmethod
    def show_win(self, board: Board):
        pass

    @abstractmethod
    def show_lose(self):
        pass
