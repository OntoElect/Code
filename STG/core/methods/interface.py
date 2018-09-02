from abc import ABC, abstractmethod


class Method(ABC):
    @abstractmethod
    def score(self, w1: str, w2: str) -> float:
        pass
