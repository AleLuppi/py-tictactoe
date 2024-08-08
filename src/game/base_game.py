from enum import Enum
from typing import Tuple, Optional

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
    def board_size(self) -> Tuple[int, ...]:
        return self.board.size

    @property
    def turn(self):
        return self.board.turn

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def num_players(self) -> int:
        return len(self._players)

    @property
    def current_player(self) -> Player:
        return self._players[self.turn % self.num_players]

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
        """
        Ask user one target cell.

        :param player: The player that shall move.
        :return: User's move.
        """
        ...

    def add_player(self, symbol: Optional[str] = None, name: Optional[str] = None):
        """
        Add a new player to the game.

        :param symbol: Unique player symbol.
        :param name: Name of the player.
        """
        # Create player with new symbol
        new_player = Player(symbol=symbol or self._get_next_player_symbol(),
                            name=name,
                            get_user_play=self.get_user_play)
        assert new_player.symbol not in [p.symbol for p in self._players], "New player symbol is already in use."

        self._players.append(new_player)

    def _get_next_player_symbol(self):
        return _DEFAULT_SYMBOLS[self.num_players % len(_DEFAULT_SYMBOLS)]

    def _get_player_by_symbol(self, symbol: str) -> Optional[Player]:
        return next((player for player in self._players if player.symbol == symbol), None)

    def step(self) -> bool:
        """
        Execute a single step of the game.
        
        :return: True if the game is still in progress, False if the game is over.
        """
        # Set playing status
        self._status = GameStatus.ONGOING

        # Do one move
        move = self.current_player.play()
        self.board.add_play(move, self.current_player.symbol)

        # Check if game is over
        if self.game_over():
            return False

        return True

    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game, if any.

        :return: The winner of the game, or None.
        """
        # Check if latest move creates a line in the board
        last_cell, last_symbol = self.board.last_cell_id, self.board.last_player_id
        connected_cells = self.board.get_connected_cells(last_cell)

        connected_symbols = ["".join(cells.values()) for cells in connected_cells]
        if any(last_symbol * 3 in cs for cs in connected_symbols):
            return self._get_player_by_symbol(last_symbol)

    def game_over(self) -> bool:
        """
        Check if the game is over.

        :return: True if the game is over, False otherwise.
        """
        winner = self.get_winner()
        if winner:
            self._status = GameStatus.OVER
            return True
        return False


if __name__ == '__main__':
    # Init game
    game = BaseGame()
    game.get_user_play = lambda player: input("Your turn: ")  # Allow game to get user input
    for i in range(2):
        game.add_player()

    # Step game
    while game.step():
        table = game.board.as_table()
        table_str = "\n--+---+--\n".join([" | ".join(col or ' ' for col in row) for row in table])
        print(table_str)
