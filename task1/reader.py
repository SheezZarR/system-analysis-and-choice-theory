from abc import ABC, abstractmethod


class Reader(ABC):

    @abstractmethod
    def get_at(self, x: int, y: int) -> str:
        pass
