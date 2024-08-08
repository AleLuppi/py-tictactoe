from typing import Dict, Tuple, Iterable, Union
import re

from ._game_item import GameItem


class Board(GameItem):
    def __init__(self, size: Union[Iterable[int], int] = 3, win_on: int = None):
        # Currently, size is supported up to 9x9, while min is always 3x3
        size = tuple(size) if isinstance(size, Iterable) else (size, size)
        size = tuple(max(3, min(int(s), 9)) for s in size)
        win_on = max(win_on or min(size), 3)

        # Init attributes
        self._size = size
        self._plays: Dict[Tuple[int, ...], str] = {}
        self._win_on = win_on

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

    @property
    def last_cell_position(self) -> Tuple[int, ...]:
        """
        Get the last cell played.

        :return:
        """
        return tuple(self._plays.keys())[-1] if self._plays else None

    @property
    def last_cell_id(self) -> str:
        """
        Get the ID of the last cell played.

        :return:
        """
        return self._cell_pos_to_id(*self.last_cell_position) if self.last_cell_position else None

    @property
    def last_player_id(self):
        """
        Get the last symbol played.
        :return:
        """
        if self.last_cell_position:
            return self._plays.get(self.last_cell_position)
        else:
            return None

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
        cell_id_match = re.match(r"\s*([a-z])\s*([1-9])\s*", cell_id.lower())
        if not cell_id_match:
            raise ValueError(f"Invalid cell id. Expected \"[a-z][1-9]\", got: {cell_id}")

        # Check if in bounds
        row_str, col_str = cell_id_match.groups()
        row = self._row2n(row_str)
        col = self._col2n(col_str)
        if row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]:
            raise ValueError(f"Selected cell {row_str}{col_str} is out of board's bounds.")

        return row, col

    def get_connected_cells(self, cell_id: str, max_dist: int = None) -> Iterable[Dict[str, str]]:
        """
        Get a list of cells that are connected to the given cell in any possible direction.

        :param cell_id: The cell id.
        :param max_dist: The maximum distance from the cell.
        :return: Iterable of nearby cells.
        """
        row, col = self._get_cell_id(cell_id)
        if max_dist is None:
            max_dist = self._win_on - 1

        # Get connected cells
        row_connected = [(r, col) for r in range(row - max_dist, row + max_dist + 1)]
        col_connected = [(row, c) for c in range(col - max_dist, col + max_dist + 1)]
        diag1_connected = [(row + i, col + i) for i in range(-max_dist, max_dist + 1)]
        diag2_connected = [(row + i, col - i) for i in range(-max_dist, max_dist + 1)]
        all_connections = [
            {self._cell_pos_to_id(*k): self._plays.get(k, ' ') for k in connection
             if 0 <= k[0] < self.size[0] and 0 <= k[1] < self.size[1]}
            for connection in [row_connected, col_connected, diag1_connected, diag2_connected]
        ]

        return all_connections

    def _cell_pos_to_id(self, row: int, col: int) -> str:
        return self._n2row(row) + self._n2col(col)

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
