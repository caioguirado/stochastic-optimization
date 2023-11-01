from abc import ABC, abstractmethod
from typing import Tuple


class Action:
    @abstractmethod
    def __init__(self, action_name, action_value) -> None:
        self.action_name = action_name
        self.action_value = action_value


class Decision:
    @abstractmethod
    def get_action(self) -> Action:
        pass


class Policy(ABC):
    @abstractmethod
    def eval(self, state) -> Decision:
        pass
