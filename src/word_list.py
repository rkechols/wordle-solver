from pathlib import Path


DATA_DIR = Path("data")


def get_word_list_path(n_chars: int = None) -> Path:
    tag = str(n_chars) if n_chars is not None else "full"
    return DATA_DIR / f"word_list-{tag}.txt"


WORD_LIST_FULL_PATH = get_word_list_path()


class WordList:
    def __init__(self, n_chars: int = 5):
        self.n_chars = n_chars
        word_list_path = get_word_list_path(self.n_chars)
        self.data = set()
        if word_list_path.is_file():  # just load it
            with open(word_list_path, "r", encoding="utf-8") as f:
                for line in f:
                    self.data.add(line.strip().lower())
        else:  # load the needed data and also create the file
            with open(WORD_LIST_FULL_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip().lower()
                    if len(word) == self.n_chars:
                        self.data.add(word)
            with open(word_list_path, "w", encoding="utf-8") as f:
                for word in sorted(self.data):
                    print(word, file=f)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        for word in self.data:
            yield word

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(n_chars={self.n_chars})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(n_chars={self.n_chars}, size={len(self)})"
