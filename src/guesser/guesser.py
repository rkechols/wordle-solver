from abc import ABC, abstractmethod
from typing import List

from game.letter_accuracy import LetterAccuracy


class Guesser(ABC):

    @abstractmethod
    def next_guess(self) -> str:
        pass

    @abstractmethod
    def apply_result(self, guess: str, result: List[LetterAccuracy]):
        pass

    @abstractmethod
    def reset(self):
        pass
