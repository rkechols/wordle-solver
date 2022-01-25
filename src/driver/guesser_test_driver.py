import random

from driver.wordle_driver import WordleDriver
from game.game_config import GameConfig
from game.wordle_game import WordleGame
from guesser.guesser import Guesser
from guesser.slot_probability_guesser import SlotProbabilityGuesser
from ui.print_text_ui import PrintTextUI
from ui.util import get_bool
from util.word_list import load_word_list


class GuesserTestDriver(WordleDriver):

    def __init__(self, guesser: Guesser, config: GameConfig = GameConfig()):
        self.guesser = guesser
        self.config = config
        self.word_list = sorted(load_word_list(config.n_chars))

    def start(self):
        try:
            while True:
                answer = random.choice(self.word_list)
                print(f"answer: {answer}\n")
                self.guesser.reset()
                game = WordleGame(ui=PrintTextUI(self.config), guesser=self.guesser,
                                  config=self.config,
                                  target_word=answer)
                n_guesses_used = game.play()
                # TODO: do something with stats
                if not get_bool("Would you like to play again? "):
                    print("\nThanks for playing!")
                    return
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return


if __name__ == "__main__":
    random.seed(42)
    n_chars = 5
    test_driver = GuesserTestDriver(
        SlotProbabilityGuesser(n_chars=n_chars),
        GameConfig(n_chars=n_chars)
    )
    test_driver.start()
