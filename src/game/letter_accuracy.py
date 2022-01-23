from enum import Enum, auto
from typing import List


class LetterAccuracy(Enum):
    BLACK = auto()
    YELLOW = auto()
    GREEN = auto()


def is_win(result: List[LetterAccuracy]) -> bool:
    for accuracy in result:
        if accuracy != LetterAccuracy.GREEN:
            return False
    return True
