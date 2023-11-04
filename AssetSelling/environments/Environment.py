from abc import ABC, abstractmethod
from policies.policy import Action
from typing import List


class Observation:
    pass


class State:
    @abstractmethod
    def __init__(self, *args) -> None:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass


class Environment:
    # init state S0
    # exog info
    # transition - step
    # objective (?)

    @abstractmethod
    def __init__(self, init_state: State, *args) -> None:
        pass

    @abstractmethod
    def step(self, action: Action) -> List[Observation]:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def get_state(self) -> State:
        pass
