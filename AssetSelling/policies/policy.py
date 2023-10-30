from abc import ABC, abstractmethod


class Decision:
    pass


class Policy(ABC):
    @abstractmethod
    def eval(self, state) -> Decision:
        pass
