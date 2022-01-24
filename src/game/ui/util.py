from typing import Optional, Tuple


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


def get_settings() -> Tuple[int, Optional[int], bool]:
    print("--------")
    print("SETTINGS")
    print("--------")
    n_chars = get_int("Number of letters per word: ", low=1)
    limited_guesses = get_bool("Are guesses limited? ")
    if limited_guesses:
        n_guesses = get_int("Number of guesses: ", low=1)
    else:
        n_guesses = None
    real_words_only = get_bool("Only 'real' words are allowed: ")
    print("--------\n")
    return n_chars, n_guesses, real_words_only
