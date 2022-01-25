from game.game_config import GameConfig
from game.util import Board
from ui.full_text_ui import FullTextUI


class PrintTextUI(FullTextUI):

    def __init__(self, config: GameConfig):
        super().__init__(config)

    def show_game_state(self, board: Board):
        pass  # override this to make it do nothing
