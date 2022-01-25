from typing import List

from game.game_config import GameConfig
from game.letter_accuracy import LetterAccuracy
from game.util import Board


def get_int(prompt: str, low: int = None, high: int = None) -> int:
    if low is not None and high is not None and low >= high:
        raise ValueError("'low' must be less than 'high'")
    while True:
        val = input(prompt)
        try:
            val_int = int(val)
        except ValueError:
            print("ERROR: enter only an integer")
        else:
            if low is not None and high is not None and not (low <= val_int <= high):
                print(f"ERROR: enter a number from {low} to {high}")
            elif low is not None and val_int < low:
                print(f"ERROR: enter a number {low} or higher")
            elif high is not None and val_int > high:
                print(f"ERROR: enter a number {high} or lower")
            else:
                return val_int


def get_bool(prompt: str) -> bool:
    while True:
        val = input(prompt).strip().lower()
        if val in ["y", "yes", "1"]:
            return True
        elif val in ["n", "no", "0"]:
            return False
        else:
            print("ERROR: enter only 'y' or 'n'")


def get_config() -> GameConfig:
    print("--------")
    print("SETTINGS")
    print("--------")
    n_chars = get_int("Number of letters per word: ", low=1)
    limited_guesses = get_bool("Are guesses limited? ")
    if limited_guesses:
        n_guesses = get_int("Number of guesses: ", low=1)
    else:
        n_guesses = None
    real_words_only = get_bool("Only 'real' words are allowed as guesses: ")
    print("--------\n")
    return GameConfig(n_chars, n_guesses, real_words_only)


def print_board(board: Board, hide_guesses: bool = False):
    if len(board) == 0:
        print("(no previous guesses)")
        return
    n = len(board[0][0])
    line = "-" * n
    if not hide_guesses:
        print(line)
    for guess, result in board:
        if not hide_guesses:
            print(guess.upper())
        print_result(result)
        if not hide_guesses:
            print(line)


def print_result(result: List[LetterAccuracy]):
    for accuracy in result:
        if accuracy == LetterAccuracy.BLACK:
            print("x", end="")
        elif accuracy == LetterAccuracy.YELLOW:
            print("~", end="")
        elif accuracy == LetterAccuracy.GREEN:
            print("#", end="")
        else:
            raise ValueError(f"Unknown value of LetterAccuracy: {accuracy}")
    print()
