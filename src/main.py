import random

from game.ui.wordle_game_text_ui import WordleGameTextUI
from game.letter_accuracy import is_win
from game.wordle_game import WordleGame
from util.word_list import load_word_list
from wordle_solver import WordleSolver


if __name__ == "__main__":
    random.seed(42)
    n_chars = 5
    answer = random.choice(sorted(load_word_list(n_chars)))
    print(f"answer: {answer}\n")
    game = WordleGame(target_word=answer)
    solver = WordleSolver(n_chars)
    while game.has_guesses:
        new_guess = solver.next_guess()
        print(f"GUESS:  {new_guess}")
        result = game.make_guess(new_guess)
        print("RESULT: ", end="")
        WordleGameTextUI.print_result(result)
        print()
        if is_win(result):
            print("YOU WIN!")
            print(f"{game.n_guesses_used} guesses used\n")
            print("your board:")
            WordleGameTextUI.print_board(game.board, hide_guesses=True)
            print()
            break
        solver.apply_result(new_guess, result)
    else:
        print("Sorry, you ran out of guesses! You lost")
