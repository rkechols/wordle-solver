from typing import List, Tuple

from game.letter_accuracy import LetterAccuracy


Board = List[Tuple[str, List[LetterAccuracy]]]


class InvalidGuess(Exception):
    pass
