from typing import List, Optional

from game.game_config import GameConfig
from game.letter_accuracy import is_win, LetterAccuracy
from game.util import Board, InvalidGuess
from guesser.guesser import Guesser
from ui.wordle_ui import WordleUI
from util import ALPHABET
from util.word_list import load_word_list


class WordleGame:

    def __init__(self, ui: WordleUI, guesser: Guesser, config: GameConfig, target_word: str = None):
        self.ui = ui
        self.guesser = guesser
        # validate target_word if given, and n_chars if not overridden
        if target_word is None:
            if config.n_chars < 1:
                raise ValueError("'n_chars' must be 1 or greater")
            self.n_chars = config.n_chars
        else:
            target_word = target_word.lower()
            for char in target_word:
                if char not in ALPHABET:
                    raise ValueError("'target_word' must contain only letters of the English alphabet.")
            self.n_chars = len(target_word)
            if self.n_chars < 1:
                raise ValueError("'target_word' must contain at least one letter")
        # validate n_guesses
        if config.n_guesses is not None and config.n_guesses < 1:
            raise ValueError("'n_guesses' must be 1 or greater (or None)")
        self.n_guesses = config.n_guesses
        # are we only using "real" words?
        if config.real_word_guesses_only:
            # load possible words
            self._word_list = load_word_list(config.n_chars)
            # pick a target word if needed
            if target_word is None:
                self._target_word = self._word_list.pop()
                self._word_list.add(self._target_word)
            else:
                # make sure the provided word is listed
                if target_word not in self._word_list:
                    # impossible to guess the target_word
                    raise ValueError("'real_word_guesses_only' was set to True, "
                                     "but the provided value for 'target_word' is not recognized as a real word.")
                self._target_word = target_word
        else:
            # no need to save the list of possible words
            self._word_list = None
            # pick a target word if needed
            if target_word is None:
                word_list = load_word_list(config.n_chars)
                self._target_word = word_list.pop()
        self.real_word_guesses_only = config.real_word_guesses_only
        # set up vars that will be used while playing
        self.board: Board = list()

    @property
    def n_guesses_used(self) -> int:
        return len(self.board)

    @property
    def n_guesses_remaining(self) -> Optional[int]:
        if self.n_guesses is None:  # unlimited guesses
            return None
        return self.n_guesses - self.n_guesses_used

    @property
    def has_guesses(self) -> bool:
        if self.n_guesses is None:  # unlimited guesses
            return True
        return self.n_guesses_remaining > 0

    def make_guess(self, new_guess: str) -> List[LetterAccuracy]:
        if not self.has_guesses:
            raise InvalidGuess("You have no guesses remaining!")
        # is it even a valid guess?
        new_guess = new_guess.lower()
        for char in new_guess:
            if char not in ALPHABET:
                raise InvalidGuess("Your guess must contain only letters of the English alphabet.")
        if len(new_guess) != self.n_chars:
            raise InvalidGuess(f"Your guess must be exactly {self.n_chars} letters long.")
        if self.real_word_guesses_only and new_guess not in self._word_list:
            raise InvalidGuess(f"Your input '{new_guess}' is not recognized as a real word.")
        # where does their guess match the real word?
        word_accuracy = list()
        letters_still_matchable = list(self._target_word)
        for guess_letter, real_letter in zip(new_guess, self._target_word):
            if guess_letter == real_letter:
                letters_still_matchable.remove(real_letter)  # TODO: MAY THROW ERROR
        for guess_letter, real_letter in zip(new_guess, self._target_word):
            if guess_letter == real_letter:
                accuracy = LetterAccuracy.GREEN
            elif guess_letter in letters_still_matchable:
                accuracy = LetterAccuracy.YELLOW
                letters_still_matchable.remove(guess_letter)
            else:
                accuracy = LetterAccuracy.BLACK
            word_accuracy.append(accuracy)
        # update state of the game
        self.board.append((new_guess, word_accuracy))
        # let them know their result
        return word_accuracy

    def play(self) -> Optional[int]:
        while self.has_guesses:
            self.ui.show_game_state(self.board)
            new_guess = self.guesser.next_guess()
            try:
                result = self.make_guess(new_guess)
            except InvalidGuess as e:
                self.ui.show_error(e)
                continue
            self.guesser.apply_result(new_guess, result)
            self.ui.show_result(new_guess, result)
            if is_win(result):
                self.ui.show_win(self.board)
                return self.n_guesses_used
        self.ui.show_lose()
        return None
