from typing import List

from game.letter_accuracy import LetterAccuracy
from guesser.guesser import Guesser


class HumanGuesser(Guesser):

    def next_guess(self) -> str:
        return input("Enter a word to guess: ")

    def apply_result(self, guess: str, result: List[LetterAccuracy]):
        pass  # showing the user is enough; it's their job to keep track of stuff

    def reset(self):
        pass  # no need to reset anything
