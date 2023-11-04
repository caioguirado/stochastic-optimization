from typing import List, Dict, Any

import numpy as np
import pandas as pd

from policies.policy import Action
from .Environment import Environment, Observation, State


class AssetSellingEnvironment(Environment):
    def __init__(
        self, init_state: State, seed: int = 42, exog_params: dict = {}
    ) -> None:
        self.init_state = init_state
        self.state = init_state
        self.seed = seed
        self.sampler = np.random.RandomState(seed)
        self.init_exog_params = exog_params
        self.exog_params = exog_params

    def sample_exog_params(self):
        # biasdf = pd.DataFrame(self.exog_params["bias_df"]).T
        biasdf = pd.DataFrame(
            data=self.exog_params["bias_df"]["rows"],
            columns=self.exog_params["bias_df"]["columns"],
            index=self.exog_params["bias_df"]["columns"],
        ).T
        biasprob = biasdf[self.state.bias]
        coin = self.sampler.random_sample()
        if coin < biasprob["Up"]:
            new_bias = "Up"
            bias = self.exog_params["up_step"]
        elif coin >= biasprob["Up"] and coin < biasprob["Neutral"]:
            new_bias = "Neutral"
            bias = 0
        else:
            new_bias = "Down"
            bias = self.exog_params["down_step"]

        updated_price = self.state.price + self.sampler.normal(
            bias, self.exog_params["variance"]
        )

        new_price = 0.0 if updated_price < 0.0 else updated_price

        return {"price": new_price, "bias": new_bias}

    def update_state(self, exog_params: dict) -> None:
        for key in exog_params:
            setattr(self.state, key, exog_params[key])
            # self.state[key] = exog_params[key]

    def transition(self, action: Action) -> Dict[str, Any]:
        new_resource = 0 if action.name == "sell" else self.state.resource
        return {"resource": new_resource}

    def step(self, action: Action) -> List[Observation]:
        # sample exog info -> observations
        new_exog_params = self.sample_exog_params()

        self.transition(action)
        # update state
        prev_state = self.state
        self.update_state(new_exog_params)

        # update exog info
        self.exog_params.update(new_exog_params)

        # return prev_state, exog_params, new_state
        return prev_state, new_exog_params, self.state

    def reset(self) -> None:
        self.state = self.init_state
        self.exog_params = self.init_exog_params

    def get_state(self) -> State:
        return self.state
