from typing import Dict, Tuple, Iterable
import re

from ._game_item import GameItem


class Board(GameItem):
    def __init__(self, size: Iterable[int] | int = 3):
        # Currently, size is supported up to 9x9, while min is always 3x3
        size = tuple(size) if isinstance(size, Iterable) else (size, size)
        size = tuple(max(3, min(int(s), 9)) for s in size)

        # Init attributes
        self._size = size
        self._plays: Dict[Tuple[int, int], str] = {}

        # Ensure reset board
        self.reset()

    @property
    def size(self) -> Tuple[int, ...]:
        """
        Get the board size.

        :return: Board size.
        """
        return self._size

    @property
    def plays(self) -> Dict[str, str]:
        """
        Get the board plays.

        :return: Board plays.
        """
        return {self._n2row(k[0]) + self._n2col(k[1]): v for k, v in self._plays.items()}

    @property
    def turn(self) -> int:
        """
        Get the current turn number.

        :return: Current turn number.
        """
        return len(self._plays)

    def reset(self):
        """
        Reset the board.
        """
        self._plays = {}

    def as_table(self) -> Tuple[Tuple[str, ...], ...]:
        """
        Get a nested list representation of the board.

        :return: Nested list representation of the board.
        """
        return tuple(
            tuple(self._plays.get((row, col), '') for col in range(self.size[1]))
            for row in range(self.size[0]))

    def add_play(self, cell_id: str, player_id: str, override: bool = False) -> bool:
        """
        Add move from player.

        :param cell_id: The cell where player wants to place their move, format "[a-z][1-9]"
        :param player_id: The id of the player.
        :param override: If true, override the cell if it is already occupied, otherwise raise an error.
        :return: True if the move was added successfully, False otherwise.
        """
        # Get usable cell id
        cell_id = self._get_cell_id(cell_id)

        # Ensure player_id is valid
        if not player_id:
            raise ValueError(f"Invalid player id. Expected valid string, got: {player_id}")

        # Ensure cell is free or can be overridden
        if cell_id in self._plays and not override:
            raise ValueError(f"Cell {cell_id} is already occupied by player {self._plays[cell_id]}")
        self._plays[cell_id] = str(player_id)

        return True

    def _get_cell_id(self, cell_id: str) -> Tuple[int, int]:
        """
        Clean cell id to conform to format "[a-z][1-9]".

        :param cell_id: The original cell id.
        :return: The cleaned cell id.
        """
        # Ensure cell_id is in format "[a-z][1-9]"
        cell_id_match = re.match(r"([a-z])\s*([1-9])", cell_id.lower())
        if not cell_id_match:
            raise ValueError(f"Invalid cell id. Expected \"[a-z][1-9]\", got: {cell_id}")

        # Check if in bounds
        row_str, col_str = cell_id_match.groups()
        row = self._row2n(row_str)
        col = self._col2n(col_str)
        if row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]:
            raise ValueError(f"Selected cell {row_str}{col_str} is out of board's bounds.")

        return row, col

    @staticmethod
    def _n2row(n: int) -> str:
        return chr(n + 97)

    @staticmethod
    def _n2col(n: int) -> str:
        return str(n + 1)

    @staticmethod
    def _row2n(row: str) -> int:
        return ord(row) - 97

    @staticmethod
    def _col2n(col: str) -> int:
        return int(col) - 1
