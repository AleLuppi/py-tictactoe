from typing import Callable

from ._game_item import GameItem


class Player(GameItem):
    def __init__(self, symbol: str, name: str | None = None, human: bool = True,
                 get_user_play: Callable[["Player"], str] = None):
        self._symbol = symbol
        self._name = name
        self._is_bot = not human

        self._get_user_play = get_user_play or (lambda player: input(f"{self.name or 'User'}'s turn: "))

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

    @property
    def is_bot(self) -> bool:
        """
        Check if the player is a bot.

        :return: True if the player is a bot, False otherwise.
        """
        return self._is_bot

    @property
    def is_human(self) -> bool:
        """
        Check if the player is a human.

        :return: True if the player is a human, False otherwise.
        """
        return not self._is_bot

    def reset(self):
        """
        Reset the player status.
        """
        pass

    def play(self) -> str:
        if self.is_bot:
            # TODO: implement bot logic
            raise NotImplementedError("Implement play() method.")
        else:
            return self._get_user_play(self)
