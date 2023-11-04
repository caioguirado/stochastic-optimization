from abc import ABC, abstractmethod
from policies.policy import Action
from environments.Environment import State


class Objective(ABC):
    @abstractmethod
    def eval(self, action: Action, state: State) -> float:
        pass
