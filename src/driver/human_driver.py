from driver.wordle_driver import WordleDriver
from game.game_config import GameConfig
from game.wordle_game import WordleGame
from guesser.human_guesser import HumanGuesser
from ui.full_text_ui import FullTextUI
from ui.util import get_bool, get_config


class HumanDriver(WordleDriver):

    def __init__(self):
        # just default settings
        self.config = GameConfig()

    def start(self):
        try:
            print("Welcome to WORDLE!\n")
            if not get_bool("Play with default settings? "):
                self.config = get_config()
            print()
            while True:
                ui = FullTextUI(self.config)
                game = WordleGame(ui=ui, guesser=HumanGuesser(), config=self.config)
                n_guesses_used = game.play()
                # TODO: do something with stats
                if get_bool("Would you like to play again? "):
                    if get_bool("Would you like to change your settings? "):
                        self.config = get_config()
                    else:
                        print()
                else:
                    print("\nThanks for playing!")
                    return
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return


if __name__ == "__main__":
    driver = HumanDriver()
    driver.start()
