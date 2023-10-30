from abc import ABC, abstractmethod
from environments import State


class Objective(ABC):
    @abstractmethod
    def eval(self, state_t: State, state_t_1: State) -> float:
        pass
