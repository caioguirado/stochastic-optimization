from abc import ABC, abstractmethod
from policies.policy import Action
from environments.Environment import Observation
from typing import List


class Objective(ABC):
    @abstractmethod
    def eval(self, action: Action, observations: List[Observation]) -> float:
        pass
