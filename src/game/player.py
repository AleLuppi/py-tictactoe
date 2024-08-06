from ._game_item import GameItem


class Player(GameItem):
    def __init__(self, symbol: str, name: str | None = None):
        self._symbol = symbol
        self._name = name

    @property
    def symbol(self) -> str:
        """
        Get the player unique symbol.

        :return: Player symbol.
        """
        return self._symbol

    @property
    def name(self) -> str:
        """
        Get the player name.

        :return: Player name.
        """
        return self._name

    def reset(self):
        """
        Reset the player status.
        """
        pass

    def play(self) -> str:
        # FIXME: implement
        raise NotImplementedError("Implement play() method.")
