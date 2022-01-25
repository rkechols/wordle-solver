import random

from driver.guesser_test_driver import GuesserTestDriver
from game.game_config import GameConfig
from guesser.slot_probability_guesser import SlotProbabilityGuesser


if __name__ == "__main__":
    # answer = "anile"
    random.seed(42)
    n_chars = 5
    test_driver = GuesserTestDriver(
        SlotProbabilityGuesser(n_chars=n_chars),
        GameConfig(n_chars=n_chars)
    )
    test_driver.start()
