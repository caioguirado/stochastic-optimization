from abc import ABC, abstractmethod
from typing import Tuple


class Action:
    @abstractmethod
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value


class Decision:
    @abstractmethod
    def __init__(self, decision_dict) -> None:
        self.items = decision_dict

    @abstractmethod
    def get_action(self) -> Action:
        for k, v in self.items.items():
            if v == 1:
                return Action(name=k, value=v)
        return Action(name="", value="")


class Policy(ABC):
    @abstractmethod
    def eval(self, state) -> Decision:
        pass
