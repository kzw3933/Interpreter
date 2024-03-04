from typing import List
import time

from lox.callable import LoxCallable

class Clock(LoxCallable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter, arguments: List[object]) -> object:
        return time.time()
    
    def __repr__(self) -> str:
        return "<native fn: clock>"