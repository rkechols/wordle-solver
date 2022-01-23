from pathlib import Path
from typing import Set


DATA_DIR = Path("data")


def get_word_list_path(n_chars: int = None) -> Path:
    tag = str(n_chars) if n_chars is not None else "full"
    return DATA_DIR / f"word_list-{tag}.txt"


WORD_LIST_FULL_PATH = get_word_list_path()


def load_word_list(n_chars: int = 5) -> Set[str]:
    word_list_path = get_word_list_path(n_chars)
    to_return = set()
    if word_list_path.is_file():  # just load it
        with open(word_list_path, "r", encoding="utf-8") as f:
            for line in f:
                to_return.add(line.strip().lower())
    else:  # load the needed data and also create the file
        with open(WORD_LIST_FULL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if len(word) == n_chars:
                    to_return.add(word)
        with open(word_list_path, "w", encoding="utf-8") as f:
            for word in sorted(to_return):
                print(word, file=f)
    return to_return
