from abc import ABC, abstractmethod


class State:
    pass


class Environment:
    # exog info
    # transition - step
    # objective (?)

    @abstractmethod
    def step(self, action) -> (State,):
        # return observation, reward, terminated, False, info
        pass

    @abstractmethod
    def reset(self):
        pass
