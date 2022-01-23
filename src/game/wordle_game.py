from typing import Dict, List, Optional

from game.letter_accuracy import LetterAccuracy
from util import ALPHABET
from util.word_list import load_word_list


class WordleGame:
    def __init__(self, n_chars: int = 5, n_guesses: Optional[int] = 6, real_word_guesses_only: bool = True):
        # process args
        if n_chars < 2:
            raise ValueError("'n_chars' must be 2 or greater")
        self.n_chars = n_chars
        if n_guesses is not None and n_guesses < 1:
            raise ValueError("'n_guesses' must be 1 or greater (or None)")
        self.n_guesses = n_guesses
        self.real_word_guesses_only = real_word_guesses_only
        # load valid words and pick a word to be the target
        self._word_list = load_word_list(n_chars)
        if len(self._word_list) == 0:
            raise ValueError(f"The full word list no words that are {n_chars} letters long.")
        self._target_word = self._word_list.pop()
        self._word_list.add(self._target_word)
        # set up vars that will be used while playing
        self.previous_guesses: Dict[str, List[LetterAccuracy]] = dict()

    @property
    def n_guesses_remaining(self) -> int:
        return self.n_guesses - len(self.previous_guesses)

    @property
    def has_guesses(self) -> bool:
        return self.n_guesses_remaining > 0

    def make_guess(self, new_guess: str) -> List[LetterAccuracy]:
        # is it even a valid guess?
        new_guess = new_guess.lower()
        for char in new_guess:
            if char not in ALPHABET:
                raise ValueError("Your guess must contain only letters of the English alphabet.")
        if len(new_guess) != self.n_chars:
            raise ValueError(f"Your guess must be exactly {self.n_chars} letters long.")
        if self.real_word_guesses_only and new_guess not in self._word_list:
            raise ValueError(f"Your input '{new_guess}' is not recognized as a real word.")
        # where does their guess match the real word?
        word_accuracy = list()
        letters_still_matchable = list(self._target_word)
        for guess_letter, real_letter in zip(new_guess, self._target_word):
            if guess_letter == real_letter:
                accuracy = LetterAccuracy.GREEN
                letters_still_matchable.remove(real_letter)
            elif guess_letter in letters_still_matchable:
                accuracy = LetterAccuracy.YELLOW
                letters_still_matchable.remove(guess_letter)
            else:
                accuracy = LetterAccuracy.BLACK
            word_accuracy.append(accuracy)
        # update state of the game
        self.previous_guesses[new_guess] = word_accuracy
        # let them know their result
        return word_accuracy
