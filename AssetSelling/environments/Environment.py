from abc import ABC, abstractmethod
from policies.policy import Action
from typing import List


class Observation:
    pass


class State:
    @abstractmethod
    def is_terminal(self) -> bool:
        pass


class Environment:
    # init state S0
    # exog info
    # transition - step
    # objective (?)

    @abstractmethod
    def step(self, action: Action) -> List[Observation]:
        # return observation, reward, terminated, False, info
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_state(self) -> State:
        pass
