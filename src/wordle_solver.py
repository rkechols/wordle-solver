from collections import Counter
from copy import copy
from math import log
from typing import List

from game.letter_accuracy import LetterAccuracy
from util.word_list import load_word_list


class WordleSolver:
    def __init__(self, n_chars: int = 5, real_word_guesses_only: bool = True):
        # TODO: what if real_word_guesses_only is False?
        self.n_chars = n_chars
        self.remaining_words = load_word_list(n_chars)
        self.black_letters = set()
        self.answer = [None] * n_chars

    def next_guess(self) -> str:
        n = len(self.remaining_words)
        if n == 0:
            raise ValueError("There are no possible words left")
        if n == 1:  # only 1 left; just return it
            return next(iter(self.remaining_words))
        # calculate (log) probabilities of each letter being in each slot
        log_probs = list()
        for i in range(self.n_chars):
            counts = Counter(word[i] for word in self.remaining_words)
            log_probs.append({word[i]: log(counts[word[i]] / n) for word in self.remaining_words})
        # find the highest likelihood word
        # TODO: find the top k words?
        best_score = None
        best_word = None
        for word in self.remaining_words:
            score = sum(these_probs[c] for c, these_probs in zip(word, log_probs))
            if best_score is None or score > best_score:
                best_score = score
                best_word = word
        return best_word

    def word_is_viable(self, word: str, guess: str, result: List[LetterAccuracy],
                       needed_letters: List[str]) -> bool:
        # does it match all the green letters, and use no black letters?
        for c_answer, c in zip(self.answer, word):
            if (c_answer is not None and c_answer != c) or c in self.black_letters:
                return False
        # yellow letters:
        for guessed_letter, accuracy, c in zip(guess, result, word):
            if accuracy == LetterAccuracy.YELLOW:
                # does it avoid using a yellow letter in that exact place?
                if c == guessed_letter:
                    return False
        # does it have all the yellow letters? (in non-green spots)
        remaining_needed_letters = copy(needed_letters)
        for c, accuracy in zip(word, result):
            if accuracy != LetterAccuracy.GREEN:  # green doesn't count
                if c in remaining_needed_letters:  # check of the ones we do have
                    remaining_needed_letters.remove(c)
        if len(remaining_needed_letters) > 0:  # did we miss any?
            return False
        # passes all tests
        return True

    def apply_result(self, guess: str, result: List[LetterAccuracy]):
        if len(guess) != len(result):
            raise ValueError("mismatch between length of guess and length of result")
        needed_letters = list()  # rebuilding this each time only works because we force yellow and green letters to be in our guess
        # update our info from the new result
        for i, (c, accuracy) in enumerate(zip(guess, result)):
            if accuracy == LetterAccuracy.BLACK:
                self.black_letters.add(c)
            elif accuracy == LetterAccuracy.GREEN:
                self.answer[i] = c
            elif accuracy == LetterAccuracy.YELLOW:
                needed_letters.append(c)
            else:
                raise ValueError(f"Unknown value of LetterAccuracy: {accuracy}")
        # prune words that don't work anymore
        new_remaining_words = set()
        for word in self.remaining_words:
            if self.word_is_viable(word, guess, result, needed_letters):
                # it passed all the requirements; keep it
                new_remaining_words.add(word)
        self.remaining_words = new_remaining_words
