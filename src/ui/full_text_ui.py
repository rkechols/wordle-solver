from typing import List

from game.game_config import GameConfig
from game.letter_accuracy import LetterAccuracy
from game.util import Board, InvalidGuess
from ui.util import print_board, print_result
from ui.wordle_ui import WordleUI


class FullTextUI(WordleUI):

    def __init__(self, config: GameConfig):
        super().__init__(config)

    # WordleUI

    def show_game_state(self, board: Board):
        n_guesses_used = len(board)
        print(f"{self.n_chars} letters:")
        print_board(board)
        if self.n_guesses is None:
            print(f"{n_guesses_used} guesses used\n")
        else:
            print(f"{n_guesses_used} of {self.n_guesses} guesses used\n")

    def show_error(self, e: InvalidGuess):
        print(e)
        print("Please try again.\n")

    def show_result(self, guess: str, result: List[LetterAccuracy]):
        print("result:")
        print(f"  {guess.upper()}")
        print("  ", end="")
        print_result(result)
        print()

    def show_win(self, board: Board):
        print("\nYOU WIN!")
        print(f"{len(board)} guesses used\n")
        print("your board:")
        print_board(board, hide_guesses=True)
        print()

    def show_lose(self):
        print("Sorry, you ran out of guesses! You lost")
