from enum import Enum
from typing import Tuple

from game._game_item import GameItem
from game.board import Board
from game.player import Player

# TODO: move to config file
_DEFAULT_SYMBOLS = "XOHW><"


class GameStatus(str, Enum):
    INIT = "init"
    READY = "ready"
    ONGOING = "ongoing"
    OVER = "over"
    ERROR = "error"


class BaseGame(GameItem):
    def __init__(self, board_size: int = 3):
        self._board = Board(board_size)
        self._players = []
        self._status: GameStatus = GameStatus.INIT

        # Reset game to allow game start
        self.reset()

    @property
    def board(self) -> Board:
        return self._board

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def num_players(self) -> int:
        return len(self._players)

    @property
    def table(self) -> Tuple[Tuple[str, ...], ...]:
        """
        Get a nested list representation of the board.

        :return: Nested list representation of the board.
        """
        return self.board.as_table()

    def reset(self):
        self._board.reset()
        [p.reset() for p in self._players]
        self._players = []
        self._status = GameStatus.READY

    @staticmethod
    def get_user_play(player: Player) -> str:
        ...

    def add_player(self, symbol: str | None = None, name: str | None = None):
        # Create player with new symbol
        new_player = Player(symbol=symbol or self._get_next_player_symbol(),
                            name=name,
                            get_user_play=self.get_user_play)
        assert new_player.symbol not in [p.symbol for p in self._players], "New player symbol is already in use."

        self._players.append(new_player)

    def _get_next_player_symbol(self):
        return _DEFAULT_SYMBOLS[self.num_players % len(_DEFAULT_SYMBOLS)]

    def step(self) -> bool:
        """
        Execute a single step of the game.
        
        :return: True if the game is still in progress, False if the game is over.
        """
        # Set playing status
        self._status = GameStatus.ONGOING

        # Get playing player
        player = self._players[self.board.turn % self.num_players]

        # Do one move
        move = player.play()
        self.board.add_play(move, player.symbol)

        # Check if game is over
        if self.game_over():
            return False

        return True

    def get_winner(self) -> Player | None:
        # FIXME: implement
        pass

    def game_over(self):
        winner = self.get_winner()
        if winner:
            self._status = GameStatus.OVER


if __name__ == '__main__':
    # Init game
    game = BaseGame()
    for i in range(2):
        game.add_player()

    # Step game
    while game.step():
        table = game.board.as_table()
        table_str = "\n--+---+--\n".join([" | ".join(col or ' ' for col in row) for row in table])
        print(table_str)
