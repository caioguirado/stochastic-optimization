from typing import List
from environments.Environment import Observation, State
from policies.policy import Action, Decision
from .objective import Objective


class AssetSellingObjective(Objective):
    def eval(self, action: Action, state: State) -> float:
        if action.name == "sell" and state.resource != 0:
            sell_size = 1
        else:
            sell_size = 0
        obj_part = state.price * sell_size
        return obj_part
