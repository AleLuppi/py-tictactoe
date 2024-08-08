from abc import ABC, abstractmethod


class GameItem(ABC):
    @abstractmethod
    def reset(self):
        ...
