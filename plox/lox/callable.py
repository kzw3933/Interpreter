from abc import ABC, abstractmethod
from typing import List

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: List[object]) -> object:
        pass

    