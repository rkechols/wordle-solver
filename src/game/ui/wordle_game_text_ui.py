from typing import List

from game.letter_accuracy import is_win, LetterAccuracy
from game.wordle_game import Board, WordleGame


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


class WordleGameTextUI:
    def __init__(self):
        self.n_chars = 5
        self.n_guesses = 6
        self.real_words_only = True

    def get_settings(self):
        print("--------")
        print("SETTINGS")
        print("--------")
        self.n_chars = get_int("Number of letters per word: ", low=1)
        limited_guesses = get_bool("Are guesses limited? ")
        if limited_guesses:
            self.n_guesses = get_int("Number of guesses: ", low=1)
        else:
            self.n_guesses = None
        self.real_words_only = get_bool("Only 'real' words are allowed: ")
        print("--------\n")

    def start(self):
        try:
            print("Welcome to WORDLE!\n")
            self.get_settings()
            while True:
                self.run_game()
                if get_bool("Would you like to play again? "):
                    if get_bool("Would you like to change your settings? "):
                        self.get_settings()
                    else:
                        print()
                else:
                    print("\nThanks for playing!")
                    return
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return

    @classmethod
    def print_board(cls, board: Board, hide_guesses: bool = False):
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
            cls.print_result(result)
            if not hide_guesses:
                print(line)

    @classmethod
    def print_result(cls, result: List[LetterAccuracy]):
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

    def run_game(self):
        game = WordleGame(n_chars=self.n_chars, n_guesses=self.n_guesses, real_word_guesses_only=self.real_words_only)
        while game.has_guesses:
            print(f"{game.n_chars} letters:")
            self.print_board(game.board)
            if game.n_guesses is None:
                print(f"{game.n_guesses_used} guesses used\n")
            else:
                print(f"{game.n_guesses_used} of {game.n_guesses} guesses used\n")
            new_guess = input("Enter a word to guess: ")
            try:
                result = game.make_guess(new_guess)
            except ValueError as e:
                print(e)
                print("Please try again.")
            else:
                print("response:")
                print(f"  {new_guess.upper()}")
                print("  ", end="")
                self.print_result(result)
                if is_win(result):
                    print("\nYOU WIN!")
                    print(f"{game.n_guesses_used} guesses used\n")
                    print("your board:")
                    self.print_board(game.board, hide_guesses=True)
                    print()
                    break
            print()
        else:
            print("Sorry, you ran out of guesses! You lost")


if __name__ == "__main__":
    game_ui = WordleGameTextUI()
    game_ui.start()
