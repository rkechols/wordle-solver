from dataclasses import dataclass
from typing import Optional


@dataclass
class GameConfig:
    n_chars: int = 5
    n_guesses: Optional[int] = 6
    real_word_guesses_only: bool = True
